"""
job_runner.py

A reusable JobRunner class for generating and managing HPC workflow scripts.
Supports both SLURM submission and local sequential execution.

EXAMPLES:
--------

1. Minimal Working Example:
```python
from job_runner import JobRunner

# Define how output files are named
def output_name(input_file, output_dir):
    basename = os.path.basename(input_file).replace('.in', '.out')
    return os.path.join(output_dir, basename)

# Create runner with required parameters
runner = JobRunner(
    input_files=['file1.in', 'file2.in'],
    output_file_name_func=output_name,
    output_dir='/path/to/output',
    bind_dirs=['/data', '/home']
)

# Set the job template (what runs inside container)
runner.container_job_template = '''#!/bin/bash
echo "Processing {input_file}"
my_program --input {input_file} --output {output_file} --events {events}
echo "Done!"
'''

# Generate all scripts
runner.run()
```

2. Advanced Example with Custom Generation:
```python
from job_runner import JobRunner

def output_name(input_file, output_dir):
    return os.path.join(output_dir, os.path.basename(input_file) + '.processed')

# Initialize with full configuration
runner = JobRunner(
    input_files=glob.glob('*.hepmc'),
    output_file_name_func=output_name,
    output_dir='/scratch/results',
    bind_dirs=['/cvmfs', '/scratch'],
    events=10000,
    container='/cvmfs/singularity.opensciencegrid.org/my_image:latest',
    slurm_time='48:00:00',
    slurm_cpus_per_task=4,
    slurm_mem_per_cpu='8G',
    slurm_account='physics',
    slurm_partition='gpu'
)

# Custom container script generation
def custom_generate(input_file):
    basename = os.path.splitext(os.path.basename(input_file))[0]
    
    # Add custom logic here
    special_params = calculate_params(input_file)
    
    content = f'''#!/bin/bash
set -e
echo "Custom processing for {basename}"
my_special_program --params {special_params} --input {input_file}
'''
    
    return {
        'basename': basename,
        'content': content
    }

# Replace default generator
runner.generate_container_script = custom_generate

# Set custom SLURM template if needed
runner.slurm_script_template = '''#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --account={account}
...
'''

runner.run()
```
"""

import argparse
import os
import textwrap
import datetime
from pathlib import Path
from typing import List, Dict, Callable, Optional
from glob import glob
from omegaconf import OmegaConf
import yaml

class JobRunner:
    """Flexible job runner for HPC workflows with container support."""
    
    def __init__(self, 
                 input_files: List[str],
                 output_file_name_func: Callable[[str, str], str],
                 output_dir: str,
                 bind_dirs: List[str],
                 events: int = 5000,
                 beam_config: str = "",
                 container: str = '/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:nightly',
                 slurm_time: str = '24:00:00',
                 slurm_cpus_per_task: int = 1,
                 slurm_mem_per_cpu: str = '5G',  # Fixed parameter name
                 slurm_account: str = 'eic',
                 slurm_partition: str = 'production',
                 ):
        """Initialize JobRunner with configuration."""
        
        # Initialize config dictionary first
        self.config = {
            'timestamp': datetime.datetime.now().isoformat(),
            'script_version': '1.0.0'
        }
        
        # Update config with parsed arguments
        self.config['input_files'] = [os.path.abspath(f) for f in input_files]
        self.config['output_dir'] = os.path.abspath(output_dir)
        self.config['jobs_dir'] = os.path.join(self.config['output_dir'], 'jobs')
        self.config['logs_dir'] = os.path.join(self.config['output_dir'], 'logs')
        self.config['bind_dirs'] = [os.path.abspath(binddir) for binddir in bind_dirs]
        self.config['events'] = events
        self.config['container'] = container
        self.config['slurm_time'] = slurm_time
        self.config['slurm_cpus_per_task'] = slurm_cpus_per_task
        self.config['slurm_mem_per_cpu'] = slurm_mem_per_cpu  # Fixed name
        self.config['slurm_account'] = slurm_account
        self.config['slurm_partition'] = slurm_partition
        self.config['beam_config'] = beam_config

        # Store output filename function
        self.output_file_name_func = output_file_name_func
        
        # Templates - MUST be set by user
        self.container_script_template = None
        self.slurm_script_template = self.get_default_slurm_template()
        
        # Job generation function - can be replaced
        self.container_script_generate_func = self.default_container_script_generator

        self.container_script_params_updater: Callable = None
        
        # Initialize storage for generated scripts
        self.generated_scripts = {
            'container': [],
            'slurm': [],
            'info': []
        }
        
        # Pretty print configuration
        self.print_config()


    def get_default_slurm_template(self) -> str:
        """Default SLURM submission script template."""
        return textwrap.dedent("""\
        #!/bin/bash
        #SBATCH --account={slurm_account}
        #SBATCH --partition={slurm_partition}
        #SBATCH --job-name={basename}
        #SBATCH --time={slurm_time}
        #SBATCH --cpus-per-task={slurm_cpus_per_task}
        #SBATCH --mem-per-cpu={slurm_mem_per_cpu}
        #SBATCH --output={log_file}
        #SBATCH --error={err_file}
        
        set -e
        
        echo "Starting job for {basename} at $(date)"
        echo "Running on: $(hostname)"
        
        singularity exec {bindings} {container} {container_script}
        
        echo "Job finished at $(date)"
        """)


    def default_container_script_generator(self, input_file: str) -> Dict[str, str]:
        """Generate the container execution script content."""
        basename = os.path.splitext(os.path.basename(input_file))[0]

        params = {
            'input_file': input_file,
            'output_file': self.output_file_name_func(input_file, self.config['output_dir']),
            'output_dir': self.config['output_dir'],
            'basename': basename,
            'events': self.config['events'],
            **self.config  # Include all config variables
        }

        # If user provided a params updater, apply it
        if self.container_script_params_updater:
            params = self.container_script_params_updater(params)
        
        content = self.container_script_template.format(**params)
        
        return {
            'basename': basename,
            'content': content
        }

    
    def create_directories(self):
        """Create necessary directories for job scripts and logs."""
        os.makedirs(self.config['output_dir'], exist_ok=True)
        os.makedirs(self.config['jobs_dir'], exist_ok=True)
        os.makedirs(self.config['logs_dir'], exist_ok=True)


    def write_container_script(self, input_file: str) -> str:
        """Write container execution script for a single input file."""
        script_data = self.container_script_generate_func(input_file)
        basename = script_data['basename']
        
        script_path = os.path.join(self.config['jobs_dir'], f"{basename}.container.sh")
        with open(script_path, 'w') as f:
            f.write(script_data['content'])
        os.chmod(script_path, 0o755)
        
        self.generated_scripts['container'].append(script_path)
        return script_path

    def write_slurm_script(self, input_file: str, container_script: str) -> str:
        """Write SLURM submission script for a single input file."""
        basename = os.path.splitext(os.path.basename(input_file))[0]

        bindings = ' '.join([f'-B {binddir}:{binddir}' for binddir in self.config['bind_dirs']])
        
        params = {
            'basename': basename,
            'slurm_account': self.config['slurm_account'],
            'slurm_partition': self.config['slurm_partition'],
            'slurm_time': self.config['slurm_time'],
            'slurm_cpus_per_task': self.config['slurm_cpus_per_task'],
            'slurm_mem_per_cpu': self.config['slurm_mem_per_cpu'],
            'log_file': os.path.join(self.config['logs_dir'], f"{basename}.slurm.log"),
            'err_file': os.path.join(self.config['logs_dir'], f"{basename}.slurm.err"),
            'container': self.config['container'],
            'container_script': container_script,
            'bindings': bindings,  # Fixed: was 'bind_dir'
            'beam_config': self.config['beam_config']
        }
        
        script_content = self.slurm_script_template.format(**params)
        script_path = os.path.join(self.config['jobs_dir'], f"{basename}.slurm.sh")
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        
        self.generated_scripts['slurm'].append(script_path)
        return script_path
    
    def write_info_yaml(self, input_file: str) -> str:
        """Write metadata YAML file for a single input file."""
        basename = os.path.splitext(os.path.basename(input_file))[0]
        yaml_path = os.path.join(self.config['jobs_dir'], f"{basename}.info.yaml")
        
        metadata = {
            'timestamp': self.config['timestamp'],
            'input_file': input_file,
            'output_dir': self.config['output_dir'],
            'container_image': self.config['container'],
            'script_version': self.config['script_version'],
            'config': self.config,
        }
        
        with open(yaml_path, 'w') as f:
            yaml.safe_dump(metadata, f, sort_keys=False)
        
        self.generated_scripts['info'].append(yaml_path)
        return yaml_path
    
    def write_submit_all_script(self):
        """Write master script to submit all SLURM jobs."""
        script_path = os.path.join(self.config['jobs_dir'], 'submit_all_slurm_jobs.sh')
        
        script_lines = [
            "#!/bin/bash",
            "set -e",
            "",
            "# Submit all generated SLURM jobs",
            ""
        ]
        
        for slurm_script in self.generated_scripts['slurm']:
            script_lines.append(f"sbatch {slurm_script}")
        
        script_lines.append("")
        script_lines.append(f"echo \"Submitted {len(self.generated_scripts['slurm'])} SLURM jobs!\"")
        
        with open(script_path, 'w') as f:
            f.write('\n'.join(script_lines))
        
        os.chmod(script_path, 0o755)
        return script_path
    
    def write_run_all_script(self):
        """Write script to run all jobs locally in sequence with timing."""
        script_path = os.path.join(self.config['jobs_dir'], 'run_all_local.sh')
        
        # Create bindings string
        bindings = ' '.join([f'-B {binddir}:{binddir}' for binddir in self.config['bind_dirs']])
        
        script_lines = [
            "#!/bin/bash",
            "set -e",
            "",
            "# Run all jobs locally in sequence",
            "",
            "START_TIME=$SECONDS",
            ""
        ]
        
        for i, container_script in enumerate(self.generated_scripts['container'], 1):
            basename = os.path.basename(container_script)
            total = len(self.generated_scripts['container'])
            
            script_lines.extend([
                f"echo \"[{i}/{total}] Running {basename}...\"",
                f"JOB_START=$SECONDS",
                f"singularity exec {bindings} "
                f"{self.config['container']} {container_script}",
                f"JOB_TIME=$((SECONDS - JOB_START))",
                f"echo \"    Completed in $JOB_TIME seconds\"",
                ""
            ])
        
        script_lines.extend([
            "TOTAL_TIME=$((SECONDS - START_TIME))",
            "echo \"=====================================\"",
            f"echo \"All {len(self.generated_scripts['container'])} jobs completed!\"",
            "echo \"Total execution time: $TOTAL_TIME seconds\"",
            "echo \"=====================================\""
        ])
        
        with open(script_path, 'w') as f:
            f.write('\n'.join(script_lines))
        
        os.chmod(script_path, 0o755)
        return script_path
    
    def process_file(self, input_file: str):
        """Process a single input file: create all necessary scripts."""
        print(f"Processing: {input_file}")
        
        # Create container script
        container_script = self.write_container_script(input_file)
        
        # Create SLURM script
        slurm_script = self.write_slurm_script(input_file, container_script)
        
        # Create info YAML
        info_yaml = self.write_info_yaml(input_file)
       
    
    def run(self):
        """Main execution method."""
        if self.container_script_template is None:
            raise ValueError("container_job_template must be set before running")
        
        # Create directory structure
        self.create_directories()
        
        # Process each input file
        for input_file in self.config['input_files']:
            self.process_file(input_file)
        
        # Create master submission scripts
        submit_script = self.write_submit_all_script()
        run_script = self.write_run_all_script()
        
        # Print summary
        self.print_summary(submit_script, run_script)
    
    def print_config(self):
        """Pretty print the current configuration."""

        print(f"JobRunner v{self.config['script_version']}")
        print("\n" + "="*80)
        print("CONFIGURATION")
        print("="*80)
        
        # Group configuration items for better display
        print("Directories:")
        print(f"  Output:     {self.config['output_dir']}")
        print(f"  Jobs:       {self.config['jobs_dir']}")
        print(f"  Logs:       {self.config['logs_dir']}")

        print("\nJob Parameters:")
        print(f"  Events:     {self.config['events']}")
        print(f"  Time limit: {self.config['slurm_time']}")
        print(f"  CPUs/task:  {self.config['slurm_cpus_per_task']}")
        print(f"  Memory/CPU: {self.config['slurm_mem_per_cpu']}")
        print(f"  Account:    {self.config['slurm_account']}")
        print(f"  Partition:  {self.config['slurm_partition']}")
        
        print("\nContainer:")
        print(f"  Image:      {self.config['container']}")

        print(f"\nBind Additional Directories:")
        for binddir in self.config['bind_dirs']:
            print(f"               {binddir}")
        
        print("="*80 + "\n")

    def print_summary(self, submit_script: str, run_script: str):
        """Print summary of generated scripts."""
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"Output directory: {self.config['output_dir']}")
        print(f"Jobs directory:   {self.config['jobs_dir']}")
        print(f"Logs directory:   {self.config['logs_dir']}")
        print(f"\nGenerated {len(self.config['input_files'])} job sets:")
        print(f"  - Container scripts: {len(self.generated_scripts['container'])}")
        print(f"  - SLURM scripts:     {len(self.generated_scripts['slurm'])}")
        print(f"  - Info YAML files:   {len(self.generated_scripts['info'])}")
        print(f"\nMaster scripts:")
        print(f"  - Submit all (SLURM): {submit_script}")
        print(f"  - Run all (local):    {run_script}")
        print("\nTo submit all jobs to SLURM:")
        print(f"  cd {self.config['jobs_dir']} && ./submit_all_slurm_jobs.sh")
        print("\nTo run all jobs locally:")
        print(f"  cd {self.config['jobs_dir']} && ./run_all_local.sh")
        print("="*80)


def load_config(config_path):
    config = OmegaConf.load(config_path)
    return config


def load_config_for_energy(config_path, energy):
    """Expand configuration paths for a specific energy."""
    config = load_config(config_path)
    return OmegaConf.merge(config, {"energy": energy})


def find_input_files(source_dir, glob_pattern='*.hepmc'):
    """Find all 'glob_pattern' files in source directory."""

    search_path = os.path.join(source_dir, glob_pattern)
    files = glob(search_path)
    files.sort()

    if not files:
        print(f"\n  WARN! No 'glob_pattern' files found in '{source_dir}'")
        return None
    
    print(f"Found {len(files)} input files")

    return files


def exension_replacer(from_ext, to_ext):
    """Create a function to replace file extensions."""

    def replacer(input_file, output_dir):
        basename = os.path.basename(input_file)

        if not basename.endswith(from_ext):
            raise ValueError(f"Expected file with extension '{from_ext}', got: '{basename}'")
        
        output_name = basename.replace(from_ext, to_ext)
        return os.path.join(output_dir, output_name)
    
    return replacer