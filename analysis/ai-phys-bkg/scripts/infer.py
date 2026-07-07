#!/usr/bin/env python3
"""
Run a trained event classifier on a dataset and write + plot the predictions.

This is the "apply the model" step, separate from training. It takes a
checkpoint written by train_dnn.py and a dataset, runs a forward pass, and
saves per-event predictions plus summary plots.

The checkpoint is self-contained: it carries the model weights, the exact
standardization constants (mean/std) used at training time, and the metadata
(top_n, feature names, class names). So inference reproduces the identical
preprocessing without you having to remember any settings.

Two kinds of input dataset are accepted
---------------------------------------
1. A raw per-particle *.feather file (e.g. a brand-new physics sample). It is
   run through the SAME top-N-particle flattening as prepare_events.py, using
   the top_n stored in the checkpoint. This is the common case: "here is a new
   dataset, what does the model think it is?".

2. A prepared *.npz from prepare_events.py. If it also contains truth labels
   `y`, the script additionally computes accuracy, a confusion matrix and ROC
   (i.e. it evaluates the model). Without `y` it only predicts.

Outputs (into --out-dir, names optionally prefixed with --prefix)
-----------------------------------------------------------------
    predictions.csv            one row per event: predicted class + probability
                               of every class (+ true class if labels existed)
    summary.txt                per-predicted-class counts and fractions (and
                               accuracy/confusion/ROC when labels are present)
    predicted_fractions.png    bar chart: fraction of events sent to each class
    score_distribution.png     histogram of the network's output probability
                               (split by true class if labels are present)
    confusion_matrix.png       only when truth labels are available
    roc_curve.png              only when truth labels are available

Usage
-----
    # Predict on a raw feather with a model trained elsewhere
    infer.py models/events_msf_vs_dis_top10/msf_vs_dis_model.pt \\
             data/msf_2026-07_reco_9x130.feather --prefix msf_infer

    # Evaluate on a labeled prepared dataset
    infer.py models/events_top10/model.pt data/events_top10.npz
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch

import matplotlib
matplotlib.use("Agg")  # save PNGs, no display needed
import matplotlib.pyplot as plt

# Reuse the exact model definition, preprocessing and metric helpers from the
# training/preparation scripts so inference can never drift out of sync with
# how the model was built and trained.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from train_dnn import (EventClassifier, confusion_matrix, classification_report,
                       roc_curve_points, roc_auc)
from prepare_events import build_event_matrix


def load_dataset(path: str, meta: dict):
    """Return (X, y_or_None, feature_names) for a .feather or .npz input.

    For a feather we rebuild the per-event matrix with the checkpoint's top_n;
    for an npz we read X (and y if present) straight from the file.
    """
    path = str(path)
    if path.endswith(".feather"):
        df = pd.read_feather(path)
        X, feature_names, _ = build_event_matrix(df, meta["top_n"])
        return X, None, feature_names
    elif path.endswith(".npz"):
        data = np.load(path)
        X = data["X"]
        y = data["y"] if "y" in data.files else None
        return X, y, meta["feature_names"]
    else:
        raise ValueError(f"Unsupported input '{path}': expected .feather or .npz")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a trained event classifier on a dataset; write and plot results.")
    parser.add_argument("model", help="Checkpoint (model.pt) from train_dnn.py")
    parser.add_argument("dataset", help="Input .feather (raw) or .npz (prepared)")
    parser.add_argument("-o", "--out-dir", default=None,
                        help="Output directory (default: next to the input dataset)")
    parser.add_argument("--prefix", default="",
                        help="Prefix for all output file names, e.g. 'msf_infer'")
    parser.add_argument("--batch-size", type=int, default=4096)
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # --- load the self-contained checkpoint ---------------------------------
    # weights_only=False because the checkpoint also stores numpy scaler arrays
    # and the meta dict, not just tensors. (Only load checkpoints you trust.)
    ckpt = torch.load(args.model, map_location=device, weights_only=False)
    meta = ckpt["meta"]
    class_names = meta["class_names"]
    n_classes = len(class_names)
    mean = ckpt["scaler_mean"]
    std = ckpt["scaler_std"]
    print(f"Model: {ckpt['n_features']} features -> "
          f"{' -> '.join(map(str, ckpt['hidden']))} -> {n_classes} classes")
    print(f"Classes: {class_names}")

    # --- load the dataset to score ------------------------------------------
    X, y, feature_names = load_dataset(args.dataset, meta)
    print(f"Dataset: {X.shape[0]:,} events, {X.shape[1]} features"
          + ("  (with truth labels)" if y is not None else "  (no labels)"))

    # Guard against feeding the model a differently-built feature vector.
    if X.shape[1] != ckpt["n_features"]:
        raise ValueError(
            f"Feature count mismatch: dataset has {X.shape[1]} features but the "
            f"model expects {ckpt['n_features']}. Was the same --top-n / feature "
            f"set used?")
    if list(feature_names) != list(meta["feature_names"]):
        print("WARNING: feature names differ from the checkpoint's; proceeding by "
              "position, but double-check the input was built the same way.")

    # --- rebuild the model and load the trained weights ---------------------
    model = EventClassifier(ckpt["n_features"], n_classes,
                            hidden=tuple(ckpt["hidden"]), dropout=ckpt["dropout"]).to(device)
    model.load_state_dict(ckpt["model_state"])
    model.eval()  # disables dropout and freezes BatchNorm to inference mode

    # --- apply the identical standardization, then run the forward pass -----
    Xs = ((X - mean) / std).astype(np.float32)
    probs_list = []
    with torch.no_grad():
        for start in range(0, len(Xs), args.batch_size):
            xb = torch.from_numpy(Xs[start:start + args.batch_size]).to(device)
            probs_list.append(torch.softmax(model(xb), dim=1).cpu().numpy())
    probs = np.concatenate(probs_list)         # [n_events, n_classes]
    y_pred = probs.argmax(axis=1)              # predicted class per event

    # --- output locations ----------------------------------------------------
    out_dir = Path(args.out_dir) if args.out_dir else Path(args.dataset).resolve().parent
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = f"{args.prefix}_" if args.prefix else ""

    def out(name):
        return out_dir / f"{prefix}{name}"

    saved = []

    # --- write per-event predictions CSV ------------------------------------
    pred_df = pd.DataFrame({
        "event_index": np.arange(len(y_pred)),
        "pred_label": y_pred,
        "pred_class": [class_names[i] for i in y_pred],
    })
    for i, name in enumerate(class_names):
        pred_df[f"prob_{name}"] = probs[:, i]
    if y is not None:
        pred_df.insert(1, "true_label", y)
        pred_df.insert(2, "true_class", [class_names[i] for i in y])
    pred_df.to_csv(out("predictions.csv"), index=False)
    saved.append(out("predictions.csv"))

    # --- text summary --------------------------------------------------------
    counts = np.bincount(y_pred, minlength=n_classes)
    lines = [f"Model:   {args.model}",
             f"Dataset: {args.dataset}   ({len(y_pred):,} events)",
             "",
             "Predicted class distribution:"]
    for i, name in enumerate(class_names):
        lines.append(f"  {name:<40} {counts[i]:>10,}  ({counts[i] / len(y_pred):6.2%})")

    if y is not None:
        acc = float((y_pred == y).mean())
        report_txt, cm = classification_report(y, y_pred, class_names)
        lines += ["", f"Truth labels present -> evaluation:",
                  f"  accuracy: {acc:.4f}", "", report_txt]
        if n_classes == 2:
            lines.append(f"\nROC AUC (class 1 vs class 0): {roc_auc(y, probs[:, 1]):.4f}")

    summary = "\n".join(lines)
    print("\n" + summary)
    out("summary.txt").write_text(summary + "\n")
    saved.append(out("summary.txt"))

    # --- plot: predicted-class fractions (bar chart) ------------------------
    fig, ax = plt.subplots(figsize=(max(5, 1.5 * n_classes), 4.5))
    ax.bar(range(n_classes), counts / len(y_pred), color="steelblue")
    ax.set_xticks(range(n_classes), class_names, rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("fraction of events")
    ax.set_title("Predicted class distribution")
    for i, c in enumerate(counts):
        ax.text(i, c / len(y_pred), f"{c / len(y_pred):.1%}", ha="center", va="bottom",
                fontsize=8)
    fig.tight_layout()
    fig.savefig(out("predicted_fractions.png"), dpi=120)
    saved.append(out("predicted_fractions.png"))

    # --- plot: score distribution -------------------------------------------
    # Binary: histogram P(class 1). Multi-class: histogram the winning
    # (max) probability - a proxy for how confident the model is per event.
    fig, ax = plt.subplots(figsize=(7, 5))
    bins = np.linspace(0, 1, 51)
    if n_classes == 2:
        if y is not None:
            for i, name in enumerate(class_names):
                ax.hist(probs[y == i, 1], bins=bins, histtype="step", lw=1.5,
                        label=f"true {name}")
        else:
            ax.hist(probs[:, 1], bins=bins, histtype="step", lw=1.5, color="steelblue",
                    label="all events")
        ax.set_xlabel(f"network output: P({class_names[1]})")
    else:
        ax.hist(probs.max(axis=1), bins=bins, histtype="step", lw=1.5, color="steelblue",
                label="all events")
        ax.set_xlabel("network output: max class probability (confidence)")
    ax.set_yscale("log")
    ax.set_ylabel("events")
    ax.set_title("Classifier score distribution")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out("score_distribution.png"), dpi=120)
    saved.append(out("score_distribution.png"))

    # --- plots that need truth labels ---------------------------------------
    if y is not None:
        cm_norm = cm / cm.sum(axis=1, keepdims=True)
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        for ax, mat, fmt, title in [
            (axes[0], cm, "d", "counts"),
            (axes[1], cm_norm, ".3f", "row-normalized (recall)"),
        ]:
            im = ax.imshow(mat, cmap="Blues")
            fig.colorbar(im, ax=ax, fraction=0.046)
            ax.set_xticks(range(n_classes), class_names, rotation=30, ha="right", fontsize=8)
            ax.set_yticks(range(n_classes), class_names, fontsize=8)
            ax.set_xlabel("predicted class"); ax.set_ylabel("true class")
            ax.set_title(f"Confusion matrix ({title})")
            for i in range(n_classes):
                for j in range(n_classes):
                    color = "white" if mat[i, j] > mat.max() / 2 else "black"
                    ax.text(j, i, format(mat[i, j], fmt), ha="center", va="center",
                            color=color)
        fig.tight_layout()
        fig.savefig(out("confusion_matrix.png"), dpi=120)
        saved.append(out("confusion_matrix.png"))

        fig, ax = plt.subplots(figsize=(6, 5.5))
        if n_classes == 2:
            fpr, tpr = roc_curve_points(y, probs[:, 1])
            ax.plot(fpr, tpr, label=f"AUC = {roc_auc(y, probs[:, 1]):.4f}")
        else:
            for i, name in enumerate(class_names):
                y_bin = (y == i).astype(int)
                fpr, tpr = roc_curve_points(y_bin, probs[:, i])
                ax.plot(fpr, tpr, label=f"{name} vs rest (AUC {roc_auc(y_bin, probs[:, i]):.4f})")
        ax.plot([0, 1], [0, 1], "k--", lw=1, label="random guess")
        ax.set_xlabel("false positive rate"); ax.set_ylabel("true positive rate")
        ax.set_title("ROC curve")
        ax.legend(loc="lower right", fontsize=8)
        fig.tight_layout()
        fig.savefig(out("roc_curve.png"), dpi=120)
        saved.append(out("roc_curve.png"))

    print()
    for path in saved:
        print(f"Saved: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
