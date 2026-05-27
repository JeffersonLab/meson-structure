#!/usr/bin/env python3
"""
22_create_npsim_background_jobs.py

Run npsim on the merged signal+background hepmc3.tree.root files produced by
11_create_background_jobs.py.

The SignalBackgroundMerger shifts each background source's generator-status by
a fixed offset (synrad=2000, ebrems=3000, ecoulomb=4000, etouschek=5000,
optionally p-beam-gas=6000) so that downstream code can tell which source
contributed which particle. DD4hep/npsim by default only treats status==1 as
'stable, propagate through Geant4' and status==2 as 'decayed, skip'. The
shifted codes (2001, 3001, ...) are unknown and would be silently dropped, so
we have to extend the stable/decay status sets via:

  --physics.alternativeStableStatuses "1 2001 3001 4001 5001 [6001]"
  --physics.alternativeDecayStatuses  "2 2002 3002 4002 5002 [6002]"

Those lists are built dynamically here from the same per-energy cocktail JSON
that stage 11 used. If you swap in an `_hgas_` cocktail (which adds a 6000
status bucket for proton beam-gas), the flags update automatically.

Output: `*.edm4hep.root` under `dd4hep_saveall_output`. Stage 30 (eicrecon)
consumes that just like in the non-background pipeline.
"""

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
# Status-list derivation
# ---------------------------------------------------------------------------

def load_status_offsets(config, energy):
    """Return the list of integer status offsets from the cocktail JSON.

    Returns None if the cocktail JSON is not available — caller will skip.
    """
    bg_configs = config.get("background_configs", {})
    if energy not in bg_configs:
        print(f"  WARN: no background_configs entry for '{energy}', skipping.")
        return None

    cocktail_path = os.path.join(
        str(config.background_config_dir), str(bg_configs[energy])
    )
    if not os.path.isfile(cocktail_path):
        print(f"  WARN: cocktail JSON not found: {cocktail_path}")
        return None

    with open(cocktail_path, "r") as fh:
        entries = json.load(fh)

    offsets = sorted(int(e["status"]) for e in entries)
    print(f"  Cocktail status offsets: {offsets}")
    return offsets


def build_status_lists(bg_offsets, signal_offset=0):
    """Return ('1 2001 3001 ...', '2 3002 4002 ...') as plain strings.

    DD4hep's CLI parser accepts a single space-separated string for both
    --physics.alternativeStableStatuses and --physics.alternativeDecayStatuses
    (see DD4hep DDG4/python/DDSim/Helper/Physics.py -> makeSet()).

    The signal's '+1' = stable and '+2' = decay must be in there too, or
    signal events get silently dropped. signal_offset defaults to 0 to match
    the merger's --signalStatus 0.
    """
    all_offsets = [signal_offset] + list(bg_offsets)
    stable = " ".join(str(off + 1) for off in all_offsets)
    decay = " ".join(str(off + 2) for off in all_offsets)
    return stable, decay


# ---------------------------------------------------------------------------
# Container script template
# ---------------------------------------------------------------------------

def create_container_script_template():
    """Container job template for npsim on background-merged input.

    Differences vs. the non-background stage 21:

      * --inputFiles is a hepmc3.tree.root, so we need
            --hepmc3.useHepMC3 true
            --runType batch
      * The status-offset flags need to be set or backgrounds disappear.

    --part.userParticleHandler="" is kept from stage 21 to match the rest of
    this pipeline (it disables the EIC custom particle handler that would
    otherwise re-filter primaries).
    """
    return textwrap.dedent("""\
    #!/bin/bash
    set -e

    echo ">"
    echo "= NPSIM (bg-merged) ======================================================="
    echo "==========================================================================="
    echo "  Input:    {input_file}"
    echo "  Output:   {output_file}"
    echo "  Stable:   {alt_stable_statuses}"
    echo "  Decay:    {alt_decay_statuses}"
    echo

    mkdir -p $(dirname {output_file})
    cd $(dirname {output_file})/..

    if [ -f "/opt/detector/epic-main/bin/thisepic.sh" ]; then
        source /opt/detector/epic-main/bin/thisepic.sh
    fi

    /usr/bin/time -v npsim \\
        --part.userParticleHandler="" \\
        --compactFile=$DETECTOR_PATH/epic_craterlake_{beam_config}.xml \\
        --runType batch \\
        --hepmc3.useHepMC3 true \\
        --physics.alternativeStableStatuses "{alt_stable_statuses}" \\
        --physics.alternativeDecayStatuses  "{alt_decay_statuses}" \\
        --inputFiles {input_file} \\
        --outputFile {output_file} \\
        --numberOfEvents {events} 2>&1

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

    bg_offsets = load_status_offsets(config, energy)
    if bg_offsets is None:
        return None

    stable_str, decay_str = build_status_lists(bg_offsets, signal_offset=0)
    print(f"  --physics.alternativeStableStatuses \"{stable_str}\"")
    print(f"  --physics.alternativeDecayStatuses  \"{decay_str}\"")

    input_files = find_inputs_or_skip(
        config.dd4hep_saveall_input, "*.bg.hepmc3.tree.root", energy,
        config.dd4hep_saveall_output,
    )
    if input_files is None:
        return None

    runner = JobCreator(
        input_files=input_files,
        output_file_name_func=exension_replacer(
            ".bg.hepmc3.tree.root", ".edm4hep.root"
        ),
        output_dir=config.dd4hep_saveall_output,
        bind_dirs=config.bind_dirs,
        events=config.event_count,
        container=config["container"],
        beam_config=energy,
    )
    runner.container_script_template = create_container_script_template()

    runner.container_script_params_updater = lambda params: {
        **params,
        "alt_stable_statuses": stable_str,
        "alt_decay_statuses": decay_str,
    }

    runner.run()
    return runner


if __name__ == "__main__":
    run_pipeline(
        process_energy,
        description="Generate npsim jobs for background-merged input "
                    "(with status-offset flags).",
    )
