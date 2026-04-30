#!/usr/bin/env python3
"""
csv_convert_pipeline.py
Generate and submit CSV conversion jobs using JobCreator.
Processes .edm4eic.root files with ROOT macros to create CSV outputs.
"""

import os
from typing import Dict
import textwrap
from job_creator import JobCreator, find_inputs_or_skip, load_config, run_pipeline

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

    if [ ! -f "{combinatorics_ppim_output}.zip" ]; then
        echo "[RUN] csv_edm4hep_combinatorics_ppim for {input_file}"
        root -x -l -b -q csv_edm4hep_combinatorics_ppim.cxx'("{input_file}","{combinatorics_ppim_output}")'
        echo "[ZIP] zipping files"
        python3 -m zipfile -c "{combinatorics_ppim_output}.zip" "{combinatorics_ppim_output}"
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
        params['combinatorics_ppim_output'] = os.path.join(output_dir, f"{csv_basename}.combinatorics_ppm.csv")

        return params
    return custom_params_updater


def output_name_func(input_file, output_dir):
    """Output files are created in the same directory as input."""
    return os.path.dirname(input_file)


def process_energy(config, energy, config_path):
    """Build a JobCreator for one beam energy."""
    csv_convert_dir = config.get('csv_convert_dir', csv_convert_dir_default)
    print(f"CSV Macros: {csv_convert_dir}")

    input_files = find_inputs_or_skip(
        config.csv_dd4hep_input, '*.edm4hep.root', energy, config.csv_dd4hep_output
    )
    if input_files is None:
        return None

    bind_dirs = config.bind_dirs.copy() if 'bind_dirs' in config else []
    if csv_convert_dir not in bind_dirs:
        bind_dirs.append(csv_convert_dir)

    runner = JobCreator(
        input_files=input_files,
        output_file_name_func=output_name_func,
        output_dir=config.csv_dd4hep_output,
        bind_dirs=bind_dirs,
        events=config.event_count,
        container=config.container,
        beam_config=energy,
    )
    runner.container_script_template = create_container_script_template()
    runner.container_script_params_updater = make_custom_params_updater(config_path)
    runner.run()
    return runner


if __name__ == "__main__":
    run_pipeline(process_energy, description="Generate CSV conversion jobs (dd4hep).")