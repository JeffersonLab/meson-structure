#!/usr/bin/env python3
"""
npsim_pipeline.py
Generate and submit afterburner jobs using JobRunner.
"""

import argparse
import os
from typing import Dict
import yaml
import glob
import textwrap
from job_runner import JobRunner, exension_replacer, find_input_files, load_config, load_config_for_energy


def create_container_script_template():
    """Create container job template for npsim."""
    return textwrap.dedent("""\
    #!/bin/bash
    set -e
    
    mkdir -p $(dirname {output_file})
    
    echo ">"
    echo "=ABCONV===================================================================="
    echo "==========================================================================="
    echo "  Running afterburner on:"
    echo "    {input_file}"
    echo "  Resulting files:"
    echo "    {output_file}.*"
    /usr/bin/time -v abconv {afterburn_preset_flag} {input_file} --output {output_file} 2>&1
    
    echo ""
    echo "=========================================================================="
    echo "Job completed!"
    echo "Output: {output_file}"
    echo "=========================================================================="
    """)



def process_energy(config, energy):
    """Process all files for a specific energy."""

    source_dir = config.afterburner_source
    output_dir = config.afterburner_output
    
    print("\n" + "="*60)
    print(f"PROCESSING ENERGY: {energy} GeV")
    print(f"Source: {source_dir}")
    print(f"Output: {output_dir}")
    
    # Find input files
    input_files = find_input_files(source_dir, '*.hepmc')
    if input_files is None:
        print(f"Skipping energy {energy} GeV due to no input files.")
        return


    # Create JobRunner instance with proper initialization
    runner = JobRunner(
        input_files=input_files,
        output_file_name_func=exension_replacer('.hepmc', ''),  # afterburner adds extension by itself, so we remove it here
        output_dir=output_dir,
        bind_dirs=config.bind_dirs,
        events=config.event_count,
        container=config['container'],
    )
    
    # Set the container job template and content generator
    runner.container_script_template = create_container_script_template()
    runner.container_script_params_updater = lambda params: {
            **params,
            'afterburn_preset_flag': "--preset=ip6_ep_130x10" if "10x130" in params['basename'] else ""
        }
    
    # Run the job generator
    runner.run()
    
    print("="*60)
    print(f"✓ Completed processing for {energy} GeV\n\n")


def main():
    """Main entry point."""

    parser = argparse.ArgumentParser(description="Generate afterburner jobs.")
    parser.add_argument('-c', '--config', required=True, help="Path to config YAML file")
    args = parser.parse_args()

    # Load config
    config = load_config(args.config)
    energies = config.get('energies', [])

    # Process each energy
    print(f"Energies to process: {energies}")
    for energy in energies:
        config = load_config_for_energy(args.config, energy)
        process_energy(config, energy)

    print("ALL ENERGIES PROCESSED SUCCESSFULLY")


if __name__ == "__main__":
    main()