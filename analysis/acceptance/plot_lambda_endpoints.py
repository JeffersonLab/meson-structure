#!/usr/bin/env python3
"""
plot_lambda_endpoints.py
========================

Plot primary-Λ decay-endpoint distributions grouped by number of daughters.
ZX plots are overlaid on the EIC center-forward detector image; ZY plots use
the same Z axis extent but no detector background (there is no sideways
picture). A third group of plots shows 1-D Z distributions with the EIC
picture as a ribbon on top so Z landmarks line up visually.

Usage
-----
    # One CSV
    python plot_lambda_endpoints.py run_001.mcpart_lambda.csv -o plots/

    # Several files concatenated with unique event IDs
    python plot_lambda_endpoints.py run_*.mcpart_lambda.csv -o plots/

    # Glob pattern (quote it!)
    python plot_lambda_endpoints.py "data/*.mcpart_lambda.csv" -o plots/ --glob

Input
-----
Any CSV product that carries `lam_is_first`, `lam_nd`, `lam_epx`, `lam_epy`,
and `lam_epz` columns. That includes:
    *.mcpart_lambda.csv
    *.acceptance_npi0.csv
    *.acceptance_ppim.csv

Primary lambdas = `lam_is_first == 1`. Daughter-count categories:

    nd = 0   - Λ did not decay inside the world volume
    nd = 1   - Λ with a single recorded daughter
    nd = 2   - canonical two-body decay
    nd ≥ 3   - showering / recharging cases

Outputs (written to OUTDIR)
---------------------------
I.  ZX plane (overlaid on eic_center_forward_bw.png):
        lam_endpoints_zx_scatter.png            (coloured by nd category)
        lam_endpoints_zx_hist2d_nd0.png
        lam_endpoints_zx_hist2d_nd1.png
        lam_endpoints_zx_hist2d_nd2.png
        lam_endpoints_zx_hist2d_nd3plus.png
        lam_endpoints_zx_hist2d_ndany.png

II. ZY plane (same Z extent, no detector backdrop):
        lam_endpoints_zy_scatter.png
        lam_endpoints_zy_hist2d_{nd0,nd1,nd2,nd3plus,ndany}.png

III. ZR plane — R = sqrt(X^2 + Y^2), overlaid on EIC image (upper half):
        lam_endpoints_zr_scatter.png
        lam_endpoints_zr_hist2d_{nd0,nd1,nd2,nd3plus,ndany}.png

IV. 1-D Z distributions with the EIC image as a header strip:
        lam_endpoints_z1d_{nd0,nd1,nd2,nd3plus,ndany}.png
        lam_endpoints_z1d_overlay.png        (all categories on one figure)
        lam_endpoints_z1d_overlay_log.png    (log y)

V. Λ polar angle wrt Z axis — all categories overlaid in a single figure:
        lam_angle_theta.png          (linear y, mrad)
        lam_angle_theta_log.png      (log y, to expose tails)

VI. Λ decay-code column chart (uses `lam_decay`, 9 codes from the converter):
        lam_decay_counts.png         (linear y)
        lam_decay_counts_log.png     (log y)
"""

import argparse
import glob
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import BoundaryNorm, ListedColormap, LogNorm

from aa_helpers import (
    DEFAULT_BCK_IMAGE,
    DEFAULT_BCK_SCALE_POINTS,
    concat_csvs_with_unique_events,
    create_plot_with_background,
)


# Daughter-count categories: (key, label, color, predicate on lam_nd series)
CATEGORIES = [
    ("nd0",     "nd = 0", "tab:blue",   lambda s: s == 0),
    ("nd1",     "nd = 1", "tab:green",  lambda s: s == 1),
    ("nd2",     "nd = 2", "tab:orange", lambda s: s == 2),
    ("nd3plus", "nd ≥ 3", "tab:red",    lambda s: s >= 3),
]


# -----------------------------------------------------------------------
# Background-image helpers
# -----------------------------------------------------------------------
def _bg_extent():
    """Compute (z_left, z_right, y_bottom, y_top) in mm for the EIC picture.

    This mirrors aa_helpers.create_plot_with_background() but does not
    open a figure — useful when the caller just wants the z range.
    """
    p0, p1 = DEFAULT_BCK_SCALE_POINTS
    x_scale = (p1["mm"]["x"] - p0["mm"]["x"]) / (p1["pixel"]["x"] - p0["pixel"]["x"])
    x_offset = p0["mm"]["x"] - x_scale * p0["pixel"]["x"]
    y_scale = (p1["mm"]["y"] - p0["mm"]["y"]) / (p1["pixel"]["y"] - p0["pixel"]["y"])
    y_offset = p0["mm"]["y"] - y_scale * p0["pixel"]["y"]
    image = mpimg.imread(DEFAULT_BCK_IMAGE)
    h_px, w_px = image.shape[:2]
    z_left = x_offset
    z_right = x_scale * w_px + x_offset
    y_top = y_offset
    y_bottom = y_scale * h_px + y_offset
    return z_left, z_right, y_bottom, y_top


def _draw_bg(ax):
    """Draw the calibrated EIC picture onto an existing Axes."""
    z_left, z_right, y_bottom, y_top = _bg_extent()
    image = mpimg.imread(DEFAULT_BCK_IMAGE)
    ax.imshow(
        image,
        extent=(z_left, z_right, y_bottom, y_top),
        origin="upper",
        interpolation="nearest",
    )
    return z_left, z_right, y_bottom, y_top


# -----------------------------------------------------------------------
# File collection
# -----------------------------------------------------------------------
def collect_files(patterns, use_glob):
    if not use_glob:
        return list(patterns)
    out = []
    for pat in patterns:
        matched = sorted(glob.glob(pat))
        if not matched:
            print(f"warning: glob '{pat}' matched no files", file=sys.stderr)
        out.extend(matched)
    return out


# -----------------------------------------------------------------------
# ZX plane
# -----------------------------------------------------------------------
# Figure size for detector-overlay plots. The image is ~39 000 × 6 000 mm
# (aspect ~6.5:1), so (20, 4.5) leaves the axes box almost filling the
# figure instead of letting aspect='equal' shrink it to a thin strip.
BG_FIGSIZE = (20, 4.5)


def plot_zx_scatter(z, x, codes, out_path):
    fig, ax = create_plot_with_background(figsize=BG_FIGSIZE)
    xlim, ylim = ax.get_xlim(), ax.get_ylim()

    cmap = ListedColormap([c for _, _, c, _ in CATEGORIES])
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)
    sc = ax.scatter(z, x, c=codes, cmap=cmap, norm=norm,
                    s=3, alpha=0.55, edgecolors="none")

    cbar = fig.colorbar(sc, ax=ax, ticks=[0, 1, 2, 3], shrink=0.75)
    cbar.set_ticklabels([lbl for _, lbl, _, _ in CATEGORIES])
    cbar.set_label("Λ daughters")

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel("Z (mm)")
    ax.set_ylabel("X (mm)")
    ax.set_title("Primary Λ endpoint, ZX plane — coloured by n daughters")
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path}  (N={len(z)})")


def plot_zx_hist2d(z, x, title, out_path, bins=(500, 250)):
    fig, ax = create_plot_with_background(figsize=BG_FIGSIZE)
    xlim, ylim = ax.get_xlim(), ax.get_ylim()

    if len(z) > 0:
        h = ax.hist2d(z, x, bins=bins, cmap="viridis",
                      norm=LogNorm(), alpha=0.80,
                      range=[xlim, ylim])
        fig.colorbar(h[3], ax=ax, shrink=0.75, label="counts (log)")
    else:
        ax.text(0.5, 0.5, "(no entries)", transform=ax.transAxes,
                ha="center", va="center", color="red", fontsize=14)

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel("Z (mm)")
    ax.set_ylabel("X (mm)")
    ax.set_title(title)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path}  (N={len(z)})")


# -----------------------------------------------------------------------
# ZY plane
# -----------------------------------------------------------------------
def plot_zy_scatter(z, y, codes, z_lim, y_lim, out_path):
    fig, ax = plt.subplots(figsize=(20, 10))
    cmap = ListedColormap([c for _, _, c, _ in CATEGORIES])
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)
    sc = ax.scatter(z, y, c=codes, cmap=cmap, norm=norm,
                    s=3, alpha=0.55, edgecolors="none")

    cbar = fig.colorbar(sc, ax=ax, ticks=[0, 1, 2, 3], shrink=0.75)
    cbar.set_ticklabels([lbl for _, lbl, _, _ in CATEGORIES])
    cbar.set_label("Λ daughters")

    ax.axhline(0, color="grey", linewidth=0.6, alpha=0.5)
    ax.set_xlim(z_lim)
    ax.set_ylim(y_lim)
    ax.set_xlabel("Z (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_title("Primary Λ endpoint, ZY plane — coloured by n daughters")
    ax.grid(alpha=0.25, linestyle="--")
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path}  (N={len(z)})")


def plot_zy_hist2d(z, y, title, out_path, z_lim, y_lim, bins=(500, 250)):
    fig, ax = plt.subplots(figsize=(20, 10))

    if len(z) > 0:
        h = ax.hist2d(z, y, bins=bins, cmap="viridis",
                      norm=LogNorm(), range=[z_lim, y_lim])
        fig.colorbar(h[3], ax=ax, shrink=0.75, label="counts (log)")
    else:
        ax.text(0.5, 0.5, "(no entries)", transform=ax.transAxes,
                ha="center", va="center", color="red", fontsize=14)

    ax.axhline(0, color="grey", linewidth=0.6, alpha=0.5)
    ax.set_xlim(z_lim)
    ax.set_ylim(y_lim)
    ax.set_xlabel("Z (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_title(title)
    ax.grid(alpha=0.25, linestyle="--")
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path}  (N={len(z)})")


# -----------------------------------------------------------------------
# ZR plane (R = sqrt(X^2+Y^2)) — identical layout to ZX, detector overlaid
# R is plotted with a minus sign so points fall into the *lower* half of
# the detector cross-section, which is where the hadron-beam pipe bends.
# -----------------------------------------------------------------------
def plot_zr_scatter(z, r, codes, out_path):
    fig, ax = create_plot_with_background(figsize=BG_FIGSIZE)
    xlim, ylim = ax.get_xlim(), ax.get_ylim()

    cmap = ListedColormap([c for _, _, c, _ in CATEGORIES])
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)
    sc = ax.scatter(z, -r, c=codes, cmap=cmap, norm=norm,
                    s=3, alpha=0.55, edgecolors="none")

    cbar = fig.colorbar(sc, ax=ax, ticks=[0, 1, 2, 3], shrink=0.75)
    cbar.set_ticklabels([lbl for _, lbl, _, _ in CATEGORIES])
    cbar.set_label("Λ daughters")

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel("Z (mm)")
    ax.set_ylabel("-R = -sqrt(X² + Y²) (mm)")
    ax.set_title("Primary Λ endpoint, Z vs. -R — coloured by n daughters")
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path}  (N={len(z)})")


def plot_zr_hist2d(z, r, title, out_path, bins=(500, 250)):
    fig, ax = create_plot_with_background(figsize=BG_FIGSIZE)
    xlim, ylim = ax.get_xlim(), ax.get_ylim()

    if len(z) > 0:
        h = ax.hist2d(z, -r, bins=bins, cmap="viridis",
                      norm=LogNorm(), alpha=0.80,
                      range=[xlim, ylim])
        fig.colorbar(h[3], ax=ax, shrink=0.75, label="counts (log)")
    else:
        ax.text(0.5, 0.5, "(no entries)", transform=ax.transAxes,
                ha="center", va="center", color="red", fontsize=14)

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel("Z (mm)")
    ax.set_ylabel("-R = -sqrt(X² + Y²) (mm)")
    ax.set_title(title)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path}  (N={len(z)})")


# -----------------------------------------------------------------------
# 1-D Z overlay — all categories + 'any' on one figure
# -----------------------------------------------------------------------
def plot_z1d_overlay(z_by_cat, z_any, out_path,
                     bins=400, log_y=False, title_suffix=""):
    fig, ax = plt.subplots(figsize=(20, 7))

    z_left, z_right, _, _ = _bg_extent()

    if len(z_any) == 0:
        ax.text(0.5, 0.5, "(no entries)", transform=ax.transAxes,
                ha="center", va="center", color="red", fontsize=14)
    else:
        rng = (z_left, z_right)
        for (key, label, color, _), data in zip(CATEGORIES, z_by_cat):
            if len(data) == 0:
                continue
            ax.hist(data, bins=bins, range=rng, histtype="step",
                    linewidth=1.6, color=color,
                    label=f"{label}  (N={len(data)})")

        ax.hist(z_any, bins=bins, range=rng, histtype="step",
                linewidth=2.0, color="black", linestyle="--",
                label=f"any nd  (N={len(z_any)})")

        if log_y:
            ax.set_yscale("log")

        ax.legend(loc="upper left")

    ax.set_xlim(z_left, z_right)
    ax.set_xlabel("Z (mm)")
    ax.set_ylabel("counts")
    ax.set_title(f"Primary Λ endpoint Z — categories overlaid{title_suffix}")
    ax.grid(alpha=0.3, linestyle="--")
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path}")


# -----------------------------------------------------------------------
# Decay-code column chart (9 codes from csv_mcpart_lambda.cxx)
# -----------------------------------------------------------------------
# (code, short label, multi-line x-tick label, bar colour)
# Codes match csv_mcpart_lambda.cxx exactly. Note: code 3 is ANY >2-daughter
# case (no Λ-in-daughters check is done by the converter). Code 8 is the
# catch-all for non-standard 1- or 2-daughter combinations (e.g. 2-daughter
# with PDGs other than {p,π-}/{n,π0}, or 1-daughter PDG not in {p,π+,n,π0}).
DECAY_CODES = [
    (0, "no daughters",       "0\nno\ndaughters",           "tab:blue"),
    (1, "p π-",               "1\np π-",                    "tab:green"),
    (2, "n π0",                "2\nn π0",                   "tab:orange"),
    (3, ">2 daughters",       "3\n>2\ndaughters",           "tab:red"),
    (4, "only p",             "4\nonly p",                  "tab:purple"),
    (5, "only π+",            "5\nonly π+",                 "tab:brown"),
    (6, "only n",             "6\nonly n",                  "tab:pink"),
    (7, "only π0",            "7\nonly π0",                 "tab:olive"),
    (8, "other (non-std 1/2)", "8\nother\nnon-std\n1/2-d",  "tab:gray"),
]


def plot_decay_counts(decay_series, out_path, log_y=False, title_suffix=""):
    codes = [c for c, *_ in DECAY_CODES]
    labels = [lbl for _, _, lbl, _ in DECAY_CODES]
    colors = [clr for *_, clr in DECAY_CODES]

    arr = decay_series.to_numpy()
    counts = [int(np.sum(arr == c)) for c in codes]
    total = sum(counts)

    fig, ax = plt.subplots(figsize=(14, 7))

    # Under log scale, bar baseline 0 -> -inf and blows up the y-range.
    # Switch to log *before* drawing and lift the baseline to 0.8.
    bar_bottom = 0.8 if log_y else 0.0
    if log_y:
        ax.set_yscale("log")

    bars = ax.bar(codes, counts, bottom=bar_bottom, color=colors,
                  edgecolor="black", linewidth=0.6)

    if total > 0:
        # Annotate each bar with count and percentage
        y_ref = max(counts) if not log_y else max(max(counts), 1)
        for bar, cnt in zip(bars, counts):
            pct = 100.0 * cnt / total
            y = bar.get_y() + bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2,
                    y + (0.01 * y_ref if not log_y else y * 0.05),
                    f"{cnt}\n{pct:.1f}%",
                    ha="center", va="bottom", fontsize=9)

    ax.set_xticks(codes)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_xlabel("lam_decay code")
    ax.set_ylabel("N primary Λ")
    ax.set_title(f"Primary Λ decay classification (N={total}){title_suffix}")
    ax.grid(axis="y", alpha=0.3, linestyle="--")

    if log_y:
        top = max(counts) if counts else 1
        ax.set_ylim(bottom=0.8, top=max(top * 2.5, 10))
    else:
        ax.set_ylim(top=max(counts) * 1.18 if max(counts) > 0 else 1)

    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path}")


# -----------------------------------------------------------------------
# Polar-angle (θ wrt Z) overlay of all categories
# -----------------------------------------------------------------------
def plot_theta_overlay(theta_by_cat, theta_any, out_path,
                       bins=200, log_y=False, title_suffix=""):
    """One figure, step histograms per category overlaid + 'any' outline."""
    fig, ax = plt.subplots(figsize=(12, 7))

    if len(theta_any) == 0:
        ax.text(0.5, 0.5, "(no entries)", transform=ax.transAxes,
                ha="center", va="center", color="red", fontsize=14)
    else:
        hi = float(np.nanpercentile(theta_any, 99.9))
        hi = max(hi, 1.0)
        rng = (0.0, hi)

        for (key, label, color, _), data in zip(CATEGORIES, theta_by_cat):
            if len(data) == 0:
                continue
            ax.hist(data, bins=bins, range=rng, histtype="step",
                    linewidth=1.6, color=color,
                    label=f"{label}  (N={len(data)})")

        ax.hist(theta_any, bins=bins, range=rng, histtype="step",
                linewidth=2.0, color="black", linestyle="--",
                label=f"any nd  (N={len(theta_any)})")

        # EIC hadron-beam crossing angle reference line
        if rng[0] <= 25.0 <= rng[1]:
            ax.axvline(25.0, color="grey", linewidth=1.0,
                       linestyle=":", alpha=0.8,
                       label="25 mrad (crossing)")

        if log_y:
            ax.set_yscale("log")

        ax.legend(loc="upper left")

    ax.set_xlabel("θ = ∠(p_Λ, +Z) (mrad)")
    ax.set_ylabel("counts")
    ax.set_title(f"Primary Λ polar angle vs. Z axis{title_suffix}")
    ax.grid(alpha=0.3, linestyle="--")
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path}")


# -----------------------------------------------------------------------
# 1-D Z with EIC ribbon on top
# -----------------------------------------------------------------------
def plot_z1d_on_bg(z, title, out_path, color="steelblue", bins=400):
    fig = plt.figure(figsize=(20, 8))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 3], hspace=0.08)
    ax_img = fig.add_subplot(gs[0])
    ax_hist = fig.add_subplot(gs[1], sharex=ax_img)

    z_left, z_right, y_bot, y_top = _draw_bg(ax_img)
    # Stretch the image to fill the axes box so its width matches the
    # histogram's (sharex is not enough — imshow's default aspect='equal'
    # shrinks the top axes and breaks vertical alignment of Z landmarks).
    ax_img.set_aspect("auto")
    ax_img.set_xlim(z_left, z_right)
    ax_img.set_ylim(y_bot, y_top)
    ax_img.tick_params(axis="x", labelbottom=False)
    ax_img.set_ylabel("X (mm)")
    ax_img.set_title(title)

    if len(z) > 0:
        ax_hist.hist(z, bins=bins, range=(z_left, z_right),
                     color=color, edgecolor="black", linewidth=0.3)
    else:
        ax_hist.text(0.5, 0.5, "(no entries)", transform=ax_hist.transAxes,
                     ha="center", va="center", color="red", fontsize=14)

    ax_hist.set_xlim(z_left, z_right)
    ax_hist.set_xlabel("Z (mm)")
    ax_hist.set_ylabel("counts")
    ax_hist.grid(alpha=0.3, linestyle="--")

    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path}  (N={len(z)})")


# -----------------------------------------------------------------------
# main
# -----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Plot primary-Λ decay-endpoint distributions by daughter count.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="See file docstring for full input / output description.",
    )
    parser.add_argument("input_files", nargs="+",
                        help="Input CSV file(s) or glob patterns (with --glob)")
    parser.add_argument("-o", "--output", required=True,
                        help="Output directory for plots")
    parser.add_argument("--glob", action="store_true",
                        help="Treat positional arguments as glob patterns")
    args = parser.parse_args()

    files = collect_files(args.input_files, args.glob)
    if not files:
        print("error: no input files", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.output, exist_ok=True)

    df = concat_csvs_with_unique_events(files)

    required = {"lam_is_first", "lam_nd", "lam_decay",
                "lam_epx", "lam_epy", "lam_epz",
                "lam_px", "lam_py", "lam_pz"}
    missing = required - set(df.columns)
    if missing:
        print(f"error: input CSV is missing columns {missing}", file=sys.stderr)
        sys.exit(1)

    df = df[df["lam_is_first"] == 1].copy()
    df = df.dropna(subset=["lam_nd", "lam_decay",
                           "lam_epx", "lam_epy", "lam_epz",
                           "lam_px", "lam_py", "lam_pz"])
    df["lam_decay"] = df["lam_decay"].astype(int)
    df["lam_nd"] = df["lam_nd"].astype(int)
    print(f"Primary Λ rows after filtering: {len(df)}")

    nd = df["lam_nd"]
    z = df["lam_epz"].to_numpy()
    x = df["lam_epx"].to_numpy()
    y = df["lam_epy"].to_numpy()

    # Map nd values to category codes 0..3 (for scatter coloring)
    nd_codes = np.select(
        [nd.to_numpy() == 0, nd.to_numpy() == 1, nd.to_numpy() == 2, nd.to_numpy() >= 3],
        [0, 1, 2, 3],
        default=-1,
    )
    valid = nd_codes >= 0  # always true given the categories, kept as safety

    # Z extent from EIC picture; Y from data percentiles (with a small pad)
    z_left, z_right, _, _ = _bg_extent()
    z_lim = (z_left, z_right)

    if len(y) > 0:
        y_lo, y_hi = np.nanpercentile(y, [0.1, 99.9])
        y_pad = 0.05 * max(abs(y_lo), abs(y_hi), 1.0)
        y_lim = (float(y_lo - y_pad), float(y_hi + y_pad))
    else:
        y_lim = (-2000.0, 2000.0)

    outdir = args.output

    # -------- I. ZX plane ---------------------------------------------
    plot_zx_scatter(z[valid], x[valid], nd_codes[valid],
                    os.path.join(outdir, "lam_endpoints_zx_scatter.png"))

    for key, label, _, pred in CATEGORIES:
        mask = pred(nd).to_numpy()
        plot_zx_hist2d(z[mask], x[mask],
                       f"Primary Λ endpoint ZX, {label}   (N={int(mask.sum())})",
                       os.path.join(outdir, f"lam_endpoints_zx_hist2d_{key}.png"))

    plot_zx_hist2d(z[valid], x[valid],
                   f"Primary Λ endpoint ZX, any nd   (N={int(valid.sum())})",
                   os.path.join(outdir, "lam_endpoints_zx_hist2d_ndany.png"))

    # -------- II. ZY plane --------------------------------------------
    plot_zy_scatter(z[valid], y[valid], nd_codes[valid], z_lim, y_lim,
                    os.path.join(outdir, "lam_endpoints_zy_scatter.png"))

    for key, label, _, pred in CATEGORIES:
        mask = pred(nd).to_numpy()
        plot_zy_hist2d(z[mask], y[mask],
                       f"Primary Λ endpoint ZY, {label}   (N={int(mask.sum())})",
                       os.path.join(outdir, f"lam_endpoints_zy_hist2d_{key}.png"),
                       z_lim, y_lim)

    plot_zy_hist2d(z[valid], y[valid],
                   f"Primary Λ endpoint ZY, any nd   (N={int(valid.sum())})",
                   os.path.join(outdir, "lam_endpoints_zy_hist2d_ndany.png"),
                   z_lim, y_lim)

    # -------- III. ZR plane (EIC image upper half) --------------------
    r = np.sqrt(x * x + y * y)

    plot_zr_scatter(z[valid], r[valid], nd_codes[valid],
                    os.path.join(outdir, "lam_endpoints_zr_scatter.png"))

    for key, label, _, pred in CATEGORIES:
        mask = pred(nd).to_numpy()
        plot_zr_hist2d(z[mask], r[mask],
                       f"Primary Λ endpoint ZR, {label}   (N={int(mask.sum())})",
                       os.path.join(outdir, f"lam_endpoints_zr_hist2d_{key}.png"))

    plot_zr_hist2d(z[valid], r[valid],
                   f"Primary Λ endpoint ZR, any nd   (N={int(valid.sum())})",
                   os.path.join(outdir, "lam_endpoints_zr_hist2d_ndany.png"))

    # -------- IV. 1-D Z on top of EIC image ---------------------------
    for key, label, color, pred in CATEGORIES:
        mask = pred(nd).to_numpy()
        plot_z1d_on_bg(z[mask],
                       f"Primary Λ endpoint Z, {label}   (N={int(mask.sum())})",
                       os.path.join(outdir, f"lam_endpoints_z1d_{key}.png"),
                       color=color)

    plot_z1d_on_bg(z[valid],
                   f"Primary Λ endpoint Z, any nd   (N={int(valid.sum())})",
                   os.path.join(outdir, "lam_endpoints_z1d_ndany.png"),
                   color="steelblue")

    z_by_cat = [z[pred(nd).to_numpy()] for _, _, _, pred in CATEGORIES]
    plot_z1d_overlay(z_by_cat, z[valid],
                     os.path.join(outdir, "lam_endpoints_z1d_overlay.png"),
                     log_y=False)
    plot_z1d_overlay(z_by_cat, z[valid],
                     os.path.join(outdir, "lam_endpoints_z1d_overlay_log.png"),
                     log_y=True, title_suffix="  (log y)")

    # -------- V. Polar angle θ with Z axis ----------------------------
    px = df["lam_px"].to_numpy()
    py = df["lam_py"].to_numpy()
    pz = df["lam_pz"].to_numpy()
    theta_mrad = 1000.0 * np.arctan2(np.sqrt(px * px + py * py), pz)

    theta_by_cat = [theta_mrad[pred(nd).to_numpy()] for _, _, _, pred in CATEGORIES]
    theta_any = theta_mrad[valid]

    plot_theta_overlay(theta_by_cat, theta_any,
                       os.path.join(outdir, "lam_angle_theta.png"),
                       log_y=False)
    plot_theta_overlay(theta_by_cat, theta_any,
                       os.path.join(outdir, "lam_angle_theta_log.png"),
                       log_y=True, title_suffix="  (log y)")

    # -------- VI. Decay-code column chart -----------------------------
    plot_decay_counts(df["lam_decay"],
                      os.path.join(outdir, "lam_decay_counts.png"),
                      log_y=False)
    plot_decay_counts(df["lam_decay"],
                      os.path.join(outdir, "lam_decay_counts_log.png"),
                      log_y=True, title_suffix="  (log y)")

    print(f"\nDone. All plots in: {outdir}")


if __name__ == "__main__":
    main()
