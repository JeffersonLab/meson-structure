#!/usr/bin/env python3
"""
slurm_simrecon.py

Generates a set of Bash scripts for each provided HepMC file to run a typical EIC workflow:
  1) afterburner -> produces *.afterburner.hepmc
  2) npsim       -> produces *.edm4hep.root
  3) eicrecon    -> produces *.edm4eic.root

Additionally, creates a YAML file <basename>.info.yaml capturing metadata about each job.

Usage example (wildcard expansion):
    python slurm_simrecon.py -o /full/path/to/workflow_scripts --time 12:00:00 /work/romanov/*.hepmc
"""

import argparse
import os
import textwrap
import datetime
import yaml  # Requires PyYAML

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate container-run and Slurm job scripts for EIC workflow."
    )
    parser.add_argument("input_files", nargs="+", 
                        help="List of input HepMC files (e.g., 'file1.hepmc file2.hepmc'). You can use wildcard expansion like '/path/*.hepmc'.")
    parser.add_argument("-o", "--outdir", required=True, 
                        help="Full path to the directory where scripts will be generated. This directory must be mounted inside the container.")
    parser.add_argument("-b", "--binddir", required=True, 
                        help="Root directory to bind to container. Usually is needed to be a parent of where hepmc and outputs are")
    parser.add_argument("-e", "--events", required=True, 
                        help="Nubmer of events per file (actually per geant to process)")
    parser.add_argument("--time", default="24:00:00",
                        help="Slurm time limit for each job (default: 24:00:00).")
    parser.add_argument("--cpus-per-task", type=int, default=1,
                        help="Slurm --cpus-per-task (default: 1).")
    parser.add_argument("--mem-per-cpu", default="5G",
                        help="Slurm memory per CPU (default: 2G).")
    parser.add_argument("--account", default="eic",
                        help="Slurm account name (default: eic).")
    parser.add_argument("--container",
                        default="/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:nightly",
                        help="Singularity container image (default: eicweb/eic_xl:nightly).")
    return parser.parse_args()

def make_container_script(input_file, output_dir, event_count):
    """
    Generates the container-run script for one HepMC file.
    All paths are absolute.
    """
    basename = os.path.splitext(os.path.basename(input_file))[0]
    # Use full paths for input and outputs.
    infile_full = os.path.abspath(input_file)
    afterburn_file = os.path.join(output_dir, f"{basename}.afterburner")     # abconv doesn't need ending .hepmc
    edm4hep_file   = os.path.join(output_dir, f"{basename}.edm4hep.root")
    edm4eic_file   = os.path.join(output_dir, f"{basename}.edm4eic.root")
    afterburn_preset_flag = "--preset=ip6_ep_130x10" if "10x130" in basename else ""

    container_script = textwrap.dedent(f"""\
    #!/bin/bash
    set -e
    # This script is intended to run INSIDE the Singularity container.

    # Ensure we sit in some writable directory
    cd {output_dir}
    
    echo "Sourcing EIC environment..."
    # Adjust the path if needed:
    source /opt/detector/epic-main/bin/thisepic.sh

    echo ">"
    echo "=ABCONV===================================================================="
    echo "==========================================================================="
    echo "  Running afterburner on:"
    echo "    {infile_full}"
    echo "  Resulting files:"
    echo "    {afterburn_file}.*"
    /usr/bin/time -v abconv {afterburn_preset_flag} {infile_full} --output {afterburn_file} 2>&1

    echo ">"
    echo "=NPSIM====================================================================="
    echo "==========================================================================="
    echo "  Running npsim on:"
    echo "    {afterburn_file}.hepmc"
    echo "  Resulting file:"
    echo "    {edm4hep_file}"
    echo "  Events to process:"
    echo "    {event_count}"
    
    /usr/bin/time -v npsim --compactFile=$DETECTOR_PATH/epic.xml --runType run --inputFiles {afterburn_file}.hepmc --outputFile {edm4hep_file} --numberOfEvents {event_count} 2>&1

    echo ">"
    echo "=EICRECON=================================================================="
    echo "==========================================================================="
    echo "  Running eicrecon on:"
    echo "    {edm4hep_file}"
    echo "  Resulting files:"
    echo "    {edm4eic_file}"
    /usr/bin/time -v eicrecon -Ppodio:output_file={edm4eic_file} {edm4hep_file} 2>&1

    echo "All steps completed for {basename}!"
    """)
    return container_script

def make_slurm_script(infile, bind_dir, outdir, container_image, time_limit, cpus_per_task, mem_per_cpu, account):
    """
    Generates the Slurm job script for one HepMC file.
    Uses full paths to ensure the container can find the scripts.
    """
    basename = os.path.splitext(os.path.basename(infile))[0]
    container_script_full = os.path.join(outdir, f"{basename}.container.sh")

    slurm_script = textwrap.dedent(f"""\
    #!/bin/bash
    #SBATCH --account={account}
    #SBATCH --partition=production
    #SBATCH --job-name={basename}
    #SBATCH --time={time_limit}
    #SBATCH --cpus-per-task={cpus_per_task}
    #SBATCH --mem-per-cpu={mem_per_cpu}
    #SBATCH --output={os.path.join(outdir, f"{basename}.slurm.log")}
    #SBATCH --error={os.path.join(outdir, f"{basename}.slurm.err")}

    set -e

    # Ensure singularity is available
    if ! command -v singularity &> /dev/null; then
      echo "singularity not found. Please load the module or install singularity."
      exit 1
    fi

    echo "Running job {basename} on $(hostname)"
    echo "Using container image: {container_image}"
    echo "Executing container-run script: {container_script_full}"

    # Execute the container-run script inside the container.
    singularity exec -B {bind_dir}:{bind_dir} {container_image} {container_script_full}

    echo "Slurm job finished for {basename}!"
    """)
    return slurm_script

def create_info_yaml(infile, outdir, container_image):
    """
    Create a small YAML file with metadata about this job.
    """
    basename = os.path.splitext(os.path.basename(infile))[0]
    yaml_filename = os.path.join(outdir, f"{basename}.info.yaml")

    data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "input_file": os.path.abspath(infile),
        "container_image": container_image,
        "script_version": "1.1",  # update as needed
        "notes": "Metadata about this job run"
    }

    with open(yaml_filename, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)

def main():
    args = parse_args()
    # Ensure outdir is an absolute path.
    outdir = os.path.abspath(args.outdir)
    bind_dir = os.path.abspath(args.binddir)
    event_count = int(args.events)
    os.makedirs(outdir, exist_ok=True)

    slurm_scripts = []
    for infile in args.input_files:
        # 1. Create the container-run script
        container_text = make_container_script(
            input_file=infile,
            output_dir=outdir,
            event_count=event_count
        )
        basename = os.path.splitext(os.path.basename(infile))[0]
        container_filename = os.path.join(outdir, f"{basename}.container.sh")
        with open(container_filename, "w") as f:
            f.write(container_text)
        os.chmod(container_filename, 0o755)

        # 2. Create the Slurm job script
        slurm_text = make_slurm_script(
            infile=infile,
            bind_dir=bind_dir,
            outdir=outdir,
            container_image=args.container,
            time_limit=args.time,
            cpus_per_task=args.cpus_per_task,
            mem_per_cpu=args.mem_per_cpu,
            account=args.account
        )
        slurm_filename = os.path.join(outdir, f"{basename}.slurm.sh")
        with open(slurm_filename, "w") as f:
            f.write(slurm_text)
        os.chmod(slurm_filename, 0o755)
        slurm_scripts.append(os.path.basename(slurm_filename))

        # 3. Create a YAML metadata file for this input
        create_info_yaml(infile, outdir, args.container)

    # 4. Create a master submit script to submit all Slurm jobs.
    master_script = os.path.join(outdir, "submit_all_slurm_jobs.sh")
    with open(master_script, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("set -e\n\n")
        f.write("# This script submits all generated slurm jobs.\n\n")
        for s in slurm_scripts:
            f.write(f"sbatch {s}\n")
        f.write("\necho \"All slurm jobs submitted!\"\n")
    os.chmod(master_script, 0o755)

    print(f"Done! Created scripts in {outdir}:")
    print(f"  Container-run scripts: {', '.join([os.path.splitext(s)[0] + '.container.sh' for s in slurm_scripts])}")
    print(f"  Slurm scripts: {', '.join(slurm_scripts)}")
    print(f"  YAML info files: {', '.join([os.path.splitext(s)[0] + '.info.yaml' for s in slurm_scripts])}")
    print(f"  Master submit script: {master_script}")

if __name__ == "__main__":
    main()

