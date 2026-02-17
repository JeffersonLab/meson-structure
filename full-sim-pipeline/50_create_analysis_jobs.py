#!/usr/bin/env python3
"""
50_create_analysis_jobs.py
Generate analysis jobs that process all CSV files for a given energy at once.

Unlike steps 10-40 which create one job per input file, analysis jobs aggregate
all files from the previous step (CSV conversion) for a given energy and run
an analysis script on the full set.

Output structure:
    {analysis_output}/{analysis_name}/{energy}/   - analysis results
    {analysis_output}/{analysis_name}/jobs/        - generated scripts
    {analysis_output}/{analysis_name}/logs/        - SLURM logs
"""

import argparse
import os
import textwrap
import datetime
import yaml
from job_runner import load_config, load_config_for_energy, find_input_files

this_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(this_dir)

# ---------------------------------------------------------------------------
# Analysis definitions
# Each entry defines one analysis to run per energy:
#   name     - output subdirectory name under analysis_output
#   script   - path relative to project root
#   csv_glob - glob pattern to find input CSVs in csv_output
# ---------------------------------------------------------------------------
ANALYSES = [
    {
        'name': 'csv_mc_dis_analysis_plot_mc',
        'script': 'analysis/csv_mc_dis_analysis/plot_mc.py',
        'csv_glob': '*.mc_dis.csv',
    },
]


def generate_container_script(analysis_name, energy, script_path, output_dir, input_files):
    """Generate container script content for an analysis job."""
    files_block = ' \\\n    '.join(f'"{f}"' for f in input_files)

    return textwrap.dedent(f"""\
    #!/bin/bash
    set -euo pipefail

    echo "= ANALYSIS ================================================================="
    echo "  Analysis: {analysis_name}"
    echo "  Energy:   {energy}"
    echo "  Script:   {script_path}"
    echo "  Output:   {output_dir}"
    echo "  Files:    {len(input_files)}"
    echo "============================================================================"

    mkdir -p "{output_dir}"

    /usr/bin/time -v python3 "{script_path}" \\
        --outdir "{output_dir}" \\
        {files_block} 2>&1

    echo "============================================================================"
    echo "Analysis complete: {analysis_name} / {energy}"
    echo "============================================================================"
    """)


def generate_slurm_script(basename, container_script_path, logs_dir, container, bind_dirs):
    """Generate SLURM submission script content."""
    bindings = ' '.join(f'-B {d}:{d}' for d in bind_dirs)

    return textwrap.dedent(f"""\
    #!/bin/bash
    #SBATCH --account=eic
    #SBATCH --partition=production
    #SBATCH --job-name={basename}
    #SBATCH --time=04:00:00
    #SBATCH --cpus-per-task=1
    #SBATCH --mem-per-cpu=5G
    #SBATCH --output={os.path.join(logs_dir, basename + '.slurm.log')}
    #SBATCH --error={os.path.join(logs_dir, basename + '.slurm.err')}

    set -e

    echo "Starting analysis job for {basename} at $(date)"
    echo "Running on: $(hostname)"

    singularity exec {bindings} {container} {container_script_path}

    echo "Job finished at $(date)"
    """)


def write_script(path, content):
    """Write a script file and make it executable."""
    with open(path, 'w') as f:
        f.write(content)
    os.chmod(path, 0o755)


def write_submit_all(jobs_dir, slurm_scripts):
    """Write master SLURM submission script."""
    lines = ["#!/bin/bash", "set -e", "", "# Submit all analysis SLURM jobs", ""]
    for s in slurm_scripts:
        lines.append(f"sbatch {s}")
    lines.append("")
    lines.append(f'echo "Submitted {len(slurm_scripts)} analysis jobs!"')

    path = os.path.join(jobs_dir, 'submit_all_slurm_jobs.sh')
    write_script(path, '\n'.join(lines))
    return path


def write_run_all(jobs_dir, container_scripts, container, bind_dirs):
    """Write local sequential execution script."""
    bindings = ' '.join(f'-B {d}:{d}' for d in bind_dirs)

    lines = [
        "#!/bin/bash", "set -e", "",
        "# Run all analysis jobs locally in sequence", "",
        "START_TIME=$SECONDS", ""
    ]
    for i, cs in enumerate(container_scripts, 1):
        basename = os.path.basename(cs)
        total = len(container_scripts)
        lines.extend([
            f'echo "[{i}/{total}] Running {basename}..."',
            "JOB_START=$SECONDS",
            f"singularity exec {bindings} {container} {cs}",
            "JOB_TIME=$((SECONDS - JOB_START))",
            'echo "    Completed in $JOB_TIME seconds"',
            ""
        ])
    lines.extend([
        "TOTAL_TIME=$((SECONDS - START_TIME))",
        'echo "====================================="',
        f'echo "All {len(container_scripts)} analysis jobs completed!"',
        'echo "Total execution time: $TOTAL_TIME seconds"',
        'echo "====================================="'
    ])

    path = os.path.join(jobs_dir, 'run_all_local.sh')
    write_script(path, '\n'.join(lines))
    return path


def process_analysis(analysis, config_path, energies):
    """Generate jobs for one analysis across all energies."""

    analysis_name = analysis['name']
    script_path = os.path.join(project_root, analysis['script'])

    print(f"\n{'='*80}")
    print(f"ANALYSIS: {analysis_name}")
    print(f"  Script:   {script_path}")
    print(f"  CSV glob: {analysis['csv_glob']}")
    print(f"{'='*80}")

    if not os.path.isfile(script_path):
        print(f"  [ERROR] Script not found: {script_path}")
        return

    # Resolve analysis_output from base config (no energy interpolation needed)
    base_config = load_config(config_path)
    analysis_base = base_config.analysis_output

    jobs_dir = os.path.join(analysis_base, analysis_name, 'jobs')
    logs_dir = os.path.join(analysis_base, analysis_name, 'logs')
    os.makedirs(jobs_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)

    all_container = []
    all_slurm = []
    bind_dirs = None
    container = None

    for energy in energies:
        econfig = load_config_for_energy(config_path, energy)
        csv_dir = econfig.csv_output
        output_dir = os.path.join(analysis_base, analysis_name, energy)
        container = econfig.container

        # Build bind_dirs: config bind_dirs + project root for analysis scripts
        bind_dirs = list(econfig.bind_dirs)
        if project_root not in bind_dirs:
            bind_dirs.append(project_root)

        print(f"\n  Energy: {energy}")
        print(f"    CSV source: {csv_dir}")
        print(f"    Output:     {output_dir}")

        input_files = find_input_files(csv_dir, analysis['csv_glob'])
        if input_files is None:
            print(f"    Skipping {energy} - no input files")
            continue

        basename = f"{analysis_name}_{energy}"

        # Container script
        container_content = generate_container_script(
            analysis_name, energy, script_path, output_dir, input_files
        )
        container_path = os.path.join(jobs_dir, f"{basename}.container.sh")
        write_script(container_path, container_content)
        all_container.append(container_path)

        # SLURM script
        slurm_content = generate_slurm_script(
            basename, container_path, logs_dir, container, bind_dirs
        )
        slurm_path = os.path.join(jobs_dir, f"{basename}.slurm.sh")
        write_script(slurm_path, slurm_content)
        all_slurm.append(slurm_path)

        # Info YAML
        info = {
            'timestamp': datetime.datetime.now().isoformat(),
            'analysis': analysis_name,
            'energy': energy,
            'script': script_path,
            'csv_glob': analysis['csv_glob'],
            'input_file_count': len(input_files),
            'input_files': input_files,
            'output_dir': output_dir,
        }
        info_path = os.path.join(jobs_dir, f"{basename}.info.yaml")
        with open(info_path, 'w') as f:
            yaml.safe_dump(info, f, sort_keys=False)

        print(f"    Generated: {basename}.container.sh, {basename}.slurm.sh")

    if all_slurm and bind_dirs and container:
        submit_path = write_submit_all(jobs_dir, all_slurm)
        run_path = write_run_all(jobs_dir, all_container, container, bind_dirs)

        print(f"\n  Summary for {analysis_name}:")
        print(f"    Container scripts: {len(all_container)}")
        print(f"    SLURM scripts:     {len(all_slurm)}")
        print(f"    Submit all: {submit_path}")
        print(f"    Run local:  {run_path}")


def main():
    """Main entry point."""

    parser = argparse.ArgumentParser(description="Generate analysis jobs.")
    parser.add_argument('-c', '--config', required=True, help="Path to config YAML file")
    args = parser.parse_args()

    config = load_config(args.config)
    energies = list(config.get('energies', []))

    print(f"{'='*80}")
    print(f" ANALYSIS PIPELINE")
    print(f"{'='*80}")
    print(f"Energies: {energies}")
    print(f"Analyses: {len(ANALYSES)}")

    for analysis in ANALYSES:
        process_analysis(analysis, args.config, energies)

    print(f"\n{'='*80}")
    print("ALL ANALYSES PROCESSED SUCCESSFULLY")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
