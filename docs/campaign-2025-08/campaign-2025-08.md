# Simulation campaigns

This page documents the 2025-08 meson structure simulation campaign.

> (!) For the list of files go to [DATA PAGE](../data.md) 


## Campaign 2025-08

Original kaon lambda MC files located in 

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

x= 0.0001 - 1.0000

q2=1 - 500

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

### Sortout mc files

```bash
mkdir /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/{5x41,10x100,10x130,18x275}-priority
mkdir /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/{5x41,10x100,10x130,18x275}-rest

mv /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/k_lambda_5x41_5000evt_{001..100}.hepmc   /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/5x41-priority
mv /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/k_lambda_10x100_5000evt_{001..100}.hepmc /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/10x100-priority
mv /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/k_lambda_10x130_5000evt_{001..100}.hepmc /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/10x130-priority
mv /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/k_lambda_18x275_5000evt_{001..100}.hepmc /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/18x275-priority
mv /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/k_lambda_5x41*   /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/5x41-rest
mv /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/k_lambda_10x100* /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/10x100-rest &&\
mv /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/k_lambda_10x130* /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/10x130-rest &&\
mv /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/k_lambda_18x275* /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/18x275-rest
```

### Priority queue

```bash
mkdir -p /volatile/eic/romanov/meson-structure-2025-08/reco/{5x41,10x100,10x130,18x275}-priority

python create_jobs.py \
       -b /volatile/eic/romanov/meson-structure-2025-08 \
       -o /volatile/eic/romanov/meson-structure-2025-08/reco/5x41-priority \
       --container /cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:25.08-stable \
       -e 5000 \
       /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/5x41-priority/*.hepmc

python create_jobs.py \
       -b /volatile/eic/romanov/meson-structure-2025-08 \
       -o /volatile/eic/romanov/meson-structure-2025-08/reco/10x100-priority \
       --container /cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:25.08-stable \
       -e 5000 \
       /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/10x100-priority/*.hepmc

python create_jobs.py \
       -b /volatile/eic/romanov/meson-structure-2025-08 \
       -o /volatile/eic/romanov/meson-structure-2025-08/reco/10x130-priority \
       --container /cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:25.08-stable \
       -e 5000 \
       /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/10x130-priority/*.hepmc

python create_jobs.py \
       -b /volatile/eic/romanov/meson-structure-2025-08 \
       -o /volatile/eic/romanov/meson-structure-2025-08/reco/18x275-priority \
       --container /cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:25.08-stable \
       -e 5000 \
       /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/18x275-priority/*.hepmc

```


The exact commands used in this campaign:


```bash
mkdir /volatile/eic/romanov/meson-structure-2025-08
mkdir /volatile/eic/romanov/meson-structure-2025-08/reco
mkdir /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/

# Using new Avnish generated files
cp /w/eic-scshelf2104/users/singhav/EIC_mesonsf_generator/OUTPUTS/kaon_lambda_v2/*.root /volatile/eic/romanov/meson-structure-2025-08/eg-orig-kaon-lambda

# Creating jobs (using latest eic_xl container)
cd /home/romanov/meson-structure-work/meson-structure/full-sim-pipeline
python create_jobs.py \
       -b /volatile/eic/romanov/meson-structure-2025-08 \
       -o /volatile/eic/romanov/meson-structure-2025-08/reco \
       --container /cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:25.08-stable \
       -e 5000 \
       /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/*.hepmc

# Submit jobs
cd /volatile/eic/romanov/meson-structure-2025-08/reco/
submit_all_slurm_jobs.sh
```

---


## Campaign 2025-05

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



### Processing Commands

The exact commands used in this campaign:

```bash
mkdir /volatile/eic/romanov/meson-structure-2025-06
mkdir /volatile/eic/romanov/meson-structure-2025-06/reco

# Using previous converted hepmc files
cp -r /volatile/eic/romanov/meson-structure-2025-03/eg-hepmc /volatile/eic/romanov/meson-structure-2025-06

# Creating jobs (using latest eic_xl container)
cd /home/romanov/meson-structure-work/meson-structure/full-sim-pipeline
python create_jobs.py \
       -b /volatile/eic/romanov/meson-structure-2025-06 \
       -o /volatile/eic/romanov/meson-structure-2025-06/reco \
       -e 5000 \
       /volatile/eic/romanov/meson-structure-2025-06/eg-hepmc/*.hepmc

# Submit jobs
cd /volatile/eic/romanov/meson-structure-2025-06/reco/
submit_all_slurm_jobs.sh
```



## Campaign 2025-03


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

### Processing Commands

The exact commands used in this campaign:

```bash
# Original MCEG files location
# Note: Using the same hepmc files as the previous campaign
cd /volatile/eic/romanov/meson-structure-2025-03
ln -s /volatile/eic/romanov/meson-structure-2025-02/eg-hepmc eg-hepmc

cd /home/romanov/meson-structure-work/meson-structure/full-sim-pipeline

# Generate job scripts (using latest eic_xl container)
python create_jobs.py \
       -b /volatile/eic/romanov/meson-structure-2025-03 \
       -o /volatile/eic/romanov/meson-structure-2025-03/reco \
       -e 5000 \
       /volatile/eic/romanov/meson-structure-2025-03/eg-hepmc/*.hepmc

# Submit jobs
cd /volatile/eic/romanov/meson-structure-2025-03/reco/
submit_all_slurm_jobs.sh
```

We used files in 

```
/w/eic-scshelf2104/users/singhav/JLEIC/USERS/trottar/OUTPUTS/raty_eic
```

With headon collisions `k_lambda_crossing_0_*`

