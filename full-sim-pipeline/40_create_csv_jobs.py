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

    convert() {{
      local label="$1" macro="$2" out="$3"

      if [ ! -f "$out" ]; then
        echo "[RUN] $label via $macro"
        root -x -l -b -q "$macro(\\"{input_file}\\",\\"$out\\")"
      else
        echo "[SKIP] $label CSV exists"
      fi

      if [ -f "$out" ] && [ ! -f "$out.zip" ]; then
        echo "[ZIP] $out -> $out.zip"
        python3 -m zipfile -c "$out.zip" "$out"
      else
        echo "[SKIP] $label zip exists or CSV missing"
      fi
    }}

    convert "mc_dis"         "csv_mc_dis.cxx"         "{csv_mc_dis}"
    convert "reco_dis"       "csv_reco_dis.cxx"       "{csv_reco_dis}"
    convert "mcpart_lambda"  "csv_mcpart_lambda.cxx"  "{csv_mcpart_lambda}"
    convert "reco_ff_lambda" "csv_reco_ff_lambda.cxx" "{csv_reco_ff_lambda}"

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
        params['csv_mc_dis'] = os.path.join(output_dir, f"{csv_basename}.mc_dis.csv")
        params['csv_reco_dis'] = os.path.join(output_dir, f"{csv_basename}.reco_dis.csv")
        params['csv_mcpart_lambda'] = os.path.join(output_dir, f"{csv_basename}.mcpart_lambda.csv")
        params['csv_reco_ff_lambda'] = os.path.join(output_dir, f"{csv_basename}.reco_ff_lambda.csv")

        return params
    return custom_params_updater


def output_name_func(input_file, output_dir):
    """Output files are created in the same directory as input."""
    return os.path.dirname(input_file)


def process_energy(config, config_path, energy):
    """Process all files for a specific energy."""

    source_dir = config.eicrecon_output
    output_dir = config.csv_output
    csv_convert_dir = config.get('csv_convert_dir', csv_convert_dir_default)

    print("\n" + "="*80)
    print(f"PROCESSING ENERGY: {energy} GeV")
    print(f"Source: {source_dir}")
    print(f"CSV Macros: {csv_convert_dir}")

    # Find input files
    input_files = find_input_files(source_dir, '*.edm4eic.root')
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