# Kaon–Lambda post-analysis

Reconstruction studies of neutral $\Lambda \to n\pi^0 \to n\gamma\gamma$ decays in Sullivan process events at the EIC events and projected constraints on kaon structure function models.

The analysis uses EICrecon ROOT files from ePIC simulation campaigns. Run the following commands from `analysis/kaon-lambda/`.

## 1. Reconstruction analysis

```bash
python run_reconstruction.py \
  --signal /path/to/signal.root \
  --background /path/to/background.root \
  --generator /path/to/generator.root \
  --outdir outputs/reconstruction
```

Produces PNG figures for detector response, $\Lambda$ reconstruction, kinematic distributions, selection efficiency, and background purity.

## 2. Structure-function projections

```bash
python run_projection.py \
  --signal /path/to/signal.root \
  --background /path/to/background.root \
  --generator /path/to/generator.root \
  --beam 18x275 \
  --methods Truth Electron JB \
  --luminosities 1 2.5 10 50 100 \
  --background-mode rate_proxy \
  --plot-models \
  --models DSE JAM \
  --outdir outputs/projections
```

Computes expected event yields and statistical uncertainties, and generates projected kaon structure-function constraints using DSE and JAM models.

The optional `rate_proxy` background treatment is exploratory and does not account for a fully realistic tratment of background versus time effects.

## 3. Regenerate model figures only

```bash
python run_projection.py \
  --plots-only --plot-models \
  --models DSE JAM \
  --beam 18x275 \
  --plot-method Truth \
  --uq-scenario background_rate_proxy \
  --outdir outputs/projections
```

Uses previously generated uncertainty CSV files without reprocessing ROOT events.

## Outputs

```text
outputs/
├── reconstruction/     # Detector, reconstruction and purity figures
└── projections/
    ├── uq_csv/         # Statistical uncertainty tables
    └── models/
        ├── dse/        # DSE projections
        └── jam/        # JAM F₂ projections
```

Figures are saved in PNG format. Only CSV files required for uncertainty projections are retained.

## Configuration

Analysis cuts, binning, beam settings, luminosities, model parameters and LHAPDF configuration are defined in `config.py`.

Use `python run_reconstruction.py --help` or `python run_projection.py --help` for all available options.