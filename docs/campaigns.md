# Simulation campaigns

This page documents the meson structure simulation campaigns.

> (!) For the list of files go to [DATA PAGE](data.md) 


## Campaign 2026-02

[Campaign 2026-02 Link](./campaign-2026-02/campaign-2026-02.md)

Overview: 
- Uses 2026-02 image - EIC software update
- On technical side: analysis automation


## Campaign 2025-10

[Campaign 2025-10 Link](./campaign-2025-10/campaign-2025-10.md)

Overview: 
- Uses 2025-10 image that should be feature freeze before preTDR
- On technical side: better script jobs automation


## Campaign 2025-08

> **Note:** Campaign 2025-08 data has been removed from disk. The commands below are kept for historical reference.

Original MC files located in

```bash
/w/eic-scshelf2104/users/singhav/EIC_mesonsf_generator/OUTPUTS/kaon_lambda_v2
```

### Overview

This campaign introduces the the new energy range 10x130 and increases the statistics to
10 million events for each energy range. 

1. 5x41 GeV
2. 10x100 GeV
2. 10x130 GeV
3. 18x275 GeV

### EG Analysis

Change directories in `full-sim-pipeline` as

```bash
SCRIPT="/home/romanov/meson-structure-work/meson-structure/analysis/eg-kinematics/eg-kinematics.py"
INPUT_DIR="/w/eic-scshelf2104/users/singhav/EIC_mesonsf_generator/OUTPUTS/kaon_lambda_v2"
OUTPUT_DIR="/home/romanov/meson-structure-work/meson-structure/docs/public/analysis/campaign-2025-08/eg-kinematics"
MAX_EVENTS=50000
```

run 

```bash
. /home/romanov/meson-structure-work/meson-structure/full-sim-pipeline/eg_analysis.sh
```

### Overview

This campaign introduces the the new energy range 10x130 and increases the statistics to
10 million events for each energy range. 

1. 5x41 GeV
2. 10x100 GeV
2. 10x130 GeV
3. 18x275 GeV

Each configuration has multiple files (indexed 001-200) with 5000 events per file.

```yaml
timestamp: '2025-06-04T12:05:06.867483'
input_file: /volatile/eic/romanov/meson-structure-2025-06/eg-hepmc/*.hepmc
container_image: /cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:nightly
```


## Campaign 2025-05

> **Note:** Campaign 2025-05 data has been removed from disk. The commands below are kept for historical reference.

### Overview

The Campaign 2025-05 run to make data current with EIC EPIC software updates. 

The campaign includes simulations with three beam energy configurations:

1. 5x41 GeV
2. 10x100 GeV
3. 18x275 GeV

Each configuration has multiple files (indexed 001-200) with 5000 events per file.

```yaml
timestamp: '2025-06-04T12:05:06.867483'
input_file: /volatile/eic/romanov/meson-structure-2025-06/eg-hepmc/*.hepmc
container_image: /cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:nightly
```

### Data Location

The campaign data is stored in the following locations (on JLab farm):

- HEPMC files:   
  `/volatile/eic/romanov/meson-structure-2025-03/eg-hepmc`
- reco info: 
  `/volatile/eic/romanov/meson-structure-2025-06/reco`


## Campaign 2025-03

> **Note:** Campaign 2025-03 data has been removed from disk. The commands below are kept for historical reference.

### Overview

The Campaign 2025-03 is focused on testing the new ZDC lambda reconstruction 
algorithm using the latest ePIC software. 
This campaign reuses meson-structure-2025-02, 
reusing some of the existing `hepmc` files while implementing improved reconstruction techniques.

### Processing Details

The campaign uses a processing pipeline that converts Monte Carlo event generator files 
to a format suitable for full detector simulation and reconstruction:

1. MCEG files are converted to HEPMC format (splitting large files into manageable chunks)
2. The HEPMC files are processed through the latest ePIC reconstruction software
3. Output files include both EDM4EIC format and histogram files

### Data Location

The campaign data is stored in the following locations:

- HEPMC files:   
  `/volatile/eic/romanov/meson-structure-2025-03/eg-hepmc`
  
   Note: These are linked from the previous campaign:
   
   `/volatile/eic/romanov/meson-structure-2025-02/eg-hepmc`
- Reconstruction output:  
  `/volatile/eic/romanov/meson-structure-2025-03/reco`



> For details on accessing the data, see the [Data](./data) page.