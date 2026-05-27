# Campaign 2026-05

This page documents the 2026-05 meson structure simulation campaign.

> (!) For the list of files go to [DATA PAGE](../data.md)


## Overview

This is the first full production campaign that incorporates the fixes from the
2026-04 investigation into the Lambda MCParticle / tracking-volume bugs:

- [eic/epic#1069](https://github.com/eic/epic/issues/1069) — MCParticle endpoints / daughter tree for Lambdas
- [eic/epic#1081](https://github.com/eic/epic/pull/1081) — Tracking-volume G4 handler dropping Lambda decay info

Two DD4hep flavors are produced in parallel:

- `dd4hep` — fixed/updated tracking volume (default, used for reconstruction-based analyses)
- `dd4hep_saveall` — keeps **all** MCParticles (no tracking volume filter); used as the basis for **acceptance / MC-truth performance** studies and as the input to EICrecon in this campaign.

> (!) All acceptance studies must use `dd4hep_saveall` data. See campaign 2026-04
> for the rationale.

Energy ranges:

1. 5x41 GeV
2. 10x100 GeV
3. 10x130 GeV
4. 18x275 GeV

DIS parameters:

- `x = 0.0001 - 1.0000`
- `q2 = 1 - 500`

Statistics:

- 5000 events per job
- priority queues: first 1'000'000 events (200 files) per energy range


## Software stack

Built and run with a custom singularity image based on the EIC `eic_xl` stack:

```
/work/eic3/users/romanov/meson-structure-work/eicdev-eic-full-2026-04-25.sif
```

Pinned for reference (used while bootstrapping the campaign):

```
/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:26.03.1-stable
```


## Data layout (ifarm)

Base directory:

```bash
/work/eic3/users/romanov/meson-structure-2026-05
```

Subdirectories:

- `afterburner`         — event generator output with crossing-angle + beam effects applied
- `dd4hep`              — DD4hep full simulation, **fixed tracking volume** (`edm4hep.root`)
- `dd4hep_saveall`      — DD4hep full simulation, **all MCParticles saved** (`edm4hep.root`)
- `reco`                — EICrecon reconstruction of `dd4hep_saveall` (`edm4eic.root`)
- `csv_dd4hep`          — CSV tables from `dd4hep` (acceptance / MC truth, fixed volume)
- `csv_dd4hep_saveall`  — CSV tables from `dd4hep_saveall` (acceptance / MC truth, all particles)
- `csv_reco`            — CSV tables from `reco`


## Pipeline config

The campaign is driven by
[`full-sim-pipeline/config-campaign-26-05.yaml`](https://github.com/JeffersonLab/meson-structure/blob/main/full-sim-pipeline/config-campaign-26-05.yaml):

```yaml
base_dir: "/work/eic3/users/romanov/meson-structure-2026-05"
container: "/work/eic3/users/romanov/meson-structure-work/eicdev-eic-full-2026-04-25.sif"
energies: ["5x41", "10x100", "10x130", "18x275"]
event_count: 5000

# DD4hep, fixed tracking volume
dd4hep_input:  "${base_dir}/afterburner/${energy}-priority"
dd4hep_output: "${base_dir}/dd4hep/${energy}"

# DD4hep, all MCParticles saved (acceptance studies + reco input)
dd4hep_saveall_input:  "${base_dir}/afterburner/${energy}-priority"
dd4hep_saveall_output: "${base_dir}/dd4hep_saveall/${energy}"

# CSV tables
csv_dd4hep_input:          "${dd4hep_output}"
csv_dd4hep_output:         "${base_dir}/csv_dd4hep/${energy}"
csv_dd4hep_saveall_input:  "${dd4hep_saveall_output}"
csv_dd4hep_saveall_output: "${base_dir}/csv_dd4hep_saveall/${energy}"

# Reconstruction runs on the saveall flavor
eicrecon_input:     "${dd4hep_saveall_output}"
eicrecon_output:    "${base_dir}/reco/${energy}"
csv_eicrecon_input:  "${eicrecon_output}"
csv_eicrecon_output: "${base_dir}/csv_reco/${energy}"
```


## Commands log

```bash
mkdir -p /work/eic3/users/romanov/meson-structure-2026-05

# cd where scripts are
cd /home/romanov/meson-structure-work/meson-structure

# sync python env
uv sync

# DD4hep (fixed tracking volume) jobs
uv run full-sim-pipeline/20_create_npsim_jobs.py \
    --config full-sim-pipeline/config-campaign-26-05.yaml

# DD4hep saveall jobs (input for EICrecon and for acceptance studies)
uv run full-sim-pipeline/21_create_npsim_saveall_jobs.py \
    --config full-sim-pipeline/config-campaign-26-05.yaml

# EICrecon jobs (run on dd4hep_saveall output)
uv run full-sim-pipeline/30_create_eicrecon_jobs.py \
    --config full-sim-pipeline/config-campaign-26-05.yaml

# CSV converters
uv run full-sim-pipeline/40_create_csv_dd4hep_jobs.py \
    --config full-sim-pipeline/config-campaign-26-05.yaml
uv run full-sim-pipeline/41_create_csv_dd4hep_saveall_jobs.py \
    --config full-sim-pipeline/config-campaign-26-05.yaml
uv run full-sim-pipeline/42_create_csv_eicrecon_jobs.py \
    --config full-sim-pipeline/config-campaign-26-05.yaml
```
