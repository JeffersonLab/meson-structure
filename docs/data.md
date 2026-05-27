# Data

## Location


The meson structure data is available from the following locations:

**LATEST PROCESSED FILES**  
*(last update of May 2026 — [campaign 2026-05](https://jeffersonlab.github.io/meson-structure/campaign-2026-05/campaign-2026-05.html))*

Campaign 2026-05 is the first full production run after the
[#1069](https://github.com/eic/epic/issues/1069) /
[#1081](https://github.com/eic/epic/pull/1081) fixes were folded in. It includes
both the regular `dd4hep` flavor (fixed tracking volume) and a `dd4hep_saveall`
flavor that keeps **all** MCParticles. EICrecon reconstruction is run on top of
the `saveall` flavor.

> There is an important distinction. Issue #1069 showed that
> even with the tracking volume not all MCParticle daughters are
> saved even if they reach calorimeter sensitives. The `_saveall`
> flavor keeps all MCParticles and their connections to hits.
>
> (!!!) ALL ACCEPTANCE STUDIES MUST BE DONE USING "_saveall" DATA.

Reconstruction-based analyses can use `reco` / `csv_reco` directly.

On JLab ifarm:

```bash
/work/eic3/users/romanov/meson-structure-2026-05
```

On XRootD (open for universities and public)

```bash
xrdfs root://dtn-eic.jlab.org
ls /work/eic3/users/romanov/meson-structure-2026-05
```

Subdirectories
- afterburner        - eg + beam effects
- dd4hep             - EDM4Hep simulated data, fixed tracking volume (#1069)
- dd4hep_saveall     - EDM4Hep simulated data, all MCParticles saved (acceptance studies)
- reco               - EICrecon reconstructed data (built on `dd4hep_saveall`)
- csv_dd4hep         - CSVs from `dd4hep` (acceptance, fixed volume)
- csv_dd4hep_saveall - CSVs from `dd4hep_saveall` (acceptance, all particles)
- csv_reco           - reconstruction-based CSVs

### Previous: 2026-04 investigation

The 2026-04 dataset is a small investigation sample tied to issues
[#1069](https://github.com/eic/epic/issues/1069) /
[#1081](https://github.com/eic/epic/pull/1081) — DD4hep + afterburner only, no
reconstruction. See
[campaign 2026-04](https://jeffersonlab.github.io/meson-structure/campaign-2026-04/campaign-2026-04.html).

```bash
/work/eic3/users/romanov/meson-structure-2026-04-check
```


Older (and not valid in terms of issue \#1069 data:)

On JLab ifarm:  

```bash
/volatile/eic/romanov/meson-structure-2026-03/reco

# CSV files 
/volatile/eic/romanov/meson-structure-2026-03/csv_eicrecon

# priority queues (first 1'000'000 events == 200 files from each energy range):
/volatile/eic/romanov/meson-structure-2026-03/reco/5x41-priority
/volatile/eic/romanov/meson-structure-2026-03/reco/10x100-priority
/volatile/eic/romanov/meson-structure-2026-03/reco/10x130-priority
/volatile/eic/romanov/meson-structure-2026-03/reco/18x275-priority

#CSV files are located in csv_eicrecon and csv_dd4hep folders now: 
/volatile/eic/romanov/meson-structure-2026-03/csv_eicrecon/5x41-priority
/volatile/eic/romanov/meson-structure-2026-03/csv_eicrecon/10x100-priority
/volatile/eic/romanov/meson-structure-2026-03/csv_eicrecon/10x130-priority
/volatile/eic/romanov/meson-structure-2026-03/csv_eicrecon/18x275-priority

```

On XRootD (open for universities and public)

```bash
xrdfs root://dtn-eic.jlab.org
ls /volatile/eic/romanov/meson-structure-2026-03/reco
```

In this campaign we put processing files in separate folders:

- `eg-orig-kaon-lambda` - original event generator files, 10mil events in each energy range
- `eg-hepmc` - event generator files split by 5k events and converted to HepMC
- `afterburner` - generator files with applied crossing angle and beam effects
- `dd4hep` - DD4Hep full simulation result (`edm4hep.root` files)
- `reco` - EICrecon reconstruction results (`edm4eic.root` files)
- `csv` -  CSV files from reconstructed results

The campaign is made with [eic-shell v26.03.0](https://github.com/eic/containers/tree/v26.03.0-stable?tab=readme-ov-file) container

Writing libraries versions (important for C++ readout compatibility):
- podio: v01-03
- edm4hep: v00-99-01
- edm4eic: v8.0.1
- cxxstd: 20

**Original MCEG files** on ifarm:
`/volatile/eic/romanov/meson-structure-2026-03/eg-orig-kaon-lambda`  
*(last update of August 2025)*


## File names: 


File names are: 

```bash
# The pattern:
k_lambda_{beam}_5000evt_{idx}.{ext}

# e.g.
k_lambda_10x100_5000evt_045.edm4eic.root
```

Where:

- `{beam}` Beam energy configuration [5x41, 10x100, 18x275]
- `{idx}` - zero padded index [001-200]
- `{ext}`
  - `*.info.yaml` - Input and processing metadata
  - `*.afterburner.hepmc` - Beam effects afterburner output 
  - `*.afterburner.hist.root` - Afterburner before-after histograms 
  - `*.edm4hep.root` - DD4Hep (Genat4) output
  - `*.edm4eic.root` - **EICRecon reconstructed files**
  - `*.mcdis.csv` - MC DIS CSV table
  - `*.mcpart_lambda.csv` - MCParticles based CSV table full lambda decay values

> 5000evt indicate each file has 5k events

## Accessing Data with XRootD

The data is available remoutly through XRootD via:  

```
root://dtn-eic.jlab.org
```

**To browse the available files** one can use `xrdfs` command:

```bash
xrdfs root://dtn-eic.jlab.org
ls /volatile/eic/romanov/meson-structure-2026-03/reco
```

**To download** files: 

```bash
xrdcp root://dtn-eic.jlab.org//volatile/eic/romanov/meson-structure-2026-03/reco/5x41-priority/k_lambda_5x41_5000evt_001.edm4eic.root ./
```

**To use directly in scripts**:

```python
# Both uproot and pyroot can work with links directly 
# if XRootD is installed in the system
import uproot
file = uproot.open("root://dtn-eic.jlab.org//volatile/eic/romanov/meson-structure-2026-03/reco/5x41-priority/k_lambda_5x41_5000evt_001.edm4eic.root")
```
