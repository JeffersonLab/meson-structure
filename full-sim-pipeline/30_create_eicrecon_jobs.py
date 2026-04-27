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
    
    mkdir -p $(dirname {output_file})
    
    echo ">"
    echo "= EICRECON ==================================================================="
    echo "==========================================================================="
    echo "  Running eicrecon on:"
    echo "    {input_file}"
    echo "  Resulting files:"
    echo "    {output_file}.*"

    if [ -f "/opt/detector/epic-main/bin/thisepic.sh" ]; then
        source /opt/detector/epic-main/bin/thisepic.sh
    fi
    cd $(dirname {output_file})
    /usr/bin/time -v /usr/bin/time -v eicrecon -Pdd4hep:xml_files=$DETECTOR_PATH/epic_craterlake_{beam_config}.xml  -Ppodio:output_file={output_file}  {input_file} 2>&1
    
    echo ""
    echo "=========================================================================="
    echo "Job completed!"
    echo "Output: {output_file}"
    echo "=========================================================================="
    """)



def process_energy(config, energy, config_path=None):
    """Build a JobCreator for one beam energy."""
    input_files = find_inputs_or_skip(
        config.dd4hep_output, '*.edm4hep.root', energy, config.eicrecon_output
    )
    if input_files is None:
        return None

    runner = JobCreator(
        input_files=input_files,
        output_file_name_func=exension_replacer('.edm4hep.root', '.edm4eic.root'),
        output_dir=config.eicrecon_output,
        bind_dirs=config.bind_dirs,
        events=config.event_count,
        container=config.container,
        beam_config=energy,
    )
    runner.container_script_template = create_container_script_template()
    runner.run()
    return runner


if __name__ == "__main__":
    run_pipeline(process_energy, description="Generate eicrecon jobs.")