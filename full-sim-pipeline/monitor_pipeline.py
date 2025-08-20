#!/usr/bin/env python3
"""
Monitor script for Meson Structure Analysis Pipeline
Provides real-time monitoring and statistics for the processing pipeline
"""

import os
import sys
import glob
import time
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Energy configurations
ENERGIES = ["5x41", "10x100", "10x130", "18x275"]

class PipelineMonitor:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.hepmc_dir = self.base_dir / "eg-hepmc"
        self.reco_dir = self.base_dir / "reco"
        self.analysis_dir = self.base_dir / "analysis"
        
    def count_files(self, pattern):
        """Count files matching a pattern"""
        files = glob.glob(str(pattern))
        return len(files)
    
    def get_slurm_jobs(self, user=None):
        """Get current SLURM job information"""
        if user is None:
            user = os.environ.get('USER')
        
        try:
            cmd = f"squeue -u {user} -o '%j %T %M' --noheader"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            jobs = defaultdict(lambda: {'running': 0, 'pending': 0})
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split()
                    if len(parts) >= 2:
                        job_name = parts[0]
                        state = parts[1]
                        
                        # Extract energy from job name
                        for energy in ENERGIES:
                            if energy in job_name:
                                if state == 'RUNNING':
                                    jobs[energy]['running'] += 1
                                elif state == 'PENDING':
                                    jobs[energy]['pending'] += 1
                                break
            
            return dict(jobs)
        except:
            return {}
    
    def check_stage_status(self, energy):
        """Check status of all stages for a given energy"""
        status = {}
        
        # 1. Split status
        split_flag = self.hepmc_dir / f"{energy}-all" / ".split_complete"
        if split_flag.exists():
            hepmc_count = self.count_files(self.hepmc_dir / f"{energy}-all" / "*.hepmc")
            status['split'] = f"Complete ({hepmc_count} files)"
        else:
            status['split'] = "Not started"
        
        # 2. Organization status
        priority_flag = self.hepmc_dir / f"{energy}-priority" / ".organized"
        full_flag = self.hepmc_dir / f"{energy}-full" / ".organized"
        
        if priority_flag.exists():
            priority_count = self.count_files(self.hepmc_dir / f"{energy}-priority" / "*.hepmc")
            status['priority_org'] = f"Complete ({priority_count} files)"
        else:
            status['priority_org'] = "Not organized"
        
        if full_flag.exists():
            full_count = self.count_files(self.hepmc_dir / f"{energy}-full" / "*.hepmc")
            status['full_org'] = f"Complete ({full_count} files)"
        else:
            status['full_org'] = "Not organized"
        
        # 3. EG Analysis
        eg_flag = self.analysis_dir / "eg-kinematics" / energy / "analysis_complete.flag"
        status['eg_analysis'] = "Complete" if eg_flag.exists() else "Not started"
        
        # 4. Priority reconstruction
        priority_reco_dir = self.reco_dir / f"{energy}-priority"
        if priority_reco_dir.exists():
            edm4eic_count = self.count_files(priority_reco_dir / "*.edm4eic.root")
            edm4hep_count = self.count_files(priority_reco_dir / "*.edm4hep.root")
            afterburn_count = self.count_files(priority_reco_dir / "*.afterburner.hepmc")
            
            complete_flag = priority_reco_dir / ".reconstruction_complete"
            if complete_flag.exists():
                status['priority_reco'] = f"Complete (edm4eic: {edm4eic_count}, edm4hep: {edm4hep_count})"
            elif edm4eic_count > 0:
                status['priority_reco'] = f"Running (edm4eic: {edm4eic_count}/500)"
            else:
                status['priority_reco'] = "Not started"
        else:
            status['priority_reco'] = "Not started"
        
        # 5. Full reconstruction
        full_reco_dir = self.reco_dir / f"{energy}-full"
        if full_reco_dir.exists():
            edm4eic_count = self.count_files(full_reco_dir / "*.edm4eic.root")
            if edm4eic_count > 0:
                status['full_reco'] = f"Running (edm4eic: {edm4eic_count}/1500)"
            else:
                started_flag = full_reco_dir / ".reconstruction_started"
                status['full_reco'] = "Started" if started_flag.exists() else "Not started"
        else:
            status['full_reco'] = "Not started"
        
        return status
    
    def print_summary(self, watch=False):
        """Print comprehensive status summary"""
        while True:
            # Clear screen if watching
            if watch:
                os.system('clear' if os.name == 'posix' else 'cls')
            
            print("\n" + "="*80)
            print(f"MESON STRUCTURE PIPELINE STATUS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*80)
            
            # Get SLURM jobs
            slurm_jobs = self.get_slurm_jobs()
            
            for energy in ENERGIES:
                print(f"\n{energy} Configuration:")
                print("-"*60)
                
                status = self.check_stage_status(energy)
                
                # Print status with formatting
                print(f"  1. MC Split:        {status['split']}")
                print(f"  2. Priority Files:  {status['priority_org']}")
                print(f"  3. Full Files:      {status['full_org']}")
                print(f"  4. EG Analysis:     {status['eg_analysis']}")
                print(f"  5. Priority Reco:   {status['priority_reco']}")
                print(f"  6. Full Reco:       {status['full_reco']}")
                
                # Show SLURM jobs if any
                if energy in slurm_jobs:
                    jobs = slurm_jobs[energy]
                    print(f"\n  SLURM Jobs: {jobs['running']} running, {jobs['pending']} pending")
            
            # Overall statistics
            print("\n" + "="*80)
            print("OVERALL STATISTICS:")
            print("-"*60)
            
            total_hepmc = 0
            total_priority_reco = 0
            total_full_reco = 0
            
            for energy in ENERGIES:
                # Count files for each type
                hepmc_pattern = self.hepmc_dir / f"{energy}-*" / "*.hepmc"
                priority_pattern = self.reco_dir / f"{energy}-priority" / "*.edm4eic.root"
                full_pattern = self.reco_dir / f"{energy}-full" / "*.edm4eic.root"
                
                total_hepmc += self.count_files(hepmc_pattern)
                total_priority_reco += self.count_files(priority_pattern)
                total_full_reco += self.count_files(full_pattern)
            
            print(f"  Total HEPMC files:        {total_hepmc}/8000 expected")
            print(f"  Priority reconstructed:   {total_priority_reco}/2000 expected")
            print(f"  Full reconstructed:       {total_full_reco}/6000 expected")
            
            # Calculate percentage complete
            total_expected = 8000
            total_complete = total_priority_reco + total_full_reco
            percentage = (total_complete / total_expected) * 100 if total_expected > 0 else 0
            
            print(f"\n  Overall Progress: {percentage:.1f}% complete")
            
            # Progress bar
            bar_length = 50
            filled = int(bar_length * percentage / 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f"  [{bar}] {total_complete}/{total_expected}")
            
            print("\n" + "="*80)
            
            if not watch:
                break
            
            # Wait before refresh
            time.sleep(30)
    
    def check_errors(self):
        """Check for errors in log files"""
        print("\n" + "="*60)
        print("ERROR CHECK")
        print("="*60)
        
        log_patterns = [
            (self.base_dir / "logs" / "*.log", "Pipeline logs"),
            (self.reco_dir / "*" / "*.slurm.err", "SLURM errors")
        ]
        
        for pattern, description in log_patterns:
            print(f"\n{description}:")
            print("-"*40)
            
            error_files = []
            for log_file in glob.glob(str(pattern)):
                if Path(log_file).stat().st_size > 0:
                    with open(log_file, 'r') as f:
                        content = f.read()
                        if 'error' in content.lower() or 'fail' in content.lower():
                            error_files.append(log_file)
            
            if error_files:
                print(f"  Found {len(error_files)} files with errors:")
                for ef in error_files[:10]:  # Show first 10
                    print(f"    - {ef}")
                if len(error_files) > 10:
                    print(f"    ... and {len(error_files) - 10} more")
            else:
                print("  No errors found")
    
    def estimate_completion_time(self):
        """Estimate completion time based on current progress"""
        print("\n" + "="*60)
        print("COMPLETION TIME ESTIMATE")
        print("="*60)
        
        # This is a simple estimate - could be made more sophisticated
        for energy in ENERGIES:
            print(f"\n{energy}:")
            
            priority_dir = self.reco_dir / f"{energy}-priority"
            if priority_dir.exists():
                # Find oldest and newest edm4eic files
                files = list(priority_dir.glob("*.edm4eic.root"))
                if len(files) > 1:
                    files_with_time = [(f, f.stat().st_mtime) for f in files]
                    files_with_time.sort(key=lambda x: x[1])
                    
                    oldest_time = files_with_time[0][1]
                    newest_time = files_with_time[-1][1]
                    elapsed = newest_time - oldest_time
                    
                    if elapsed > 0:
                        rate = len(files) / (elapsed / 3600)  # files per hour
                        remaining = 500 - len(files)
                        
                        if rate > 0:
                            hours_remaining = remaining / rate
                            completion_time = datetime.now() + timedelta(hours=hours_remaining)
                            
                            print(f"  Priority: {len(files)}/500 complete")
                            print(f"  Rate: {rate:.1f} files/hour")
                            print(f"  Est. completion: {completion_time.strftime('%Y-%m-%d %H:%M')}")
                        else:
                            print(f"  Priority: {len(files)}/500 complete")
                            print(f"  Rate: calculating...")
                else:
                    print(f"  Priority: Not enough data for estimate")

def main():
    parser = argparse.ArgumentParser(description="Monitor Meson Structure Pipeline")
    parser.add_argument("--base-dir", 
                       default="/volatile/eic/romanov/meson-structure-2025-08",
                       help="Base directory for the campaign")
    parser.add_argument("--watch", action="store_true",
                       help="Continuously monitor (refresh every 30s)")
    parser.add_argument("--errors", action="store_true",
                       help="Check for errors in log files")
    parser.add_argument("--estimate", action="store_true",
                       help="Estimate completion time")
    
    args = parser.parse_args()
    
    monitor = PipelineMonitor(args.base_dir)
    
    if args.errors:
        monitor.check_errors()
    elif args.estimate:
        monitor.estimate_completion_time()
    else:
        monitor.print_summary(watch=args.watch)

if __name__ == "__main__":
    main()
