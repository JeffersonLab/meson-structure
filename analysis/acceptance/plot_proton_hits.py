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
    parser = argparse.ArgumentParser(description="Plot proton hits 2D histogram over detector geometry")
    parser.add_argument("input_file", help="Path to the proton hits CSV file")
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

    # Create plot with background
    # Assuming the background image is in the same directory or handled by aa_helpers defaults
    # We might need to ensure aa_helpers can find the image if run from elsewhere.
    # aa_helpers uses "eic_center_forward_bw.png" by default.
    
    try:
        fig, ax = create_plot_with_background()
    except FileNotFoundError:
        print("Warning: Background image not found. Creating standard plot.")
        fig, ax = plt.subplots(figsize=(20, 10))

    # Plot 2D histogram
    # Z is usually horizontal (beam axis), X is vertical/transverse in top-down or side view?
    # In the notebook example: hist2d(df.prot_epz, df.prot_epx) -> Z vs X
    # So we plot Z on X-axis and X on Y-axis?
    # create_plot_with_background sets X label to "X (mm)" and Y to "Y (mm)".
    # But the notebook plots Z vs X.
    # Let's check aa_helpers again.
    # It sets xlabel "X (mm)" and ylabel "Y (mm)".
    # The calibration points:
    # p0: mm(0,0) -> pix(371, 281)
    # p1: mm(4937, 2622) -> pix(739, 85)
    # This looks like Z (beam) is on X-axis (0 to 4937 mm) and X (transverse) is on Y-axis?
    # Or maybe it is X and Y?
    # 4937 mm is ~5 meters. That sounds like Z (length of detector).
    # 2622 mm is ~2.6 meters. That sounds like radius/transverse.
    # So likely the background image is Z vs X (or Z vs R).
    # So we should plot df.z as x-coordinate and df.x as y-coordinate on the plot?
    # Wait, the notebook says: `h = ax.hist2d(df.prot_epz, df.prot_epx, ...)`
    # `hist2d(x, y)` plots x on horizontal, y on vertical.
    # So it plots epz on horizontal (X-axis of plot) and epx on vertical (Y-axis of plot).
    # So we should use `ax.hist2d(df.z, df.x, ...)`
    
    h = ax.hist2d(df.z, df.x, bins=500, cmap="viridis", norm="log", alpha=0.8)
    
    ax.set_xlabel("Z (mm)") # Overwrite labels if needed, but aa_helpers sets "X (mm)"
    ax.set_ylabel("X (mm)") # aa_helpers sets "Y (mm)"
    # If the background is indeed Z-X, then aa_helpers labels might be generic.
    # I will update them to be specific.
    
    ax.set_title("Proton Hits Distribution (Z vs X)")

    output_path = os.path.join(args.output, "proton_hits_2d.png")
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")

if __name__ == "__main__":
    main()
