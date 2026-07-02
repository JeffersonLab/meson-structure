# Campaign 2026-07

This page documents the 2026-07 meson structure simulation campaign.

> (!) For the list of files go to [DATA PAGE](../data.md)


## Overview

The July 2026 campaign introduces the **new `9xN` energy scheme** in compliance
with the EIC early-science program (the proton beam moves from 10/18 GeV to a
single 9 GeV electron beam against 100/130/275 GeV protons, plus the low-energy
`5x41`). It is a **single-flavor production** run: one afterburned signal →
DD4hep → EICrecon, with CSV tables produced from both the DD4hep and reco
outputs.

Energy ranges:

1. 5x41 GeV
2. 9x100 GeV
3. 9x130 GeV
4. 9x275 GeV

DIS parameters (from the event-generator inputs):

- `x = 0.0001 - 1.0000`
- `q2 = 1 - 500`

Statistics:

- **1000 events per file** (note: smaller per-file statistics than the
  5000-evt/file 2025/2026 campaigns), file index `NNNN`, ~1000 files per energy.

> (!) Unlike campaign [2026-06](../campaign-2026-06/campaign-2026-06.md), this
> campaign has **no** `-official` / `-saveall` / `-background` / `-stv` variant
> split — reconstruction is run directly on the single `dd4hep` output. For
> machine-background-mixed data see campaign 2026-06 and the
> [Data](../data.md#machine-background-2026-06) page.


## Software stack

Built and run with the official EIC image from cvmfs:

```
/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:26.06-stable
```


## Data layout (ifarm)

Base directory:

```bash
/work/eic3/users/romanov/meson-structure-2026-07
```

Subdirectories:

- `eg-original-2026-06`  — original event-generator ROOT files (one per energy, `k_lambda_crossing_*.root`, ~19 GB)
- `eg-split`             — event-generator files split into 1000-event chunks (~20 GB)
- `eg-hepmc`             — split files converted to HepMC (`<energy>`, `<energy>-priority`, `<energy>-rest`; ~2.3 GB)
- `afterburner`          — event-generator output with crossing-angle + beam effects (`<energy>-priority`, `*.hepmc3.tree.root` + `*.hist.root`; ~6.5 GB)
- `dd4hep`               — DD4hep full simulation (`*.edm4hep.root`; ~5.0 TB)
- `reco`                 — EICrecon reconstruction of `dd4hep` (`*.edm4eic.root`; ~2.2 TB)
- `csv_dd4hep`           — acceptance / MC-truth CSV tables from `dd4hep` (~21 GB)
- `csv_reco`             — reconstruction CSV tables from `reco` (~1.2 GB)
- `analysis`             — analysis outputs (acceptance, eg-kinematics, gary_scripts, multicalo-lambda, …)

Per-energy `.root` file counts and sizes (from the ifarm disk):

| Energy  | `dd4hep/` (`.edm4hep.root`) | `reco/` (`.edm4eic.root`) |
| ------- | -------------------------: | ------------------------: |
| 5x41    | 998 files &nbsp; (647 GB)  | 998 files &nbsp; (472 GB) |
| 9x100   | 1000 files (1.4 TB)        | 999 files &nbsp; (718 GB) |
| 9x130   | 1000 files (1.7 TB)        | 1000 files (421 GB)       |
| 9x275   | 1000 files (1.4 TB)        | 1000 files (630 GB)       |


## Pipeline config

The campaign is driven by
[`full-sim-pipeline/config-campaign-26-07.yaml`](https://github.com/JeffersonLab/meson-structure/blob/main/full-sim-pipeline/config-campaign-26-07.yaml):

```yaml
base_dir: "/work/eic3/users/romanov/meson-structure-2026-07"
container: "/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:26.06-stable/"
energies: ["5x41", "9x100", "9x130", "9x275"]
event_count: 1000

afterburner_input:  "${base_dir}/eg-hepmc/${energy}-priority"
afterburner_output: "${base_dir}/afterburner/${energy}-priority"

# DD4hep (afterburner output is the input)
dd4hep_input:  "${base_dir}/afterburner/${energy}-priority"
dd4hep_output: "${base_dir}/dd4hep/${energy}"

# CSV tables from DD4hep
csv_dd4hep_input:  "${dd4hep_output}"
csv_dd4hep_output: "${base_dir}/csv_dd4hep/${energy}"

# Reconstruction runs on the dd4hep output
eicrecon_input:  "${dd4hep_output}"
eicrecon_output: "${base_dir}/reco/${energy}"
csv_eicrecon_input:  "${eicrecon_output}"
csv_eicrecon_output: "${base_dir}/csv_reco/${energy}"
```


## Commands log

### Event-generator split (ROOT → HepMC, 1000 events/file)

```bash
# EG originals (one file per energy)
/work/eic3/users/romanov/meson-structure-2026-07/eg-original-2026-06/k_lambda_crossing_0.000-5.0on41.0_x0.0001-1.0000_q1.0-500.0.root
/work/eic3/users/romanov/meson-structure-2026-07/eg-original-2026-06/k_lambda_crossing_0.000-9.0on100.0_x0.0001-1.0000_q1.0-500.0.root
/work/eic3/users/romanov/meson-structure-2026-07/eg-original-2026-06/k_lambda_crossing_0.000-9.0on130.0_x0.0001-1.0000_q1.0-500.0.root
/work/eic3/users/romanov/meson-structure-2026-07/eg-original-2026-06/k_lambda_crossing_0.000-9.0on275.0_x0.0001-1.0000_q1.0-500.0.root

# split each into 1000-event chunks (repeat per energy)
uv run 01_root_hepmc_klam_convert.py \
      --input-files .../eg-original-2026-06/k_lambda_crossing_0.000-9.0on275.0_x0.0001-1.0000_q1.0-500.0.root \
      --chunk-size 1000 \
      --events 10000000 \
      --output-prefix .../eg-split/9x275/msf_ev1000 \
      --events-per-file 1000
```

### Full simulation pipeline

```bash
mkdir -p /work/eic3/users/romanov/meson-structure-2026-07

# cd where scripts are
cd /home/romanov/meson-structure-work/meson-structure

# sync python env
uv sync

# afterburner (crossing angle + beam effects)
uv run full-sim-pipeline/10_create_afterburner_jobs.py \
    --config full-sim-pipeline/config-campaign-26-07.yaml

# DD4hep full simulation
uv run full-sim-pipeline/20_create_npsim_jobs.py \
    --config full-sim-pipeline/config-campaign-26-07.yaml

# EICrecon reconstruction (runs on dd4hep output)
uv run full-sim-pipeline/30_create_eicrecon_jobs.py \
    --config full-sim-pipeline/config-campaign-26-07.yaml

# CSV converters (from dd4hep and from reco)
uv run full-sim-pipeline/40_create_csv_dd4hep_jobs.py \
    --config full-sim-pipeline/config-campaign-26-07.yaml
uv run full-sim-pipeline/42_create_csv_eicrecon_jobs.py \
    --config full-sim-pipeline/config-campaign-26-07.yaml
```

Each `XX_create_*_jobs.py` writes per-file container + SLURM scripts under
`<output>/jobs/` plus a top-level `submit_all_slurm_jobs.sh` / `run_all_local.sh`.
