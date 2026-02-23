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
# Root directory
/volatile/eic/romanov/meson-structure-2026-02/

# Event generator root files
/volatile/eic/romanov/meson-structure-2026-02/eg-orig-kaon-lambda

# Event generator files in HepMC (split to 5000k events)
/volatile/eic/romanov/meson-structure-2025-08/eg-hepmc
```

Commands log

```bash
# cd where scripts are
cd /home/romanov/meson-structure-work/meson-structure

# run using uv
uv sync

# make campaign config and make it "main" config.yaml

# Create npsim jobs
uv run full-sim-pipeline/20_create_npsim_jobs.py --config full-sim-pipeline/config-campaign-2026-02.yaml 


```
