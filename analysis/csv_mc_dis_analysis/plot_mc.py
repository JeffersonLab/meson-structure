import os
import glob
import argparse
import re
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


VARS_16 = [
    "q2",
    "xbj",
    "y_d",
    "x_d",
    "yplus",
    "nu",
    "twopdotk",
    "s_e",
    "twopdotq",
    "s_q",
    "mx2",
    "w",
    "alphas",
    "pperps",
    "tspectator",
    "tprime",
]


def check_required_columns(df, filename):
    missing = [v for v in VARS_16 if v not in df.columns]
    if missing:
        raise ValueError(f"File '{filename}' is missing required columns: {missing}")


def load_merge(files):
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        check_required_columns(df, f)
        dfs.append(df[VARS_16])
    return pd.concat(dfs, ignore_index=True)


def plot_hist(data, var, outpng, bins=500, dpi=150):
    data = data[np.isfinite(data)]
    if data.size == 0:
        print(f"[WARN] {var}: no finite values, skip plot")
        return

    outdir = os.path.dirname(outpng)
    if outdir:
        os.makedirs(outdir, exist_ok=True)

    plt.figure(figsize=(8, 6))
    plt.hist(data, bins=bins, histtype="step")
    plt.xlabel("Value (float)")
    plt.ylabel("Counts")
    plt.title(f"dis_{var}")
    plt.ylim(bottom=0)
    plt.tight_layout()
    plt.savefig(outpng, dpi=dpi)
    plt.close()
    print(f"Saved: {outpng}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", default=".")
    parser.add_argument("--bins", type=int, default=500)
    parser.add_argument("--dpi", type=int, default=150)
    parser.add_argument(
        "inputs",
        nargs="+",
        help="k_lambda_*_5000evt_*.mc_dis.csv (files / dirs / globs)"
    )
    args = parser.parse_args()

    files = []
    for it in args.inputs:
        if os.path.isdir(it):
            files.extend(glob.glob(os.path.join(it, "k_lambda_*_5000evt_*.mc_dis.csv")))
        else:
            files.extend(glob.glob(it) if any(ch in it for ch in "*?[]") else [it])

    files = sorted(set(files))
    if not files:
        raise ValueError("No input files found.")

    energy_re = re.compile(r"_(5x41|10x100|18x275)_", re.IGNORECASE)
    groups = {
        "5x41GeV": [],
        "10x100GeV": [],
        "18x275GeV": [],
    }

    for f in files:
        base = os.path.basename(f)
        m = energy_re.search(base)
        if not m:
            print(f"[WARN] Cannot parse energy from filename, skip: {base}")
            continue

        tag = m.group(1).lower()
        if tag == "5x41":
            groups["5x41GeV"].append(f)
        elif tag == "10x100":
            groups["10x100GeV"].append(f)
        elif tag == "18x275":
            groups["18x275GeV"].append(f)

    for label, flist in groups.items():
        if not flist:
            print(f"[WARN] No files for {label}")
            continue

        df = load_merge(flist)

        for v in VARS_16:
            outpng = os.path.join(args.outdir, f"{v}_{label}.png")
            plot_hist(df[v].to_numpy(), v, outpng, bins=args.bins, dpi=args.dpi)

