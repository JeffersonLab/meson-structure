#!/usr/bin/env python3
"""
Tutorial: Analyzing Particle Physics Data with Uproot
----------------------------------------------------
This script demonstrates how to:
1. Read ROOT files containing particle physics data
2. Process data in manageable chunks
3. Create histograms directly during processing
4. Save analysis results as plots
"""

import argparse
import os
import uproot
import numpy as np
import matplotlib.pyplot as plt
import hist
import awkward as ak

# PDG (Particle Data Group) codes for reference
PDG_LAMBDA = 3122
PDG_PROTON = 2212
PDG_NEUTRON = 2112
PDG_PION_PLUS = 211
PDG_PION_MINUS = -211


def parse_args():
    """Parse command line arguments for the tutorial script"""
    parser = argparse.ArgumentParser(description="Tutorial script for analyzing particle physics data with uproot.")
    parser.add_argument("input_files", nargs="+", help="List of ROOT files containing MCParticles.")
    parser.add_argument("-o", "--outdir", default="01_plots", help="Output directory for plots.")
    parser.add_argument("--step-size", default=1000, type=int, help="Number of events to read per chunk.")
    parser.add_argument("-n", "--nevents", default=1_000_000_000, type=int, help="Number of events to process")
    return parser.parse_args()


def create_histograms():
    """Create histogram objects to be filled during processing"""
    histograms = {
        # Histogram for particle momentum in z-direction (pz)
        "pz": hist.Hist(hist.axis.Regular(100, -50, 50, name="momentum_z")),

        # Histogram for particle endpoint in z-direction
        "endpoint_z": hist.Hist(hist.axis.Regular(100, 0, 40000, name="endpoint_z")),

        # Simple histograms for Lambda and Proton pz
        "lambda_pz": hist.Hist(hist.axis.Regular(100, -50, 50, name="lambda_momentum_z")),
        "proton_pz": hist.Hist(hist.axis.Regular(100, -50, 50, name="proton_momentum_z"))
    }
    return histograms


def process_chunk(chunk, histograms):
    """
    Process one chunk of data and fill histograms using whole arrays

    Args:
        chunk: Dict of awkward arrays for this chunk of events
        histograms: Dictionary of histogram objects to fill
    """
    # Extract relevant arrays from the chunk
    pdg = chunk["MCParticles.PDG"]
    pz = chunk["MCParticles.momentum.z"]
    endpoint_z = chunk["MCParticles.endpoint.z"]

    n_events = len(pdg)  # number of events in this chunk
    print(f"Processing chunk with {n_events} events")

    # Flatten arrays for all particles in all events
    # This converts the jagged array to a flat array containing all particles
    flat_pdg = ak.flatten(pdg)
    flat_pz = ak.flatten(pz)
    flat_endpoint_z = ak.flatten(endpoint_z)

    # Fill histograms for all particles at once
    histograms["pz"].fill(flat_pz)
    histograms["endpoint_z"].fill(flat_endpoint_z)

    # Create masks for specific particle types
    lambda_mask = (flat_pdg == PDG_LAMBDA)
    proton_mask = (flat_pdg == PDG_PROTON)

    # Fill particle-specific histograms
    if ak.sum(lambda_mask) > 0:
        lambda_pz = flat_pz[lambda_mask]
        histograms["lambda_pz"].fill(lambda_pz)

    if ak.sum(proton_mask) > 0:
        proton_pz = flat_pz[proton_mask]
        histograms["proton_pz"].fill(proton_pz)


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
    # Create histograms that will be filled during processing
    histograms = create_histograms()

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
            process_chunk(chunk, histograms)

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
    create_plots(histograms, outdir)


def create_plots(histograms, outdir):
    """
    Create and save plots from the filled histograms

    Args:
        histograms: Dictionary of histogram objects
        outdir: Output directory for plots
    """
    # Create output directory if it doesn't exist
    os.makedirs(outdir, exist_ok=True)

    # 1. Plot momentum in z-direction
    plt.figure(figsize=(10, 6))
    hist_pz = histograms["pz"]
    edges = hist_pz.axes[0].edges
    centers = (edges[1:] + edges[:-1]) / 2
    values = hist_pz.values()

    plt.bar(centers, values, width=(edges[1]-edges[0]), alpha=0.7, color='blue')
    plt.xlabel("Momentum in z-direction [GeV/c]")
    plt.ylabel("Count")
    plt.title("Particle Momentum (pz)")
    plt.grid(True, alpha=0.3)

    out_path = os.path.join(outdir, "momentum_z.png")
    plt.savefig(out_path)
    plt.close()
    print(f"Saved plot to: {out_path}")

    # 2. Plot endpoint in z-direction
    plt.figure(figsize=(10, 6))
    hist_endpoint = histograms["endpoint_z"]
    edges = hist_endpoint.axes[0].edges
    centers = (edges[1:] + edges[:-1]) / 2
    # Convert mm to m for better readability
    centers_m = centers / 1000.0
    values = hist_endpoint.values()

    plt.bar(centers_m, values, width=(edges[1]-edges[0])/1000, alpha=0.7, color='green')
    plt.xlabel("Endpoint position in z-direction [m]")
    plt.ylabel("Count")
    plt.title("Particle Endpoint (z)")
    plt.grid(True, alpha=0.3)

    out_path = os.path.join(outdir, "endpoint_z.png")
    plt.savefig(out_path)
    plt.close()
    print(f"Saved plot to: {out_path}")

    # 3. Plot PDG-specific momentum histograms
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Lambda plot
    hist_lambda = histograms["lambda_pz"]
    edges = hist_lambda.axes[0].edges
    centers = (edges[1:] + edges[:-1]) / 2
    values = hist_lambda.values()

    axs[0].bar(centers, values, width=(edges[1]-edges[0]), alpha=0.7, color='green')
    axs[0].set_xlabel("Momentum in z-direction [GeV/c]")
    axs[0].set_ylabel("Count")
    axs[0].set_title("Lambda Momentum (pz)")
    axs[0].grid(True, alpha=0.3)

    # Proton plot
    hist_proton = histograms["proton_pz"]
    edges = hist_proton.axes[0].edges
    centers = (edges[1:] + edges[:-1]) / 2
    values = hist_proton.values()

    axs[1].bar(centers, values, width=(edges[1]-edges[0]), alpha=0.7, color='red')
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