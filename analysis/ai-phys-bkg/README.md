# ai-phys-bkg — DNN event-type discrimination

Experiment: can a neural network tell apart DIS event types (different Q²
ranges, later signal vs background) looking only at the reconstructed
particles of the event?

## Pipeline overview

```
per-run CSVs (csv_convert/reco_particles.cxx, one row = one particle)
        │
        │  scripts/merge_reco_particles_to_feather.py
        ▼
data/<dataset>.feather          one row = one particle, unique event IDs
        │
        │  scripts/prepare_events.py
        ▼
data/events_top10.npz           one row = one EVENT: flattened top-10 particles
data/events_top10.meta.json     + labels y (0, 1, ... one per input dataset)
        │
        │  scripts/train_dnn.py
        ▼
models/events_top10/model.pt    trained classifier + preprocessing constants
models/events_top10/report.txt  accuracy, per-class metrics, confusion matrix
models/events_top10/training_curves.png
        │
        │  scripts/infer.py  (apply a trained model to any dataset)
        ▼
<out>/predictions.csv           per-event predicted class + probabilities
<out>/summary.txt + plots       predicted fractions, scores, (confusion/ROC if labeled)
```

## Step 1 — merge run CSVs into feather

Each dataset in `/data/dis_csv_2026_06/` is ~100 zipped CSVs (one per run).
Event numbers restart at 0 in each run, so the merge offsets them to be
globally unique and adds a `run` column for traceability:

```bash
python scripts/merge_reco_particles_to_feather.py \
    "/data/dis_csv_2026_06/dis_nc_ep_9x130_q2_1to10/*.csv.zip" \
    -o data/dis_nc_ep_9x130_q2_1to10.feather --glob
```

## Step 2 — build the per-event ML dataset

`prepare_events.py` turns the particle table into fixed-length event vectors:

- take the **top-10 particles by momentum |p|** (descending; `--top-n` to change),
- per particle, 22 features: a `present` padding flag, kinematics
  (p, px, py, pz, energy, mass, charge), a one-hot particle-type category
  derived from the PDG code (9 categories), and 5 detector multiplicities
  (clusters, tracks, calorimeter hits, track measurements, tracker hits),
- events with fewer than 10 particles are zero-padded (`present`=0 marks padding),
- one event-level feature appended: total reconstructed multiplicity `n_reco`,
- **class balancing**: every class is downsampled to the smallest class,
  so the network cannot win by always guessing the majority class,
- classes are concatenated and shuffled with a fixed seed → reproducible.

```bash
python scripts/prepare_events.py \
    data/dis_nc_ep_9x130_q2_1to10.feather \
    data/dis_nc_ep_9x130_q2_100to1000.feather \
    -o data/events_top10.npz --top-n 10
```

The **order of the input files defines the labels**: first file → class 0,
second → class 1, etc. Adding a third event type is just adding a third
feather to the command line — everything downstream is N-class already.

Several feathers can be combined into ONE class (comma-joined, optional
`name=` for the class name), e.g. both DIS Q² samples as a single "dis" class
against the meson-structure sample:

```bash
python scripts/prepare_events.py \
    "dis_nc_combined=data/dis_nc_ep_9x130_q2_1to10.feather,data/dis_nc_ep_9x130_q2_100to1000.feather" \
    "msf=data/msf_2026-07_reco_9x130.feather" \
    -o data/events_msf_vs_dis_top10.npz --top-n 10
```

> Why one-hot the PDG code? A PDG code is a *categorical* value disguised as
> a number: "211 < 2212" carries no meaning, and a network fed raw codes would
> try to exploit that fake ordering. One-hot encoding gives each particle type
> its own independent input.

## Step 3 — train the DNN

`train_dnn.py` trains a plain fully-connected network (MLP):

```
input 221 → [Linear 256 → BatchNorm → ReLU → Dropout]
          → [Linear 128 → BatchNorm → ReLU → Dropout]
          → [Linear  64 → BatchNorm → ReLU → Dropout]
          → Linear n_classes (raw scores / "logits")
```

Key choices, and why (all overridable via CLI flags):

| What | Choice | Why |
|---|---|---|
| split | 70 / 15 / 15 train/val/test | val steers training, test is touched once at the end |
| scaling | standardize continuous cols, stats from **train only** | using all data would leak test-set info |
| loss | cross-entropy | the standard multi-class classification loss |
| optimizer | AdamW, lr 1e-3, weight decay 1e-4 | robust default; decay regularizes |
| regularization | dropout 0.1 + BatchNorm + early stopping | guards against overfitting |
| early stopping | stop after 10 epochs without val-loss improvement, keep best epoch | the main anti-overfitting mechanism |

```bash
python scripts/train_dnn.py data/events_top10.npz
# variations:
python scripts/train_dnn.py data/events_top10.npz --hidden 512 256 128 --dropout 0.2
# prefix all output files (plots, report, model):
python scripts/train_dnn.py data/events_msf_vs_dis_top10.npz --prefix msf_vs_dis
```

Outputs land in `models/<dataset-stem>/` (file names prefixed with
`--prefix` if given). The checkpoint `model.pt` is self-contained: weights
**and** the standardization mean/std **and** the feature metadata, so
inference can exactly reproduce the preprocessing.

Saved plots and how to read them:

- `training_curves.png` — loss/accuracy vs epoch. If the *train* curve keeps
  improving while *validation* flattens or gets worse, the network is
  memorizing the training events instead of learning physics — that's
  overfitting. The dashed line marks the epoch whose weights were kept.
- `confusion_matrix.png` — counts and row-normalized; the diagonal of the
  normalized panel is the per-class recall (efficiency).
- `roc_curve.png` — background rejection vs signal efficiency across all
  score thresholds; one-vs-rest curves when there are >2 classes.
- `score_distribution.png` — the network output probability, histogrammed
  separately per true class (log-y). Clean humps at 0 and 1 = confident
  classifier; whatever piles up in the middle is what the classes genuinely
  share.

## Step 4 — infer on a dataset

`infer.py` applies an already-trained checkpoint to a dataset and writes/plots
the predictions. It accepts either input type:

- a **raw `*.feather`** (a new sample) — flattened with the same top_n stored
  in the checkpoint, then scored (prediction only), or
- a **prepared `*.npz`** — if it carries truth labels `y`, the script also
  evaluates the model (accuracy, confusion matrix, ROC).

The checkpoint is self-contained (weights + standardization mean/std + top_n +
class names), so no training settings need to be repeated.

```bash
# Predict on a raw feather
python scripts/infer.py \
    models/events_msf_vs_dis_top10/msf_vs_dis_model.pt \
    data/msf_2026-07_reco_9x130.feather \
    -o out/msf_infer --prefix msf_infer

# Evaluate on a labeled prepared dataset
python scripts/infer.py models/events_top10/model.pt data/events_top10.npz
```

Outputs: `predictions.csv` (per event: predicted class + probability of every
class, plus true class when labels exist), `summary.txt`, and plots
(`predicted_fractions.png`, `score_distribution.png`, and
`confusion_matrix.png` + `roc_curve.png` when labels are present).

## Physics caveat

The scattered electron is kept among the particles (deliberate v1 choice).
Its kinematics alone essentially fix Q², so discriminating q2_1to10 vs
q2_100to1000 is expected to be *easy* — treat the first result as a pipeline
shakedown, not a physics achievement. The interesting follow-up is dropping
the scattered electron and asking whether the *hadronic final state alone*
carries the Q² information.
