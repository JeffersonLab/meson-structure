#!/usr/bin/env python3
"""
Count Lambdas based on detection of proton and pion in trackers and calorimeters.
"""

import argparse
import sys
import pandas as pd

# Detector collections (must match those in csv_edm4hep_acceptance_ppim.cxx)
TRACKER_COLLECTIONS = [
    "B0TrackerHits",
    "BackwardMPGDEndcapHits",
    "DIRCBarHits",
    "DRICHHits",
    "ForwardMPGDEndcapHits",
    "ForwardOffMTrackerHits",
    "ForwardRomanPotHits",
    "LumiSpecTrackerHits",
    "MPGDBarrelHits",
    "OuterMPGDBarrelHits",
    "RICHEndcapNHits",
    "SiBarrelHits",
    "TOFBarrelHits",
    "TOFEndcapHits",
    "TaggerTrackerHits",
    "TrackerEndcapHits",
    "VertexBarrelHits"
]

CALORIMETER_COLLECTIONS = [
    "EcalFarForwardZDCHits",
    "B0ECalHits",
    "EcalEndcapPHits",
    "EcalEndcapPInsertHits",
    "HcalFarForwardZDCHits",
    "HcalEndcapPInsertHits",
    "LFHCALHits"
]

def main():
    parser = argparse.ArgumentParser(description="Count detected Lambdas")
    parser.add_argument("input_file", help="Path to the acceptance CSV file")
    args = parser.parse_args()

    print(f"Reading {args.input_file}...")
    try:
        df = pd.read_csv(args.input_file)
    except Exception as e:
        print(f"Error reading CSV: {e}", file=sys.stderr)
        sys.exit(1)

    total_events = len(df)
    print(f"Total events: {total_events}")

    # Helper to check if particle is detected in any of the given detectors
    def is_detected(row, prefix, detectors):
        for det in detectors:
            col = f"{prefix}_{det}"
            if col in row and row[col] == 1:
                return True
        return False

    # Vectorized check for performance
    # Check proton in trackers
    prot_tracker_cols = [f"prot_{d}" for d in TRACKER_COLLECTIONS if f"prot_{d}" in df.columns]
    df['prot_in_tracker'] = df[prot_tracker_cols].sum(axis=1) > 0

    # Check pion in trackers
    pimin_tracker_cols = [f"pimin_{d}" for d in TRACKER_COLLECTIONS if f"pimin_{d}" in df.columns]
    df['pimin_in_tracker'] = df[pimin_tracker_cols].sum(axis=1) > 0

    # Check proton in calorimeters
    prot_calo_cols = [f"prot_{d}" for d in CALORIMETER_COLLECTIONS if f"prot_{d}" in df.columns]
    df['prot_in_calo'] = df[prot_calo_cols].sum(axis=1) > 0

    # Check pion in calorimeters
    pimin_calo_cols = [f"pimin_{d}" for d in CALORIMETER_COLLECTIONS if f"pimin_{d}" in df.columns]
    df['pimin_in_calo'] = df[pimin_calo_cols].sum(axis=1) > 0

    # 1. Both proton and pion detected in at least one tracker
    both_in_tracker = df[(df['prot_in_tracker']) & (df['pimin_in_tracker'])]
    count_both_tracker = len(both_in_tracker)

    # 2. Both proton and pion detected in at least one calorimeter
    both_in_calo = df[(df['prot_in_calo']) & (df['pimin_in_calo'])]
    count_both_calo = len(both_in_calo)

    # 3. Both (detected in tracker AND detected in calorimeter)
    both_in_both = df[
        (df['prot_in_tracker']) & (df['pimin_in_tracker']) &
        (df['prot_in_calo']) & (df['pimin_in_calo'])
    ]
    count_both_in_both = len(both_in_both)

    # 4. Union: Both in Tracker OR Both in Calorimeter
    # This answers "at least one tracker or calorimeter" if interpreted as the union of the two main categories
    union_tracker_calo = df[
        ((df['prot_in_tracker']) & (df['pimin_in_tracker'])) |
        ((df['prot_in_calo']) & (df['pimin_in_calo']))
    ]
    count_union = len(union_tracker_calo)

    # 5. Any: (Proton in Tracker OR Calo) AND (Pion in Tracker OR Calo)
    # This is the most general "detected anywhere" condition
    any_detection = df[
        ((df['prot_in_tracker']) | (df['prot_in_calo'])) &
        ((df['pimin_in_tracker']) | (df['pimin_in_calo']))
    ]
    count_any = len(any_detection)

    print("-" * 40)
    print(f"Total events: {total_events}")
    print(f"1. Both p and pi- in at least one tracker: {count_both_tracker} ({count_both_tracker/total_events*100:.1f}%)")
    print(f"2. Both p and pi- in at least one calorimeter: {count_both_calo} ({count_both_calo/total_events*100:.1f}%)")
    print(f"3. Both p and pi- in both tracker and calorimeter: {count_both_in_both} ({count_both_in_both/total_events*100:.1f}%)")
    print(f"4. Union (1 OR 2): Both in Tracker OR Both in Calo: {count_union} ({count_union/total_events*100:.1f}%)")
    print(f"5. Any: (p in T or C) AND (pi in T or C): {count_any} ({count_any/total_events*100:.1f}%)")
    print("-" * 40)

if __name__ == "__main__":
    main()
