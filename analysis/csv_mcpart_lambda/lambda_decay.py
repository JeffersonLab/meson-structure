#!/usr/bin/env python3
"""
Script: lambda_decay.py

MC truth analysis for Lambda particles and their decays from mcpart_lambda CSV files.
Plots kinematic distributions (momentum, pT) and decay vertex locations.

Usage:
    python lambda_decay.py -o output_dir -b 10x100 file1.csv file2.csv
    python lambda_decay.py -o plots data/*.mcpart_lambda.csv

Dependencies:
    pip install pandas numpy matplotlib hist mplhep
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import hist
from hist import Hist
from hist.axis import Regular as Axis

import argparse
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Optional: Use HEP styling
try:
    import mplhep as hep
    plt.style.use(hep.style.ROOT)
except ImportError:
    print("Note: mplhep not installed, using default matplotlib style")


###############################################################################
# Histogram Definitions
###############################################################################

def create_histograms():
    """Create all histograms with explicit explicit names and predefined binning."""
    hists = {}

    # --- Lambda Kinematics ---
    hists['hist_lam_p'] = Hist(Axis(100, 0.0, 50.0, name="p", label=r"True $\Lambda$ $|\vec{p}|$ [GeV/c]"))
    hists['hist_lam_pt'] = Hist(Axis(100, 0.0, 5.0, name="pt", label=r"True $\Lambda$ $p_T$ [GeV/c]"))
    hists['hist_lam_pz'] = Hist(Axis(120, -10.0, 50.0, name="pz", label=r"True $\Lambda$ $p_z$ [GeV/c]"))
    hists['hist_lam_eta'] = Hist(Axis(100, -6.0, 6.0, name="eta", label=r"True $\Lambda$ $\eta$"))

    # --- Lambda Decay Vertices ---
    # epz = End Point Z, decay_r = sqrt(epx^2 + epy^2)
    hists['hist_lam_decay_z'] = Hist(Axis(150, -5000.0, 40000.0, name="decay_z", label=r"$\Lambda$ Decay $z$ [mm]"))
    hists['hist_lam_decay_r'] = Hist(Axis(100, 0.0, 2000.0, name="decay_r", label=r"$\Lambda$ Decay $r$ [mm]"))
    
    # 2D Decay Vertex Map
    hists['hist_lam_decay_rz_2d'] = Hist(
        Axis(150, -5000.0, 40000.0, name="decay_z", label=r"$\Lambda$ Decay $z$ [mm]"),
        Axis(100, 0.0, 2000.0, name="decay_r", label=r"$\Lambda$ Decay $r$ [mm]")
    )

    # --- Daughter Kinematics (Proton & Pion from p + pi- decay) ---
    hists['hist_prot_p'] = Hist(Axis(100, 0.0, 50.0, name="p", label=r"True Proton $|\vec{p}|$ [GeV/c]"))
    hists['hist_pimin_p'] = Hist(Axis(100, 0.0, 20.0, name="p", label=r"True $\pi^-$ $|\vec{p}|$ [GeV/c]"))

    return hists


###############################################################################
# Data Loading
###############################################################################

def concat_csvs_with_unique_events(files):
    """Load and concatenate CSV files with globally unique event IDs."""
    dfs = []
    offset = 0

    for file in files:
        print(f"  Reading: {file}")
        if str(file).endswith('.zip'):
            df = pd.read_csv(file, compression='zip')
        else:
            df = pd.read_csv(file)

        df['event'] = df['event'] + offset
        offset = df['event'].max() + 1
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


###############################################################################
# Derived Quantities
###############################################################################

def add_derived_columns(df):
    """Compute total momentum, transverse momentum, and spatial coordinates."""

    # Lambda kinematics
    df['lam_p']  = np.sqrt(df['lam_px']**2 + df['lam_py']**2 + df['lam_pz']**2)
    df['lam_pt'] = np.sqrt(df['lam_px']**2 + df['lam_py']**2)
    df['lam_eta'] = np.where(
        df['lam_pt'] > 0,
        np.arctanh(df['lam_pz'] / df['lam_p']),
        np.nan
    )

    # Lambda decay spatial properties
    # epx, epy, epz are the end points of the Lambda track (decay point)
    df['lam_decay_r'] = np.sqrt(df['lam_epx']**2 + df['lam_epy']**2)
    df['lam_decay_z'] = df['lam_epz']
    
    # Flags for decays
    # lam_nd is number of daughters. If > 0, it decayed inside the simulated world.
    df['has_decay'] = df['lam_nd'] > 0
    df['is_ppi_decay'] = df['prot_id'].notna() & df['pimin_id'].notna()
    df['is_npi0_decay'] = df['neut_id'].notna() & df['pizero_id'].notna()

    # Proton kinematics (if it exists)
    df['prot_p']  = np.sqrt(df['prot_px']**2 + df['prot_py']**2 + df['prot_pz']**2)
    df['prot_pt'] = np.sqrt(df['prot_px']**2 + df['prot_py']**2)

    # Pion- kinematics (if it exists)
    df['pimin_p']  = np.sqrt(df['pimin_px']**2 + df['pimin_py']**2 + df['pimin_pz']**2)
    df['pimin_pt'] = np.sqrt(df['pimin_px']**2 + df['pimin_py']**2)

    return df


###############################################################################
# Fill Histograms
###############################################################################

def fill_histograms(hists, df):
    """Explicitly fill histograms using dataframe series to avoid obfuscation."""
    print("\nFilling histograms...")

    # 1. Lambda Kinematics (All primary lambdas)
    valid_lam_p = df.dropna(subset=['lam_p', 'lam_pt', 'lam_pz', 'lam_eta'])
    if not valid_lam_p.empty:
        hists['hist_lam_p'].fill(valid_lam_p['lam_p'].values)
        hists['hist_lam_pt'].fill(valid_lam_p['lam_pt'].values)
        hists['hist_lam_pz'].fill(valid_lam_p['lam_pz'].values)
        hists['hist_lam_eta'].fill(valid_lam_p['lam_eta'].values)
        print(f"  Filled Lambda kinematics: {len(valid_lam_p)} entries")

    # 2. Lambda Decay Vertices (Only for lambdas that actually decayed)
    decayed_lam = df[df['has_decay']].dropna(subset=['lam_decay_r', 'lam_decay_z'])
    if not decayed_lam.empty:
        hists['hist_lam_decay_r'].fill(decayed_lam['lam_decay_r'].values)
        hists['hist_lam_decay_z'].fill(decayed_lam['lam_decay_z'].values)
        hists['hist_lam_decay_rz_2d'].fill(decayed_lam['lam_decay_z'].values, decayed_lam['lam_decay_r'].values)
        print(f"  Filled Decay Vertices: {len(decayed_lam)} entries")

    # 3. Daughter Kinematics (Proton from p pi- decay)
    valid_prot = df[df['is_ppi_decay']].dropna(subset=['prot_p'])
    if not valid_prot.empty:
        hists['hist_prot_p'].fill(valid_prot['prot_p'].values)
        print(f"  Filled Proton kinematics: {len(valid_prot)} entries")

    # 4. Daughter Kinematics (Pion from p pi- decay)
    valid_pimin = df[df['is_ppi_decay']].dropna(subset=['pimin_p'])
    if not valid_pimin.empty:
        hists['hist_pimin_p'].fill(valid_pimin['pimin_p'].values)
        print(f"  Filled Pion kinematics: {len(valid_pimin)} entries")


###############################################################################
# Plotting Helpers
###############################################################################

def _stats_text(values, edges):
    """Return a stats-box string for a filled 1D histogram."""
    total = values.sum()
    if total == 0:
        return ""
    centers = (edges[:-1] + edges[1:]) / 2
    mean = np.average(centers, weights=values)
    std  = np.sqrt(np.average((centers - mean)**2, weights=values))
    return f"Entries: {int(total)}\nMean: {mean:.4f}\nStd: {std:.4f}"


def plot_single_1d(h, path):
    """Save a single 1-D histogram to *path*."""
    fig, ax = plt.subplots(figsize=(10, 6))
    h.plot1d(ax=ax, linewidth=2, color="#4878d0")

    stats = _stats_text(h.values(), h.axes[0].edges)
    if stats:
        ax.text(0.95, 0.95, stats, transform=ax.transAxes,
                verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                fontsize=11)

    ax.set_xlabel(h.axes[0].label or h.axes[0].name)
    ax.set_ylabel("Counts")
    ax.set_title(f"{h.axes[0].name} Distribution")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")


def plot_single_2d(h, path):
    """Save a 2-D histogram to *path*."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot using a log scale for better visibility of vertex distributions
    w, x, y = h.to_numpy()
    mesh = ax.pcolormesh(x, y, w.T, norm=LogNorm(), cmap='viridis')
    fig.colorbar(mesh, ax=ax, label='Counts')

    ax.set_xlabel(h.axes[0].label or h.axes[0].name)
    ax.set_ylabel(h.axes[1].label or h.axes[1].name)
    ax.set_title(f"2D Distribution: {h.axes[1].name} vs {h.axes[0].name}")

    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")


###############################################################################
# Event Counts Bar Chart
###############################################################################

def plot_decay_channels(df, path):
    """Bar chart: total lambdas, decayed, p pi-, n pi0 channels."""
    n_total = len(df)
    n_decayed = int(df['has_decay'].sum())
    n_ppi = int(df['is_ppi_decay'].sum())
    n_npi0 = int(df['is_npi0_decay'].sum())
    n_other = n_decayed - (n_ppi + n_npi0)

    categories = ["Total Lambda", "Decayed", "p + pi-", "n + pi0", "Other Decays"]
    counts = [n_total, n_decayed, n_ppi, n_npi0, n_other]
    colors = ["#4878d0", "#6acc64", "#ee854a", "#d65f5f", "#956cb4"]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(categories, counts, color=colors, edgecolor='black', linewidth=1.0)

    for bar in bars:
        height = bar.get_height()
        pct = 100.0 * height / n_total if n_total > 0 else 0
        label = f"{int(height)}\n({pct:.1f}%)"
        ax.text(bar.get_x() + bar.get_width() / 2, height,
                label, ha='center', va='bottom', fontsize=11)

    ax.set_ylabel("Count")
    ax.set_title(r"MC Truth $\Lambda$ Decay Channels")
    ax.grid(axis='y', alpha=0.3)
    
    # Extend Y axis slightly to fit the text labels
    ax.set_ylim(0, max(counts) * 1.15)

    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")


###############################################################################
# Main Analysis
###############################################################################

def main():
    parser = argparse.ArgumentParser(description="MC Truth Lambda analysis using mcpart_lambda CSV files")
    parser.add_argument('-o', '--output', type=str, default='mcpart_lambda_plots', help='Directory for output plots')
    parser.add_argument('-b', '--beam', type=str, default=None, help='Beam configuration (e.g. 10x100)')
    parser.add_argument('-e', '--events', type=int, default=None, help='Max number of events to process')
    parser.add_argument('files', nargs='+', help='Input mcpart_lambda CSV files')
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"{'=' * 70}")
    print(f"MC Truth Lambda Analysis")
    if args.beam:
        print(f"Beam: {args.beam}")
    print(f"{'=' * 70}")

    # --- Load data ---
    print("\nLoading CSV files...")
    df = concat_csvs_with_unique_events([Path(f) for f in args.files])

    if args.events is not None:
        print(f"Limiting to {args.events} events")
        df = df.head(args.events)

    print(f"Total events processed: {len(df)}")

    # --- Derived columns ---
    df = add_derived_columns(df)

    # --- Create & fill histograms ---
    hists = create_histograms()
    fill_histograms(hists, df)

    # --- Plotting ---
    print("\nCreating plots...")
    for name, h in hists.items():
        if h.sum() > 0:
            if isinstance(h.axes, tuple) and len(h.axes) == 2:
                plot_single_2d(h, output_dir / f"{name}.png")
            else:
                plot_single_1d(h, output_dir / f"{name}.png")

    # --- Decay channel summary chart ---
    print("\nCreating decay channel summary chart...")
    plot_decay_channels(df, output_dir / "decay_channels.png")

    # --- Summary ---
    print("\n" + "=" * 70)
    print("Analysis Complete!")
    print(f"Output plots saved in: {output_dir}")
    print("=" * 70)


if __name__ == "__main__":
    main()
