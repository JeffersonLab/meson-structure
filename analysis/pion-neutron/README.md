# Pion–neutron post-analysis

Reconstruction studies of forward neutrons in Sullivan process events at the EIC and projected constraints on pion structure function models.

The analysis uses EICrecon ROOT files from ePIC simulation campaigns. Run the following commands from `analysis/pion-neutron/`.

## 1. Reconstruction analysis

```bash
python run_reconstruction.py \
  --signal /path/to/signal_assoMC.root \
  --background /path/to/background_assoMC.root \
  --outdir outputs/reconstruction
```

Produces PNG figures for detector response, neutron reconstruction, kinematic distributions, selection efficiency, and background purity.

The `--background` argument is optional. MC-associated ROOT files (`_assoMC.root`) are recommended for particle-origin studies.

## 2. Structure-function projections

```bash
python run_projection.py \
  --signal /path/to/signal_assoMC.root \
  --background /path/to/background_assoMC.root \
  --generator /path/to/generator.root \
  --beam 9x275 \
  --methods Truth Electron JB \
  --luminosities 1 2.5 10 50 100 \
  --background-mode rate_proxy \
  --plot-models \
  --models DSE JAM \
  --outdir outputs/projections
```

Computes expected event yields and statistical uncertainties, and generates projected pion structure-function constraints using DSE and JAM models.

The optional `rate_proxy` background treatment is exploratory and does not account for all background normalization or timing effects.

## 3. Regenerate model figures only

```bash
python run_projection.py \
  --plots-only --plot-models \
  --models DSE JAM \
  --beam 9x275 \
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