#!/usr/bin/env python3
"""
23_create_npsim_stv_jobs.py

Generate npsim jobs for the "smart tracking volume" (STV) variant of the
2026-06 campaign.

This variant runs npsim with the EIC smart-tracking-volume particle handler

    --part.userParticleHandler=Geant4TVEicParticleHandler

which is provided by the custom `smart-tracking-volume` branch of npsim that
ships inside the eicdev/eic-full:latest image (set as `container` in
config-campaign-26-06-stv.yaml). It is the counterpart of:

  * 20_create_npsim_jobs.py          -> Geant4TVUserParticleHandler (default TV)
  * 21_create_npsim_saveall_jobs.py  -> ""  (no handler, keep all particles)

Input : afterburned signal *.afterburner.hepmc under config.dd4hep_stv_input
Output: *.edm4hep.root under config.dd4hep_stv_output
"""

import textwrap
from job_creator import JobCreator, exension_replacer, find_inputs_or_skip, run_pipeline


def create_container_script_template():
    """Create container job template for npsim (smart tracking volume)."""
    return textwrap.dedent("""\
    #!/bin/bash
    set -e

    echo ">"
    echo "= NPSIM (smart tracking volume) ==========================================="
    echo "==========================================================================="
    echo "  Running npsim on:"
    echo "    {input_file}"
    echo "  Resulting files:"
    echo "    {output_file}.*"

    mkdir -p $(dirname {output_file})
    cd $(dirname {output_file})/..

    if [ -f "/opt/detector/epic-main/bin/thisepic.sh" ]; then
        source /opt/detector/epic-main/bin/thisepic.sh
    fi
    /usr/bin/time -v npsim --part.userParticleHandler=Geant4TVEicParticleHandler --compactFile=$DETECTOR_PATH/epic_craterlake_{beam_config}.xml --runType run --inputFiles {input_file} --outputFile {output_file} --numberOfEvents {events} 2>&1

    echo ""
    echo "=========================================================================="
    echo "Job completed!"
    echo "Output: {output_file}"
    echo "=========================================================================="
    """)



def process_energy(config, energy, config_path=None):
    """Build a JobCreator for one beam energy."""
    input_files = find_inputs_or_skip(
        config.dd4hep_stv_input, '*.hepmc', energy, config.dd4hep_stv_output
    )
    if input_files is None:
        return None

    runner = JobCreator(
        input_files=input_files,
        output_file_name_func=exension_replacer('.afterburner.hepmc', '.edm4hep.root'),
        output_dir=config.dd4hep_stv_output,
        bind_dirs=config.bind_dirs,
        events=config.event_count,
        container=config['container'],
        beam_config=energy,
    )
    runner.container_script_template = create_container_script_template()
    runner.run()
    return runner


if __name__ == "__main__":
    run_pipeline(process_energy, description="Generate npsim (smart tracking volume) jobs.")
