#!/usr/bin/env python3
"""
Analyse ppim combinatorics CSV produced by csv_edm4hep_ppim_combinatorics.

Usage:
    python analyse_ppim_combinatorics.py input.csv -o output_dir/

Produces PNG histograms in output_dir:
  - combinations_per_event.png  : distribution of combo count per event
  - true_vs_nontrue.png         : true-lambda pairs vs background combinations
  - reversed_assignments.png    : cases where proton/pion detector roles are swapped
"""

import argparse
import os
import sys

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def save(fig: plt.Figure, output_dir: str, name: str) -> None:
    path = os.path.join(output_dir, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved {path}")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyse ppim combinatorics CSV"
    )
    parser.add_argument("input", help="Input CSV file")
    parser.add_argument(
        "-o", "--output",
        default=".",
        help="Output directory for PNG histograms (default: current directory)",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.output, exist_ok=True)

    df = pd.read_csv(args.input)

    # -----------------------------------------------------------------------
    # Basic counts
    # -----------------------------------------------------------------------
    n_rows   = len(df)
    n_events = df["evt"].nunique()

    print("=" * 60)
    print(f"Input file           : {args.input}")
    print(f"Number of events     : {n_events}")
    print(f"Total rows (combos)  : {n_rows}")
    print("=" * 60)

    # -----------------------------------------------------------------------
    # 1. Number of combinations per event  (ignoring events with 0 combos –
    #    those never appear as rows in the CSV)
    # -----------------------------------------------------------------------
    combos_per_evt = df.groupby("evt").size()

    print(f"\n[1] Combinations per event (events with ≥1 combo)")
    print(f"    Events with ≥1 combo : {len(combos_per_evt)}")
    print(f"    Mean   : {combos_per_evt.mean():.2f}")
    print(f"    Median : {combos_per_evt.median():.0f}")
    print(f"    Max    : {combos_per_evt.max()}")

    max_combos = int(combos_per_evt.max())
    bins = range(1, max_combos + 2)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(
        combos_per_evt,
        bins=bins,
        align="left",
        rwidth=0.8,
        color="steelblue",
        edgecolor="black",
    )
    ax.set_xlabel("Combinations per event")
    ax.set_ylabel("Events")
    ax.set_title("Combinations per event  (events with ≥1 combination)")
    ax.set_xticks(range(1, min(max_combos + 1, 30)))   # cap x-ticks for readability
    fig.tight_layout()
    save(fig, args.output, "combinations_per_event.png")

    # -----------------------------------------------------------------------
    # 2. True-lambda pairs vs background  (and total)
    # -----------------------------------------------------------------------
    n_true     = int(df["is_true_lam"].sum())
    n_nontrue  = n_rows - n_true

    print(f"\n[2] True λ pairs vs non-true combinations")
    print(f"    True lambda pairs   : {n_true}")
    print(f"    Non-true combos     : {n_nontrue}")
    print(f"    Total               : {n_rows}")
    if n_rows:
        print(f"    Signal fraction     : {100.0 * n_true / n_rows:.2f} %")

    labels = ["True λ pair", "Non-true", "Total"]
    counts = [n_true, n_nontrue, n_rows]
    colors = ["mediumseagreen", "tomato", "steelblue"]

    fig, ax = plt.subplots(figsize=(5, 4))
    bars = ax.bar(labels, counts, color=colors, edgecolor="black")
    ax.bar_label(bars, fmt="%d", padding=3)
    ax.set_ylabel("Combinations")
    ax.set_title("True λ vs non-true combinations")
    fig.tight_layout()
    save(fig, args.output, "true_vs_nontrue.png")

    # -----------------------------------------------------------------------
    # 3. Reversed-assignment cases
    #    "Reversed" = the particle that reached B0 (pi candidate) is the
    #    TRUE proton, AND the particle that reached RomanPot (prot candidate)
    #    is the TRUE pion.
    #    Detected using true_prot_id and true_pi_id written alongside each row.
    # -----------------------------------------------------------------------
    known_mask = (df["true_prot_id"] >= 0) & (df["true_pi_id"] >= 0)
    df_known   = df[known_mask]
    n_known    = len(df_known)
    n_unknown  = n_rows - n_known

    reversed_mask = (
        (df_known["pi_id"]   == df_known["true_prot_id"]) &
        (df_known["prot_id"] == df_known["true_pi_id"])
    )
    n_reversed = int(reversed_mask.sum())
    n_correct  = n_known - n_reversed   # combos from events with a true lambda, not reversed

    print(f"\n[3] Reversed detector assignment (prot↔pion swapped)")
    print(f"    Rows with known true IDs      : {n_known}")
    print(f"    Rows without true lambda      : {n_unknown}")
    print(f"      → Normal assignment         : {n_correct}")
    print(f"      → Reversed (prot in B0,")
    print(f"          pion in RomanPot)        : {n_reversed}")
    if n_known:
        print(f"    Reversal rate (of known rows) : {100.0 * n_reversed / n_known:.2f} %")

    labels2 = [
        "Correct\n(pion→B0, prot→RP)",
        "Reversed\n(prot→B0, pion→RP)",
        "No true λ\nin event",
    ]
    counts2 = [n_correct, n_reversed, n_unknown]
    colors2 = ["steelblue", "tomato", "lightgray"]

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(labels2, counts2, color=colors2, edgecolor="black")
    ax.bar_label(bars, fmt="%d", padding=3)
    ax.set_ylabel("Combinations")
    ax.set_title("Detector assignment: reversed proton/pion candidates")
    fig.tight_layout()
    save(fig, args.output, "reversed_assignments.png")

    print("\nDone.")


if __name__ == "__main__":
    main()
