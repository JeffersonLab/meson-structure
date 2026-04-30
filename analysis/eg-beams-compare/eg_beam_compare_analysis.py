#!/usr/bin/env python3

"""
Script: analysis_3energies.py

Processes three k_lambda crossing files (5x41, 10x100, 18x275) simultaneously,
building 1D histograms for various kinematic variables from the "Evnts" TTree's
`invts` struct and the `lamb_scat` TLorentzVector. Compares the three energies
on the same set of plots in a style similar to an older fill + step design.

Usage Example:
    python analysis_3energies.py --outdir my_plots --chunk-size 100000 --max-events 200000

Dependencies:
    pip install uproot hist awkward matplotlib
"""

import os
import argparse
import numpy as np
import awkward as ak
import hist
from hist import Hist
import uproot
import matplotlib.pyplot as plt


###############################################################################
# Global Settings
###############################################################################

# Hardcode the file paths for each beam-energy configuration:
FILE_PATHS = {
    "5x41":   r"/mnt/e/data/meson-structure/k_lambda_crossing_0_5.0on41.0_x0.0001-0.9000_q1.0-500.0.root",
    "10x100": r"/mnt/e/data/meson-structure/k_lambda_crossing_0_10.0on100.0_x0.0001-0.9000_q1.0-500.0.root",
    "10x130": r"/mnt/e/data/meson-structure/k_lambda_crossing_0_10.0on100.0_x0.0001-0.9000_q1.0-500.0.root",
    "18x275": r"/mnt/e/data/meson-structure/k_lambda_crossing_0_18.0on275.0_x0.0001-0.9000_q1.0-500.0.root",
}

# Distinguish each beam energy with a color:
COLORS = {
    "5x41":  "green",
    "10x100": "magenta",
    "10x130": "brown",
    "18x275": "blue",
}


###############################################################################
# Histogram Creation
###############################################################################

def create_histograms():
    """
    Returns a dictionary of scikit-hep hist.Hist objects for the
    relevant variables in the Evnts tree: Q2, xBj, yD, W, |tSpec|, pDrest, alphaS,
    plus lambda_pt, lambda_rapidity from the lamb_scat TLorentzVector.
    """
    # 1D hist: Q2
    h_Q2 = Hist.new.Reg(120, 0, 120, name="Q2", label=r"$Q^2$ (GeV^2)").Double()

    # 1D hist: xBj
    h_xbj = Hist.new.Reg(100, 0, 1, name="xbj", label=r"$x_{\mathrm{Bj}}$").Double()

    # 1D hist: yD
    h_yD = Hist.new.Reg(100, 0, 1, name="yD", label="y_D").Double()

    # 1D hist: W
    h_W = Hist.new.Reg(100, 0, 10, name="W", label="W (GeV)").Double()

    # 1D hist: |tSpec|
    h_tSpec = Hist.new.Reg(100, 0, 2, name="tSpec", label=r"$|t_{\mathrm{spectator}}|$ (GeV^2)").Double()

    # 1D hist: pDrest
    h_pDrest = Hist.new.Reg(100, 0, 5, name="pDrest", label="pDrest").Double()

    # 1D hist: alphaS
    h_alphaS = Hist.new.Reg(100, 0, 2, name="alphaS", label="alphaS").Double()

    # 1D hist: lambda_pt
    h_lambda_pt = Hist.new.Reg(100, 0, 4, name="lambda_pt", label=r"Lambda $p_T$ (GeV/c)").Double()

    # 1D hist: lambda_rapidity
    h_lambda_rap = Hist.new.Reg(100, -5, 5, name="lambda_rapidity", label="Lambda Rapidity").Double()

    # Build a dict for convenience
    return {
        "Q2": h_Q2,
        "xbj": h_xbj,
        "yD": h_yD,
        "W": h_W,
        "tSpec": h_tSpec,
        "pDrest": h_pDrest,
        "alphaS": h_alphaS,
        "lambda_pt": h_lambda_pt,
        "lambda_rapidity": h_lambda_rap,
    }


###############################################################################
# Filling Histograms
###############################################################################

def fill_histograms(hists, chunk):
    """
    Fills the histogram dictionary with data from one chunk (awkward arrays)
    from the 'Evnts' tree.
    """
    # Access "invts" struct fields
    Q2_vals     = chunk["invts.Q2"]
    xBj_vals    = chunk["invts.xBj"]
    yD_vals     = chunk["invts.y_D"]
    W_vals      = chunk["invts.W"]
    tSpec_vals  = chunk["invts.tSpectator"]
    pDrest_vals = chunk["invts.pDrest"]
    alphaS_vals = chunk["invts.alphaS"]

    # Fill them
    hists["Q2"].fill(Q2=Q2_vals)
    hists["xbj"].fill(xbj=xBj_vals)
    hists["yD"].fill(yD=yD_vals)
    hists["W"].fill(W=W_vals)
    hists["tSpec"].fill(tSpec=np.abs(tSpec_vals))  # store absolute value
    hists["pDrest"].fill(pDrest=pDrest_vals)
    hists["alphaS"].fill(alphaS=alphaS_vals)

    # Access "lamb_scat" TLorentzVector
    lamb_scat = chunk["lamb_scat"]
    lambda_px = lamb_scat["px"]
    lambda_py = lamb_scat["py"]
    lambda_pz = lamb_scat["pz"]
    lambda_E  = lamb_scat["E"]

    # Derived Lambda kinematics
    lambda_pt = np.sqrt(lambda_px**2 + lambda_py**2)
    eps = 1e-9
    lambda_rapidity = 0.5 * np.log((lambda_E + lambda_pz + eps) / (lambda_E - lambda_pz + eps))

    hists["lambda_pt"].fill(lambda_pt=lambda_pt)
    hists["lambda_rapidity"].fill(lambda_rapidity=lambda_rapidity)


###############################################################################
# Processing a Single File
###############################################################################

def process_file(filename, chunk_size=100_000, max_events=None):
    """
    Reads the 'Evnts' tree in the given ROOT file, in chunks,
    fills the histograms, and returns the histogram dictionary.
    """
    hists = create_histograms()

    tree_name = "Evnts"
    expressions = [
        "invts.Q2", "invts.xBj", "invts.y_D", "invts.W", "invts.tSpectator",
        "invts.pDrest", "invts.alphaS",
        "lamb_scat"
    ]

    events_processed = 0
    root_tree = uproot.open(f"{filename}:{tree_name}")
    print(root_tree.keys())
    for chunk in root_tree.iterate(
            expressions=expressions,
            step_size=chunk_size
    ):
        fill_histograms(hists, chunk)

        events_processed += len(chunk["invts.Q2"])
        if max_events and events_processed >= max_events:
            break

    return hists


###############################################################################
# Plotting Routines
###############################################################################

def plot_1d_comparison(hists_by_energy, var_key, outdir="plots", xlog=False):
    """
    Plots the 1D histograms for the same variable across 3 energies on one figure.
    hists_by_energy is a dict: { '5x41': <histdict>, '10x100': <histdict>, ... }
    var_key is the key in each histdict for the variable (e.g. "Q2", "xbj", etc.)
    """
    os.makedirs(outdir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8,6))

    # We'll define a local function that mimics the fill+step style from your snippet
    def _plot_fill_step(hist_obj, label="", color="blue", alpha=0.2):
        # 'hist_obj.plot1d' can accept histtype='fill', but we can do it in two calls:
        hist_obj.plot1d(ax=ax, histtype='fill', color=color, alpha=alpha, label=label)
        hist_obj.plot1d(ax=ax, histtype='step', color=color)

    # Plot each energy's histogram
    for energy, hdict in hists_by_energy.items():
        hist_obj = hdict[var_key]
        _plot_fill_step(hist_obj, label=energy, color=COLORS[energy], alpha=0.3)

    # Set axis labels (take the label from one hist)
    any_hist = list(hists_by_energy.values())[0][var_key]
    if any_hist.axes[0].label is not None:
        ax.set_xlabel(any_hist.axes[0].label)
    else:
        ax.set_xlabel(var_key)

    ax.set_ylabel("Counts")

    if xlog:
        ax.set_xscale("log")

    ax.set_title(f"{var_key} comparison among 3 energies")
    ax.legend(loc='best')
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, f"compare_{var_key}.png"))
    plt.close(fig)


def make_all_comparison_plots(hists_by_energy, outdir="plots"):
    """
    Calls plot_1d_comparison for each variable we want to compare.
    """
    # Just list the keys we used
    variable_keys = [
        "Q2", "xbj", "yD", "W", "tSpec", "pDrest", "alphaS",
        "lambda_pt", "lambda_rapidity"
    ]

    # We can define which ones we might want in log scale, for example Q2:
    logx_vars = {"Q2": True}  # or add more as needed

    for var in variable_keys:
        xlog = logx_vars.get(var, False)
        plot_1d_comparison(hists_by_energy, var, outdir=outdir, xlog=xlog)


###############################################################################
# Main Script Logic
###############################################################################

def parse_args():
    parser = argparse.ArgumentParser(
        description="Process three k_lambda crossing files for 5x41, 10x100, 18x275 energies."
    )
    parser.add_argument("--chunk-size", type=int, default=100000,
                        help="Number of events to read per chunk. (default: 100000)")
    parser.add_argument("--max-events", type=int, default=None,
                        help="Max number of events to process for each file.")
    parser.add_argument("--outdir", default="plots",
                        help="Where to store the output comparison plots.")
    return parser.parse_args()


def main():
    args = parse_args()

    # Process each file to produce a dictionary of histograms
    hists_by_energy = {}

    for energy, filepath in FILE_PATHS.items():
        print(f"\nProcessing {energy} file: {filepath}")
        hdict = process_file(
            filename=filepath,
            chunk_size=args.chunk_size,
            max_events=args.max_events
        )
        hists_by_energy[energy] = hdict

    # Now produce comparison plots for each variable
    make_all_comparison_plots(hists_by_energy, outdir=args.outdir)

    print("\nDone! Comparison plots saved to:", args.outdir)


if __name__ == "__main__":
    main()
