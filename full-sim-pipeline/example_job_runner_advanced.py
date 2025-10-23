#!/usr/bin/env python3
"""
example_advanced.py

Advanced example showing custom script generation with JobRunner.
Demonstrates how to override the default generation function for complex workflows.
"""

import os
import glob
from job_runner import JobRunner


def main():
    """Advanced example with custom script generation."""
    
    # Custom function to determine output names with subdirectories
    def output_name_with_subdir(input_file, output_dir):
        """Create output path with energy-based subdirectory."""
        basename = os.path.basename(input_file)
        
        # Extract energy from filename (assuming format like "data_100GeV.hepmc")
        if 'GeV' in basename:
            energy = basename.split('GeV')[0].split('_')[-1]
            subdir = f"{energy}GeV"
        else:
            subdir = "unknown"
        
        # Create output path with subdirectory
        output_subdir = os.path.join(output_dir, subdir)
        output_name = basename.replace('.hepmc', '.root')
        return os.path.join(output_subdir, output_name)
    
    # Find all input files
    input_files = glob.glob('/data/sim/raw/*.hepmc')
    
    # Initialize runner with full configuration
    runner = JobRunner(
        input_files=input_files,
        output_file_name_func=output_name_with_subdir,
        output_dir='/scratch/results',
        bind_dirs=['/cvmfs', '/scratch', '/data'],
        events=10000,
        container='/cvmfs/singularity.opensciencegrid.org/my/analysis:latest',
        slurm_time='48:00:00',
        slurm_cpus_per_task=4,
        slurm_mem_per_cpu='8G',
        slurm_account='physics',
        slurm_partition='gpu'
    )
    
    # Custom container script generation function
    def custom_generate_script(input_file):
        """Generate custom script with additional parameters and logic."""
        basename = os.path.splitext(os.path.basename(input_file))[0]
        
        # Extract parameters from filename or calculate them
        if '100GeV' in input_file:
            detector_config = 'high_energy'
            beam_energy = 100
        elif '50GeV' in input_file:
            detector_config = 'medium_energy'
            beam_energy = 50
        else:
            detector_config = 'default'
            beam_energy = 10
        
        # Get the output file path
        output_file = runner.output_file_name_func(input_file, runner.config['output_dir'])
        
        # Build the custom script content
        content = f'''#!/bin/bash
set -e

# Job information
echo "=============================================="
echo "Custom Analysis Pipeline"
echo "=============================================="
echo "Hostname: $(hostname)"
echo "Date: $(date)"
echo "Input: {input_file}"
echo "Output: {output_file}"
echo "Beam Energy: {beam_energy} GeV"
echo "Detector Config: {detector_config}"
echo "=============================================="

# Set up environment
source /opt/setup.sh
export DETECTOR_CONFIG={detector_config}
export BEAM_ENERGY={beam_energy}

# Create output directory
mkdir -p $(dirname {output_file})

# Step 1: Pre-processing
echo "Step 1: Pre-processing..."
preprocess_data \\
    --input {input_file} \\
    --config $DETECTOR_CONFIG \\
    --output /tmp/{basename}.preprocessed

# Step 2: Main analysis
echo "Step 2: Running main analysis..."
run_analysis \\
    --input /tmp/{basename}.preprocessed \\
    --beam-energy $BEAM_ENERGY \\
    --events {runner.config['events']} \\
    --threads {runner.config['slurm_cpus_per_task']} \\
    --output /tmp/{basename}.analyzed

# Step 3: Post-processing and validation
echo "Step 3: Post-processing..."
postprocess_results \\
    --input /tmp/{basename}.analyzed \\
    --validate \\
    --output {output_file}

# Cleanup temporary files
rm -f /tmp/{basename}.*

# Generate QA plots
echo "Generating QA plots..."
generate_qa_plots \\
    --input {output_file} \\
    --output $(dirname {output_file})/qa_{basename}.pdf

echo "=============================================="
echo "Job completed successfully!"
echo "Results: {output_file}"
echo "=============================================="
'''
        
        return {
            'basename': basename,
            'content': content
        }
    
    # Replace the default generator with our custom one
    runner.generate_container_script = custom_generate_script
    
    # Custom SLURM template with GPU support
    runner.slurm_script_template = '''#!/bin/bash
#SBATCH --account={slurm_account}
#SBATCH --partition={slurm_partition}
#SBATCH --job-name={basename}
#SBATCH --time={slurm_time}
#SBATCH --cpus-per-task={slurm_cpus_per_task}
#SBATCH --mem-per-cpu={slurm_mem_per_cpu}
#SBATCH --gres=gpu:1
#SBATCH --output={log_file}
#SBATCH --error={err_file}

set -e

echo "Starting GPU-enabled job for {basename} at $(date)"
echo "Running on: $(hostname)"
echo "GPU info:"
nvidia-smi

# Load required modules
module load cuda/11.8
module load singularity

# Run container with GPU support
singularity exec --nv {bindings} {container} {container_script}

echo "Job finished at $(date)"
'''
    
    # Generate all scripts
    runner.run()
    
    print("\n✅ Advanced job pipeline generated successfully!")
    print("This example demonstrated:")
    print("  - Custom output path generation with subdirectories")
    print("  - Custom script generation based on input file properties")
    print("  - Multi-step processing pipeline")
    print("  - Custom SLURM template with GPU support")
    print("  - Dynamic parameter calculation")


if __name__ == "__main__":
    main()