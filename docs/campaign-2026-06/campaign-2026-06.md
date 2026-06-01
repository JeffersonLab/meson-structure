# Campaign 2026-06

This page documents the 2026-06 meson structure simulation campaign.

> (!) For the list of files go to [DATA PAGE](../data.md)


## Overview

The June 2026 campaign runs the **same afterburned signal** through **four
parallel DD4hep simulation variants**. They differ only in the npsim step (and,
for `-stv`, in the container / npsim build), which makes them directly
comparable:

| Variant        | npsim particle handler                              | Container                          | Output subdir       | Creator script                          |
| -------------- | --------------------------------------------------- | ---------------------------------- | ------------------- | --------------------------------------- |
| `-official`    | `Geant4TVUserParticleHandler` (default tracking volume) | cvmfs `eic_xl:nightly`         | `dd4hep-official/`  | `20_create_npsim_jobs.py`               |
| `-saveall`     | `""` (handler disabled → keep all MCParticles)      | cvmfs `eic_xl:nightly`             | `dd4hep-saveall/`   | `21_create_npsim_saveall_jobs.py`       |
| `-background`  | `""` + status-offset flags (background-mixed)       | cvmfs `eic_xl:nightly`             | `dd4hep-background/`| `11_…` + `22_create_npsim_background_jobs.py` |
| `-stv`         | `Geant4TVEicParticleHandler` (smart tracking volume)| `eicdev/eic-full:latest` (`.sif`)  | `dd4hep-stv/`       | `23_create_npsim_stv_jobs.py`           |

Energy ranges (all variants):

1. 5x41 GeV
2. 10x100 GeV
3. 10x130 GeV
4. 18x275 GeV

Statistics: 5000 events per job.

> (!) The `-background` variant skips 5x41 (no official 5x41 cocktail is
> published); see the cocktail table below.


## Variants in detail

### `-official` — production baseline

Standard npsim with the default EIC tracking-volume handler:

```bash
npsim --part.userParticleHandler="Geant4TVUserParticleHandler" ... --runType run
```

Run from the **existing official EIC container** (`eic_xl:nightly`). This is the
reference the other three variants are compared against.

### `-saveall` — keep all MCParticles

The EIC custom particle handler is disabled so that **every** MCParticle is kept
regardless of the tracking volume:

```bash
npsim --part.userParticleHandler="" ... --runType run
```

This is the flavor used for acceptance / MC-truth performance studies and as the
input to EICrecon (same as campaign
[2026-05](../campaign-2026-05/campaign-2026-05.md)).

### `-background` — background-mixed

The afterburned signal is mixed with the official ePIC background cocktails
(`synrad`, `ebrems`, `ecoulomb`, `etouschek`, optionally proton beam-gas) using
`SignalBackgroundMerger` into 2 µs timeframes (one signal per frame), then npsim
is run on the merged `hepmc3.tree.root` with the status-offset flags:

```bash
npsim --part.userParticleHandler="" --runType batch --hepmc3.useHepMC3 true \
      --physics.alternativeStableStatuses "1 2001 3001 4001 5001" \
      --physics.alternativeDecayStatuses  "2 2002 3002 4002 5002" ...
```

The status lists are derived automatically from the per-energy cocktail JSON.
See **[Backgrounds in ePIC simulation](../background.md)** for the full picture
(status offsets, merger command, why the flags matter).

### `-stv` — smart tracking volume

New npsim handler `Geant4TVEicParticleHandler` from the custom
`smart-tracking-volume` branch:

```bash
npsim --part.userParticleHandler=Geant4TVEicParticleHandler ... --runType run
```

This handler only exists in the **`eicdev/eic-full:latest`** image, so this is
the only variant that does not use the stock cvmfs `eic_xl` build. It is the
follow-up to the tracking-volume investigation from campaign
[2026-04](../campaign-2026-04/tracking-volume.md).


## Software stack

Non-STV variants use the official EIC image from cvmfs:

```
/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:nightly
```

The `-stv` variant uses a singularity image built from
`eicdev/eic-full:latest` (custom `smart-tracking-volume` npsim branch):

```
# TODO: replace with the actual .sif path
/work/eic3/users/romanov/meson-structure-work/eic-full-stv.sif
```


## Data layout (ifarm)

Base directory (shared by all four variants):

```bash
/work/eic3/users/romanov/meson-structure-2026-06
```

Subdirectories:

- `afterburner`          — **shared** event-generator output with crossing-angle + beam effects (input to all variants)
- `dd4hep-official`      — DD4hep, default tracking volume (`edm4hep.root`)
- `dd4hep-saveall`       — DD4hep, all MCParticles saved (`edm4hep.root`)
- `bg_merged`            — `SignalBackgroundMerger` output (`*.bg.hepmc3.tree.root`)
- `dd4hep-background`    — DD4hep on the background-merged input (`edm4hep.root`)
- `dd4hep-stv`           — DD4hep, smart tracking volume (`edm4hep.root`)
- `csv_dd4hep-*`         — CSV tables per variant
- `reco-saveall`, `reco-background` — EICrecon reconstruction (`edm4eic.root`)


## Pipeline configs

One config per variant, all in
[`full-sim-pipeline/`](https://github.com/JeffersonLab/meson-structure/tree/main/full-sim-pipeline):

- [`config-campaign-26-06-official.yaml`](https://github.com/JeffersonLab/meson-structure/blob/main/full-sim-pipeline/config-campaign-26-06-official.yaml)
- [`config-campaign-26-06-saveall.yaml`](https://github.com/JeffersonLab/meson-structure/blob/main/full-sim-pipeline/config-campaign-26-06-saveall.yaml)
- [`config-campaign-26-06-background.yaml`](https://github.com/JeffersonLab/meson-structure/blob/main/full-sim-pipeline/config-campaign-26-06-background.yaml)
- [`config-campaign-26-06-stv.yaml`](https://github.com/JeffersonLab/meson-structure/blob/main/full-sim-pipeline/config-campaign-26-06-stv.yaml)


## Commands log

```bash
mkdir -p /work/eic3/users/romanov/meson-structure-2026-06

# cd where scripts are
cd /home/romanov/meson-structure-work/meson-structure

# sync python env
uv sync

# --- shared afterburner (run once, feeds all four variants) ---------------
uv run full-sim-pipeline/10_create_afterburner_jobs.py \
    --config full-sim-pipeline/config-campaign-26-06-official.yaml

# --- -official: default tracking volume -----------------------------------
uv run full-sim-pipeline/20_create_npsim_jobs.py \
    --config full-sim-pipeline/config-campaign-26-06-official.yaml

# --- -saveall: keep all MCParticles ---------------------------------------
uv run full-sim-pipeline/21_create_npsim_saveall_jobs.py \
    --config full-sim-pipeline/config-campaign-26-06-saveall.yaml

# --- -background: mix cocktails, then npsim with status-offset flags -------
uv run full-sim-pipeline/11_create_background_jobs.py \
    --config full-sim-pipeline/config-campaign-26-06-background.yaml
uv run full-sim-pipeline/22_create_npsim_background_jobs.py \
    --config full-sim-pipeline/config-campaign-26-06-background.yaml

# --- -stv: smart tracking volume (eicdev/eic-full:latest) -----------------
uv run full-sim-pipeline/23_create_npsim_stv_jobs.py \
    --config full-sim-pipeline/config-campaign-26-06-stv.yaml

# --- EICrecon on the saveall / background flavors (optional) ---------------
uv run full-sim-pipeline/30_create_eicrecon_jobs.py \
    --config full-sim-pipeline/config-campaign-26-06-saveall.yaml
```

Each `XX_create_*_jobs.py` writes per-file container + SLURM scripts under
`<output>/jobs/` plus a top-level `submit_all_slurm_jobs.sh` / `run_all_local.sh`.
