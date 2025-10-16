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

