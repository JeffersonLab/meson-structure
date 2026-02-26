# Campaign 2026-02

This page documents the 2026-02 meson structure simulation campaign.

> (!) For the list of files go to [DATA PAGE](../data.md) 


### Overview

This campaign:

- Includes 2026-02 EIC EPIC software stack


Energy ranges:

1. 5x41 GeV
2. 10x100 GeV
2. 10x130 GeV
3. 18x275 GeV

DIS parameters:

- `x= 0.0001 - 1.0000`
- `q2=1 - 500`

```bash
# Event generator root files (previous campaign)
/work/eic3/users/romanov/meson-structure-2026-02/eg-orig-kaon-lambda

# Event generator files in HepMC (split to 5000k events)
/work/eic3/users/romanov/meson-structure-2026-02/eg-hepmc
```

## Commands log

```bash

mkdir /work/eic3/users/romanov/meson-structure-2026-03
mkdir /volatile/eic/romanov/meson-structure-2026-03

# cd where scripts are
cd /home/romanov/meson-structure-work/meson-structure


# run using uv
uv sync

# make campaign config and make it "main" config.yaml

# Create npsim jobs
uv run full-sim-pipeline/20_create_npsim_jobs.py --config full-sim-pipeline/config-campaign-2026-03.yaml 

# After... Create eicrecon jobs
uv run full-sim-pipeline/30_create_eicrecon_jobs.py --config full-sim-pipeline/config-campaign-2026-03.yaml

# After now we have csv_dd4hep and csv_eicrecon different jobs
uv run full-sim-pipeline/40_create_csv_dd4hep_jobs.py --config full-sim-pipeline/config-campaign-2026-03.yaml
uv run full-sim-pipeline/41_create_csv_eicrecon_jobs.py --config full-sim-pipeline/config-campaign-2026-03.yaml

# Build custom singularity image with multicalo branch
cd /work/eic/users/romanov/meson-structure-work/
singularity build --fakeroot eicrecon_ff_multicalo.sif meson-structure/containers/eicrecon_custom.def
```
