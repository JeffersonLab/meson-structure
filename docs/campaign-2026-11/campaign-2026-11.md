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
for every source, so the campaign uses a patched build with a per-source
`fixed_time_offset` option (see Software stack). The signal is placed at
t = 0 and the background bunch crossings are drawn in [0, 200) ns on the
10.15 ns grid, so no crossing before the signal's is included. Beam-gas and
SynRad sources are attached to the beam (`attach_to_beam`, the ePIC cocktail
convention): their sub-event time is the bunch time plus the vertex z / c, so
an event 14 m upstream of the IP carries a time 47 ns before its crossing.
Sub-event times therefore range from about -50 ns to +220 ns in the 200 ns
frames; the hits still arrive at the detector together with their bunch.

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

TimeframeBuilder: v0.9.2 plus two patches, built in the `eic_xl:26.11-stable`
image and installed as `meson-structure-2026-11/bin/timeframe_builder`
(source: `TimeframeBuilder` branch `fixed-time-offset`):

1. `fixed_time_offset` per source (YAML key and `--source:NAME:fixed_time_offset`),
   used to pin the signal at t = 0 in the 200 ns frames.
2. `repeat_on_eof` fix for EDM4hep sources. In 0.9.2 the event index is never
   wrapped at the end of a pool; `TChain::GetEntry` past the end reads
   nothing and the last event is merged again and again with its time and
   `generatorStatus` offsets applied cumulatively. Every frame job of this
   campaign reads its pools several times over, so without the fix all
   frames after the first pass over a pool would have been wrong (found in
   the 9x130 smoke test, 2026-11-05).


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

Production finished 2026-11-05 (pools and signal overnight, 200 ns frames by
04:00, 2 µs frames by 12:00 ET); every file has 500 events or frames:

| Dataset | Energies | Files per energy | Size per energy (9x100 / 9x130 / 9x275) |
| --- | --- | --- | --- |
| signal `dd4hep/<E>/` | 5x41, 9x100, 9x130, 9x275 | 80 (40,000 events) | 28 (5x41) / 60 / 72 / 62 GB |
| 200 ns frames `dd4hep-tfb200ns/<E>/` | 9x100, 9x130, 9x275 | 80 (40,000 frames) | 87 / 99 / 89 GB |
| 2 µs frames `dd4hep-tfb2us/<E>/` | 9x100, 9x130, 9x275 | 80 (40,000 frames) | 325 / 338 / 335 GB |
| background-only 2 µs `background-only-2026-11/frames-2us/<E>/` | 9x100, 9x130, 9x275 | 80 (40,000 frames) | 265 / 265 / 271 GB |
| background pools `background-only-2026-11/pools/<E>/<source>/` | 9x100, 9x130, 9x275 | 127 (SynRad 34, e-gas 30, Coulomb 6, Touschek 50, p-gas 7) | 98 / 98 / 116 GB |

About 2.9 TB in total. Job wall times per 500: signal 17–40 min, 200 ns
frames 3.5–19.5 min, 2 µs frames 28–67 min; TimeframeBuilder needs
1.7–2.0 GB resident. Eleven production files (first and last 200 ns file of
every energy, two background-only and three 2 µs signal files) passed
`check_tfb_frames.py`: 500 frames each, one signal per frame at the
configured time, background rates at the cocktail values (about 26,550
SynRad photons per 2 µs frame), generator statuses only in the cocktail
blocks.


## Reconstruction and CSV (added 2026-11-05)

After the frames were done the campaign was extended to EICrecon and eic2ai
CSV on all four datasets, with the same pipeline config
(`eicrecon`, `csv_signal`, `csv_tfb200ns`, `csv_tfb2us`, `csv_bkg2us`):

| Input | EICrecon output | CSV output (eic2ai, one zip per role) |
| --- | --- | --- |
| `dd4hep/<E>/` | `reco/<E>/` | `csv-reco/<E>/` (all 15 roles) |
| `dd4hep-tfb200ns/<E>/` | `reco-tfb200ns/<E>/` | `csv-tfb200ns/<E>/` (all 15 roles) |
| `dd4hep-tfb2us/<E>/` | `reco-tfb2us/<E>/` | `csv-tfb2us/<E>/` (14 roles, no `mc_particles`) |
| `background-only-2026-11/frames-2us/<E>/` | `background-only-2026-11/reco-2us/<E>/` | `background-only-2026-11/csv-2us/<E>/` (14 roles) |

EICrecon is the image's 1.43.0; it seeds B0 tracks from Geant4 secondaries
by default (EICrecon PR #2901), so no truth-seeding flags are set. Measured
per 500: signal 6 min and 3.1 GB, 200 ns frames 12 min and up to 8 GB,
2 µs frames 35–45 min and up to 10 GB (some 9x275 frames exceeded 5 GB per
CPU, hence 8 and 10 GB per CPU in the config). EICrecon does not copy
`SubEventHeaders` to its output; the simulation files keep it. eic2ai
(sroai/eic2ai 234d2cd, built in this image) needs 1–1.3 GB and 1–8 min per
file pair. One eic2ai rule was added for TimeframeBuilder frames: the
builder adds the source offset to every particle of a sub-event, so a
Geant4 secondary carries e.g. 2000 and its primary 2001; a status that is a
multiple of 1000 is now `prt_origin` 4 (secondary of background), as in the
merger-based CSVs. The `prt_gen_status` column keeps the source band on
every hit row. Counts and sizes of these outputs are added when the arrays
finish.

### Control sample on the merger path

To compare the two mixing methods, 20,000 2 µs frames per energy at 9x100
and 9x275 were also produced the old way: `SignalBackgroundMerger` mixes the
afterburner HepMC with the cocktail before Geant4 and npsim simulates whole
frames (stages 11 and 22; `bg_merged/<E>/{msf_merger,bkg_merger}/`,
`dd4hep-merger/<E>/`, `background-only-2026-11/frames-2us-merger/<E>/`).
The signal set is the same first 40 files × 500 events as the
TimeframeBuilder flavours; the background-only frames carry a ghost signal
(status 7000, never simulated). A whole 2 µs frame takes about 4.5 s in
Geant4 (37 min per 500, 2.7 GB). The comparison (hits per frame per
collection by origin, time and energy distributions, signal hit yields) is
reported separately.


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
are submitted with the standing `%16` throttle; the Geant4 stages ask 4 GB per
CPU (2.5 to 3.2 GB resident measured), TimeframeBuilder 3 GB (1.7 to 2.0 GB
resident measured on 2 µs frames). SLURM logs go
to `/farm_out/romanov/...` and are gzip-copied next to the job scripts at exit.
