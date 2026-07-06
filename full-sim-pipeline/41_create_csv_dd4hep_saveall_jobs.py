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
    # NOTE: `set -u -o pipefail` but NOT `-e`. Each converter is independent: one
    # crashing (a ROOT macro that throws) must not abort the others. `run_macro`
    # isolates failures and deletes any empty output so it is retried next run
    # instead of being skipped as "already exists".
    return textwrap.dedent("""\
    #!/bin/bash
    set -uo pipefail

    echo "= CSV CONVERSION ============================================================"
    echo "  Input: {input_file}"
    echo "  Macros dir: {csv_convert_dir}"
    echo "==========================================================================="

    cd "{csv_convert_dir}"

    rc=0

    run_macro() {{
      local label="$1" macro="$2" out="$3"
      if [ ! -s "$out" ]; then
        echo "[RUN] $label via $macro"
        if ! root -x -l -b -q "$macro(\\"{input_file}\\",\\"$out\\")"; then
          echo "[WARN] $label: macro returned non-zero"; rc=1
        fi
        if [ -f "$out" ] && [ ! -s "$out" ]; then
          echo "[WARN] $label: produced empty $out -- removing"; rm -f "$out"; rc=1
        fi
      else
        echo "[SKIP] $label ($out exists, non-empty)"
      fi
    }}

    zip_if() {{
      local f="$1"
      if [ -s "$f" ] && [ ! -f "$f.zip" ]; then
        echo "[ZIP] $f -> $f.zip"
        python3 -m zipfile -c "$f.zip" "$f" || {{ echo "[WARN] zip $f failed"; rc=1; }}
      fi
    }}

    # acceptance_ppim writes three CSVs (ppim + pimin_hits + prot_hits).
    run_macro "acceptance_ppim" "csv_edm4hep_acceptance_ppim.cxx" "{acceptance_ppim_output}"
    zip_if "{acceptance_ppim_output}"
    zip_if "{acceptance_ppim_pimin_hits_output}"
    zip_if "{acceptance_ppim_prot_hits_output}"

    run_macro "acceptance_npi0" "csv_edm4hep_acceptance_npi0.cxx" "{acceptance_npi0_output}"
    zip_if "{acceptance_npi0_output}"

    run_macro "combinatorics_ppim" "csv_edm4hep_combinatorics_ppim.cxx" "{combinatorics_ppim_output}"
    zip_if "{combinatorics_ppim_output}"

    echo "==========================================================================="
    echo "Done. Outputs in: {input_dir} (rc=$rc)"
    exit $rc
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
        config.csv_dd4hep_saveall_input, '*.edm4hep.root', energy, config.csv_dd4hep_saveall_output
    )
    if input_files is None:
        return None

    bind_dirs = config.bind_dirs.copy() if 'bind_dirs' in config else []
    if csv_convert_dir not in bind_dirs:
        bind_dirs.append(csv_convert_dir)

    runner = JobCreator(
        input_files=input_files,
        output_file_name_func=output_name_func,
        output_dir=config.csv_dd4hep_saveall_output,
        bind_dirs=bind_dirs,
        events=config.event_count,
        container=config.container,
        beam_config=energy,
        slurm_files_per_job=int(config.get('slurm_files_per_job', 20)),
    )
    runner.container_script_template = create_container_script_template()
    runner.container_script_params_updater = make_custom_params_updater(config_path)
    runner.run()
    return runner


if __name__ == "__main__":
    run_pipeline(process_energy, description="Generate CSV conversion jobs (dd4hep).")