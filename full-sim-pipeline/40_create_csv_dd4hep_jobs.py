#!/usr/bin/env python3
"""
csv_convert_pipeline.py
Generate and submit CSV conversion jobs using JobRunner.
Processes .edm4eic.root files with ROOT macros to create CSV outputs.
"""

import argparse
import os
from typing import Dict
import textwrap
from job_runner import JobRunner, find_input_files, load_config, load_config_for_energy

this_dir = os.path.dirname(os.path.abspath(__file__))
csv_convert_dir_default = os.path.join(os.path.dirname(this_dir), 'csv_convert')


def create_container_script_template():
    """Create container job template for CSV conversion (simple & readable)."""
    return textwrap.dedent("""\
    #!/bin/bash
    set -euo pipefail

    echo "= CSV CONVERSION ============================================================"
    echo "  Input: {input_file}"
    echo "  Macros dir: {csv_convert_dir}"
    echo "==========================================================================="

    cd "{csv_convert_dir}"

    if [ ! -f "{acceptance_ppim_output}.zip" ] || [ ! -f "{acceptance_ppim_pimin_hits_output}.zip" ] || [ ! -f "{acceptance_ppim_prot_hits_output}.zip" ]; then
        echo "[RUN] ccsv_edm4hep_acceptance_ppim for {input_file}"
        root -x -l -b -q csv_edm4hep_acceptance_ppim.cxx'("{input_file}","{acceptance_ppim_output}")'
        echo "[ZIP] zipping files"
        python3 -m zipfile -c "{acceptance_ppim_output}.zip" "{acceptance_ppim_output}"
        python3 -m zipfile -c "{acceptance_ppim_pimin_hits_output}.zip" "{acceptance_ppim_pimin_hits_output}"
        python3 -m zipfile -c "{acceptance_ppim_prot_hits_output}.zip" "{acceptance_ppim_prot_hits_output}"
    else
        echo "[SKIP] zipped files exists for {input_file}"
    fi

    echo "==========================================================================="

    if [ ! -f "{acceptance_npi0_output}.zip" ]; then
        echo "[RUN] csv_edm4hep_acceptance_npi0 for {input_file}"
        root -x -l -b -q csv_edm4hep_acceptance_npi0.cxx'("{input_file}","{acceptance_npi0_output}")'
        echo "[ZIP] zipping files"
        python3 -m zipfile -c "{acceptance_npi0_output}.zip" "{acceptance_npi0_output}"
    else
        echo "[SKIP] zipped files exists for {input_file}"
    fi
    
   
    echo "==========================================================================="
    echo "Done. Outputs in: {input_dir}"
    """)



def make_custom_params_updater(config_path):
    """Create a custom params updater with access to the config path."""
    def custom_params_updater(params: Dict) -> Dict:
        """Add custom parameters for CSV conversion."""
        config = load_config(config_path)

        input_file = params['input_file']
        input_dir = os.path.dirname(input_file)
        output_dir = params['output_dir']
        csv_basename = os.path.basename(input_file).replace('.edm4eic.root', '')

        params['csv_convert_dir'] = config.get('csv_convert_dir', csv_convert_dir_default)
        params['input_dir'] = input_dir
        params['acceptance_ppim_output'] = os.path.join(output_dir, f"{csv_basename}.acceptance_ppim.csv")
        params['acceptance_ppim_pimin_hits_output'] = os.path.join(output_dir, f"{csv_basename}.acceptance_ppim_pimin_hits.csv")
        params['acceptance_ppim_prot_hits_output'] = os.path.join(output_dir, f"{csv_basename}.acceptance_ppim_prot_hits.csv")
        params['acceptance_npi0_output'] = os.path.join(output_dir, f"{csv_basename}.acceptance_npi0.csv")
   

        return params
    return custom_params_updater


def output_name_func(input_file, output_dir):
    """Output files are created in the same directory as input."""
    return os.path.dirname(input_file)


def process_energy(config, config_path, energy):
    """Process all files for a specific energy."""

    output_dir = config.csv_dd4hep_output
    csv_convert_dir = config.get('csv_convert_dir', csv_convert_dir_default)

    print("\n" + "="*80)
    print(f"PROCESSING ENERGY: {energy} GeV")
    print(f"Source: {config.dd4hep_output}")
    print(f"CSV Macros: {csv_convert_dir}")

    # Find input files
    input_files = find_input_files(config.dd4hep_output, '*.edm4hep.root')
    if input_files is None:
        print(f"Skipping energy {energy} GeV due to no input files.")
        return

    # Build bind_dirs - include csv_convert_dir
    bind_dirs = config.bind_dirs.copy() if 'bind_dirs' in config else []

    # Ensure csv_convert_dir is in bind_dirs
    if csv_convert_dir not in bind_dirs:
        bind_dirs.append(csv_convert_dir)

    # Create JobRunner instance
    runner = JobRunner(
        input_files=input_files,
        output_file_name_func=output_name_func,
        output_dir=output_dir,
        bind_dirs=bind_dirs,
        events=config.event_count,
        container=config.container,
        beam_config=energy
    )

    # Set the container job template
    runner.container_script_template = create_container_script_template()

    # Add custom parameters updater
    runner.container_script_params_updater = make_custom_params_updater(config_path)

    # Run the job generator
    runner.run()

    print("="*80)
    print(f"✓ Completed processing for {energy} GeV\n\n")


def main():
    """Main entry point."""

    parser = argparse.ArgumentParser(description="Generate CSV conversion jobs.")
    parser.add_argument('-c', '--config', required=True, help="Path to config YAML file")
    args = parser.parse_args()

    config = load_config(args.config)
    energies = config.get('energies', [])

    print(f"{'='*80}\n CSV CONVERSION PIPELINE\n{'='*80}")
    print(f"Energies to process: {energies}\n")

    # Process each energy
    for energy in energies:
        config = load_config_for_energy(args.config, energy)
        process_energy(config, args.config, energy)

    print("\n" + "="*80)
    print("ALL ENERGIES PROCESSED SUCCESSFULLY")
    print("="*80)


if __name__ == "__main__":
    main()