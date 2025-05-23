#!/usr/bin/env python3
"""
# Lambda Decay Visualizer

This script analyzes Lambda decay data from CSV files generated by the Lambda decay analyzer
and creates histograms showing the spatial distribution of decay products.

The script produces:
1. 1D histograms of the z-coordinate of endpoints for Lambda, proton, and π- particles
2. 2D histograms showing z vs y coordinates of endpoints for each particle type

Usage:
    python lambda_decay_visualizer.py -i INPUT_FILE.csv -o OUTPUT_FOLDER
"""

import argparse
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LogNorm


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Visualize Lambda decay data with histograms.")
    parser.add_argument("-i", "--input-file", required=True,
                        help="Path to CSV file with Lambda decay data.")
    parser.add_argument("-o", "--output-folder", default="lambda_plots",
                        help="Output folder for plots (default: 'lambda_plots').")
    return parser.parse_args()


def ensure_output_folder(folder):
    """Create output folder if it doesn't exist."""
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created output folder: {folder}")


def load_data(file_path):
    """Load Lambda decay data from CSV file."""
    print(f"Loading data from {file_path}")
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} Lambda decay events")
    return df


def create_1d_histograms(df, output_folder):
    """Create 1D histograms of endpoint z-coordinates."""
    print("Creating 1D histograms of endpoint z-coordinates...")

    # Set up the figure
    fig, axs = plt.subplots(3, 1, figsize=(10, 15), sharex=True)

    # Define z-range for all histograms (-5 to 40 meters as requested)
    z_bins = np.linspace(-5, 40, 100)

    # Lambda endpoint z
    axs[0].hist(df['lam_endpoint_z'] / 1000, bins=z_bins, alpha=0.7, color='blue')
    axs[0].set_title('Lambda Endpoint Z Distribution', fontsize=14)
    axs[0].set_ylabel('Count', fontsize=12)
    axs[0].grid(True, alpha=0.3)

    # Proton endpoint z
    axs[1].hist(df['prot_endpoint_z'] / 1000, bins=z_bins, alpha=0.7, color='green')
    axs[1].set_title('Proton Endpoint Z Distribution', fontsize=14)
    axs[1].set_ylabel('Count', fontsize=12)
    axs[1].grid(True, alpha=0.3)

    # Pion endpoint z
    axs[2].hist(df['piminus_endpoint_z'] / 1000, bins=z_bins, alpha=0.7, color='red')
    axs[2].set_title('π⁻ Endpoint Z Distribution', fontsize=14)
    axs[2].set_xlabel('Z-coordinate (meters)', fontsize=12)
    axs[2].set_ylabel('Count', fontsize=12)
    axs[2].grid(True, alpha=0.3)

    # Adjust layout and save
    plt.tight_layout()
    output_path = os.path.join(output_folder, "1d_endpoint_z_histograms.png")
    plt.savefig(output_path, dpi=300)
    print(f"Saved 1D histograms to {output_path}")
    plt.close()


def create_2d_histograms(df, output_folder):
    """Create 2D histograms of endpoint z vs y coordinates."""
    print("Creating 2D histograms of endpoint z vs y coordinates...")

    # Create subplots for each particle type
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))

    # Define coordinate ranges (convert to meters)
    z_range = [-5, 40]  # meters
    y_range = [-1, 1]  # meters

    # Lambda endpoint z vs y
    h1 = axs[0].hist2d(
        df['lam_endpoint_z'] / 1000,  # Convert to meters
        df['lam_endpoint_y'] / 1000,  # Convert to meters
        bins=[100, 100],
        range=[z_range, y_range],
        cmap='Blues',
        norm=LogNorm()
    )
    axs[0].set_title('Lambda Endpoint (Z vs Y)', fontsize=14)
    axs[0].set_xlabel('Z-coordinate (meters)', fontsize=12)
    axs[0].set_ylabel('Y-coordinate (meters)', fontsize=12)
    fig.colorbar(h1[3], ax=axs[0], label='Count')

    # Proton endpoint z vs y
    h2 = axs[1].hist2d(
        df['prot_endpoint_z'] / 1000,
        df['prot_endpoint_y'] / 1000,
        bins=[100, 100],
        range=[z_range, y_range],
        cmap='Greens',
        norm=LogNorm()
    )
    axs[1].set_title('Proton Endpoint (Z vs Y)', fontsize=14)
    axs[1].set_xlabel('Z-coordinate (meters)', fontsize=12)
    axs[1].set_ylabel('Y-coordinate (meters)', fontsize=12)
    fig.colorbar(h2[3], ax=axs[1], label='Count')

    # Pion endpoint z vs y
    h3 = axs[2].hist2d(
        df['piminus_endpoint_z'] / 1000,
        df['piminus_endpoint_y'] / 1000,
        bins=[100, 100],
        range=[z_range, y_range],
        cmap='Reds',
        norm=LogNorm()
    )
    axs[2].set_title('π⁻ Endpoint (Z vs Y)', fontsize=14)
    axs[2].set_xlabel('Z-coordinate (meters)', fontsize=12)
    axs[2].set_ylabel('Y-coordinate (meters)', fontsize=12)
    fig.colorbar(h3[3], ax=axs[2], label='Count')

    # Adjust layout and save
    plt.tight_layout()
    output_path = os.path.join(output_folder, "2d_endpoint_zy_histograms.png")
    plt.savefig(output_path, dpi=300)
    print(f"Saved 2D histograms to {output_path}")
    plt.close()

    # Create more detailed individual 2D plots
    create_individual_2d_plots(df, output_folder)


def create_individual_2d_plots(df, output_folder):
    """Create individual 2D plots with more detail for each particle."""
    particles = [
        ('lam', 'Lambda', 'Blues'),
        ('prot', 'Proton', 'Greens'),
        ('piminus', 'π⁻', 'Reds')
    ]

    z_range = [-5, 40]  # meters
    y_range = [-2, 2]  # meters

    for prefix, name, cmap in particles:
        plt.figure(figsize=(12, 10))

        # Create a 2D histogram with Seaborn for better visualization
        z_data = df[f'{prefix}_endpoint_z'] / 1000  # Convert to meters
        y_data = df[f'{prefix}_endpoint_y'] / 1000  # Convert to meters

        # Filter outliers
        mask = (z_data >= z_range[0]) & (z_data <= z_range[1]) & (y_data >= y_range[0]) & (y_data <= y_range[1])

        h = plt.hist2d(
            z_data[mask],
            y_data[mask],
            bins=[150, 150],
            range=[z_range, y_range],
            cmap=cmap,
            norm=LogNorm()
        )

        plt.title(f'{name} Endpoint (Z vs Y)', fontsize=16)
        plt.xlabel('Z-coordinate (meters)', fontsize=14)
        plt.ylabel('Y-coordinate (meters)', fontsize=14)
        plt.colorbar(label='Count')
        plt.grid(alpha=0.3)

        output_path = os.path.join(output_folder, f"2d_{prefix}_endpoint_zy.png")
        plt.savefig(output_path, dpi=300)
        print(f"Saved detailed 2D plot for {name} to {output_path}")
        plt.close()


def main():
    """Main function."""
    args = parse_args()

    # Ensure output folder exists
    ensure_output_folder(args.output_folder)

    # Load data
    df = load_data(args.input_file)

    # Create histograms
    create_1d_histograms(df, args.output_folder)
    create_2d_histograms(df, args.output_folder)

    print("Analysis complete!")


if __name__ == "__main__":
    main()