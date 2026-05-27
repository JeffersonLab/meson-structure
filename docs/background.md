# Backgrounds in ePIC simulation

How signal events get mixed with the official ePIC background into
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

1. **Afterburner** — Applies crossing angle, beam effects.

2. **SignalBackgroundMerger** — Pulls one
   already-afterburned signal file and background files  (four or five with different backgrounds), 
   and Poisson-samples them into 2 µs timeframes. Each background source's particles get a fixed
   *generator-status offset* added so downstream code can tell what came
   from where.
3. **npsim** — runs Geant4 on the merged HepMC3. Needs special flags (compared to usual EPIC runs) to be told that the
   shifted status codes (2001, 3001, 4001, 5001, …) also mean "stable,
   propagate" / "decayed, skip", otherwise it drops them silently.

## The merger

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
