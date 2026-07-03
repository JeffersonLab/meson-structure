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
    # crashing (e.g. a ROOT macro that throws) must not abort the others. The
    # `convert` helper isolates failures and deletes any empty output so it is
    # retried on the next run instead of being skipped as "already exists".
    return textwrap.dedent("""\
    #!/bin/bash
    set -uo pipefail

    echo "= CSV CONVERSION ============================================================"
    echo "  Input: {input_file}"
    echo "  Macros dir: {csv_convert_dir}"
    echo "==========================================================================="

    cd "{csv_convert_dir}"

    rc=0

    convert() {{
      local label="$1" macro="$2" out="$3"

      # Regenerate when the CSV is missing OR empty (-s: exists and non-empty).
      if [ ! -s "$out" ]; then
        echo "[RUN] $label via $macro"
        if ! root -x -l -b -q "$macro(\\"{input_file}\\",\\"$out\\")"; then
          echo "[WARN] $label: macro returned non-zero"
          rc=1
        fi
        # A crashed macro leaves a 0-byte file; drop it so it is not mistaken
        # for a valid output (and gets retried next run) and is not zipped.
        if [ -f "$out" ] && [ ! -s "$out" ]; then
          echo "[WARN] $label: produced empty $out -- removing"
          rm -f "$out"
          rc=1
        fi
      else
        echo "[SKIP] $label CSV exists (non-empty)"
      fi

      if [ -s "$out" ] && [ ! -f "$out.zip" ]; then
        echo "[ZIP] $out -> $out.zip"
        python3 -m zipfile -c "$out.zip" "$out" || {{ echo "[WARN] $label: zip failed"; rc=1; }}
      fi
    }}

    convert "mc_dis"         "csv_mc_dis.cxx"         "{csv_mc_dis}"
    convert "reco_dis"       "csv_reco_dis.cxx"       "{csv_reco_dis}"
    convert "mcpart_lambda"  "csv_mcpart_lambda.cxx"  "{csv_mcpart_lambda}"
    convert "reco_ff_lambda" "csv_reco_ff_lambda.cxx" "{csv_reco_ff_lambda}"

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
        params['csv_mc_dis'] = os.path.join(output_dir, f"{csv_basename}.mc_dis.csv")
        params['csv_reco_dis'] = os.path.join(output_dir, f"{csv_basename}.reco_dis.csv")
        params['csv_mcpart_lambda'] = os.path.join(output_dir, f"{csv_basename}.mcpart_lambda.csv")
        params['csv_reco_ff_lambda'] = os.path.join(output_dir, f"{csv_basename}.reco_ff_lambda.csv")

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
        config.csv_eicrecon_input, '*.edm4eic.root', energy, config.csv_eicrecon_output
    )
    if input_files is None:
        return None

    bind_dirs = config.bind_dirs.copy() if 'bind_dirs' in config else []
    if csv_convert_dir not in bind_dirs:
        bind_dirs.append(csv_convert_dir)

    runner = JobCreator(
        input_files=input_files,
        output_file_name_func=output_name_func,
        output_dir=config.csv_eicrecon_output,
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
    run_pipeline(process_energy, description="Generate CSV conversion jobs (eicrecon).")