#!/usr/bin/env python3
"""
Train a DNN to classify event types from the top-N-particle arrays.

Reads the .npz + .meta.json pair written by prepare_events.py and trains a
plain fully-connected network (a multi-layer perceptron, MLP) to predict the
event class. Works for any number of classes.

The pipeline, step by step
--------------------------
1. SPLIT the events into train / validation / test (default 70/15/15).
     - train:      the network learns from these events (gradients flow).
     - validation: watched during training to detect overfitting and to pick
                   the best epoch; never used for gradient updates.
     - test:       touched exactly once, at the very end, for the honest
                   final numbers you quote.

2. STANDARDIZE the continuous columns: x -> (x - mean) / std, with mean/std
   computed on the TRAINING set only (computing them on all data would leak
   information about the test set - a classic subtle mistake). One-hot PID
   columns and the `present` flags are already 0/1 and are left alone.
   The mean/std are saved inside the checkpoint so inference can reproduce
   the exact same transformation.

3. TRAIN with mini-batch gradient descent:
     - loss:      cross-entropy - the standard classification loss. The model
                  outputs one raw score ("logit") per class; softmax turns
                  them into probabilities; cross-entropy punishes the model
                  when the true class gets low probability.
     - optimizer: AdamW, a robust default (per-parameter adaptive learning
                  rates + correct weight-decay regularization).
     - early stopping: after every epoch we check the validation loss; if it
                  has not improved for `--patience` epochs we stop and keep
                  the weights from the best epoch. This is the main guard
                  against overfitting.

4. EVALUATE on the test set: accuracy, per-class precision/recall, the
   confusion matrix, and (for 2 classes) the ROC AUC.

Outputs (into --out-dir, all names optionally prefixed with --prefix)
---------------------------------------------------------------------
    model.pt                checkpoint: weights + scaler + meta (self-contained)
    report.txt              the same metrics that are printed to the console
    training_curves.png     loss and accuracy vs epoch for train/validation
    confusion_matrix.png    counts + row-normalized (recall) heatmaps
    roc_curve.png           ROC curve(s); one-vs-rest for >2 classes
    score_distribution.png  network output probability, split by true class -
                            THE plot to judge separation quality by eye

Usage
-----
    train_dnn.py data/events_top10.npz
    train_dnn.py data/events_top10.npz --hidden 256 128 64 --epochs 100
    train_dnn.py data/events_msf_vs_dis.npz --prefix msf_vs_dis
"""

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

import matplotlib
matplotlib.use("Agg")  # no display needed - we only save PNGs
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
class EventClassifier(nn.Module):
    """A plain MLP: input vector -> hidden layers -> one logit per class.

    Each hidden block is Linear -> BatchNorm -> ReLU -> Dropout:
      - Linear:    the learnable affine map (weights live here).
      - BatchNorm: re-centers activations per mini-batch; speeds up and
                   stabilizes training of deeper MLPs.
      - ReLU:      the nonlinearity - without it the whole stack would
                   collapse into a single linear map.
      - Dropout:   randomly zeroes a fraction of activations during training
                   so the net cannot rely on any single neuron (regularizer).

    The output layer is a bare Linear producing raw class scores (logits);
    softmax is applied implicitly inside the cross-entropy loss.
    """

    def __init__(self, n_features: int, n_classes: int,
                 hidden=(256, 128, 64), dropout: float = 0.1):
        super().__init__()
        layers = []
        n_in = n_features
        for n_out in hidden:
            layers += [
                nn.Linear(n_in, n_out),
                nn.BatchNorm1d(n_out),
                nn.ReLU(),
                nn.Dropout(dropout),
            ]
            n_in = n_out
        layers.append(nn.Linear(n_in, n_classes))
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)


# ---------------------------------------------------------------------------
# Metrics (numpy - no sklearn dependency, and you can see the math)
# ---------------------------------------------------------------------------
def confusion_matrix(y_true, y_pred, n_classes):
    """cm[i, j] = number of events whose TRUE class is i and PREDICTED class is j."""
    cm = np.zeros((n_classes, n_classes), dtype=np.int64)
    np.add.at(cm, (y_true, y_pred), 1)
    return cm


def roc_curve_points(y_true, score):
    """ROC curve for binary labels: false-positive rate vs true-positive rate
    as the decision threshold slides from "accept everything" to "accept nothing".

    Sort events by score (descending); walking down that list, each positive
    event moves the curve up (one more true positive), each negative event
    moves it right (one more false positive).
    """
    order = np.argsort(-score)
    y_sorted = y_true[order]
    tps = np.cumsum(y_sorted == 1)          # true positives at each threshold
    fps = np.cumsum(y_sorted == 0)          # false positives at each threshold
    tpr = tps / max(tps[-1], 1)
    fpr = fps / max(fps[-1], 1)
    # prepend the (0,0) starting point of the curve
    return np.concatenate([[0.0], fpr]), np.concatenate([[0.0], tpr])


def roc_auc(y_true, score):
    """Area under the ROC curve for binary labels (probability that a random
    positive event gets a higher score than a random negative one).

    Computed via the rank-sum (Mann-Whitney U) identity - no curve needed.
    """
    order = np.argsort(score)
    ranks = np.empty(len(score))
    ranks[order] = np.arange(1, len(score) + 1)
    n_pos = (y_true == 1).sum()
    n_neg = len(y_true) - n_pos
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    return (ranks[y_true == 1].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)


def classification_report(y_true, y_pred, class_names):
    """Human-readable per-class precision / recall / F1 plus confusion matrix."""
    n = len(class_names)
    cm = confusion_matrix(y_true, y_pred, n)
    lines = []
    lines.append(f"{'class':<40} {'precision':>9} {'recall':>9} {'f1':>9} {'events':>9}")
    for i, name in enumerate(class_names):
        tp = cm[i, i]
        precision = tp / cm[:, i].sum() if cm[:, i].sum() else 0.0  # of predicted-i, how many were i
        recall = tp / cm[i, :].sum() if cm[i, :].sum() else 0.0     # of true-i, how many we caught
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        lines.append(f"{name:<40} {precision:9.4f} {recall:9.4f} {f1:9.4f} {cm[i].sum():9d}")
    lines.append("")
    lines.append("Confusion matrix (rows = true class, columns = predicted class):")
    header = " " * 12 + "".join(f"pred {j:<6d}" for j in range(n))
    lines.append(header)
    for i in range(n):
        lines.append(f"  true {i:<4d}" + "".join(f"{cm[i, j]:<11d}" for j in range(n)))
    return "\n".join(lines), cm


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------
def run_epoch(model, loader, loss_fn, device, optimizer=None):
    """One pass over a DataLoader. With an optimizer -> training (gradients);
    without -> evaluation only. Returns (mean loss, accuracy)."""
    training = optimizer is not None
    model.train(training)
    total_loss, total_correct, total_n = 0.0, 0, 0
    # torch.set_grad_enabled saves memory/time when we don't need gradients
    with torch.set_grad_enabled(training):
        for xb, yb in loader:
            xb, yb = xb.to(device, non_blocking=True), yb.to(device, non_blocking=True)
            logits = model(xb)
            loss = loss_fn(logits, yb)
            if training:
                optimizer.zero_grad()
                loss.backward()      # backpropagation: compute gradients
                optimizer.step()     # update the weights
            total_loss += loss.item() * len(yb)
            total_correct += (logits.argmax(dim=1) == yb).sum().item()
            total_n += len(yb)
    return total_loss / total_n, total_correct / total_n


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Train an MLP event-type classifier on a prepare_events.py dataset.")
    parser.add_argument("dataset", help=".npz file from prepare_events.py")
    parser.add_argument("--out-dir", default=None,
                        help="Output directory (default: models/<dataset-stem>/)")
    parser.add_argument("--prefix", default="",
                        help="Prefix for all output file names, e.g. 'msf_vs_dis'")
    parser.add_argument("--hidden", type=int, nargs="+", default=[256, 128, 64],
                        help="Hidden layer sizes (default: 256 128 64)")
    parser.add_argument("--dropout", type=float, default=0.1)
    parser.add_argument("--batch-size", type=int, default=512)
    parser.add_argument("--epochs", type=int, default=100,
                        help="Max epochs; early stopping usually ends sooner")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate")
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--patience", type=int, default=10,
                        help="Early stopping: epochs without val-loss improvement")
    parser.add_argument("--val-frac", type=float, default=0.15)
    parser.add_argument("--test-frac", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    torch.manual_seed(args.seed)
    rng = np.random.default_rng(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}"
          + (f" ({torch.cuda.get_device_name(0)})" if device.type == "cuda" else ""))

    # --- load dataset + metadata --------------------------------------------
    data = np.load(args.dataset)
    X, y = data["X"], data["y"]
    meta = json.loads(Path(str(args.dataset)[: -len(".npz")] + ".meta.json").read_text())
    class_names = meta["class_names"]
    continuous = np.array(meta["continuous"])  # which columns to standardize
    n_classes = len(class_names)
    print(f"Dataset: {X.shape[0]:,} events, {X.shape[1]} features, {n_classes} classes")

    # --- train / validation / test split ------------------------------------
    # The dataset is already shuffled and class-balanced by prepare_events.py,
    # so a simple contiguous split is fine (we re-shuffle anyway for safety).
    perm = rng.permutation(len(X))
    n_test = int(len(X) * args.test_frac)
    n_val = int(len(X) * args.val_frac)
    idx_test, idx_val, idx_train = np.split(perm, [n_test, n_test + n_val])
    print(f"Split: train {len(idx_train):,} / val {len(idx_val):,} / test {len(idx_test):,}")

    # --- standardize continuous columns (stats from TRAIN only!) ------------
    mean = X[idx_train].mean(axis=0)
    std = X[idx_train].std(axis=0)
    std[std == 0] = 1.0            # constant columns: avoid division by zero
    mean[~continuous] = 0.0        # leave flags/one-hots untouched:
    std[~continuous] = 1.0         # (x - 0) / 1 == x
    Xs = (X - mean) / std

    def make_loader(idx, shuffle):
        ds = TensorDataset(torch.from_numpy(Xs[idx]), torch.from_numpy(y[idx]))
        return DataLoader(ds, batch_size=args.batch_size, shuffle=shuffle,
                          num_workers=0, pin_memory=(device.type == "cuda"))

    train_loader = make_loader(idx_train, shuffle=True)
    val_loader = make_loader(idx_val, shuffle=False)
    test_loader = make_loader(idx_test, shuffle=False)

    # --- model / loss / optimizer -------------------------------------------
    model = EventClassifier(X.shape[1], n_classes,
                            hidden=tuple(args.hidden), dropout=args.dropout).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"Model: MLP {X.shape[1]} -> {' -> '.join(map(str, args.hidden))} -> {n_classes}"
          f"   ({n_params:,} parameters)\n")
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr,
                                  weight_decay=args.weight_decay)

    # --- training loop with early stopping ----------------------------------
    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}
    best_val_loss = float("inf")
    best_state = None
    best_epoch = 0
    t0 = time.time()

    for epoch in range(1, args.epochs + 1):
        train_loss, train_acc = run_epoch(model, train_loader, loss_fn, device, optimizer)
        val_loss, val_acc = run_epoch(model, val_loader, loss_fn, device)

        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)

        marker = ""
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_epoch = epoch
            # keep a CPU copy of the best weights (small model - cheap)
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
            marker = "  <- best"
        print(f"epoch {epoch:3d}  train loss {train_loss:.4f} acc {train_acc:.4f}"
              f"  |  val loss {val_loss:.4f} acc {val_acc:.4f}{marker}")

        if epoch - best_epoch >= args.patience:
            print(f"\nEarly stopping: no val-loss improvement for {args.patience} epochs "
                  f"(best was epoch {best_epoch}).")
            break

    print(f"Training time: {time.time() - t0:.1f}s")
    model.load_state_dict(best_state)  # roll back to the best epoch

    # --- final evaluation on the held-out test set ---------------------------
    test_loss, test_acc = run_epoch(model, test_loader, loss_fn, device)

    model.eval()
    with torch.no_grad():
        logits = torch.cat([model(xb.to(device)).cpu() for xb, _ in test_loader])
    y_pred = logits.argmax(dim=1).numpy()
    y_true = y[idx_test]

    report_txt, cm = classification_report(y_true, y_pred, class_names)
    lines = [
        f"Best epoch: {best_epoch}   (val loss {best_val_loss:.4f})",
        f"TEST  loss {test_loss:.4f}   accuracy {test_acc:.4f}",
        "",
        report_txt,
    ]
    # Softmax turns the raw logits into per-class probabilities - these drive
    # the ROC curve and the score-distribution plot below.
    probs = torch.softmax(logits, dim=1).numpy()
    if n_classes == 2:
        lines.append(f"\nROC AUC (class 1 vs class 0): {roc_auc(y_true, probs[:, 1]):.4f}")
    report = "\n".join(lines)
    print("\n" + report)

    # --- save everything ------------------------------------------------------
    out_dir = Path(args.out_dir) if args.out_dir else \
        Path(__file__).resolve().parent.parent / "models" / Path(args.dataset).stem
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = f"{args.prefix}_" if args.prefix else ""

    def out(name):
        return out_dir / f"{prefix}{name}"

    # A self-contained checkpoint: everything needed to rebuild the model and
    # apply the identical preprocessing at inference time.
    torch.save({
        "model_state": model.state_dict(),
        "hidden": args.hidden,
        "dropout": args.dropout,
        "n_features": X.shape[1],
        "scaler_mean": mean,
        "scaler_std": std,
        "meta": meta,
    }, out("model.pt"))

    out("report.txt").write_text(report + "\n")

    saved = [out("model.pt"), out("report.txt")]

    # --- plot 1: training curves ---------------------------------------------
    # The train/val gap is your overfitting diagnostic - if train keeps
    # improving while val flattens or worsens, the model is memorizing
    # instead of generalizing.
    epochs_axis = np.arange(1, len(history["train_loss"]) + 1)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    ax1.plot(epochs_axis, history["train_loss"], label="train")
    ax1.plot(epochs_axis, history["val_loss"], label="validation")
    ax1.axvline(best_epoch, ls="--", c="gray", label=f"best epoch ({best_epoch})")
    ax1.set_xlabel("epoch"); ax1.set_ylabel("cross-entropy loss"); ax1.legend()
    ax2.plot(epochs_axis, history["train_acc"], label="train")
    ax2.plot(epochs_axis, history["val_acc"], label="validation")
    ax2.axvline(best_epoch, ls="--", c="gray")
    ax2.set_xlabel("epoch"); ax2.set_ylabel("accuracy"); ax2.legend()
    fig.tight_layout()
    fig.savefig(out("training_curves.png"), dpi=120)
    saved.append(out("training_curves.png"))

    # --- plot 2: confusion matrix --------------------------------------------
    # Left: raw event counts. Right: each row normalized to 1, i.e. "of all TRUE
    # class-i events, what fraction landed in each predicted class" - the
    # diagonal of the right panel is the per-class recall (efficiency).
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
                # readable text on both light and dark cells
                color = "white" if mat[i, j] > mat.max() / 2 else "black"
                ax.text(j, i, format(mat[i, j], fmt), ha="center", va="center",
                        color=color)
    fig.tight_layout()
    fig.savefig(out("confusion_matrix.png"), dpi=120)
    saved.append(out("confusion_matrix.png"))

    # --- plot 3: ROC curve(s) --------------------------------------------------
    # Binary: single curve for "is it class 1". Multi-class: one-vs-rest
    # curve per class. The diagonal is a random classifier (AUC 0.5).
    fig, ax = plt.subplots(figsize=(6, 5.5))
    if n_classes == 2:
        fpr, tpr = roc_curve_points(y_true, probs[:, 1])
        ax.plot(fpr, tpr, label=f"AUC = {roc_auc(y_true, probs[:, 1]):.4f}")
    else:
        for i, name in enumerate(class_names):
            y_bin = (y_true == i).astype(int)
            fpr, tpr = roc_curve_points(y_bin, probs[:, i])
            ax.plot(fpr, tpr, label=f"{name} vs rest (AUC {roc_auc(y_bin, probs[:, i]):.4f})")
    ax.plot([0, 1], [0, 1], "k--", lw=1, label="random guess")
    ax.set_xlabel("false positive rate"); ax.set_ylabel("true positive rate")
    ax.set_title("ROC curve (test set)")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(out("roc_curve.png"), dpi=120)
    saved.append(out("roc_curve.png"))

    # --- plot 4: score distribution -------------------------------------------
    # For each true class, histogram the network's output probability.
    # Well-separated humps at 0 and 1 = confident classifier; overlap in the
    # middle = the physics the two classes share. Log-y so tails are visible.
    fig, ax = plt.subplots(figsize=(7, 5))
    if n_classes == 2:
        bins = np.linspace(0, 1, 51)
        for i, name in enumerate(class_names):
            ax.hist(probs[y_true == i, 1], bins=bins, histtype="step", lw=1.5,
                    label=f"true {name}")
        ax.set_xlabel(f"network output: P({class_names[1]})")
    else:
        bins = np.linspace(0, 1, 51)
        for i, name in enumerate(class_names):
            ax.hist(probs[y_true == i, i], bins=bins, histtype="step", lw=1.5,
                    label=f"P(own class) for true {name}")
        ax.set_xlabel("network output probability of the true class")
    ax.set_yscale("log")
    ax.set_ylabel("events")
    ax.set_title("Classifier score distribution (test set)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out("score_distribution.png"), dpi=120)
    saved.append(out("score_distribution.png"))

    print()
    for path in saved:
        print(f"Saved: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
