#!/usr/bin/env python3
"""
npsim_pipeline.py

Generate and submit npsim jobs using JobRunner.
Reads config.yaml from the same directory.
"""

import os
import yaml
import glob
import textwrap
from job_runner import JobRunner



def create_npsim_template():
    """Create container job template for npsim."""
    return textwrap.dedent("""\
    #!/bin/bash
    set -e
    
    echo "=========================================================================="
    echo "=NPSIM===================================================================="
    echo "=========================================================================="
    echo "  Running npsim on:"
    echo "    {input_file}"
    echo "  Resulting file:"
    echo "    {output_file}"
    echo "  Events to process:"
    echo "    {events}"
    echo "  DETECTOR_PATH:"
    echo "    $DETECTOR_PATH"
    echo "=========================================================================="
    echo ""
    
    mkdir -p $(dirname {output_file})
    
    /usr/bin/time -v npsim \\
        --compactFile=$DETECTOR_PATH/epic.xml \\
        --runType run \\
        --inputFiles {input_file} \\
        --outputFile {output_file} \\
        --numberOfEvents {events} \\
        2>&1
    
    echo ""
    echo "=========================================================================="
    echo "Job completed!"
    echo "Output: {output_file}"
    echo "=========================================================================="
    """)


def load_config():
    """Load configuration from config.yaml in script directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.yaml')
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def find_input_files(source_dir):
    """Find all *.afterburner.hepmc files in source directory."""
    search_path = os.path.join(source_dir, '*.afterburner.hepmc')
    files = glob.glob(search_path)
    files.sort()
    return files


def get_output_filename(input_file, output_dir):
    """Generate output filename from input filename."""
    basename = os.path.basename(input_file)
    
    if not basename.endswith('.afterburner.hepmc'):
        raise ValueError(f"Expected .afterburner.hepmc file, got: {basename}")
    
    output_name = basename.replace('.afterburner.hepmc', '.edm4hep.root')
    return os.path.join(output_dir, output_name)




def process_energy(config, energy):
    """Process all files for a specific energy."""
    
    print("\n" + "="*60)
    print(f"PROCESSING ENERGY: {energy} GeV")
    print("="*60)
    
    # Expand paths
    base_dir = config['base_dir']
    source_dir = config['dd4hep_source'].format(base_dir=base_dir, energy=energy)
    output_dir = config['dd4hep_output'].format(base_dir=base_dir, energy=energy)
    
    print(f"Source: {source_dir}")
    print(f"Output: {output_dir}")
    
    # Find input files
    input_files = find_input_files(source_dir)
    
    if not input_files:
        print(f"\n⚠️  No *.afterburner.hepmc files found in {source_dir}")
        return
    
    print(f"Found {len(input_files)} input files")
    
    # Determine bind directories - include base_dir and any additional ones
    bind_dirs = [base_dir]
    if 'bind_dirs' in config:
        bind_dirs.extend(config['bind_dirs'])

    # Get event count from config
    event_count = config.get('event_count', 5000)
    
   
    # Create JobRunner instance with proper initialization
    runner = JobRunner(
        input_files=input_files,
        output_file_name_func=get_output_filename,
        output_dir=output_dir,
        bind_dirs=bind_dirs,
        events=event_count,
        container=config['container'],
    )
    
    # Set the container job template
    runner.container_job_template = create_npsim_template()
    
    # Run the job generator
    runner.run()
    
    print(f"\n✓ Completed processing for {energy} GeV")


def main():
    """Main entry point."""
    
    # Load config
    config = load_config()
    
    print("\n" + "="*60)
    print("NPSIM DD4HEP JOB GENERATOR")
    print("="*60)
    print(f"Base directory: {config['base_dir']}")
    print(f"Container:      {config['container']}")
    print(f"Event count:    {config.get('event_count', -1)}")
    
    # Get list of energies to process
    energies = config.get('energies', [])
    if not energies:
        print("\n⚠️  No energies specified in config.yaml")
        print("   Add 'energies: [100, 200, 500]' to your config")
        return
    
    print(f"Energies to process: {energies}")

    # Process each energy
    for energy in energies:
        process_energy(config, energy)

    print("\n" + "="*60)
    print("ALL ENERGIES PROCESSED SUCCESSFULLY")
    print("="*60)
    print("\nNext steps:")
    print("1. Review the generated scripts in each energy's jobs/ directory")
    print("2. Submit SLURM jobs: cd to jobs/ and run ./submit_all_slurm_jobs.sh")
    print("3. Or run locally: cd to jobs/ and run ./run_all_local.sh")


if __name__ == "__main__":
    main()