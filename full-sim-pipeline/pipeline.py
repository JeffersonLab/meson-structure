#!/usr/bin/env python3
"""
Simple pipeline script for meson structure priority reconstruction
No Snakemake, just straightforward Python!
"""

import os
import sys
import glob
import subprocess
import argparse
import time
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = "/volatile/eic/romanov/meson-structure-2025-08"
HEPMC_DIR = f"{BASE_DIR}/eg-hepmc"
RECO_DIR = f"{BASE_DIR}/reco"
CONTAINER = "/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:25.07-stable"
SCRIPTS_DIR = "/home/romanov/meson-structure-work/meson-structure/full-sim-pipeline"
CREATE_JOBS_SCRIPT = f"{SCRIPTS_DIR}/create_jobs.py"

ENERGIES = ["5x41", "10x100", "10x130", "18x275"]
EVENTS_PER_FILE = 5000

# Colors for output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def run_command(cmd, capture=False, verbose=True):
    """Run a shell command and optionally capture output"""
    if verbose:
        print(f"{BLUE}Running: {cmd}{RESET}")
    
    if capture:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr, result.returncode
    else:
        return subprocess.run(cmd, shell=True).returncode

def list_hepmc_files():
    """List all HEPMC files in priority directories"""
    print(f"\n{GREEN}=== HEPMC Files in Priority Directories ==={RESET}")
    
    total_files = 0
    for energy in ENERGIES:
        hepmc_pattern = f"{HEPMC_DIR}/{energy}-priority/*.hepmc"
        files = glob.glob(hepmc_pattern)
        total_files += len(files)
        
        print(f"\n{energy}-priority: {len(files)} files")
        if files and len(files) > 0:
            files.sort()
            print(f"  First: {os.path.basename(files[0])}")
            print(f"  Last:  {os.path.basename(files[-1])}")
    
    print(f"\n{GREEN}Total: {total_files} files{RESET}")
    return total_files

def create_jobs(energy, test_mode=False):
    """Create reconstruction jobs for a given energy"""
    input_dir = f"{HEPMC_DIR}/{energy}-priority"
    output_dir = f"{RECO_DIR}/{energy}-priority"
    flag_file = f"{output_dir}/.jobs_created"
    
    # Check if already created
    if os.path.exists(flag_file):
        print(f"{YELLOW}Jobs already created for {energy}-priority{RESET}")
        return True
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Get HEPMC files
    hepmc_files = glob.glob(f"{input_dir}/*.hepmc")
    if not hepmc_files:
        print(f"{RED}ERROR: No HEPMC files found in {input_dir}{RESET}")
        return False
    
    print(f"\n{BLUE}Creating jobs for {len(hepmc_files)} files in {energy}-priority...{RESET}")
    
    if test_mode:
        print(f"{YELLOW}TEST MODE: Would create jobs but skipping actual creation{RESET}")
        Path(flag_file).touch()
        return True
    
    # Run create_jobs.py
    cmd = f"python {CREATE_JOBS_SCRIPT} -b {BASE_DIR} -o {output_dir} --container {CONTAINER} -e {EVENTS_PER_FILE} {input_dir}/*.hepmc"
    
    log_file = f"logs/create_jobs_{energy}_priority.log"
    with open(log_file, 'w') as log:
        result = subprocess.run(cmd, shell=True, stdout=log, stderr=subprocess.STDOUT)
    
    if result.returncode != 0:
        print(f"{RED}ERROR: Failed to create jobs for {energy}. Check {log_file}{RESET}")
        return False
    
    # Verify submit script was created
    submit_script = f"{output_dir}/submit_all_slurm_jobs.sh"
    if not os.path.exists(submit_script):
        print(f"{RED}ERROR: Submit script not created for {energy}{RESET}")
        return False
    
    # Create flag file
    Path(flag_file).touch()
    print(f"{GREEN}✓ Jobs created for {energy}-priority{RESET}")
    return True

def submit_jobs(energy, test_mode=False):
    """Submit jobs for a given energy"""
    jobs_dir = f"{RECO_DIR}/{energy}-priority"
    flag_file = f"{jobs_dir}/.jobs_submitted"
    submit_script = f"{jobs_dir}/submit_all_slurm_jobs.sh"
    
    # Check if already submitted
    if os.path.exists(flag_file):
        print(f"{YELLOW}Jobs already submitted for {energy}-priority{RESET}")
        return True
    
    # Check if jobs were created
    if not os.path.exists(f"{jobs_dir}/.jobs_created"):
        print(f"{RED}ERROR: Jobs not created yet for {energy}-priority{RESET}")
        return False
    
    if test_mode:
        print(f"{YELLOW}TEST MODE: Would submit jobs for {energy}-priority{RESET}")
        slurm_files = glob.glob(f"{jobs_dir}/*.slurm.sh")[:3]
        for sf in slurm_files:
            print(f"  Would submit: {os.path.basename(sf)}")
        Path(flag_file).touch()
        return True
    
    print(f"\n{BLUE}Submitting jobs for {energy}-priority...{RESET}")
    
    log_file = f"logs/submit_jobs_{energy}_priority.log"
    with open(log_file, 'w') as log:
        result = subprocess.run(f"bash {submit_script}", shell=True, cwd=jobs_dir, 
                              stdout=log, stderr=subprocess.STDOUT)
    
    if result.returncode != 0:
        print(f"{RED}ERROR: Failed to submit jobs for {energy}. Check {log_file}{RESET}")
        return False
    
    # Create flag file
    Path(flag_file).touch()
    print(f"{GREEN}✓ Jobs submitted for {energy}-priority{RESET}")
    return True

def check_status():
    """Check status of all processing"""
    print(f"\n{GREEN}=== Pipeline Status ==={RESET}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    for energy in ENERGIES:
        print(f"\n{energy}-priority:")
        
        # Check HEPMC files
        hepmc_count = len(glob.glob(f"{HEPMC_DIR}/{energy}-priority/*.hepmc"))
        print(f"  HEPMC files: {hepmc_count}")
        
        # Check job creation
        jobs_created = os.path.exists(f"{RECO_DIR}/{energy}-priority/.jobs_created")
        print(f"  Jobs created: {'✓' if jobs_created else '✗'}")
        
        # Check job submission  
        jobs_submitted = os.path.exists(f"{RECO_DIR}/{energy}-priority/.jobs_submitted")
        print(f"  Jobs submitted: {'✓' if jobs_submitted else '✗'}")
        
        # Count output files
        reco_dir = f"{RECO_DIR}/{energy}-priority"
        if os.path.exists(reco_dir):
            edm4eic = len(glob.glob(f"{reco_dir}/*.edm4eic.root"))
            edm4hep = len(glob.glob(f"{reco_dir}/*.edm4hep.root"))
            afterburn = len(glob.glob(f"{reco_dir}/*.afterburner.hepmc"))
            print(f"  Outputs: afterburn={afterburn}, edm4hep={edm4hep}, edm4eic={edm4eic}")
        
        # Check SLURM queue
        user = os.environ.get('USER', 'romanov')
        cmd = f"squeue -u {user} -n '*{energy}*' --noheader | wc -l"
        stdout, _, _ = run_command(cmd, capture=True, verbose=False)
        try:
            active_jobs = int(stdout.strip())
            if active_jobs > 0:
                print(f"  {YELLOW}Active SLURM jobs: {active_jobs}{RESET}")
        except:
            pass

def monitor_progress():
    """Monitor job progress in real-time"""
    print(f"{GREEN}=== Monitoring Progress (Ctrl+C to stop) ==={RESET}")
    
    user = os.environ.get('USER', 'romanov')
    
    try:
        while True:
            os.system('clear')
            print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*60)
            
            for energy in ENERGIES:
                reco_dir = f"{RECO_DIR}/{energy}-priority"
                
                # Count completed files
                edm4eic = len(glob.glob(f"{reco_dir}/*.edm4eic.root"))
                edm4hep = len(glob.glob(f"{reco_dir}/*.edm4hep.root"))
                afterburn = len(glob.glob(f"{reco_dir}/*.afterburner.hepmc"))
                
                # Count active jobs
                cmd = f"squeue -u {user} -n '*{energy}*' --noheader | wc -l"
                stdout, _, _ = run_command(cmd, capture=True, verbose=False)
                active_jobs = int(stdout.strip()) if stdout else 0
                
                print(f"\n{energy}-priority:")
                print(f"  Active jobs: {active_jobs}")
                print(f"  Completed: afterburn={afterburn}, edm4hep={edm4hep}, edm4eic={edm4eic}")
            
            print("\nRefreshing in 30 seconds...")
            time.sleep(30)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Monitoring stopped{RESET}")

def clean_flags():
    """Clean flag files to allow re-running"""
    print(f"{YELLOW}Cleaning flag files...{RESET}")
    for energy in ENERGIES:
        flags = [
            f"{RECO_DIR}/{energy}-priority/.jobs_created",
            f"{RECO_DIR}/{energy}-priority/.jobs_submitted"
        ]
        for flag in flags:
            if os.path.exists(flag):
                os.remove(flag)
                print(f"  Removed: {flag}")
    print(f"{GREEN}Flag files cleaned{RESET}")

def main():
    parser = argparse.ArgumentParser(description="Simple pipeline for meson structure priority processing")
    parser.add_argument('action', choices=['list', 'create', 'submit', 'run', 'status', 'monitor', 'clean'],
                       help='Action to perform')
    parser.add_argument('--energy', choices=ENERGIES, help='Process only specific energy')
    parser.add_argument('--test', action='store_true', help='Test mode - no actual job submission')
    
    args = parser.parse_args()
    
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    
    if args.action == 'list':
        list_hepmc_files()
    
    elif args.action == 'create':
        energies = [args.energy] if args.energy else ENERGIES
        for energy in energies:
            create_jobs(energy, test_mode=args.test)
    
    elif args.action == 'submit':
        energies = [args.energy] if args.energy else ENERGIES
        for energy in energies:
            submit_jobs(energy, test_mode=args.test)
    
    elif args.action == 'run':
        # Create and submit all
        energies = [args.energy] if args.energy else ENERGIES
        print(f"{GREEN}Creating and submitting jobs for all energies...{RESET}")
        for energy in energies:
            if create_jobs(energy, test_mode=args.test):
                submit_jobs(energy, test_mode=args.test)
    
    elif args.action == 'status':
        check_status()
    
    elif args.action == 'monitor':
        monitor_progress()
    
    elif args.action == 'clean':
        clean_flags()

if __name__ == "__main__":
    main()
