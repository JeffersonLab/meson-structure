# Simulation campaigns

This page documents the 2025-03 meson structure simulation campaign.

> (!) For the list of files go to [DATA PAGE](data.md) 


## Campaign 2025-08

Original MC files located in 

```
/w/eic-scshelf2104/users/singhav/EIC_mesonsf_generator/OUTPUTS/kaon_lambda_v2
```

Testing MC

```bash
python3 /home/romanov/meson-structure-work/meson-structure/analysis/eg-kinematics/eg-kinematics.py \
--input-file /w/eic-scshelf2104/users/singhav/JLEIC/USERS/trottar/OUTPUTS/raty_eic/k_lambda_crossing_0_10.0on100.0_x0.0001-0.9000_q1.0-500.0.root \
--outdir /home/romanov/meson-structure-work/meson-structure/docs/public/analysis/campaign-2025-07/eg-kinematics \
--max-events 50000

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


 A two-step plan for file processing. To better isolate any potential issues as there too many changes (new software, updated generator, new energy level, etc.).

For all processing, the latest stable EIC container: 25.07-stable.

1. Reprocess the existing Monte Carlo files with the new 25.07-stable container. I.e. usual generator data with the latest reconstruction.

2. Process new 10 million event files, with new energy


### Processing Commands

The exact commands used in this campaign:

Old data using 25.07-stable

```bash
mkdir /volatile/eic/romanov/meson-structure-2025-07
mkdir /volatile/eic/romanov/meson-structure-2025-07/reco
mkdir /volatile/eic/romanov/meson-structure-2025-07/reco-oldmc
mkdir /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc/


# Using previous converted hepmc files
cp -r /volatile/eic/romanov/meson-structure-2025-06/eg-hepmc /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc-oldmc

# Using new Avnish generated files
mkdir /volatile/eic/romanov/meson-structure-2025-07/kaon_lambda_mc_2025-07
mv /volatile/eic/romanov/meson-structure-2025-07/kaon_lambda_mc_2025-07 /volatile/eic/romanov/meson-structure-2025-07/mc_kaon_lambda_2025-07

# split 5x41
python root_hepmc_converter.py \
      --input-files /volatile/eic/romanov/meson-structure-2025-07/mc_kaon_lambda_2025-07/k_lambda_crossing_0_5.0on41.0_x0.0001-1.0000_q1.0-500.0.root \
      --output-prefix /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc/k_lambda_5x41_5000evt \
      --events-per-file 5000

# split 10x100
python root_hepmc_converter.py \
      --input-files /volatile/eic/romanov/meson-structure-2025-07/mc_kaon_lambda_2025-07/k_lambda_crossing_0_10.0on100.0_x0.0001-1.0000_q1.0-500.0.root \
      --output-prefix /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc/k_lambda_10x100_5000evt \
      --events-per-file 5000

# split 10x130
python root_hepmc_converter.py \
      --input-files /volatile/eic/romanov/meson-structure-2025-07/mc_kaon_lambda_2025-07/k_lambda_crossing_0_10.0on130.0_x0.0001-1.0000_q1.0-500.0.root \
      --output-prefix /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc/k_lambda_10x130_5000evt \
      --events-per-file 5000

# split 18x275
python root_hepmc_converter.py \
      --input-files /volatile/eic/romanov/meson-structure-2025-07/mc_kaon_lambda_2025-07/k_lambda_crossing_0_18.0on275.0_x0.0001-1.0000_q1.0-500.0.root \
      --output-prefix /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc/k_lambda_18x275_5000evt \
      --events-per-file 5000


# Priority reconstruction of each 100 files for each energy range

mkdir /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc-priority-5x41
mkdir /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc-priority-10x100
mkdir /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc-priority-10x130
mkdir /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc-priority-18x275

mv /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc/k_lambda_5x41_5000evt_{001..100}.hepmc /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc-priority-5x41
mv /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc/k_lambda_10x100_5000evt_{001..100}.hepmc /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc-priority-10x100
mv /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc/k_lambda_10x130_5000evt_{001..100}.hepmc /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc-priority-10x130
mv /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc/k_lambda_18x275_5000evt_{001..100}.hepmc /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc-priority-18x275

# Jobs for priority
python create_jobs.py \
       -b /volatile/eic/romanov/meson-structure-2025-07 \
       -o /volatile/eic/romanov/meson-structure-2025-07/reco \
       --container /cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:25.07-stable \
       -e 5000 \
       /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc-priority-*/*.hepmc



k_lambda_crossing_0_5.0on41.0_x0.0001-1.0000_q1.0-500.0.root

# Creating jobs (using latest eic_xl container)
cd /home/romanov/meson-structure-work/meson-structure/full-sim-pipeline
python create_jobs.py \
       -b /volatile/eic/romanov/meson-structure-2025-07 \
       -o /volatile/eic/romanov/meson-structure-2025-07/reco \
       --container /cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:25.07-stable \
       -e 5000 \
       /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc/*.hepmc


# Submit jobs
cd /volatile/eic/romanov/meson-structure-2025-07/reco/
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



> For details on accessing the data, see the [Data](./data) page.