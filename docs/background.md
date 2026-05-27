# Backgrounds in ePIC simulation

How signal events get mixed with the official ePIC background cocktails into
2 µs timeframes, what gets called when, and what flags actually matter.

::: tip TL;DR
```
generator  →  abconv (afterburner)  →  SignalBackgroundMerger  →  npsim  →  eicrecon
   (rest frame)     (beam effects        (Poisson into 2 µs       (with status-
                     applied once,        timeframes, every         offset flags)
                     cached on XrootD)    source tagged with a
                                          generator-status offset)
```
:::

## The big picture

ePIC's background-mixed simulations are built in three independent stages.
Mix them up and you'll silently lose particles, double-apply beam effects, or
end up with backgrounds that disagree with the published frequencies.

1. **Afterburner** — once per generator output, before anything reaches the
   XrootD store. Applies crossing angle, beam divergence, crab kick, and
   vertex spread. Files come out with names like
   `…_beamEffects_xAngle=-0.025_hiDiv_*.hepmc3.tree.root`.
2. **SignalBackgroundMerger** — per simulation job. Pulls one
   already-afterburned signal file and the four (or five) background files
   from the official cocktail JSON, and Poisson-samples them into 2 µs
   timeframes. Each background source's particles get a fixed
   *generator-status offset* added so downstream code can tell what came
   from where.
3. **npsim** — runs Geant4 on the merged HepMC3. Needs to be told that the
   shifted status codes (2001, 3001, 4001, 5001, …) also mean "stable,
   propagate" / "decayed, skip", otherwise it drops them silently.

## Stage 1 — afterburner (beam effects)

**Repo:** [eic/afterburner](https://github.com/eic/afterburner) · CLI binary `abconv`

The afterburner is *input preprocessing*. Generators (Pythia6/8, EpIC,
eSTARlight, BeAGLE, DEMPgen, Klam, Pin, …) produce events in beam-rest frame,
head-on, no crossing angle. `abconv` reads each event, applies:

- crossing angle (e.g. `xAngle = -0.025 rad` for IP6)
- beam divergence (`hiDiv` / `hiAcc` presets)
- crab cavity kick
- vertex position + time spread

…and writes a new HepMC3 file with these effects baked into the four-vectors
and vertices. The output is then uploaded once to
`/volatile/eic/EPIC/EVGEN/…` on `dtn-eic.jlab.org` and reused by thousands of
downstream jobs.

::: warning Backgrounds usually do NOT go through abconv
SR, e-beam-gas (Xsuite / GETaLM), and proton beam-gas files are generated
*inside* the actual beamline simulation, so beam effects are already
intrinsic to them. Only physics signal generators (which produce rest-frame
events) need abconv. You can tell from the filename: a `_beamEffects_…`
suffix means already afterburned.
:::

In this repo, stage 10 of the pipeline applies `abconv` to our local signal
HepMC files:

```bash
python full-sim-pipeline/10_create_afterburner_jobs.py \
    -c full-sim-pipeline/config-campaign-26-05-background.yaml
```

## Stage 2 — the merger

**Repo:** [eic/HEPMC_Merger](https://github.com/eic/HEPMC_Merger) · CLI binary `SignalBackgroundMerger` · Spack package: `hepmcmerger`

For each 2 µs timeframe (default 2000 ns) the merger:

- places exactly one signal event (because the campaigns set `--signalFreq 0`,
  which is the merger's "guaranteed one signal per slice" mode),
- draws each background source's event count from a Poisson with mean
  `freq × slice_length`,
- distributes particles uniformly in time inside the slice,
- and adds the source's `status` value to every `MCParticle.generatorStatus`
  it touches.

The current campaign convention for status offsets is:

| Source         | Offset | Stable code | Decay code |
| -------------- | -----: | ----------: | ---------: |
| signal         |      0 |           1 |          2 |
| synrad         |   2000 |        2001 |       2002 |
| ebrems         |   3000 |        3001 |       3002 |
| ecoulomb       |   4000 |        4001 |       4002 |
| etouschek      |   5000 |        5001 |       5002 |
| p-beam-gas     |   6000 |        6001 |       6002 |

(See [eic/eic.github.io / background\_mixed\_samples](https://github.com/eic/eic.github.io/blob/main/_resources/background_mixed_samples.md)
for the official conventions and worked examples with timeframe diagrams.)

### Where the cocktail recipes live

**Repo:** [eic/simulation\_campaign\_datasets](https://github.com/eic/simulation_campaign_datasets)
(tracked here as the submodule `eic_official_campaign_info`)

`config_data/*.json` — one cocktail per beam-energy / vacuum-condition
combination. Each file is a list of entries like:

```json
[
  {"file": "root://.../synrad_18x275_run001....hepmc3.tree.root",
   "freq": 3324000, "skip": 0.0, "status": 2000},
  {"file": "root://.../GETaLM..._ElectronBeamGas_18GeV_….hepmc3.tree.root",
   "freq": 316.94,  "skip": 0.0, "status": 3000},
  {"file": "root://.../electron_coulomb_18x275_….hepmc3.tree.root",
   "freq": 0.86,    "skip": 0.0, "status": 4000},
  {"file": "root://.../electron_touschek_18x275_….hepmc3.tree.root",
   "freq": 0.55,    "skip": 0.0, "status": 5000}
]
```

Field meanings:

| Field    | Meaning                                                                 |
| -------- | ----------------------------------------------------------------------- |
| `file`   | XrootD URL of an already-prepared background HepMC3.                    |
| `freq`   | Poisson rate in **events/ns** (so 3.3 M = 3.3 GHz for synrad).          |
| `skip`   | Fraction of the file's events to skip before sampling (parallel jobs use this to read non-overlapping windows of the same source). |
| `status` | Generator-status offset added to every particle from this source.       |

### Merger command (what the campaign actually runs)

```bash
SignalBackgroundMerger \
    --rngSeed     <per-job seed> \
    --nSlices     <events_per_task> \
    --signalFile  <afterburned signal>.hepmc3.tree.root \
    --signalFreq  0 \
    --signalStatus 0 \
    --bgFile <synrad_url>   3324000 0.0 2000 \
    --bgFile <egas_url>      316.94 0.0 3000 \
    --bgFile <coulomb_url>     0.86 0.0 4000 \
    --bgFile <touschek_url>    0.55 0.0 5000 \
    --outputFile  merged.hepmc3.tree.root
```

`--signalFreq 0` is the special "one signal per slice" mode. Setting it to a
nonzero events/ns value would make signals Poisson-sampled too, which is the
right thing for low-rate processes like SIDIS-pythia6 where you may want
events that are pure background.

::: tip There is a second mixer
[eic/TimeframeBuilder](https://github.com/eic/TimeframeBuilder) is the newer
mixer (evaluated in `detector_benchmarks`). It can mix in pre-simulated
edm4hep files too, supports beam-attachment / bunch-crossing discretisation /
Gaussian time spread, and is reviewed via CI capybara reports. Production
campaigns still use `SignalBackgroundMerger`, so that's what this pipeline
calls.
:::

## Stage 3 — npsim with status-offset flags

DD4hep / npsim by default treats only `generatorStatus == 1` particles as
Geant4 primaries and `== 2` as decayed-intermediate. The merger has just
created particles with statuses like 2001 or 3002 — unknown numbers, silently
dropped.

The two flags that fix this:

```bash
npsim ... \
    --hepmc3.useHepMC3                  true \
    --runType                           batch \
    --physics.alternativeStableStatuses "1 2001 3001 4001 5001" \
    --physics.alternativeDecayStatuses  "2 2002 3002 4002 5002" \
    --inputFiles                        merged.hepmc3.tree.root \
    --outputFile                        sim.edm4hep.root
```

Three gotchas:

1. **The lists fully replace, not augment.** Forgetting `1` in the stable
   list = signal events stop reaching Geant4.
2. **Don't forget `--hepmc3.useHepMC3 true`.** Without it npsim falls back to
   the older HepMC2 reader, which handles `.hepmc3.tree.root` input
   differently and may not honour the alternative status lists at all.
3. **`--runType batch`, not `run`.** `run` is for steering/gun input;
   `batch` is the right mode for `--inputFiles`.

The defining file in DD4hep is
[DDG4/python/DDSim/Helper/Physics.py](https://github.com/AIDASoft/DD4hep/blob/master/DDG4/python/DDSim/Helper/Physics.py)
— that's where `_alternativeStableStatuses` / `_alternativeDecayStatuses`
live, and they are exposed verbatim on the npsim CLI.

If you write a steering file instead of using CLI flags:

```python
from DDSim.DD4hepSimulation import DD4hepSimulation
SIM = DD4hepSimulation()
SIM.physics.alternativeStableStatuses = {1, 2001, 3001, 4001, 5001}
SIM.physics.alternativeDecayStatuses  = {2, 2002, 3002, 4002, 5002}
SIM.hepmc3.useHepMC3 = True
```

## How this repo wires it all together

The pipeline for the background-mixed campaign is split into numbered stages
under `full-sim-pipeline/` driven by
`config-campaign-26-05-background.yaml`:

```
01/02  upstream signal ROOT  →  *.hepmc
10     abconv                →  afterburner/<energy>-priority/*.afterburner.hepmc
11     SignalBackgroundMerger→  bg_merged/<energy>/*.bg.hepmc3.tree.root
22     npsim (status flags)  →  dd4hep_saveall/<energy>/*.edm4hep.root
30     eicrecon              →  reco/<energy>/*.edm4eic.root
```

### `11_create_background_jobs.py`

Per-energy, this script:

1. Looks up `background_configs[energy]` in the YAML — the cocktail filename
   for that beam configuration.
2. Loads the JSON from `${background_config_dir}/<filename>`.
3. For every afterburned signal `*.afterburner.hepmc`, emits a SLURM +
   container script pair that calls `SignalBackgroundMerger` with the full
   `--bgFile <url> <freq> <skip> <status>` argument set.
4. Uses a deterministic per-basename RNG seed (md5 of basename) so parallel
   jobs produce *different* Poisson realisations of the same background
   sources.

### `22_create_npsim_background_jobs.py`

Per-energy, this script:

1. Re-loads the same cocktail JSON.
2. Builds the status-offset lists from `entries[*].status` — automatically
   picks up `_hgas_` cocktails (which add a 6000 entry) if you ever swap one
   in.
3. Renders the npsim command with the three critical flags above.

### Config keys you actually edit

`config-campaign-26-05-background.yaml`:

```yaml
# Path to the cloned eic/simulation_campaign_datasets submodule
background_config_dir: ".../eic_official_campaign_info/config_data"

# Per-energy choice of cocktail (filename inside background_config_dir)
background_configs:
  "10x100": "synrad_egasbrems_egascoulomb_egastouschek_10GeVx100GeV_GoldCoating_10um_10000Ahr_machineruntime_50s.json"
  "10x130": "synrad_egasbrems_egascoulomb_egastouschek_10GeVx130GeV_GoldCoating_10um_10000Ahr_machineruntime_50s.json"
  "18x275": "synrad_egasbrems_egascoulomb_egastouschek_18GeVx275GeV_vacuum_10000Ahr_machineruntime_50s.json"

# Stage I/O
bg_merger_input:  "${base_dir}/afterburner/${energy}-priority"
bg_merger_output: "${base_dir}/bg_merged/${energy}"
dd4hep_saveall_input:  "${bg_merger_output}"           # stage 22 reads merged files
dd4hep_saveall_output: "${base_dir}/dd4hep_saveall/${energy}"
```

To switch to an `_hgas_…` cocktail (adds proton beam-gas, status 6000), just
swap the filename in `background_configs[<energy>]` — the status-offset flag
list rebuilds itself in stage 22.

## Provenance of the background source files

| Source     | Generator / pipeline                                           | Repo                                                                        |
| ---------- | -------------------------------------------------------------- | --------------------------------------------------------------------------- |
| synrad     | Geant4 sim of photons emitted by the electron beam through IR  | (internal, output published under `EVGEN/BACKGROUNDS/SYNRAD/`)              |
| ebrems     | GETaLM electron-beam-gas (bremsstrahlung)                      | published under `EVGEN/BACKGROUNDS/BEAMGAS/electron/GETaLM*/`               |
| ecoulomb   | Xsuite tracking through the actual lattice (Coulomb)           | published under `EVGEN/BACKGROUNDS/BEAMGAS/electron/coulomb/EIC_ESR_Xsuite/` |
| etouschek  | Xsuite tracking through the actual lattice (Touschek)          | published under `EVGEN/BACKGROUNDS/BEAMGAS/electron/touschek/EIC_ESR_Xsuite/` |
| p-beam-gas | Pythia8 hadron beam-gas (when used)                            | published under `EVGEN/BACKGROUNDS/BEAMGAS/proton/pythia8.306-1.0/`         |

Reproducer scripts for the electron beam-gas HepMC files live in
[eic/ElectronBeamGas](https://github.com/eic/ElectronBeamGas) and
[eic/electron\_background\_simulation](https://github.com/eic/electron_background_simulation).

## Where the campaign code lives (for cross-reference)

| What                                          | Repo                                                                                                                                |
| --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Afterburner (`abconv`)                        | [eic/afterburner](https://github.com/eic/afterburner)                                                                               |
| Signal-background merger                      | [eic/HEPMC\_Merger](https://github.com/eic/HEPMC_Merger)                                                                            |
| Newer timeframe mixer                         | [eic/TimeframeBuilder](https://github.com/eic/TimeframeBuilder)                                                                     |
| Per-job campaign driver (`run.sh`)            | [eic/simulation\_campaign\_hepmc3](https://github.com/eic/simulation_campaign_hepmc3)                                               |
| Condor submitter, BG-fetch glue               | [eic/job\_submission\_condor](https://github.com/eic/job_submission_condor)                                                         |
| Cocktail JSONs + CSV chunk manifests          | [eic/simulation\_campaign\_datasets](https://github.com/eic/simulation_campaign_datasets) (submodule `eic_official_campaign_info`)  |
| ePIC production docs (release tags, paths)    | [eic/epic-prod](https://github.com/eic/epic-prod)                                                                                   |
| Official background-mixed sample docs         | [eic/eic.github.io / background\_mixed\_samples](https://github.com/eic/eic.github.io/blob/main/_resources/background_mixed_samples.md) |
| Spack package for the merger                  | `spack_repo/eic/packages/hepmcmerger/package.py` in [eic/eic-spack](https://github.com/eic/eic-spack)                               |
| Background-mixed Rucio metadata (`is_background_mixed`) | `scripts/register_to_rucio.py` in [eic/simulation\_campaign\_hepmc3](https://github.com/eic/simulation_campaign_hepmc3)             |

## XrootD / Rucio access

Outputs of the campaign land in
`xroots://dtn2201.jlab.org//eic/eic2/EPIC/{RECO,FULL,LOG}/<release>/<detector>/...`
and are registered to Rucio under account `eicprod` with a metadata schema
that includes `is_background_mixed: true|false`. The `update-data-md` skill
in this repo queries Rucio with that flag to rebuild `docs/data.md`.

Mixed simulation outputs from official campaigns can also be browsed
directly:

```
root://dtn-eic.jlab.org//volatile/eic/EPIC/FULL/<release>/epic_craterlake/Bkg_1SignalPer2usFrame/...
root://dtn-eic.jlab.org//volatile/eic/EPIC/RECO/<release>/epic_craterlake/Bkg_1SignalPer2usFrame/...
```

(Increment the `<release>` tag — e.g. `25.06.1` — to find the latest
campaign. RECO is preserved across campaigns; FULL is not always.)
