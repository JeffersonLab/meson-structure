#!/usr/bin/env python3
import argparse
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys
from aa_helpers import create_plot_with_background

def main():
    parser = argparse.ArgumentParser(description="Plot pion hits 2D histogram over detector geometry")
    parser.add_argument("input_file", help="Path to the pion hits CSV file")
    parser.add_argument("-o", "--output", required=True, help="Output directory for the plot")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    print(f"Reading {args.input_file}...")
    try:
        df = pd.read_csv(args.input_file)
    except Exception as e:
        print(f"Error reading CSV: {e}", file=sys.stderr)
        sys.exit(1)

    if 'z' not in df.columns or 'x' not in df.columns:
        print("Error: CSV must contain 'z' and 'x' columns.", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(df)} hits.")

    try:
        fig, ax = create_plot_with_background()
    except FileNotFoundError:
        print("Warning: Background image not found. Creating standard plot.")
        fig, ax = plt.subplots(figsize=(20, 10))

    # Plot Z vs X
    h = ax.hist2d(df.z, df.x, bins=500, cmap="viridis", norm="log", alpha=0.8)
    
    ax.set_xlabel("Z (mm)")
    ax.set_ylabel("X (mm)")
    ax.set_title("Pion Hits Distribution (Z vs X)")

    output_path = os.path.join(args.output, "pion_hits_2d.png")
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")

if __name__ == "__main__":
    main()
