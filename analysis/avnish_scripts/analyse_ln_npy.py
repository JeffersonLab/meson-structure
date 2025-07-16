#!/usr/bin/env python3
"""
analyze_ln_npy.py
---------------------------------------------------------------
Post-analysis of the .npy files produced by run_leading_neutron_analysis.py

• verifies that each fπ(xL) curve is area-normalised to 0.1
• prints ⟨F2π⟩ and ⟨F2LN⟩ over the xL grid
• generates extra plots:
      - ratios of fπ models to a reference (Pauli-Villars by default)
      - ratios of F2π variants to NLO
      - LN–to–pion structure-function ratio check
---------------------------------------------------------------
"""

from pathlib import Path
import argparse
import numpy as np
from scipy.integrate import simpson
import matplotlib.pyplot as plt

# -------- user-friendly matplotlib style ----------
plt.rcParams.update({"figure.figsize": (6, 4),
                     "font.size": 11,
                     "grid.alpha": 0.3})

# --------------------------------------------------
# 1. command-line options
# --------------------------------------------------
parser = argparse.ArgumentParser(
    description="Analyse splitting / pion / LN .npy files")
parser.add_argument("datadir", help="directory containing .npy files (outputs_ln/)")
parser.add_argument("--ref", default="Pauli-Villars",
                    help="reference splitting model for ratio plots")
args = parser.parse_args()
datadir = Path(args.datadir).expanduser().resolve()

# basic check
if not datadir.is_dir():
    raise SystemExit(f"Directory {datadir} not found")

# same xL grid used in production script
xL = np.arange(0.0001, 1.0, 0.001)
xL_bar = 1.0 - xL

# --------------------------------------------------
# 2. load splitting arrays
# --------------------------------------------------
split_files = sorted(datadir.glob("fpi_*.npy"))
splitting = {f.stem.split("_", 1)[1]: np.load(f) for f in split_files}

print("\n=== Splitting-function normalisation check (∫ dxL fπ) ===")
for label, arr in splitting.items():
    area = simpson(arr, xL)
    print(f"{label:15s}: area = {area:.4f}")

# --------------------------------------------------
# 3. load pion structure functions
# --------------------------------------------------
pi_files = sorted(datadir.glob("F2pi_*.npy"))
pion_structure = {f.stem.split("_", 1)[1]: np.load(f) for f in pi_files}

print("\n=== 〈F2π〉 over xL (simple mean, NaNs ignored) ===")
for tag, arr in pion_structure.items():
    mean_val = np.nanmean(arr)
    print(f"{tag:18s}: mean = {mean_val:.5e}")

# --------------------------------------------------
# 4. load LN structure functions (only NLO variant for quick demo)
# --------------------------------------------------
ln_files = sorted(datadir.glob("F2LN_*_nlo.npy"))
ln_structure = {f.stem.split("_", 1)[1].rsplit("_", 1)[0]: np.load(f)
                for f in ln_files}

print("\n=== 〈F2LN〉 over xL (NLO PDF) ===")
for label, arr in ln_structure.items():
    mean_val = np.nanmean(arr)
    print(f"{label:15s}: mean = {mean_val:.5e}")

# --------------------------------------------------
# 5. extra diagnostic plots
# --------------------------------------------------
outplots = datadir / "analysis_plots"
outplots.mkdir(exist_ok=True)

# 5a) ratio of fπ curves to reference
ref = args.ref
if ref not in splitting:
    raise SystemExit(f"Reference model '{ref}' not found in {list(splitting)}")

plt.figure()
for label, arr in splitting.items():
    plt.plot(xL_bar, arr / splitting[ref], label=label)
plt.xlabel(r"$1-x_L$")
plt.ylabel(r"$f_{\pi/p}(x_L) / f_{\pi/p}^\mathrm{{{ref}}}$")
plt.title("Splitting-function ratios")
plt.grid(); plt.legend(); plt.tight_layout()
plt.savefig(outplots/"splitting_ratio.pdf")

# 5b) ratio of F2π variants to NLO
plt.figure()
for tag, arr in pion_structure.items():
    if tag == "nlo":
        base = arr
        continue
for tag, arr in pion_structure.items():
    if tag == "nlo":
        continue
    plt.plot(xL_bar, arr / base, label=tag)
plt.xlabel(r"$1-x_L$")
plt.ylabel(r"$F_2^{\pi,\;variant} / F_2^{\pi,\;NLO}$")
plt.title("Pion-PDF ratio check")
plt.grid(); plt.legend(); plt.tight_layout()
plt.savefig(outplots/"F2pi_ratio.pdf")

# 5c) sanity:  F2LN /(2 fπ F2π)  => should be ≈1 for each model
plt.figure()
for label, ln_arr in ln_structure.items():
    ratio = ln_arr / (2.0 * splitting[label] * pion_structure["nlo"])
    plt.plot(xL_bar, ratio, label=label)
plt.xlabel(r"$1-x_L$")
plt.ylabel(r"$F_2^{LN}/\bigl(2 f_{\pi/p} F_2^{\pi}\bigr)$")
plt.title("Consistency check (NLO PDF)")
plt.ylim(0.8, 1.2)
plt.grid(); plt.legend(); plt.tight_layout()
plt.savefig(outplots/"LN_consistency.pdf")

print(f"\nAll analysis plots saved to: {outplots}/")
