# Campaign 2026-11

This page documents the 2026-11 meson structure simulation campaign.

> (!) For the list of files go to [DATA PAGE](../data.md)


## Overview

The November 2026 campaign is a **streaming-readout study set**: a small
K⁺Λ signal sample simulated alone through Geant4, then **mixed after Geant4**
into timeframes with the official ePIC background cocktails by
[TimeframeBuilder](https://github.com/eic/TimeframeBuilder). The campaign
stops at the EDM4hep (DD4hep) level: no EICrecon reconstruction and no CSV
tables are produced.

Energy ranges (the `9xN` scheme of campaign 2026-07):

1. 5x41 GeV — signal only (its background cocktail inputs are not available, see below)
2. 9x100 GeV
3. 9x130 GeV
4. 9x275 GeV

Statistics: **40,000 signal events per energy** — the first 500 events of the
first 80 afterburner files of campaign 2026-07 (one 500-event job per file).
Output file names keep the 2026-07 stems (`msf_<E>_1000evt_NNNN`) although each
holds 500 events.

Datasets per energy:

| Dataset | Content | Output subdir |
| --- | --- | --- |
| signal | K⁺Λ events alone through Geant4 (`Geant4TVUserParticleHandler`) | `dd4hep/<E>/` |
| 2 µs frames | one signal event at a random bunch crossing of a 2 µs frame + background | `dd4hep-tfb2us/<E>/` |
| 200 ns frames | one signal event pinned at **t = 0** of a 200 ns frame + background (the "found event" readout window, see below) | `dd4hep-tfb200ns/<E>/` |
| background-only 2 µs frames | 40,000 frames per energy, background cocktail only | `background-only-2026-11/frames-2us/<E>/` |
| background pools | each cocktail source alone through Geant4 (inputs of TimeframeBuilder) | `background-only-2026-11/pools/<E>/<source>/` |

Background cocktails are the closest-energy ePIC recipes: the
`10GeVxN GoldCoating 10um + hgas` cocktails for the 9xN beams. The 5x41 cocktail
needs SynRad 5x100, electron beam-gas 5 GeV and proton beam-gas 41 GeV inputs
that are neither on the farm nor on the public XRootD door (checked
2026-11-04), so 5x41 is skipped for pools and frames and has the signal only.

Frame contents follow the ePIC convention: background particles carry the
cocktail status offsets (2000 SynRad, 3000 e-gas, 4000 Coulomb, 5000 Touschek,
6000 p-gas), every sub-event is listed in `SubEventHeaders`, bunch crossings
are 10.15 ns apart and beam-gas sources are attached to the beam time.


## 200 ns frames: the "found event" readout window

The idea: pretend an event-finding stage located the physics event inside a
long streaming frame and cut a short readout window around it; that window
then goes through reconstruction as if it were a triggered event. For this the
signal must sit at a known time. TimeframeBuilder 0.9.2 draws a random offset
for every source, so the campaign uses a build with a per-source
`fixed_time_offset` option (branch `fixed-time-offset`, built in the
`eic_xl:26.11-stable` image, installed as `meson-structure-2026-11/bin/timeframe_builder`).
The signal is placed at t = 0 and the background offsets are drawn in
[0, 200) ns on the 10.15 ns bunch grid, so no background from before the
signal is included.

Window length: measured on 2026-07 signal at 9x130 (raw Geant4 hit times),
B0 hits arrive 19–25 ns after the collision, the Off-Momentum trackers at
85–91 ns, the Roman Pots at 108–116 ns and the ZDC from 119 ns; 99.3 % of the
signal tracker hits fall within t0 + 200 ns. A 70 ns window (three times the
light travel time to the B0 region) would keep the central detector and B0
only, so the window is **200 ns** (about 20 bunch crossings). Hadron
calorimeter afterglow from slow neutrons continues for tens of µs and is cut
by any window.

## Software stack

Official EIC image from cvmfs:

```
/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:26.11-stable
```

TimeframeBuilder: v0.9.2 plus the `fixed_time_offset` patch (see above).


## Data layout (ifarm)

Campaign directory:

```bash
/work/eic3/users/romanov/meson-structure-2026-11
```

- `dd4hep/<E>/`          — signal-only DD4hep output (`*.edm4hep.root`, 80 files x 500 events per energy)
- `dd4hep-tfb2us/<E>/`   — 2 µs frames, one signal per frame (`msf_tfb2us_<E>_NNNN.edm4hep.root`, 500 frames per file)
- `dd4hep-tfb200ns/<E>/` — 200 ns frames, signal at t = 0 (`msf_tfb200ns_<E>_NNNN.edm4hep.root`, 500 frames per file)
- `datasets/`            — the dataset cards of every stage
- `bin/timeframe_builder` — the patched TimeframeBuilder

Background-only directory:

```bash
/work/eic3/users/romanov/background-only-2026-11
```

- `pools/<E>/<source>/`  — per-source Geant4 pools (`<input stem>.cNNNN.rR.edm4hep.root`; `r` = replica with its own Geant4 seed)
- `frames-2us/<E>/`      — background-only 2 µs frames (`bkg_2us_<E>_NNNN.edm4hep.root`, 500 frames per file, 80 files per energy)

Every TimeframeBuilder job keeps its exact configuration in `jobs/<name>.tfb.yaml`
next to the output.

File counts and sizes are filled in when the production finishes.


## Pipeline config

The campaign is driven by
[`simulation-pipeline/configs/config-msf-26-11.yaml`](https://github.com/JeffersonLab/msf-simulation-pipeline/blob/main/configs/config-msf-26-11.yaml)
(one self-contained file) and the cards script
`simulation-pipeline/scripts/msf_2026_11_make_cards.sh`.


## Commands log

```bash
cd /home/romanov/meson-structure-work/meson-structure/simulation-pipeline
CFG=configs/config-msf-26-11.yaml

# background pools: each cocktail source alone through Geant4 (no cards)
python simulation_pipeline/23_create_npsim_bgsource_jobs.py -c $CFG

# signal: first 80 afterburner files of 2026-07, 500 events each
bash scripts/msf_2026_11_make_cards.sh npsim
python simulation_pipeline/20_create_npsim_jobs.py -c $CFG

# frames (after the pools and the signal exist)
bash scripts/msf_2026_11_make_cards.sh bkg_2us tfb_2us tfb_200ns
python simulation_pipeline/13_create_timeframe_builder_jobs.py bkg_2us  -c $CFG
python simulation_pipeline/13_create_timeframe_builder_jobs.py tfb_2us  -c $CFG
python simulation_pipeline/13_create_timeframe_builder_jobs.py tfb_200ns -c $CFG
```

Each `NN_create_*_jobs.py` writes per-file container + SLURM scripts under
`<output>/jobs/` plus `submit_all_slurm_jobs.sh` / `run_all_local.sh`. Arrays
are submitted with the standing `%16` throttle and 2 GB per CPU; SLURM logs go
to `/farm_out/romanov/...` and are gzip-copied next to the job scripts at exit.
