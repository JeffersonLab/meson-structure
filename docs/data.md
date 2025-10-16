# Data

## Location

The meson structure data is available from the following locations:

**LATEST PROCESSED FILES**  
*(last update of September 2025)*

On JLab ifarm:  

```bash
/volatile/eic/romanov/meson-structure-2025-08/reco

# priority queues (first 100 files from each energy range):
/volatile/eic/romanov/meson-structure-2025-08/reco/5x41-priority
/volatile/eic/romanov/meson-structure-2025-08/reco/10x100-priority
/volatile/eic/romanov/meson-structure-2025-08/reco/10x130-priority
/volatile/eic/romanov/meson-structure-2025-08/reco/18x275-priority

```

On XRootD (open for universities and public)

```bash
xrdfs root://dtn-eic.jlab.org
ls /volatile/eic/romanov/meson-structure-2025-08/reco
```

Writing libraries versions (important for C++ readout compatibility):
- podio: v01-02
- edm4hep: v00-99-01
- edm4eic: v8.0.1

**Original MCEG files** on ifarm:
`/volatile/eic/romanov/meson-structure-2025-08/eg-orig-kaon-lambda`  
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
ls /volatile/eic/romanov/meson-structure-2025-08/reco
```

**To download** files: 

```bash
xrdcp root://dtn-eic.jlab.org//volatile/eic/romanov/meson-structure-2025-08/reco/5x41-priority/k_lambda_5x41_5000evt_001.edm4eic.root ./
```

**To use directly in scripts**:

```python
# Both uproot and pyroot can work with links directly 
# if XRootD is installed in the system
import uproot
file = uproot.open("root://dtn-eic.jlab.org//volatile/eic/romanov/meson-structure-2025-08/reco/5x41-priority/k_lambda_5x41_5000evt_001.edm4eic.root")
```
