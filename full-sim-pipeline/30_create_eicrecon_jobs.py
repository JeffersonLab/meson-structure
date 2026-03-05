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
    echo "= EICRECON ==================================================================="
    echo "==========================================================================="
    echo "  Running eicrecon on:"
    echo "    {input_file}"
    echo "  Resulting files:"
    echo "    {output_file}.*"

    source /opt/detector/epic-main/bin/thisepic.sh
    cd $(dirname {output_file})
    /usr/bin/time -v /usr/bin/time -v eicrecon -Pdd4hep:xml_files=$DETECTOR_PATH/epic_craterlake_{beam_config}.xml  -Ppodio:output_file={output_file}  {input_file} 2>&1
    
    echo ""
    echo "=========================================================================="
    echo "Job completed!"
    echo "Output: {output_file}"
    echo "=========================================================================="
    """)



def process_energy(config, energy):
    """Process all files for a specific energy."""

    source_dir = config.dd4hep_output
    output_dir = config.eicrecon_output
    
    print("\n" + "="*60)
    print(f"PROCESSING ENERGY: {energy} GeV")
    print(f"Source: {source_dir}")
    print(f"Output: {output_dir}")
    
    # Find input files
    input_files = find_input_files(source_dir, '*.edm4hep.root')
    if input_files is None:
        print(f"Skipping energy {energy} GeV due to no input files.")
        return

    # Create JobRunner instance with proper initialization
    runner = JobRunner(
        input_files=input_files,
        output_file_name_func=exension_replacer('.edm4hep.root', '.edm4eic.root'),
        output_dir=output_dir,
        bind_dirs=config.bind_dirs,
        events=config.event_count,
        container=config.container,
        beam_config=energy
    )
    
    # Set the container job template
    runner.container_script_template = create_container_script_template()
    
    # Run the job generator
    runner.run()
    
    print("="*60)
    print(f"✓ Completed processing for {energy} GeV\n\n")


def main():
    """Main entry point."""

    parser = argparse.ArgumentParser(description="Generate eicrecon jobs.")
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