#!/usr/bin/env python3
"""
pimin_acceptance_plots.py

Usage:
    python pimin_acceptance_plots.py acceptance_file hits_file -o results
"""
import argparse
from pathlib import Path
import os
import sys
import pandas as pd
import duckdb
import matplotlib.pyplot as plt
import numpy as np

def read_acceptance_counts(path_acceptance: Path, cols_for_counts):
    """Read only the columns needed for counting and return counts and total rows.
       Supports .csv, .parquet, .feather.
    """
    suffix = path_acceptance.suffix.lower()
    if suffix in (".parquet", ".parq"):
        df_small = pd.read_parquet(path_acceptance, columns=cols_for_counts)
    elif suffix in (".feather",):
        df_small = pd.read_feather(path_acceptance, columns=cols_for_counts)
    elif suffix in (".csv", ".txt"):
        # read only the columns we need (fast & memory friendly)
        df_small = pd.read_csv(path_acceptance, usecols=cols_for_counts)
    else:
        raise ValueError(f"Unsupported acceptance file type: {suffix}")
    total = len(df_small)   # number of rows/events
    return df_small, total

def fetch_hits_with_duckdb(path_hits: Path, detector_name: str, z_cut: float):
    """Use duckdb to select x,y,z for a single detector, applying a z < z_cut filter.
       Works for parquet or csv by choosing the appropriate table function.
    """
    suffix = path_hits.suffix.lower()
    con = duckdb.connect(database=":memory:")  # ephemeral connection
    try:
        if suffix in (".parquet", ".parq"):
            # parquet_scan reads parquet files
            sql = f"""
                SELECT x, y, z
                FROM parquet_scan('{path_hits}')
                WHERE detector = '{detector_name}' AND z < {float(z_cut)}
            """
        else:
            # read_csv_auto works for CSV; duckdb will auto-detect schema
            sql = f"""
                SELECT CAST(x AS DOUBLE) AS x, CAST(y AS DOUBLE) AS y, CAST(z AS DOUBLE) AS z
                FROM read_csv_auto('{path_hits}')
                WHERE detector = '{detector_name}' AND z < {float(z_cut)}
            """
        df = con.execute(sql).fetchdf()
    finally:
        con.close()
    return df

def make_and_save_hist2d(x, y, bins, out_path:Path, title, xlabel="x", ylabel="y", cmap="viridis"):
    """Make a 2D histogram plot and save it. Closes figure to free memory."""
    fig, ax = plt.subplots(figsize=(6,5))
    h = ax.hist2d(x, y, bins=bins, cmin=1, cmap=cmap)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    cbar = fig.colorbar(h[3], ax=ax)
    cbar.set_label("Counts")
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)   # important to free memory

def plot_and_tabulate(path_acceptance: Path, path_hits: Path, outdir: Path):
    path_acceptance = Path(path_acceptance)
    path_hits = Path(path_hits)
    outdir.mkdir(parents=True, exist_ok=True)

    # === columns / detectors to analyze (customize if needed) ===
    RP_hits = "pimin_ForwardRomanPotHits"
    LFHCAL_hits = "pimin_LFHCALHits"
    B0_tracker_hits = "pimin_B0TrackerHits"

    cols_for_counts = [RP_hits, LFHCAL_hits, B0_tracker_hits]

    # read only the small acceptance table
    df_small, total = read_acceptance_counts(path_acceptance, cols_for_counts)

    # compute counts (vectorized)
    count_RP = int((df_small[RP_hits] == 1).sum())
    count_LFHCAL = int((df_small[LFHCAL_hits] == 1).sum())
    count_B0_tracker = int((df_small[B0_tracker_hits] == 1).sum())

    fraction_RP = count_RP / max(1, total)
    fraction_LFHCAL = count_LFHCAL / max(1, total)
    fraction_B0_tracker = count_B0_tracker / max(1, total)

    # write the stats CSV
    stats_data = [
        {"Detector": "ForwardRomanPotHits", "Hits": count_RP,           "Fraction of Events": fraction_RP},
        {"Detector": "LFHCALHits",          "Hits": count_LFHCAL,     "Fraction of Events": fraction_LFHCAL},
        {"Detector": "B0TrackerHits",       "Hits": count_B0_tracker, "Fraction of Events": fraction_B0_tracker},
    ]
    df_stats = pd.DataFrame(stats_data)
    stats_path = outdir / "pimin_acceptance_stats.csv"
    df_stats.to_csv(stats_path, index=False)

    # === Now fetch (x,y,z) for each detector using duckdb (filtered by z in SQL) ===
    # choose z-cuts
    b0_z_cut = 5905  # mm
    rp_z_cut = 32556 # mm
    # LFHCAL no z cut
    # fetch
    print("Querying hits for B0TrackerHits ...")
    b0_df = fetch_hits_with_duckdb(path_hits, "B0TrackerHits", b0_z_cut)
    print("Querying hits for ForwardRomanPotHits ...")
    rp_df = fetch_hits_with_duckdb(path_hits, "ForwardRomanPotHits", rp_z_cut)
    print("Querying hits for LFHCALHits ...")
    lfhcal_df = fetch_hits_with_duckdb(path_hits, "LFHCALHits", z_cut=1e9)  # effectively no cut

    # === make and save histograms ===
    make_and_save_hist2d(b0_df['x'], b0_df['y'], bins=(100,100),
                        out_path=outdir / "pi_min_B0.png",
                        title=r"1st Layer B0 Tracker Acceptance $\pi^-$",
                        xlabel="x (mm)", ylabel="y (mm)")

    make_and_save_hist2d(rp_df['x'], rp_df['y'], bins=(100,100),
                        out_path=outdir / "pi_min_RP.png",
                        title=r"1st Layer Roman Pots Acceptance $\pi^-$",
                        xlabel="x (mm)", ylabel="y (mm)")

    make_and_save_hist2d(lfhcal_df['x'], lfhcal_df['y'], bins=(100,100),
                        out_path=outdir / "LFHCAL.png",
                        title="LFHCAL Acceptance",
                        xlabel="x (mm)", ylabel="y (mm)")

    return {
        "stats_csv": str(stats_path),
        "b0_png": str(outdir / "pi_min_B0.png"),
        "rp_png": str(outdir / "pi_min_RP.png"),
        "lfhcal_png": str(outdir / "LFHCAL.png"),
    }

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Process paired acceptance and hits CSV files",
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="CSV files given as pairs: acceptance1 hits1 acceptance2 hits2 ...",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=".",
        help="Output directory for results",
    )

    args = parser.parse_args()

    if len(args.files) % 2 != 0:
        raise ValueError(
            "You must provide an even number of files: acceptance/hits pairs."
        )

    file_pairs = list(zip(args.files[0::2], args.files[1::2]))

    for acceptance_file, hits_file in file_pairs:
        print(f"Processing pair:\n  acceptance = {acceptance_file}\n  hits = {hits_file}")
        # call your processing function here
        # process_pair(acceptance_file, hits_file, args.output)

if __name__ == "__main__":
    main()