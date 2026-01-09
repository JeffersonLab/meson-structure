#!/usr/bin/env python3
"""Plot detector acceptance analysis for proton and pion from Lambda decay.

This script processes the main CSV output from csv_edm4hep_acceptance_ppim.cxx
and creates various visualizations of detector hit distributions.
"""

import argparse
import os
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


# Detector collections from csv_edm4hep_acceptance_ppim.cxx
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


def shorten_detector_name(name):
    """Shorten detector names for better display in charts.
    
    Args:
        name: Full detector name
        
    Returns:
        Shortened detector name
    """
    # Remove common suffixes
    name = name.replace("Hits", "")
    # Add line breaks for long names
    if len(name) > 15:
        words = []
        current = ""
        for i, char in enumerate(name):
            if char.isupper() and i > 0:
                words.append(current)
                current = char
            else:
                current += char
        words.append(current)
        
        # Join with newlines for pie charts
        if len(words) > 2:
            mid = len(words) // 2
            return '\n'.join([''.join(words[:mid]), ''.join(words[mid:])])
    
    return name


def count_detector_hits(df, particle_prefix, detector_list):
    """Count total hits for each detector.
    
    Args:
        df: DataFrame with acceptance data
        particle_prefix: 'prot' or 'pimin'
        detector_list: List of detector names
        
    Returns:
        Dictionary with detector names and hit counts
    """
    counts = {}
    for detector in detector_list:
        col_name = f"{particle_prefix}_{detector}"
        if col_name in df.columns:
            counts[detector] = df[col_name].sum()
        else:
            print(f"Warning: Column {col_name} not found in CSV", file=sys.stderr)
            counts[detector] = 0
    
    return counts


def plot_pie_chart(counts, title, output_path, min_percentage=2.0):
    """Create a pie chart of detector hits.
    
    Args:
        counts: Dictionary of detector names and counts
        title: Plot title
        output_path: Path to save the plot
        min_percentage: Minimum percentage to show label (default 2%)
    """
    # Filter out detectors with zero hits
    filtered_counts = {k: v for k, v in counts.items() if v > 0}
    
    if not filtered_counts:
        print(f"No hits found for {title}")
        return
    
    # Sort by count for consistent colors
    sorted_items = sorted(filtered_counts.items(), key=lambda x: x[1], reverse=True)
    labels = [shorten_detector_name(item[0]) for item in sorted_items]
    sizes = [item[1] for item in sorted_items]
    
    # Calculate percentages
    total = sum(sizes)
    percentages = [100.0 * size / total for size in sizes]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create custom labels with percentages (only if above threshold)
    def make_autopct(values):
        def my_autopct(pct):
            return f'{pct:.1f}%' if pct >= min_percentage else ''
        return my_autopct
    
    # Plot pie chart
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=None,  # We'll use legend instead
        autopct=make_autopct(sizes),
        startangle=90,
        counterclock=False,
        textprops={'fontsize': 9}
    )
    
    # Create legend with detector names and counts
    legend_labels = [f"{labels[i]}: {sizes[i]} ({percentages[i]:.1f}%)" 
                     for i in range(len(labels))]
    ax.legend(wedges, legend_labels, 
              title="Detectors",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1),
              fontsize=9)
    
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Saved pie chart: {output_path}")


def plot_column_chart(counts, title, output_path, color='steelblue'):
    """Create a column chart of detector hits sorted by count.
    
    Args:
        counts: Dictionary of detector names and counts
        title: Plot title
        output_path: Path to save the plot
        color: Bar color
    """
    # Filter out detectors with zero hits
    filtered_counts = {k: v for k, v in counts.items() if v > 0}
    
    if not filtered_counts:
        print(f"No hits found for {title}")
        return
    
    # Sort by count (descending)
    sorted_items = sorted(filtered_counts.items(), key=lambda x: x[1], reverse=True)
    labels = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Create bars
    x_pos = np.arange(len(labels))
    bars = ax.bar(x_pos, values, color=color, alpha=0.8, edgecolor='black', linewidth=0.7)
    
    # Add value labels on top of bars
    for i, (bar, value) in enumerate(zip(bars, values)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(value)}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Customize axes
    ax.set_xlabel('Detector', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Hits', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Set y-axis to start at 0
    ax.set_ylim(bottom=0)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Saved column chart: {output_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Plot detector acceptance for proton and pion from Lambda decay"
    )
    parser.add_argument("input_file", help="Path to the main acceptance CSV file")
    parser.add_argument("-o", "--output", required=True, 
                       help="Output directory for plots")
    args = parser.parse_args()
    
    # Check input file
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    
    # Create output directory
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    # Load CSV
    print(f"Reading {args.input_file}...")
    try:
        df = pd.read_csv(args.input_file)
    except Exception as e:
        print(f"Error reading CSV: {e}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Loaded {len(df)} events")
    
    # Count hits for each detector
    print("\nCounting detector hits...")
    
    proton_calo_counts = count_detector_hits(df, "prot", CALORIMETER_COLLECTIONS)
    pion_calo_counts = count_detector_hits(df, "pimin", CALORIMETER_COLLECTIONS)
    proton_tracker_counts = count_detector_hits(df, "prot", TRACKER_COLLECTIONS)
    pion_tracker_counts = count_detector_hits(df, "pimin", TRACKER_COLLECTIONS)
    
    # Combine all calorimeter and tracker counts
    all_calo_counts = {}
    all_tracker_counts = {}
    
    for detector in CALORIMETER_COLLECTIONS:
        all_calo_counts[detector] = proton_calo_counts.get(detector, 0) + pion_calo_counts.get(detector, 0)
    
    for detector in TRACKER_COLLECTIONS:
        all_tracker_counts[detector] = proton_tracker_counts.get(detector, 0) + pion_tracker_counts.get(detector, 0)
    
    # Create plots
    print("\nGenerating plots...")
    
    # 1. Pie chart: Proton calorimeter hits
    plot_pie_chart(
        proton_calo_counts,
        "Proton Detection in Calorimeters",
        os.path.join(args.output, "proton_calorimeter_pie.png")
    )
    
    # 2. Pie chart: Pion calorimeter hits
    plot_pie_chart(
        pion_calo_counts,
        "Pion Detection in Calorimeters",
        os.path.join(args.output, "pion_calorimeter_pie.png")
    )
    
    # 3. Column plot: All calorimeter hits (sorted)
    plot_column_chart(
        all_calo_counts,
        "Total Calorimeter Hits (Proton + Pion)",
        os.path.join(args.output, "calorimeter_hits_column.png"),
        color='coral'
    )
    
    # 4. Column plot: All tracker hits (sorted)
    plot_column_chart(
        all_tracker_counts,
        "Total Tracker Hits (Proton + Pion)",
        os.path.join(args.output, "tracker_hits_column.png"),
        color='steelblue'
    )
    
    # 5. Pie chart: Tracker hits
    all_tracker_counts_combined = {k: v for k, v in all_tracker_counts.items()}
    plot_pie_chart(
        all_tracker_counts_combined,
        "Total Tracker Hits Distribution",
        os.path.join(args.output, "tracker_hits_pie.png")
    )
    
    print("\n✓ All plots generated successfully!")
    print(f"Output directory: {args.output}")


if __name__ == "__main__":
    main()
