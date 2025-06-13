#!/usr/bin/env python3
"""
Tutorial: Analyzing EICrecon Data with Uproot
----------------------------------------------------
This script demonstrates how to:
1. Read ROOT files containing particle physics data
2. Process data in manageable chunks
3. Create and fill histograms directly
4. Save analysis results as plots
"""

import argparse
import os
import uproot
import matplotlib.pyplot as plt
import hist
import awkward as ak

# PDG (Particle Data Group) codes for reference
PDG_LAMBDA = 3122
PDG_PROTON = 2212

# Global histograms
# Histogram for all particle momentum in z-direction
pz_hist = hist.Hist(hist.axis.Regular(100, -50, 50, name="momentum_z"))

# Histogram for Lambda decay position in z-direction
lambda_decay_z = hist.Hist(hist.axis.Regular(100, 0, 40000, name="lambda_decay_z"))

# Particle-specific momentum histograms
lambda_pz = hist.Hist(hist.axis.Regular(100, -50, 50, name="lambda_momentum_z"))
proton_pz = hist.Hist(hist.axis.Regular(100, -50, 50, name="proton_momentum_z"))


def parse_args():
    """Parse command line arguments for the tutorial script"""
    parser = argparse.ArgumentParser(description="Tutorial script for analyzing particle physics data with uproot.")
    parser.add_argument("input_files", nargs="+", help="List of ROOT files containing MCParticles.")
    parser.add_argument("-o", "--outdir", default="01_plots", help="Output directory for plots.")
    parser.add_argument("--step-size", default=1000, type=int, help="Number of events to read per chunk.")
    parser.add_argument("-n", "--nevents", default=1_000_000_000, type=int, help="Number of events to process")
    return parser.parse_args()


def process_chunk(chunk):
    """
    Process one chunk of data and fill histograms using whole arrays

    Args:
        chunk: Dict of awkward arrays for this chunk of events
    """
    # Extract relevant arrays from the chunk
    pdg = chunk["MCParticles.PDG"]
    pz = chunk["MCParticles.momentum.z"]
    decay_z = chunk["MCParticles.endpoint.z"]

    n_events = len(pdg)  # number of events in this chunk
    print(f"Processing chunk with {n_events} events")

    # Flatten arrays for all particles in all events
    flat_pdg = ak.flatten(pdg)
    flat_pz = ak.flatten(pz)
    flat_decay_z = ak.flatten(decay_z)

    # Fill histograms for all particles at once
    pz_hist.fill(flat_pz)

    # Create masks for specific particle types
    lambda_mask = (flat_pdg == PDG_LAMBDA)
    proton_mask = (flat_pdg == PDG_PROTON)

    # Fill particle-specific histograms
    if ak.sum(lambda_mask) > 0:
        lambda_pz.fill(flat_pz[lambda_mask])
        lambda_decay_z.fill(flat_decay_z[lambda_mask])

    if ak.sum(proton_mask) > 0:
        proton_pz.fill(flat_pz[proton_mask])


def analyze_files(file_list, tree_name, step_size, outdir, max_events=float('inf')):
    """
    Analyze ROOT files containing particle data

    Args:
        file_list: List of ROOT files to process
        tree_name: Name of the TTree to read
        step_size: Number of events to process per chunk
        outdir: Output directory for plots
        max_events: Maximum number of events to process
    """
    # Track how many events we've processed
    total_events = 0

    # Process all files chunk by chunk
    for filename in file_list:
        print(f"Processing file: {filename}")

        # Create file specification for uproot
        file_dict = {filename: tree_name}

        # Read and process file in chunks
        for chunk in uproot.iterate(
                file_dict,
                expressions=[
                    "MCParticles.PDG",
                    "MCParticles.momentum.z",
                    "MCParticles.endpoint.z",
                ],
                step_size=step_size,
                library="ak"):  # using awkward arrays

            # Process this chunk and update our histograms
            process_chunk(chunk)

            # Update events counter
            total_events += len(chunk["MCParticles.PDG"])

            # Check if we've processed enough events
            if total_events >= max_events:
                print(f"Reached maximum events limit ({max_events})")
                break

        # Check again after finishing a file
        if total_events >= max_events:
            break

    # After processing all chunks, create and save plots
    create_plots(outdir)


def create_plots(outdir):
    """
    Create and save plots from the filled histograms

    Args:
        outdir: Output directory for plots
    """
    # Create output directory if it doesn't exist
    os.makedirs(outdir, exist_ok=True)

    # Simplest way to plot
    # Plot Lambda decay position in z-direction
    fig, ax = plt.subplots(figsize=(10, 6))
    lambda_decay_z.plot(ax=ax)

    out_path = os.path.join(outdir, "lambda_pz.png")
    fig.savefig(out_path)
    print(f"Saved plot to: {out_path}")

    # more praramenters to stePlot momentum in z-direction
    fig, ax = plt.subplots(figsize=(10, 6))
    pz_hist.plot(ax=ax, color='blue', alpha=0.7)
    ax.set_xlabel("Momentum in z-direction [GeV/c]")
    ax.set_ylabel("Count")
    ax.set_title("Particle Momentum (pz)")
    ax.grid(True, alpha=0.3)

    out_path = os.path.join(outdir, "lambda_pz.png")
    plt.savefig(out_path)
    plt.close()
    print(f"Saved plot to: {out_path}")


    # 3. Plot PDG-specific momentum histograms
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Lambda plot
    lambda_pz.plot(ax=axs[0], color='green', alpha=0.7)
    axs[0].set_xlabel("Momentum in z-direction [GeV/c]")
    axs[0].set_ylabel("Count")
    axs[0].set_title("Lambda Momentum (pz)")
    axs[0].grid(True, alpha=0.3)

    # Proton plot
    proton_pz.plot(ax=axs[1], color='red', alpha=0.7)
    axs[1].set_xlabel("Momentum in z-direction [GeV/c]")
    axs[1].set_ylabel("Count")
    axs[1].set_title("Proton Momentum (pz)")
    axs[1].grid(True, alpha=0.3)

    plt.tight_layout()
    out_path = os.path.join(outdir, "pdg_momentum_z.png")
    plt.savefig(out_path)
    plt.close()
    print(f"Saved plot to: {out_path}")


def main():
    """Main function to run the tutorial analysis"""
    # Parse command-line arguments
    args = parse_args()

    print(f"Starting analysis of {len(args.input_files)} files")
    print(f"Using chunk size of {args.step_size} events")
    print(f"Will process up to {args.nevents} events")

    # Analyze the files and create plots
    analyze_files(args.input_files, "events", args.step_size, args.outdir, args.nevents)

    print("Analysis complete!")


if __name__ == "__main__":
    main()