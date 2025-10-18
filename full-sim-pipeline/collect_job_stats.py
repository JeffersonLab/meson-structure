#!/usr/bin/env python3
"""
collect_job_stats.py

Collects statistics from *.slurm.log files in a given directory.

We look for two patterns:
  1) "Initializing event XXX. Within run:0 event XXX" (from DD4hep / NPSim)
  2) "Status: XXX events processed at" (from EICrecon)

For each log file, we store the last encountered event number for both patterns.
Then we create two histograms:
  - how far the simulation (DD4hep) got
  - how far the EICrecon got
"""

import argparse
import os
import re
import glob
import matplotlib.pyplot as plt

def parse_args():
    parser = argparse.ArgumentParser(description="Collect last processed event numbers from Slurm logs.")
    parser.add_argument("log_dir", help="Directory containing *.slurm.log files.")
    return parser.parse_args()

def main():
    args = parse_args()
    log_pattern = os.path.join(args.log_dir, "*.slurm.log")
    log_files = glob.glob(log_pattern)
    print(f"Found {len(log_files)} log files")

    # Regex for DD4hep lines, e.g.: "Initializing event 810. Within run:0 event 810"
    dd4hep_pattern = re.compile(r"Initializing event (\d+)\. Within run:0 event")
    # Regex for EICrecon lines, e.g.: "Status: 12345 events processed at"
    eicrecon_pattern = re.compile(r"Status:\s+(\d+)\s+events processed at")

    dd4hep_last_events = []
    eicrecon_last_events = []

    for lf in log_files:
        with open(lf, "r") as f:
            dd4hep_val = None
            eicrecon_val = None

            for line in f:
                dd_match = dd4hep_pattern.search(line)
                if dd_match:
                    dd4hep_val = int(dd_match.group(1))
                eic_match = eicrecon_pattern.search(line)
                if eic_match:
                    eicrecon_val = int(eic_match.group(1))

        # Store the last encountered values (if any)
        if dd4hep_val is not None:
            dd4hep_last_events.append(dd4hep_val)
        else:
            dd4hep_last_events.append(0)  # or skip if you want

        if eicrecon_val is not None:
            eicrecon_last_events.append(eicrecon_val)
        else:
            eicrecon_last_events.append(0)  # or skip if you want

    print(f"Found {len(log_files)} logs.")
    print("DD4hep last-event list (first 10):", dd4hep_last_events[:10])
    print("EICrecon last-event list (first 10):", eicrecon_last_events[:10])

    # Make histograms
    if len(dd4hep_last_events) > 0:
        plt.figure(figsize=(6,4))
        plt.hist(dd4hep_last_events, bins=20, color='steelblue', edgecolor='k')
        plt.title("DD4hep / NPSim - Last Event Processed")
        plt.xlabel("Event Number")
        plt.ylabel("Count of Logs")
        plt.tight_layout()
        plt.savefig("dd4hep_last_event_hist.png")
        plt.close()
        print("Saved dd4hep_last_event_hist.png")

    if len(eicrecon_last_events) > 0:
        plt.figure(figsize=(6,4))
        plt.hist(eicrecon_last_events, bins=20, color='orange', edgecolor='k')
        plt.title("EICrecon - Last Event Processed")
        plt.xlabel("Event Number")
        plt.ylabel("Count of Logs")
        plt.tight_layout()
        plt.savefig("eicrecon_last_event_hist.png")
        plt.close()
        print("Saved eicrecon_last_event_hist.png")

    print("Done!")

if __name__ == "__main__":
    main()
