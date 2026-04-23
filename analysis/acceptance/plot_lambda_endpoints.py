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

V. Λ polar angle wrt Z axis — all categories overlaid in a single figure:
        lam_angle_theta.png          (linear y, mrad)
        lam_angle_theta_log.png      (log y, to expose tails)
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
def plot_zx_scatter(z, x, codes, out_path):
    fig, ax = create_plot_with_background()
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
    fig, ax = create_plot_with_background()
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
# ZR plane (R = sqrt(X^2+Y^2)) — EIC image upper half as backdrop
# -----------------------------------------------------------------------
def plot_zr_scatter(z, r, codes, out_path):
    fig, ax = create_plot_with_background()
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    r_max = max(abs(ylim[0]), abs(ylim[1]))

    cmap = ListedColormap([c for _, _, c, _ in CATEGORIES])
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)
    sc = ax.scatter(z, r, c=codes, cmap=cmap, norm=norm,
                    s=3, alpha=0.55, edgecolors="none")

    cbar = fig.colorbar(sc, ax=ax, ticks=[0, 1, 2, 3], shrink=0.75)
    cbar.set_ticklabels([lbl for _, lbl, _, _ in CATEGORIES])
    cbar.set_label("Λ daughters")

    ax.set_xlim(xlim)
    ax.set_ylim(0, r_max)
    ax.set_xlabel("Z (mm)")
    ax.set_ylabel("R = sqrt(X² + Y²) (mm)")
    ax.set_title("Primary Λ endpoint, ZR plane — coloured by n daughters")
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path}  (N={len(z)})")


def plot_zr_hist2d(z, r, title, out_path, bins=(500, 150)):
    fig, ax = create_plot_with_background()
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    r_max = max(abs(ylim[0]), abs(ylim[1]))
    r_range = (0.0, r_max)

    if len(z) > 0:
        h = ax.hist2d(z, r, bins=bins, cmap="viridis",
                      norm=LogNorm(), alpha=0.80,
                      range=[xlim, r_range])
        fig.colorbar(h[3], ax=ax, shrink=0.75, label="counts (log)")
    else:
        ax.text(0.5, 0.5, "(no entries)", transform=ax.transAxes,
                ha="center", va="center", color="red", fontsize=14)

    ax.set_xlim(xlim)
    ax.set_ylim(0, r_max)
    ax.set_xlabel("Z (mm)")
    ax.set_ylabel("R = sqrt(X² + Y²) (mm)")
    ax.set_title(title)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path}  (N={len(z)})")


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

        ax.legend(loc="upper right")

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

    required = {"lam_is_first", "lam_nd",
                "lam_epx", "lam_epy", "lam_epz",
                "lam_px", "lam_py", "lam_pz"}
    missing = required - set(df.columns)
    if missing:
        print(f"error: input CSV is missing columns {missing}", file=sys.stderr)
        sys.exit(1)

    df = df[df["lam_is_first"] == 1].copy()
    df = df.dropna(subset=["lam_nd",
                           "lam_epx", "lam_epy", "lam_epz",
                           "lam_px", "lam_py", "lam_pz"])
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

    print(f"\nDone. All plots in: {outdir}")


if __name__ == "__main__":
    main()
