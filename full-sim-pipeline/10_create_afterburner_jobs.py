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
    echo "=ABCONV===================================================================="
    echo "==========================================================================="
    echo "  Running afterburner on:"
    echo "    {input_file}"
    echo "  Resulting files:"
    echo "    {output_file}.*"
    /usr/bin/time -v abconv {afterburn_preset_flag} {input_file} --output {output_file} 2>&1
    
    echo ""
    echo "=========================================================================="
    echo "Job completed!"
    echo "Output: {output_file}"
    echo "=========================================================================="
    """)



def process_energy(config, energy, config_path=None):
    """Build a JobCreator for one beam energy."""
    input_files = find_inputs_or_skip(
        config.afterburner_input, '*.hepmc', energy, config.afterburner_output
    )
    if input_files is None:
        return None

    runner = JobCreator(
        input_files=input_files,
        output_file_name_func=exension_replacer('.hepmc', ''),  # afterburner adds extension itself
        output_dir=config.afterburner_output,
        bind_dirs=config.bind_dirs,
        events=config.event_count,
        container=config['container'],
    )
    

    def update_params(params):
        """Update the parameters for the container script."""
        flag = ""
        if "10x130" in params['input_file']:
            flag = "--preset=ip6_ep_130x10"
        if "5x41" in params['input_file']:
            flag = "--preset=ip6_hidiv_41x5" 
        if "9x100" in params['input_file']:
            flag = "--preset=ip6_hidiv_100x10" 
        if "9x130" in params['input_file']:
            flag = "--preset=ip6_ep_130x10" 
        if "9x275" in params['input_file']:
            flag = "--preset=ip6_hidiv_275x9"  
        
        return {**params, 'afterburn_preset_flag': flag}
    
    runner.container_script_params_updater = update_params
    runner.container_script_template = create_container_script_template()
    runner.run()
    return runner


if __name__ == "__main__":
    run_pipeline(process_energy, description="Generate afterburner jobs.")