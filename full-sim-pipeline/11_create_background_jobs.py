#!/usr/bin/env python3
"""
11_create_background_jobs.py

Generate SignalBackgroundMerger jobs that mix the afterburned signal HepMC
files with the official ePIC background cocktails into 2us timeframes.

For each energy listed in the campaign YAML this script:

  1. looks up the per-energy cocktail JSON in `background_configs[energy]`
  2. loads `${background_config_dir}/<json>`, which is a list of entries
        {"file": <xrootd URL>, "freq": <events/ns>, "skip": <fraction>,
         "status": <generator-status offset>}
  3. for every afterburned signal *.afterburner.hepmc file under
     `bg_merger_input`, emits a container script that runs
     `SignalBackgroundMerger` with --signalFreq 0 (= exactly one signal per
     2 us frame) and one --bgFile entry per cocktail source.

Output: `*.bg.hepmc3.tree.root` files under `bg_merger_output`, consumed by
22_create_npsim_background_jobs.py.

The cocktail JSON is also the source of truth for stage 22's status-offset
flags — 22 re-reads it (it does NOT depend on this script having run first).
"""

import hashlib
import json
import os
import textwrap

from job_creator import (
    JobCreator,
    exension_replacer,
    find_inputs_or_skip,
    run_pipeline,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_bg_cocktail(config, energy):
    """Return the list of {file, freq, skip, status} dicts for one energy.

    Returns None if the energy is not present in `background_configs` (the
    caller will skip the energy).
    """
    bg_configs = config.get("background_configs", {})
    if energy not in bg_configs:
        print(f"  WARN: no background_configs entry for '{energy}', skipping.")
        return None

    cocktail_path = os.path.join(
        str(config.background_config_dir), str(bg_configs[energy])
    )

    if not os.path.isfile(cocktail_path):
        # Soft-fail with a clear message — we still want to emit jobs that the
        # user can fix later, rather than crashing the whole pipeline.
        print(f"  WARN: cocktail JSON not found: {cocktail_path}")
        print(f"        (it must be visible inside the container too)")
        return None

    with open(cocktail_path, "r") as fh:
        entries = json.load(fh)

    print(f"  Cocktail: {cocktail_path}")
    print(f"    {len(entries)} background sources:")
    for e in entries:
        print(f"      status={e['status']:>5}  freq={e['freq']:<12g}  "
              f"skip={e['skip']:<5}  {os.path.basename(e['file'])}")
    return entries


def build_bg_args(entries):
    """Build the `--bgFile <file> <freq> <skip> <status>` argument string."""
    parts = []
    for e in entries:
        # SignalBackgroundMerger takes 4 positional values after --bgFile.
        parts.append(
            f"--bgFile {e['file']} {e['freq']} {e['skip']} {int(e['status'])}"
        )
    # Backslash-newline so the rendered container script stays readable.
    return " \\\n        ".join(parts)


def derive_seed(basename):
    """Per-file deterministic RNG seed for the merger.

    All bg jobs in this pipeline share the same input set, so we want each
    output file to use a different Poisson realisation. Hashing the basename
    gives us reproducible, distinct seeds without an explicit chunk index.
    """
    h = hashlib.md5(basename.encode()).hexdigest()[:8]
    # Keep it inside a signed-int32 range to play nice with everything.
    return (int(h, 16) % (2**31 - 1)) + 1


# ---------------------------------------------------------------------------
# Container script template
# ---------------------------------------------------------------------------

def create_container_script_template():
    """Container job template for SignalBackgroundMerger.

    Note on streaming: the bg cocktail entries are root://dtn-eic.jlab.org/...
    URLs, so the container needs XRootD access. inside `eic_xl` that works
    out of the box for read-only public files; if you ever hit auth issues,
    set BEARER_TOKEN or X509_USER_PROXY before sbatch.
    """
    return textwrap.dedent("""\
    #!/bin/bash
    set -e

    echo ">"
    echo "= SIGNAL+BG MERGE ========================================================="
    echo "==========================================================================="
    echo "  Signal:    {input_file}"
    echo "  Cocktail:  {bg_cocktail_path}"
    echo "  Slices:    {events}   (each = 1 signal event + Poisson bg, 2us frame)"
    echo "  RNG seed:  {rng_seed}"
    echo "  Output:    {output_file}"
    echo

    mkdir -p $(dirname {output_file})

    if [ -f "/opt/detector/epic-main/bin/thisepic.sh" ]; then
        source /opt/detector/epic-main/bin/thisepic.sh
    fi

    /usr/bin/time -v SignalBackgroundMerger \\
        --rngSeed {rng_seed} \\
        --nSlices {events} \\
        --signalFile {input_file} \\
        --signalFreq 0 \\
        --signalStatus 0 \\
        {bg_args} \\
        --outputFile {output_file} 2>&1

    echo
    echo "=========================================================================="
    echo "Job completed!"
    echo "Output: {output_file}"
    echo "=========================================================================="
    """)


# ---------------------------------------------------------------------------
# Pipeline entry point
# ---------------------------------------------------------------------------

def process_energy(config, energy, config_path=None):
    """Build a JobCreator for one beam energy."""

    # Load the cocktail JSON first — if missing, skip the whole energy.
    bg_entries = load_bg_cocktail(config, energy)
    if bg_entries is None:
        return None

    input_files = find_inputs_or_skip(
        config.bg_merger_input, "*.afterburner.hepmc", energy,
        config.bg_merger_output,
    )
    if input_files is None:
        return None

    bg_args_str = build_bg_args(bg_entries)
    bg_cocktail_path = os.path.join(
        str(config.background_config_dir),
        str(config.background_configs[energy]),
    )

    runner = JobCreator(
        input_files=input_files,
        output_file_name_func=exension_replacer(
            ".afterburner.hepmc", ".bg.hepmc3.tree.root"
        ),
        output_dir=config.bg_merger_output,
        bind_dirs=config.bind_dirs,
        events=config.event_count,
        container=config["container"],
        beam_config=energy,
    )
    runner.container_script_template = create_container_script_template()

    # Inject per-job (rng_seed) and per-energy (bg_args, cocktail path) fields
    # into the template's format() call.
    def updater(params):
        return {
            **params,
            "bg_args": bg_args_str,
            "bg_cocktail_path": bg_cocktail_path,
            "rng_seed": derive_seed(params["basename"]),
        }

    runner.container_script_params_updater = updater
    runner.run()
    return runner


if __name__ == "__main__":
    run_pipeline(
        process_energy,
        description="Generate SignalBackgroundMerger jobs (signal+bg mixing).",
    )
