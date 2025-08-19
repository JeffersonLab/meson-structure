#!/usr/bin/env python3

"""
analyze_kinematics.py

Reads the 'Evnts' TTree from a large ROOT file for EIC analysis.
Analyzes incident and scattered particles with appropriate kinematics.

For incident particles (inc_p, inc_e):
  - pT, pz, p (total momentum)
  - Minimal angle with Z-axis in mrad

For scattered particles (scat_e, kaon, lambda):
  - pT, pz, p (total momentum)
  - theta, phi in radians
  - pseudorapidity (eta)

Usage example:
  python analyze_kinematics.py --input-file k_lambda_crossing_0_10.0on100.0.root --energy 10x100 --max-events 100000
"""

import argparse
import os
import json
import uproot
import awkward as ak
import numpy as np
import matplotlib.pyplot as plt
import hist
from hist import Hist
from hist.axis import Regular as RegAx

# Branch names in ROOT file
branches = ["P_Inc.", "e_Inc.", "e_Scat.", "k.", "lamb_scat."]

# Friendly particle names for everything else
particles = ["inc_p", "inc_e", "scat_e", "kaon", "lambda"]

# Map between branches and particle names
particle_to_branch = {particle: branch for particle, branch in zip(particles, branches)}
branch_to_particle = {branch: particle for particle, branch in zip(particles, branches)}

# Define particle categories
incident_particles = ["inc_p", "inc_e"]
scattered_particles = ["scat_e", "kaon", "lambda"]

# Full descriptive names for plots
particle_full_names = {
    "inc_p": "Incident Proton",
    "inc_e": "Incident Electron",
    "scat_e": "Scattered Electron",
    "kaon": "Scattered Kaon",
    "lambda": "Scattered Lambda"
}


def parse_energy(energy_str):
    """Parse energy string like '10x100' into (e_energy, p_energy)"""
    parts = energy_str.split('x')
    if len(parts) != 2:
        raise ValueError("Energy must be in format NxM (e.g., 10x100)")
    return float(parts[0]), float(parts[1])


def create_histograms(e_energy, p_energy):
    """
    Returns a dict of hist.Hist objects customized for each particle type.
    
    For incident particles:
      - pt, pz, p, angle_z_mrad
    
    For scattered particles:
      - pt, pz, p, theta_rad, phi_rad, eta
    """
    hists = {}
    
    # Incident proton histograms
    # Expected momentum ~ p_energy
    p_max = p_energy * 1.2
    hists[("inc_p", "pt")] = Hist(RegAx(100, 0, 2, name="pt", label="pT [GeV/c]"))
    hists[("inc_p", "px")] = Hist(RegAx(200, -p_energy*0.1, p_energy*0.1, name="px", label="px [GeV/c]"))
    hists[("inc_p", "py")] = Hist(RegAx(200, -p_energy*0.1, p_energy*0.1, name="py", label="py [GeV/c]"))
    hists[("inc_p", "pz")] = Hist(RegAx(200, p_energy-1, p_energy+1, name="pz", label="pz [GeV/c]"))
    hists[("inc_p", "p")] = Hist(RegAx(200, p_energy-1, p_energy+1, name="p", label="P [GeV/c]"))
    hists[("inc_p", "angle_z_mrad")] = Hist(RegAx(100, 0, 10, name="angle_z", label="Min. angle with Z [mrad]"))
    
    # Incident electron histograms
    # Expected momentum ~ e_energy
    hists[("inc_e", "pt")] = Hist(RegAx(100, 0, 1, name="pt", label="pT [GeV/c]"))
    hists[("inc_e", "px")] = Hist(RegAx(200, -e_energy*0.1, e_energy*0.1, name="px", label="px [GeV/c]"))
    hists[("inc_e", "py")] = Hist(RegAx(200, -e_energy*0.1, e_energy*0.1, name="py", label="py [GeV/c]"))
    hists[("inc_e", "pz")] = Hist(RegAx(200, -e_energy*1.05, -e_energy*0.95, name="pz", label="pz [GeV/c]"))
    hists[("inc_e", "p")] = Hist(RegAx(200, e_energy*0.9, e_energy*1.1, name="p", label="P [GeV/c]"))
    hists[("inc_e", "angle_z_mrad")] = Hist(RegAx(100, 0, 30, name="angle_z", label="Min. angle with Z [mrad]"))
    
    # Scattered electron histograms
    hists[("scat_e", "pt")] = Hist(RegAx(100, 0, p_energy, name="pt", label="pT [GeV/c]"))
    hists[("scat_e", "pz")] = Hist(RegAx(200, -p_energy, p_energy, name="pz", label="pz [GeV/c]"))
    hists[("scat_e", "p")] = Hist(RegAx(200, 0, p_energy, name="p", label="P [GeV/c]"))
    hists[("scat_e", "theta")] = Hist(RegAx(180, 0, np.pi, name="theta", label=r"$\theta$ [rad]"))
    hists[("scat_e", "phi")] = Hist(RegAx(360, -np.pi, np.pi, name="phi", label=r"$\phi$ [rad]"))
    hists[("scat_e", "eta")] = Hist(RegAx(100, -5, 5, name="eta", label=r"$\eta$ (pseudorapidity)"))
    
    # Scattered kaon histograms
    # Kaon momentum can be substantial fraction of beam energy
    max_p = max(e_energy, p_energy) * 0.8
    hists[("kaon", "pt")] = Hist(RegAx(100, 0, p_max*0.5, name="pt", label="pT [GeV/c]"))
    hists[("kaon", "pz")] = Hist(RegAx(200, -p_max*0.5, p_max, name="pz", label="pz [GeV/c]"))
    hists[("kaon", "p")] = Hist(RegAx(200, 0, p_max, name="p", label="P [GeV/c]"))
    hists[("kaon", "theta")] = Hist(RegAx(180, 0, np.pi, name="theta", label=r"$\theta$ [rad]"))
    hists[("kaon", "phi")] = Hist(RegAx(360, -np.pi, np.pi, name="phi", label=r"$\phi$ [rad]"))
    hists[("kaon", "eta")] = Hist(RegAx(100, -5, 5, name="eta", label=r"$\eta$ (pseudorapidity)"))
    
    # Scattered lambda histograms
    # Lambda will carry remaining momentum
    hists[("lambda", "pt")] = Hist(RegAx(100, 0, 1, name="pt", label="pT [GeV/c]"))
    hists[("lambda", "px")] = Hist(RegAx(200, -p_energy*0.03, p_energy*0.03, name="px", label="px [GeV/c]"))
    hists[("lambda", "py")] = Hist(RegAx(200, -p_energy*0.03, p_energy*0.03, name="py", label="py [GeV/c]"))
    hists[("lambda", "pz")] = Hist(RegAx(200, p_max*0.7, p_max*1.05, name="pz", label="pz [GeV/c]"))
    hists[("lambda", "p")] = Hist(RegAx(200, p_max*0.7, p_max*1.05, name="p", label="P [GeV/c]"))
    hists[("lambda", "angle_z_mrad")] = Hist(RegAx(100, 0, 30, name="angle_z", label="Min. angle with Z [mrad]"))
    
    return hists


def calculate_pseudorapidity(theta):
    """Calculate pseudorapidity from theta"""
    # Avoid log(0) by adding small epsilon
    return -np.log(np.tan(theta/2) + 1e-30)


def fill_histograms(hists, chunk):
    """
    Extract kinematics and fill appropriate histograms based on particle type.
    """
    for particle in particles:
        # Get the branch name for this particle
        branch = particle_to_branch[particle]
        arr = chunk[branch]
        
        # Extract momentum components
        px = arr["fP"]["fX"]
        py = arr["fP"]["fY"]
        pz = arr["fP"]["fZ"]

        # print(chunk.fields)
        # print(particle)
        # print(px)
        # print(py)
        # print(pz)
        
        # Calculate common quantities
        pt = np.sqrt(px**2 + py**2)
        p_mag = np.sqrt(px**2 + py**2 + pz**2 + 1e-30)
        
        # Fill common histograms
        hists[(particle, "pt")].fill(pt=pt)
        hists[(particle, "pz")].fill(pz=pz)
        hists[(particle, "p")].fill(p=p_mag)

       
        if particle in incident_particles + ["lambda"]:
            # For incident particles: minimal angle with Z-axis
            # This is the angle from z-axis: arccos(|pz|/p)
            cos_angle = np.abs(pz) / p_mag
            # Clamp to valid range for arccos
            cos_angle = np.clip(cos_angle, -1, 1)
            min_angle_z = np.arccos(cos_angle)  # in radians
            angle_z_mrad = min_angle_z * 1000  # convert to mrad
            
            hists[(particle, "angle_z_mrad")].fill(angle_z_mrad)
            hists[(particle, "px")].fill(px=px)
            hists[(particle, "py")].fill(py=py)
            
        elif particle in scattered_particles:
            # For scattered particles: theta, phi in radians and eta
            theta = np.arctan2(pt, pz)  # polar angle [0, pi]
            phi = np.arctan2(py, px)    # azimuthal angle [-pi, pi]
            eta = calculate_pseudorapidity(theta)
            
            hists[(particle, "theta")].fill(theta=theta)
            hists[(particle, "phi")].fill(phi=phi)
            hists[(particle, "eta")].fill(eta=eta)


def save_histogram_json(hist_obj, particle, var, filepath):
    """
    Save a single histogram to JSON file with the same name as the PNG.
    """
    # Get axis info
    axis = hist_obj.axes[0]
    
    # Get data
    counts = hist_obj.values()
    bin_centers = axis.centers
    
    # Calculate statistics
    total_entries = np.sum(counts)
    if total_entries > 0:
        mean = np.sum(bin_centers * counts) / total_entries
        variance = np.sum(counts * (bin_centers - mean)**2) / total_entries
        std = np.sqrt(variance)
    else:
        mean = 0.0
        std = 0.0
    
    # Simple JSON structure
    data = {
        "particle": particle,
        "variable": var,
        "title": f"{particle_full_names[particle]} - {var.replace('_', ' ')}",
        "x_label": axis.label,
        "bins": {
            "edges": axis.edges.tolist(),
            "centers": bin_centers.tolist(),
            "counts": counts.tolist()
        },
        "stats": {
            "entries": int(total_entries),
            "mean": float(mean),
            "std": float(std)
        }
    }
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def plot_histograms(hists, outdir="plots"):
    """
    Create matplotlib plots for each histogram and save them.
    """
    os.makedirs(outdir, exist_ok=True)
    
    for (particle, var), hist_obj in hists.items():
        fig, ax = plt.subplots(figsize=(7, 5))
        
        # Plot the histogram
        hist_obj.plot1d(ax=ax)
        
        # Set title with full particle name
        full_name = particle_full_names[particle]
        ax.set_title(f"{full_name} - {var.replace('_', ' ')}")
        
        # Labels are already set from histogram creation
        ax.set_ylabel("Counts")
        ax.grid(True, alpha=0.3)
        
        fig.tight_layout()
        
        # Save with friendly particle name
        filename_base = f"{particle}_{var}"
        
        # Save PNG
        png_filepath = os.path.join(outdir, f"{filename_base}.png")
        plt.savefig(png_filepath, dpi=100)
        plt.close(fig)
        
        # Save JSON with same name
        json_filepath = os.path.join(outdir, f"{filename_base}.json")
        save_histogram_json(hist_obj, particle, var, json_filepath)
        
        print(f"Saved: {filename_base}.png and {filename_base}.json")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze kinematics of EIC final state particles from Evnts TTree."
    )
    parser.add_argument(
        "--input-file", "-i", 
        required=True, 
        help="Path to the ROOT file with the Evnts TTree."
    )
    parser.add_argument(
        "--energy", "-e",
        required=True,
        help="Beam energies in format ExP (e.g., 10x100 for 10 GeV e- and 100 GeV p+)"
    )
    parser.add_argument(
        "--outdir", "-o", 
        default="plots", 
        help="Directory to save output plots (default: plots)."
    )
    parser.add_argument(
        "--max-events", "-m", 
        type=int, 
        default=None, 
        help="Maximum number of events to process (default: all)."
    )
    parser.add_argument(
        "--chunk-size", 
        type=int, 
        default=100_000, 
        help="How many TTree entries to read per chunk (default: 100000)."
    )
    args = parser.parse_args()
    
    # Parse energy argument
    e_energy, p_energy = parse_energy(args.energy)
    print(f"Beam configuration: {e_energy} GeV electron x {p_energy} GeV proton")
    
    # Create histograms with appropriate limits
    hists = create_histograms(e_energy, p_energy)
    
    # Read and process TTree
    tree_name = "Evnts"
    events_processed = 0
    
    print(f"Processing file: {args.input_file}")
    
    for data_chunk in uproot.iterate(
            f"{args.input_file}:{tree_name}",
            expressions=branches,  # Use the actual branch names for ROOT access
            library="ak",
            step_size=args.chunk_size
    ):
        fill_histograms(hists, data_chunk)
        
        # Count events
        chunk_len = len(data_chunk[branches[0]])
        events_processed += chunk_len
        
        if args.max_events and events_processed >= args.max_events:
            print(f"Reached maximum events limit: {args.max_events}")
            break
    
    print(f"Processed {events_processed} events in total.")
    
    # Generate plots and JSON files
    print(f"Creating plots and JSON files in directory: {args.outdir}")
    plot_histograms(hists, outdir=args.outdir)
    print("\nDone!")


if __name__ == "__main__":
    main()