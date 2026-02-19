# Campaign 2025-10

This page documents the 2025-10 meson structure simulation campaign.

> (!) For the list of files go to [DATA PAGE](../data.md) 


### Overview

This campaign:

- Includes 2025-10 EIC EPIC software stack


Energy ranges:

1. 5x41 GeV
2. 10x100 GeV
2. 10x130 GeV
3. 18x275 GeV

DIS parameters:

- `x= 0.0001 - 1.0000`
- `q2=1 - 500`

```bash
# Root directory
/volatile/eic/romanov/meson-structure-2025-10/

# Event generator root files
/volatile/eic/romanov/meson-structure-2025-08/eg-orig-kaon-lambda

# Event generator files in HepMC (split to 5000k events)
/volatile/eic/romanov/meson-structure-2025-08/eg-hepmc
```

Commands log

```bash
mkdir -p /volatile/eic/romanov/meson-structure-2025-10/
cp -r /volatile/eic/romanov/meson-structure-2025-08/eg-orig-kaon-lambda /volatile/eic/romanov/meson-structure-2025-10/
cp -r /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc /volatile/eic/romanov/meson-structure-2025-10/

# cd where scripts are
cd /home/romanov/meson-structure-work/meson-structure/full-sim-pipeline

# make campaign config and make it "main" config.yaml
ln -s config-campaign-2025-10.yaml config.yaml

# Create afterburner jobs
python create_afterburner_jobs.py

# Run jobs
cd /volatile/eic/romanov/meson-structure-2025-10/afterburner/5x41-priority/jobs && ./submit_all_slurm_jobs.sh &&\
cd /volatile/eic/romanov/meson-structure-2025-10/afterburner/10x100-priority/jobs && ./submit_all_slurm_jobs.sh &&\
cd /volatile/eic/romanov/meson-structure-2025-10/afterburner/10x130-priority/jobs && ./submit_all_slurm_jobs.sh &&\
cd /volatile/eic/romanov/meson-structure-2025-10/afterburner/18x275-priority/jobs && ./submit_all_slurm_jobs.sh

# Now same for DD4Hep jobs
cd /home/romanov/meson-structure-work/meson-structure/full-sim-pipeline
python create_npsim_jobs.py

cd /volatile/eic/romanov/meson-structure-2025-10/dd4hep/5x41-priority/jobs && ./submit_all_slurm_jobs.sh &&\
cd /volatile/eic/romanov/meson-structure-2025-10/dd4hep/10x100-priority/jobs && ./submit_all_slurm_jobs.sh &&\
cd /volatile/eic/romanov/meson-structure-2025-10/dd4hep/10x130-priority/jobs && ./submit_all_slurm_jobs.sh &&\
cd /volatile/eic/romanov/meson-structure-2025-10/dd4hep/18x275-priority/jobs && ./submit_all_slurm_jobs.sh

# Check for file sizes and see if there are files with 0 sizes or similar
cd /volatile/eic/romanov/meson-structure-2025-10/dd4hep/5x41-priority && du -h *.edm4hep.root | sort -r
cd /volatile/eic/romanov/meson-structure-2025-10/dd4hep/10x100-priority && du -h *.edm4hep.root | sort -r
cd /volatile/eic/romanov/meson-structure-2025-10/dd4hep/10x130-priority && du -h *.edm4hep.root | sort -r
cd /volatile/eic/romanov/meson-structure-2025-10/dd4hep/18x275-priority && du -h *.edm4hep.root | sort -r


# Create reconstruction jobs
python create_eicrecon_jobs.py

# Run EICRecon jobs
cd /volatile/eic/romanov/meson-structure-2025-10/reco/5x41-priority/jobs && ./submit_all_slurm_jobs.sh &&\
cd /volatile/eic/romanov/meson-structure-2025-10/reco/10x100-priority/jobs && ./submit_all_slurm_jobs.sh &&\
cd /volatile/eic/romanov/meson-structure-2025-10/reco/10x130-priority/jobs && ./submit_all_slurm_jobs.sh &&\
cd /volatile/eic/romanov/meson-structure-2025-10/reco/18x275-priority/jobs && ./submit_all_slurm_jobs.sh


# create CSV convert jobs
python create_csv_jobs.py

# Run CSV convert jobs
cd /volatile/eic/romanov/meson-structure-2025-10/csv/5x41-priority/jobs && ./submit_all_slurm_jobs.sh &&\
cd /volatile/eic/romanov/meson-structure-2025-10/csv/10x100-priority/jobs && ./submit_all_slurm_jobs.sh &&\
cd /volatile/eic/romanov/meson-structure-2025-10/csv/10x130-priority/jobs && ./submit_all_slurm_jobs.sh &&\
cd /volatile/eic/romanov/meson-structure-2025-10/csv/18x275-priority/jobs && ./submit_all_slurm_jobs.sh

# For some reason CSVs happen to be in reco folder
mv /volatile/eic/romanov/meson-structure-2025-10/reco/5x41-priority/*.csv   /volatile/eic/romanov/meson-structure-2025-10/csv/5x41-priority/ &&\
mv /volatile/eic/romanov/meson-structure-2025-10/reco/10x100-priority/*.csv /volatile/eic/romanov/meson-structure-2025-10/csv/10x100-priority/ &&\
mv /volatile/eic/romanov/meson-structure-2025-10/reco/10x130-priority/*.csv /volatile/eic/romanov/meson-structure-2025-10/csv/10x130-priority/ &&\
mv /volatile/eic/romanov/meson-structure-2025-10/reco/18x275-priority/*.csv /volatile/eic/romanov/meson-structure-2025-10/csv/18x275-priority/

```
