#!/usr/bin/env python3
"""
Simple 2-layer DNN to classify true-Λ vs background combinatoric pairs.

Uses Keras 3 with the JAX backend (lightweight, no full TensorFlow needed).

Input features  – pion & proton momenta + first-hit positions:
    pi_px, pi_py, pi_pz,  prot_px, prot_py, prot_pz,
    pi_first_b0_x, pi_first_b0_y, pi_first_b0_z,
    prot_first_rp_x, prot_first_rp_y, prot_first_rp_z

Target          – is_true_lam  (binary 0/1)

Usage
-----
    python train_true_lambda_dnn.py  data.csv  -o results/

Outputs (in -o directory):
    model.keras          – saved trained model
    training_history.png – loss & accuracy curves
    roc_curve.png        – ROC on the test set
    confusion_matrix.png – confusion matrix on the test set
    summary.txt          – printed model summary + final metrics
"""

from __future__ import annotations

import argparse
import os
import sys
import textwrap

# ---- Set Keras backend BEFORE importing keras --------------------------------
os.environ.setdefault("KERAS_BACKEND", "jax")

import keras                       # noqa: E402  (must come after env-var)
import numpy as np                 # noqa: E402
import pandas as pd                # noqa: E402
import matplotlib                  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt    # noqa: E402
from sklearn.model_selection import train_test_split   # noqa: E402
from sklearn.metrics import roc_curve, auc, confusion_matrix, ConfusionMatrixDisplay  # noqa: E402

# ------------------------------------------------------------------------------
# Feature columns
# ------------------------------------------------------------------------------
FEATURE_COLS = [
    # Pion momentum
    "pi_px", "pi_py", "pi_pz",
    # Proton momentum
    "prot_px", "prot_py", "prot_pz",
    # Pion first B0 tracker hit position
    "pi_first_b0_x", "pi_first_b0_y", "pi_first_b0_z",
    # Proton first Roman-pot hit position
    "prot_first_rp_x", "prot_first_rp_y", "prot_first_rp_z",
]

LABEL_COL = "is_true_lam"


# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------

def load_data(path: str, test_size: float = 0.2, seed: int = 42):
    """Read CSV, select features/label, split into train/test."""
    df = pd.read_csv(path)

    missing = [c for c in FEATURE_COLS + [LABEL_COL] if c not in df.columns]
    if missing:
        sys.exit(f"ERROR: missing columns in CSV: {missing}")

    X = df[FEATURE_COLS].values.astype("float32")
    y = df[LABEL_COL].values.astype("float32")

    n_pos = int(y.sum())
    n_neg = len(y) - n_pos
    print(f"Dataset: {len(y)} rows  |  signal (is_true_lam=1): {n_pos}  |  background: {n_neg}")
    if n_pos == 0:
        sys.exit("ERROR: no positive (is_true_lam=1) samples – cannot train.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed, stratify=y,
    )

    # Per-feature standardisation (fit on train only)
    mean = X_train.mean(axis=0)
    std = X_train.std(axis=0) + 1e-8
    X_train = (X_train - mean) / std
    X_test = (X_test - mean) / std

    return X_train, X_test, y_train, y_test, mean, std


def build_model(n_features: int) -> keras.Model:
    """Simple 2 hidden-layer DNN for binary classification."""
    model = keras.Sequential([
        keras.layers.Input(shape=(n_features,)),
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(32, activation="relu"),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(1, activation="sigmoid"),
    ], name="true_lambda_classifier")
    return model


def plot_history(history, out_dir: str) -> None:
    """Save loss & accuracy curves."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    ax1.plot(history.history["loss"], label="train")
    ax1.plot(history.history["val_loss"], label="val")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Loss")
    ax1.set_title("Binary cross-entropy loss")
    ax1.legend()

    ax2.plot(history.history["binary_accuracy"], label="train")
    ax2.plot(history.history["val_binary_accuracy"], label="val")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Accuracy")
    ax2.set_title("Accuracy")
    ax2.legend()

    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "training_history.png"), dpi=150)
    plt.close(fig)


def plot_roc(y_true, y_score, out_dir: str) -> float:
    """Save ROC curve, return AUC."""
    fpr, tpr, _ = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(fpr, tpr, color="steelblue", lw=2, label=f"AUC = {roc_auc:.3f}")
    ax.plot([0, 1], [0, 1], "k--", lw=1)
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.set_title("ROC – true-Λ classifier")
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "roc_curve.png"), dpi=150)
    plt.close(fig)
    return roc_auc


def plot_confusion(y_true, y_pred, out_dir: str) -> None:
    """Save confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(5, 4))
    ConfusionMatrixDisplay(cm, display_labels=["background", "true Λ"]).plot(ax=ax, cmap="Blues")
    ax.set_title("Confusion matrix (test set)")
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "confusion_matrix.png"), dpi=150)
    plt.close(fig)


# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Train a simple DNN to classify true-Λ combinatoric pairs",
    )
    parser.add_argument("input", help="ppim_combinatorics CSV file")
    parser.add_argument("-o", "--output", default=".", help="Output directory for model & plots")
    parser.add_argument("--epochs", type=int, default=50, help="Training epochs (default: 50)")
    parser.add_argument("--batch-size", type=int, default=256, help="Batch size (default: 256)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    print(f"Keras backend : {keras.backend.backend()}")
    print(f"Keras version : {keras.__version__}")

    # --- Data -----------------------------------------------------------------
    X_train, X_test, y_train, y_test, mean, std = load_data(
        args.input, seed=args.seed,
    )
    print(f"Train samples : {len(y_train)}  |  Test samples : {len(y_test)}")

    # --- Class weights --------------------------------------------------------
    n_pos = float(y_train.sum())
    n_neg = float(len(y_train) - n_pos)
    class_weight = {0: 1.0, 1: n_neg / max(n_pos, 1.0)}
    print(f"Class weight for signal: {class_weight[1]:.2f}")

    # --- Model ----------------------------------------------------------------
    model = build_model(X_train.shape[1])
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss="binary_crossentropy",
        metrics=["binary_accuracy"],
    )
    model.summary()

    # --- Train ----------------------------------------------------------------
    history = model.fit(
        X_train, y_train,
        validation_split=0.15,
        epochs=args.epochs,
        batch_size=args.batch_size,
        class_weight=class_weight,
        verbose=2,
    )

    # --- Evaluate -------------------------------------------------------------
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    y_score = model.predict(X_test, verbose=0).ravel()
    y_pred = (y_score >= 0.5).astype(int)

    roc_auc = plot_roc(y_test, y_score, args.output)
    plot_confusion(y_test, y_pred, args.output)
    plot_history(history, args.output)

    # --- Save model -----------------------------------------------------------
    model_path = os.path.join(args.output, "model.keras")
    model.save(model_path)
    print(f"\nModel saved to {model_path}")

    # --- Summary text ---------------------------------------------------------
    summary_path = os.path.join(args.output, "summary.txt")
    with open(summary_path, "w") as f:
        f.write(f"Keras backend  : {keras.backend.backend()}\n")
        f.write(f"Input CSV      : {args.input}\n")
        f.write(f"Train samples  : {len(y_train)}\n")
        f.write(f"Test samples   : {len(y_test)}\n")
        f.write(f"Epochs         : {args.epochs}\n")
        f.write(f"Batch size     : {args.batch_size}\n\n")
        f.write(f"Features ({len(FEATURE_COLS)}):\n")
        for c in FEATURE_COLS:
            f.write(f"  {c}\n")
        f.write(f"\nTest loss      : {test_loss:.4f}\n")
        f.write(f"Test accuracy  : {test_acc:.4f}\n")
        f.write(f"ROC AUC        : {roc_auc:.4f}\n\n")

        # Capture model.summary() into the file
        lines: list[str] = []
        model.summary(print_fn=lambda x: lines.append(x))
        f.write("Model summary:\n")
        f.write("\n".join(lines))
        f.write("\n")

    print(f"\n{'=' * 50}")
    print(f"Test loss     : {test_loss:.4f}")
    print(f"Test accuracy : {test_acc:.4f}")
    print(f"ROC AUC       : {roc_auc:.4f}")
    print(f"{'=' * 50}")
    print(f"All outputs saved to: {args.output}")


if __name__ == "__main__":
    main()
