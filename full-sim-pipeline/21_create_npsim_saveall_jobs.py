#!/usr/bin/env python3
"""
npsim_pipeline.py
Generate and submit afterburner jobs using JobCreator.
"""

import textwrap
from job_creator import JobCreator, exension_replacer, find_inputs_or_skip, run_pipeline


def create_container_script_template():
    """Create container job template for npsim."""
    return textwrap.dedent("""\
    #!/bin/bash
    set -e
    
    echo ">"
    echo "= NPSIM ==================================================================="
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
    /usr/bin/time -v npsim --part.userParticleHandler="" --compactFile=$DETECTOR_PATH/epic_craterlake_{beam_config}.xml --runType run --inputFiles {input_file} --outputFile {output_file} --numberOfEvents 1000 2>&1
    
    echo ""
    echo "=========================================================================="
    echo "Job completed!"
    echo "Output: {output_file}"
    echo "=========================================================================="
    """)



def process_energy(config, energy, config_path=None):
    """Build a JobCreator for one beam energy."""
    input_files = find_inputs_or_skip(
        config.dd4hep_saveall_input, '*.hepmc', energy, config.dd4hep_saveall_output
    )
    if input_files is None:
        return None

    runner = JobCreator(
        input_files=input_files,
        output_file_name_func=exension_replacer('.afterburner.hepmc', '.edm4hep.root'),
        output_dir=config.dd4hep_saveall_output,
        bind_dirs=config.bind_dirs,
        events=config.event_count,
        container=config['container'],
        beam_config=energy,
    )
    runner.container_script_template = create_container_script_template()
    runner.run()
    return runner


if __name__ == "__main__":
    run_pipeline(process_energy, description="Generate npsim (save-all) jobs.")