#!/usr/bin/env python3
"""
Script: scattered_electron.py

Scattered electron analysis comparing MC truth vs reconstructed electron.
Plots residual distributions (reco - MC), momentum distributions,
and pseudorapidity distributions from reco_dis CSV files.

Usage:
    python scattered_electron.py -o output_dir file1.csv file2.csv
    python scattered_electron.py -o plots data/*.reco_dis.csv

Dependencies:
    pip install pandas numpy matplotlib hist mplhep
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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
# Quality cuts — edit thresholds here (in GeV/c)
###############################################################################

GOOD_ELEC_DPX_MAX = 0.150   # |dpx| < 150 MeV/c
GOOD_ELEC_DPY_MAX = 0.150   # |dpy| < 150 MeV/c
GOOD_ELEC_DPZ_MAX = 0.400   # |dpz| < 400 MeV/c


###############################################################################
# Histogram Definitions — edit binning/ranges here
###############################################################################

def create_histograms():
    """Create all histograms with predefined binning.

    Modify the Axis(nbins, lo, hi, ...) parameters below to tweak ranges.
    """
    h = {}

    # --- Residuals (reco − MC) ---
    h['dpx'] = Hist(Axis(120, -1.0, 1.0, name="dpx", label=r"$p_x^{\mathrm{reco}} - p_x^{\mathrm{MC}}$ [GeV/c]"))
    h['dpy'] = Hist(Axis(120, -1.0, 1.0, name="dpy", label=r"$p_y^{\mathrm{reco}} - p_y^{\mathrm{MC}}$ [GeV/c]"))
    h['dpz'] = Hist(Axis(120, -2.0, 2.0, name="dpz", label=r"$p_z^{\mathrm{reco}} - p_z^{\mathrm{MC}}$ [GeV/c]"))

    # --- MC electron momentum ---
    h['mc_px'] = Hist(Axis(100, -5.0, 5.0, name="mc_px", label=r"MC $p_x^{e'}$ [GeV/c]"))
    h['mc_py'] = Hist(Axis(100, -5.0, 5.0, name="mc_py", label=r"MC $p_y^{e'}$ [GeV/c]"))
    h['mc_pz'] = Hist(Axis(100, -20.0, 20, name="mc_pz", label=r"MC $p_z^{e'}$ [GeV/c]"))
    h['mc_p']  = Hist(Axis(100, 0.0, 20.0, name="mc_p", label=r"MC $|\vec{p}^{e'}|$ [GeV/c]"))
    h['mc_pt'] = Hist(Axis(100, 0.0, 6.0, name="mc_pt", label=r"MC $p_T^{e'}$ [GeV/c]"))

    # --- Reconstructed electron momentum ---
    h['reco_px'] = Hist(Axis(100, -5.0, 5.0, name="reco_px", label=r"Reco $p_x^{e'}$ [GeV/c]"))
    h['reco_py'] = Hist(Axis(100, -5.0, 5.0, name="reco_py", label=r"Reco $p_y^{e'}$ [GeV/c]"))
    h['reco_pz'] = Hist(Axis(100, -20.0, 20, name="reco_pz", label=r"Reco $p_z^{e'}$ [GeV/c]"))
    h['reco_p']  = Hist(Axis(100, 0.0, 20.0, name="reco_p", label=r"Reco $|\vec{p}^{e'}|$ [GeV/c]"))
    h['reco_pt'] = Hist(Axis(100, 0.0, 6.0, name="reco_pt", label=r"Reco $p_T^{e'}$ [GeV/c]"))

    # --- Pseudorapidity ---
    h['mc_eta']   = Hist(Axis(100, -6.0, 6, name="mc_eta", label=r"MC $\eta^{e'}$"))
    h['reco_eta'] = Hist(Axis(100, -6.0, 6, name="reco_eta", label=r"Reco $\eta^{e'}$"))

    return h


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
    """Compute total momentum, transverse momentum, and pseudorapidity."""

    # MC electron
    df['mc_p']  = np.sqrt(df['mc_elec_px']**2 + df['mc_elec_py']**2 + df['mc_elec_pz']**2)
    df['mc_pt'] = np.sqrt(df['mc_elec_px']**2 + df['mc_elec_py']**2)
    df['mc_eta'] = np.where(
        df['mc_pt'] > 0,
        np.arctanh(df['mc_elec_pz'] / df['mc_p']),
        np.nan
    )

    # Reconstructed electron
    df['reco_p']  = np.sqrt(df['elec_px']**2 + df['elec_py']**2 + df['elec_pz']**2)
    df['reco_pt'] = np.sqrt(df['elec_px']**2 + df['elec_py']**2)
    df['reco_eta'] = np.where(
        df['reco_pt'] > 0,
        np.arctanh(df['elec_pz'] / df['reco_p']),
        np.nan
    )

    # Residuals
    df['dpx'] = df['elec_px'] - df['mc_elec_px']
    df['dpy'] = df['elec_py'] - df['mc_elec_py']
    df['dpz'] = df['elec_pz'] - df['mc_elec_pz']

    # Good-electron flag: reconstructed AND residuals within cuts
    df['has_reco'] = df['elec_px'].notna()
    df['good_elec'] = (
        df['has_reco']
        & (df['dpx'].abs() < GOOD_ELEC_DPX_MAX)
        & (df['dpy'].abs() < GOOD_ELEC_DPY_MAX)
        & (df['dpz'].abs() < GOOD_ELEC_DPZ_MAX)
    )

    return df


###############################################################################
# Fill Histograms
###############################################################################

def fill_histograms(hists, df):
    """Fill all histograms from DataFrame."""
    print("\nFilling histograms...")

    # Map from histogram key to DataFrame column
    column_map = {
        # residuals
        'dpx': 'dpx',   'dpy': 'dpy',   'dpz': 'dpz',
        # MC
        'mc_px': 'mc_elec_px', 'mc_py': 'mc_elec_py', 'mc_pz': 'mc_elec_pz',
        'mc_p': 'mc_p',       'mc_pt': 'mc_pt',
        # reco
        'reco_px': 'elec_px', 'reco_py': 'elec_py', 'reco_pz': 'elec_pz',
        'reco_p': 'reco_p',   'reco_pt': 'reco_pt',
        # eta
        'mc_eta': 'mc_eta',   'reco_eta': 'reco_eta',
    }

    for hname, col in column_map.items():
        data = df[col].dropna().values
        if len(data) > 0:
            hists[hname].fill(data)
            print(f"  {hname:12s}  ({col:16s}): {len(data)} entries")


###############################################################################
# Plotting Helpers
###############################################################################

def _stats_text(values, edges):
    """Return a stats-box string for a filled histogram."""
    total = values.sum()
    if total == 0:
        return ""
    centers = (edges[:-1] + edges[1:]) / 2
    mean = np.average(centers, weights=values)
    std  = np.sqrt(np.average((centers - mean)**2, weights=values))
    return f"Entries: {int(total)}\nMean: {mean:.4f}\nStd: {std:.4f}"


def plot_single(h, path):
    """Save a single 1-D histogram to *path*."""
    fig, ax = plt.subplots(figsize=(10, 6))
    h.plot1d(ax=ax)

    stats = _stats_text(h.values(), h.axes[0].edges)
    if stats:
        ax.text(0.05, 0.95, stats, transform=ax.transAxes,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                fontsize=10)

    ax.set_xlabel(h.axes[0].label or h.axes[0].name)
    ax.set_ylabel("Counts")
    ax.set_title(f"{h.axes[0].name} Distribution")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")


def plot_overlay(h_list, labels, colors, xlabel, title, path):
    """Overlay several 1-D histograms on one canvas."""
    fig, ax = plt.subplots(figsize=(10, 6))

    for h, label, color in zip(h_list, labels, colors):
        if h.sum() > 0:
            h.plot1d(ax=ax, label=label, color=color, linewidth=2)

    ax.set_xlabel(xlabel)
    ax.set_ylabel("Counts")
    ax.set_title(title)
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")


###############################################################################
# Event Counts Bar Chart
###############################################################################

def plot_event_counts(df, path):
    """Bar chart: total events, reconstructed electrons, good electrons."""
    n_total = len(df)
    n_reco  = int(df['has_reco'].sum())
    n_good  = int(df['good_elec'].sum())

    pct_reco = 100.0 * n_reco / n_total if n_total else 0
    pct_good_total = 100.0 * n_good / n_total if n_total else 0
    pct_good_reco  = 100.0 * n_good / n_reco if n_reco else 0

    categories = ["Total events", "Reconstructed", "Good electrons"]
    counts = [n_total, n_reco, n_good]
    colors = ["#4878d0", "#ee854a", "#6acc64"]

    labels = [
        f"{n_total}",
        f"{n_reco}  ({pct_reco:.1f}%)",
        f"{n_good}  ({pct_good_total:.1f}%,  {pct_good_reco:.1f}% of reco)",
    ]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(categories, counts, color=colors, edgecolor='black', linewidth=0.5)

    for bar, label in zip(bars, labels):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                label, ha='center', va='bottom', fontsize=12)

    ax.set_ylabel("Events")
    ax.set_title("Scattered Electron: Event Counts")
    ax.grid(axis='y', alpha=0.3)

    cut_text = (f"|dpx| < {GOOD_ELEC_DPX_MAX*1e3:.0f} MeV/c\n"
                f"|dpy| < {GOOD_ELEC_DPY_MAX*1e3:.0f} MeV/c\n"
                f"|dpz| < {GOOD_ELEC_DPZ_MAX*1e3:.0f} MeV/c")
    ax.text(0.98, 0.95, cut_text, transform=ax.transAxes,
            ha='right', va='top', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")


###############################################################################
# Main Analysis
###############################################################################

def main():
    parser = argparse.ArgumentParser(
        description="Scattered-electron analysis of reco_dis CSV files")
    parser.add_argument('-o', '--outdir', type=str, default='scattered_electron_output',
                        help='Directory for output plots')
    parser.add_argument('-e', '--events', type=int, default=None,
                        help='Max number of events to process')
    parser.add_argument('files', nargs='+', help='Input reco_dis CSV files')
    args = parser.parse_args()

    output_dir = Path(args.outdir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("Scattered Electron Analysis")
    print("=" * 70)

    # --- Load data ---
    print("\nLoading CSV files...")
    df = concat_csvs_with_unique_events([Path(f) for f in args.files])

    if args.events is not None:
        print(f"Limiting to {args.events} events")
        df = df.head(args.events)

    print(f"Total events: {len(df)}")

    # --- Derived columns ---
    df = add_derived_columns(df)

    # --- Create & fill histograms ---
    hists = create_histograms()
    fill_histograms(hists, df)

    # --- Individual plots ---
    print("\nCreating individual plots...")
    for name, h in hists.items():
        if h.sum() > 0:
            plot_single(h, output_dir / f"{name}.png")

    # --- Overlay: MC vs Reco momentum components ---
    print("\nCreating overlay plots...")
    mc_reco_pairs = [
        ('mc_px', 'reco_px', r"$p_x^{e'}$ [GeV/c]", "Scattered Electron $p_x$: MC vs Reco"),
        ('mc_py', 'reco_py', r"$p_y^{e'}$ [GeV/c]", "Scattered Electron $p_y$: MC vs Reco"),
        ('mc_pz', 'reco_pz', r"$p_z^{e'}$ [GeV/c]", "Scattered Electron $p_z$: MC vs Reco"),
        ('mc_p',  'reco_p',  r"$|\vec{p}^{e'}|$ [GeV/c]", "Scattered Electron $|p|$: MC vs Reco"),
        ('mc_pt', 'reco_pt', r"$p_T^{e'}$ [GeV/c]", "Scattered Electron $p_T$: MC vs Reco"),
        ('mc_eta', 'reco_eta', r"$\eta^{e'}$", r"Scattered Electron $\eta$: MC vs Reco"),
    ]

    for mc_key, reco_key, xlabel, title in mc_reco_pairs:
        plot_overlay(
            [hists[mc_key], hists[reco_key]],
            labels=["MC truth", "Reconstructed"],
            colors=["blue", "red"],
            xlabel=xlabel, title=title,
            path=output_dir / f"overlay_{mc_key}_vs_{reco_key}.png",
        )

    # --- Event counts bar chart ---
    print("\nCreating event counts chart...")
    plot_event_counts(df, output_dir / "event_counts.png")

    # --- Summary ---
    print("\n" + "=" * 70)
    print("Analysis Complete!")
    print(f"Output directory: {output_dir}")
    print("=" * 70)


if __name__ == "__main__":
    main()
