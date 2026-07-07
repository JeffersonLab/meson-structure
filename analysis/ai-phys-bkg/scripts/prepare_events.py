#!/usr/bin/env python3
"""
Build a per-EVENT machine-learning dataset from per-PARTICLE feather files.

Input
-----
One or more feather files produced by merge_reco_particles_to_feather.py.
Each row there is a single reconstructed particle; the ``event`` column groups
particles into events. Each feather file is one "event type" (= one class the
network will learn to recognize), e.g.:

    class 0 : dis_nc_ep_9x130_q2_1to10       (user label "1")
    class 1 : dis_nc_ep_9x130_q2_100to1000   (user label "2")

More files -> more classes; the script is N-class from the start.

What one training row looks like
--------------------------------
For every event we take the TOP_N particles with the highest momentum |p|
(sorted descending) and lay their features side by side into one fixed-length
vector:

    [ features of particle #1 | features of particle #2 | ... | #TOP_N | n_reco ]

If an event has fewer than TOP_N particles the missing slots are ZERO-PADDED,
and every particle slot carries an explicit ``present`` flag (1 = real
particle, 0 = padding) so the network can tell padding from a genuine
zero-valued feature.

Per-particle features (the "everything" feature set):

    present                      1 if the slot holds a real particle
    p, px, py, pz, energy, mass  kinematics (|p| is the sort key, kept as a feature)
    charge                       -1 / 0 / +1
    pid_<cat>                    one-hot particle-type category from the PDG code
                                 (unknown, e, mu, photon, pi, K, p, n_hadron, other)
    n_clusters, n_tracks         how many calorimeter clusters / tracks
    n_cluster_hits               total calorimeter hits behind the clusters
    n_track_measurements         tracker measurements on the tracks
    n_tracker_hits               tracker hits behind those measurements

Plus one event-level feature appended at the end:

    n_reco                       total number of reconstructed particles in the event
                                 (before the top-N cut - multiplicity is physics info!)

Class balancing & mixing
------------------------
Classes are balanced by downsampling every class to the size of the SMALLEST
one (a network trained on imbalanced classes learns to just guess the majority
class). All classes are then concatenated and shuffled with a fixed random
seed, so the saved file is already "mixed" and reproducible.

NOTE: the train/validation/test split is NOT done here - that belongs to the
training script, so you can re-split without rebuilding the dataset.

Output
------
    <out>.npz        X: float32 [n_events, TOP_N*n_feat + 1],  y: int64 [n_events]
    <out>.meta.json  feature names, class names, which columns are continuous
                     (the training script standardizes only those), settings used

Usage
-----
    prepare_events.py class0.feather class1.feather ... -o events_top10.npz
    prepare_events.py a.feather b.feather -o out.npz --top-n 10 --seed 42

    # Several feathers can form ONE class: join them with commas, and
    # optionally give the class a name with "name=" (default: first stem).
    prepare_events.py "dis=q2_1to10.feather,q2_100to1000.feather" msf.feather -o out.npz
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# PDG code -> small particle-type category.
# A raw PDG code (e.g. 211, -321, 2212) is a terrible neural-net input: it is
# categorical data pretending to be a number ("211 < 2212" means nothing).
# We map it to a small set of physics categories and one-hot encode it instead.
# ---------------------------------------------------------------------------
PID_CATEGORIES = ["unknown", "e", "mu", "photon", "pi", "K", "p", "n_hadron", "other"]

_PDG_TO_CATEGORY = {
    0: 0,       # unidentified reco object (track w/o PID or neutral cluster)
    11: 1,      # electron / positron
    13: 2,      # muon
    22: 3,      # photon
    211: 4,     # charged pion
    321: 5,     # charged kaon
    2212: 6,    # proton
    2112: 7,    # neutron
    130: 7,     # K0_L  (long-lived neutral kaon -> "neutral hadron" bucket)
    310: 7,     # K0_S
    3122: 7,    # Lambda
}


def pdg_to_category(pdg: pd.Series) -> pd.Series:
    """Map (signed) PDG codes to category indices; anything unlisted -> 'other'."""
    other = len(PID_CATEGORIES) - 1
    return pdg.abs().map(_PDG_TO_CATEGORY).fillna(other).astype(np.int64)


# Continuous per-particle columns taken straight from the particle table.
# These get standardized (mean 0, std 1) later in training; the one-hot PID
# columns and the `present` flag are already in [0, 1] and are left alone.
KINEMATIC_COLS = ["p", "px", "py", "pz", "energy", "mass", "charge"]
DETECTOR_COLS = ["n_clusters", "n_tracks", "n_cluster_hits",
                 "n_track_measurements", "n_tracker_hits"]


def build_event_matrix(df: pd.DataFrame, top_n: int):
    """Turn a per-particle table of ONE dataset into a per-event feature matrix.

    Parameters
    ----------
    df : pd.DataFrame
        Particle table with at least: event, px, py, pz, energy, mass, charge,
        pdg and the detector-count columns.
    top_n : int
        Number of highest-|p| particles kept per event.

    Returns
    -------
    X : np.ndarray, float32, shape [n_events, top_n * n_particle_features + 1]
    feature_names : list of str, one per column of X
    continuous : list of bool, one per column of X - True where the column is
        a real-valued quantity that should be standardized during training.
    """
    df = df.copy()
    df["p"] = np.sqrt(df["px"] ** 2 + df["py"] ** 2 + df["pz"] ** 2)
    df["pid_cat"] = pdg_to_category(df["pdg"])

    # Event multiplicity BEFORE the top-N cut - a per-event physics feature.
    n_reco = df.groupby("event").size().rename("n_reco")

    # Rank particles inside each event by momentum (0 = highest |p|) and keep
    # only the top_n. sort + cumcount is the vectorized version of
    # "for each event: sort particles, take first top_n".
    df = df.sort_values(["event", "p"], ascending=[True, False], kind="mergesort")
    df["rank"] = df.groupby("event").cumcount()
    top = df[df["rank"] < top_n]

    # pivot: rows = events, columns = particle rank, values = one feature.
    # Missing (event, rank) cells - events with fewer than top_n particles -
    # become NaN, which we replace with 0 (zero padding).
    def pivot(col):
        return top.pivot(index="event", columns="rank", values=col) \
                  .reindex(columns=range(top_n))

    # The `present` mask: 1 where the slot holds a real particle, 0 for padding.
    present = pivot("p").notna().astype(np.float32)

    blocks = [present.to_numpy()]
    per_particle_names = ["present"]
    per_particle_cont = [False]  # `present` is a flag, don't standardize

    for col in KINEMATIC_COLS + DETECTOR_COLS:
        blocks.append(pivot(col).fillna(0.0).to_numpy(dtype=np.float32))
        per_particle_names.append(col)
        per_particle_cont.append(True)

    # One-hot PID: one 0/1 matrix per category.
    pid = pivot("pid_cat")
    for icat, cat in enumerate(PID_CATEGORIES):
        blocks.append((pid == icat).astype(np.float32).to_numpy())
        per_particle_names.append(f"pid_{cat}")
        per_particle_cont.append(False)

    # blocks[k] has shape [n_events, top_n] (feature k for all ranks).
    # stack -> [n_events, n_feat, top_n]; transpose -> [n_events, top_n, n_feat];
    # reshape flattens to [n_events, top_n * n_feat] so that all features of
    # particle #1 come first, then all of particle #2, etc. - exactly the
    # "first n columns = highest-p particle" layout.
    stacked = np.stack(blocks, axis=1)
    X_particles = stacked.transpose(0, 2, 1).reshape(stacked.shape[0], -1)

    # Append the event-level multiplicity as the last column.
    events_index = present.index  # events, in pivot's sorted order
    X = np.concatenate(
        [X_particles, n_reco.loc[events_index].to_numpy(dtype=np.float32)[:, None]],
        axis=1,
    )

    feature_names = [f"p{rank:02d}_{name}"
                     for rank in range(top_n) for name in per_particle_names]
    feature_names.append("n_reco")
    continuous = per_particle_cont * top_n + [True]

    return X.astype(np.float32), feature_names, continuous


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a per-event top-N-particles ML dataset from particle feathers.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  %(prog)s data/dis_nc_ep_9x130_q2_1to10.feather \\
           data/dis_nc_ep_9x130_q2_100to1000.feather \\
           -o data/events_top10.npz --top-n 10
""",
    )
    parser.add_argument("inputs", nargs="+",
                        help="One argument per class (order defines class indices "
                             "0, 1, ...). Each argument is '[name=]file1[,file2,...]': "
                             "comma-joined feathers are concatenated into a single "
                             "class; 'name=' overrides the class name (default: "
                             "stem of the first file)")
    parser.add_argument("-o", "--output", required=True,
                        help="Output .npz path (a .meta.json is written next to it)")
    parser.add_argument("--top-n", type=int, default=10,
                        help="Highest-|p| particles kept per event (default: 10)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for balancing/shuffling (default: 42)")
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)

    per_class = []
    class_names = []
    feature_names = continuous = None

    for spec in args.inputs:
        # Parse "[name=]file1[,file2,...]" - one class per argument.
        if "=" in spec:
            name, _, files_part = spec.partition("=")
        else:
            files_part = spec
            name = Path(files_part.split(",")[0]).stem
        paths = files_part.split(",")

        print(f"\n=== class {len(class_names)}: {name} ({len(paths)} file(s)) ===")
        # When a class combines several feathers, offset the event IDs of each
        # subsequent file (same trick as in the CSV merge) so that events from
        # different feathers cannot collapse into one during the groupby.
        parts = []
        offset = 0
        for p in paths:
            df = pd.read_feather(p)
            df["event"] = df["event"] + offset
            offset = int(df["event"].max()) + 1
            print(f"  {p}: {df['event'].nunique():,} events")
            parts.append(df)
        df = pd.concat(parts, ignore_index=True)

        X, feature_names, continuous = build_event_matrix(df, args.top_n)
        print(f"events: {X.shape[0]:,}   features per event: {X.shape[1]}")
        per_class.append(X)
        class_names.append(name)

    # --- balance: downsample every class to the smallest class size ---------
    n_min = min(len(X) for X in per_class)
    print(f"\nBalancing: {n_min:,} events per class "
          f"(sizes were {[len(X) for X in per_class]})")
    Xs, ys = [], []
    for label, X in enumerate(per_class):
        pick = rng.choice(len(X), size=n_min, replace=False)
        Xs.append(X[pick])
        ys.append(np.full(n_min, label, dtype=np.int64))

    # --- mix: concatenate all classes and shuffle rows ----------------------
    X = np.concatenate(Xs)
    y = np.concatenate(ys)
    perm = rng.permutation(len(X))
    X, y = X[perm], y[perm]

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out, X=X, y=y)

    meta = {
        "top_n": args.top_n,
        "seed": args.seed,
        "class_names": class_names,      # index in this list == label in y
        "feature_names": feature_names,
        "continuous": continuous,        # True -> standardize in training
        "n_events": int(len(X)),
        "n_features": int(X.shape[1]),
        "inputs": [str(Path(p).resolve()) for p in args.inputs],
    }
    stem = str(out)[: -len(".npz")] if out.suffix == ".npz" else str(out)
    meta_path = Path(stem + ".meta.json")
    meta_path.write_text(json.dumps(meta, indent=2))

    print("\n" + "=" * 60)
    print(f"Saved dataset:  {out}")
    print(f"Saved metadata: {meta_path}")
    print(f"Events (rows):  {len(X):,}   ({n_min:,} per class x {len(class_names)})")
    print(f"Features:       {X.shape[1]}  "
          f"({args.top_n} particles x {X.shape[1] // args.top_n} + n_reco)")
    for i, name in enumerate(class_names):
        print(f"  class {i} = {name}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
