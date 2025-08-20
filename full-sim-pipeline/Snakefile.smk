"""
Simplified Snakemake workflow for meson structure analysis
Campaign 2025-08 - Priority processing only

This simplified workflow handles:
1. Creating reconstruction jobs for priority files
2. Submitting jobs to SLURM
3. Monitoring completion

# Check what you have
snakemake -s Snakefile_simple.smk list_hepmc

# Test (dry run)
snakemake -s Snakefile_simple.smk -n

# Create jobs only
snakemake -s Snakefile_simple.smk create_only -j 4

# Create and submit
snakemake -s Snakefile_simple.smk -j 4

# Monitor
snakemake -s Snakefile_simple.smk monitor

# Check logs
tail -f logs/create_jobs_5x41_priority.log
"""

import os
import glob
import yaml
from pathlib import Path
from datetime import datetime

# ===== Configuration =====
configfile: "config_simple.yaml"

# Base directories
BASE_DIR = config.get("base_dir", "/volatile/eic/romanov/meson-structure-2025-08")
HEPMC_DIR = config.get("hepmc_dir", f"{BASE_DIR}/eg-hepmc")
RECO_DIR = config.get("reco_dir", f"{BASE_DIR}/reco")
CONTAINER = config.get("container", "/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:25.07-stable")

# Scripts
SCRIPTS_DIR = config.get("scripts_dir", "/home/romanov/meson-structure-work/meson-structure/full-sim-pipeline")
CREATE_JOBS = f"{SCRIPTS_DIR}/create_jobs.py"

# Energy configurations - matching your existing directory names
ENERGIES = ["5x41", "10x100", "10x130", "18x275"]

# Processing parameters
EVENTS_PER_FILE = 5000

# ===== Helper Functions =====

def count_reco_outputs(energy):
    """Count reconstruction output files"""
    reco_dir = f"{RECO_DIR}/{energy}-priority"
    if not os.path.exists(reco_dir):
        return 0, 0, 0
    
    edm4eic = len(glob.glob(f"{reco_dir}/*.edm4eic.root"))
    edm4hep = len(glob.glob(f"{reco_dir}/*.edm4hep.root"))
    afterburn = len(glob.glob(f"{reco_dir}/*.afterburner.hepmc"))
    
    return edm4eic, edm4hep, afterburn

# ===== Main Rule =====

rule all:
    """Main target - process priority files for all energies"""
    input:
        # Create and submit jobs for all priority energies
        expand(f"{RECO_DIR}/{{energy}}-priority/.jobs_submitted", energy=ENERGIES),
        # Status report
        f"{RECO_DIR}/.status_report.txt"

# ===== Create Jobs =====

rule create_priority_jobs:
    """Create reconstruction jobs for priority files"""
    output:
        flag = f"{RECO_DIR}/{{energy}}-priority/.jobs_created",
        submit_script = f"{RECO_DIR}/{{energy}}-priority/submit_all_slurm_jobs.sh"
    params:
        input_dir = f"{HEPMC_DIR}/{{energy}}-priority",
        output_dir = f"{RECO_DIR}/{{energy}}-priority"
    log:
        f"logs/create_jobs_{{energy}}_priority.log"
    shell:
        """
        mkdir -p {params.output_dir} logs
        
        # Check if jobs already created
        if [ -f "{output.flag}" ]; then
            echo "Jobs already created for {wildcards.energy}-priority" | tee {log}
            exit 0
        fi
        
        # Count HEPMC files
        HEPMC_COUNT=$(ls -1 {params.input_dir}/*.hepmc 2>/dev/null | wc -l)
        if [ "$HEPMC_COUNT" -eq 0 ]; then
            echo "ERROR: No HEPMC files found in {params.input_dir}" | tee {log}
            exit 1
        fi
        
        echo "Creating jobs for $HEPMC_COUNT files in {wildcards.energy}-priority" | tee {log}
        
        # Run create_jobs.py
        python {CREATE_JOBS} \
            -b {BASE_DIR} \
            -o {params.output_dir} \
            --container {CONTAINER} \
            -e {EVENTS_PER_FILE} \
            {params.input_dir}/*.hepmc \
            2>&1 | tee -a {log}
        
        # Check if submit script was created
        if [ ! -f "{output.submit_script}" ]; then
            echo "ERROR: Submit script not created" | tee -a {log}
            exit 1
        fi
        
        # Create flag file
        touch {output.flag}
        echo "✓ Jobs created for {wildcards.energy}-priority" | tee -a {log}
        """

# ===== Submit Jobs =====

rule submit_priority_jobs:
    """Submit priority reconstruction jobs to SLURM"""
    input:
        flag = f"{RECO_DIR}/{{energy}}-priority/.jobs_created",
        submit_script = f"{RECO_DIR}/{{energy}}-priority/submit_all_slurm_jobs.sh"
    output:
        flag = f"{RECO_DIR}/{{energy}}-priority/.jobs_submitted"
    params:
        jobs_dir = f"{RECO_DIR}/{{energy}}-priority"
    log:
        f"logs/submit_jobs_{{energy}}_priority.log"
    shell:
        """
        # Check if already submitted
        if [ -f "{output.flag}" ]; then
            echo "Jobs already submitted for {wildcards.energy}-priority" | tee {log}
            exit 0
        fi
        
        # Check if we're in test mode
        if [ "{config[test_mode]}" = "True" ]; then
            echo "TEST MODE: Would submit jobs for {wildcards.energy}-priority" | tee {log}
            echo "Would run: {input.submit_script}" | tee -a {log}
            ls -la {params.jobs_dir}/*.slurm.sh | head -5 | tee -a {log}
            touch {output.flag}
            exit 0
        fi
        
        # Actually submit jobs
        echo "Submitting jobs for {wildcards.energy}-priority..." | tee {log}
        
        cd {params.jobs_dir}
        bash {input.submit_script} 2>&1 | tee -a {log}
        
        if [ ${{PIPESTATUS[0]}} -ne 0 ]; then
            echo "ERROR: Job submission failed" | tee -a {log}
            exit 1
        fi
        
        # Create flag file
        touch {output.flag}
        echo "✓ Jobs submitted for {wildcards.energy}-priority" | tee -a {log}
        """

# ===== Status Monitoring =====

rule check_status:
    """Generate status report for all energies"""
    input:
        flags = expand(f"{RECO_DIR}/{{energy}}-priority/.jobs_submitted", energy=ENERGIES)
    output:
        report = f"{RECO_DIR}/.status_report.txt"
    run:
        import subprocess
        from datetime import datetime
        
        report_lines = []
        report_lines.append("="*70)
        report_lines.append(f"MESON STRUCTURE PIPELINE STATUS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("="*70)
        report_lines.append("")
        
        for energy in ENERGIES:
            report_lines.append(f"\n{energy}-priority:")
            report_lines.append("-"*50)
            
            # Check HEPMC files
            hepmc_count = len(glob.glob(f"{HEPMC_DIR}/{energy}-priority/*.hepmc"))
            report_lines.append(f"  HEPMC files: {hepmc_count}")
            
            # Check job creation
            jobs_created = os.path.exists(f"{RECO_DIR}/{energy}-priority/.jobs_created")
            report_lines.append(f"  Jobs created: {'✓' if jobs_created else '✗'}")
            
            # Check job submission
            jobs_submitted = os.path.exists(f"{RECO_DIR}/{energy}-priority/.jobs_submitted")
            report_lines.append(f"  Jobs submitted: {'✓' if jobs_submitted else '✗'}")
            
            # Count output files
            edm4eic, edm4hep, afterburn = count_reco_outputs(energy)
            report_lines.append(f"  Reconstruction outputs:")
            report_lines.append(f"    - Afterburner: {afterburn}")
            report_lines.append(f"    - EDM4HEP: {edm4hep}")
            report_lines.append(f"    - EDM4EIC: {edm4eic}")
            
            # Check SLURM queue (if not in test mode)
            if not config.get("test_mode", False):
                try:
                    user = os.environ.get('USER', 'romanov')
                    cmd = f"squeue -u {user} -n '*{energy}*' --noheader | wc -l"
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    active_jobs = int(result.stdout.strip())
                    report_lines.append(f"  Active SLURM jobs: {active_jobs}")
                except:
                    pass
        
        report_lines.append("\n" + "="*70)
        
        # Write report
        report_text = "\n".join(report_lines)
        with open(output.report, 'w') as f:
            f.write(report_text)
        
        # Also print to console
        print(report_text)

# ===== Utility Rules =====

rule clean_logs:
    """Clean log files"""
    shell:
        """
        rm -f logs/*.log
        echo "Logs cleaned"
        """

rule clean_flags:
    """Clean flag files (allows re-running)"""
    shell:
        """
        rm -f {RECO_DIR}/*-priority/.jobs_created
        rm -f {RECO_DIR}/*-priority/.jobs_submitted
        rm -f {RECO_DIR}/.status_report.txt
        echo "Flag files cleaned - ready to re-run"
        """

rule test_create:
    """Test job creation without submitting"""
    input:
        expand(f"{RECO_DIR}/{{energy}}-priority/.jobs_created", energy=ENERGIES)
    run:
        print("\n" + "="*60)
        print("TEST: Job creation complete")
        print("="*60)
        
        for energy in ENERGIES:
            jobs_dir = f"{RECO_DIR}/{energy}-priority"
            slurm_files = glob.glob(f"{jobs_dir}/*.slurm.sh")
            container_files = glob.glob(f"{jobs_dir}/*.container.sh")
            
            print(f"\n{energy}-priority:")
            print(f"  SLURM scripts: {len(slurm_files)}")
            print(f"  Container scripts: {len(container_files)}")
            
            if slurm_files:
                print(f"  Sample: {os.path.basename(slurm_files[0])}")

rule list_hepmc:
    """List HEPMC files in priority directories"""
    run:
        print("\n" + "="*60)
        print("HEPMC FILES IN PRIORITY DIRECTORIES")
        print("="*60)
        
        total_files = 0
        for energy in ENERGIES:
            hepmc_dir = f"{HEPMC_DIR}/{energy}-priority"
            files = glob.glob(f"{hepmc_dir}/*.hepmc")
            total_files += len(files)
            
            print(f"\n{energy}-priority: {len(files)} files")
            if files:
                # Show first and last file
                files.sort()
                print(f"  First: {os.path.basename(files[0])}")
                print(f"  Last:  {os.path.basename(files[-1])}")
        
        print(f"\nTotal HEPMC files: {total_files}")

rule monitor:
    """Monitor job progress"""
    run:
        import subprocess
        import time
        
        print("\n" + "="*60)
        print("MONITORING RECONSTRUCTION PROGRESS")
        print("="*60)
        
        user = os.environ.get('USER', 'romanov')
        
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            
            print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*60)
            
            for energy in ENERGIES:
                edm4eic, edm4hep, afterburn = count_reco_outputs(energy)
                
                # Get SLURM job count
                cmd = f"squeue -u {user} -n '*{energy}*' --noheader | wc -l"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                active_jobs = int(result.stdout.strip()) if result.returncode == 0 else 0
                
                print(f"\n{energy}-priority:")
                print(f"  Active jobs: {active_jobs}")
                print(f"  Completed: afterburn={afterburn}, edm4hep={edm4hep}, edm4eic={edm4eic}")
            
            print("\nPress Ctrl+C to stop monitoring")
            time.sleep(30)  # Refresh every 30 seconds

rule create_only:
    """Create jobs without submitting"""
    input:
        expand(f"{RECO_DIR}/{{energy}}-priority/.jobs_created", energy=ENERGIES)
    run:
        print("\n✓ Jobs created for all priority energies")
        print("\nTo submit jobs, run:")
        print("  snakemake -s Snakefile_simple.smk submit_only")

rule submit_only:
    """Submit already created jobs"""
    input:
        expand(f"{RECO_DIR}/{{energy}}-priority/.jobs_submitted", energy=ENERGIES)
    run:
        print("\n✓ Jobs submitted for all priority energies")
        print("\nTo monitor progress, run:")
        print("  snakemake -s Snakefile_simple.smk monitor")
