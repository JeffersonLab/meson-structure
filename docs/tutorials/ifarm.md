# Run jobs on ifarm


## Slurm jobs

Here is a memo for running jobs with slurm

- [JLab Scientific Computing website](https://scicomp.jlab.org/scicomp/home)
- [Simple(very) slurm start](https://scicomp.jlab.org/docs/farm_batch_auger_to_slurm)
- [Check that you are not in jobLimit list](https://scicomp.jlab.org/scicomp/slurmJob/jobLimit)
- [Check jobs by username](https://scicomp.jlab.org/scicomp/slurmJob/activeJob?user=romanov&account=eic)
- [JLab slurm info page (partitions, nodes, etc)](https://scicomp.jlab.org/scicomp/slurmJob/slurmInfo)
- [Slurm commands cheat sheet](https://slurm.schedmd.com/pdfs/summary.pdf)
- [More explanation from JLab](https://scicomp.jlab.org/docs/farm_slurm_batch)

Common commands:

```bash
# Start a job
sbatch try_slurm

# see jobs
squeue -u romanov

# Stop/cancel jobs
scancel 41887209

# Check what accound belongs to
sacctmgr show user romanov

# Check existing partitions
sinfo -s
```

Error output can be redirected with `#SBATCH --output=` by default both error and output are redirected to one file. 
But there is a separate `#SBATCH --error=` can be added to split output and error streams. 
[filename-pattern](https://slurm.schedmd.com/sbatch.html#SECTION_%3CB%3Efilename-pattern%3C/B%3E):

```
#SBATCH --output=/u/scratch/romanov/test_slurm/%j.out
#SBATCH --error=/u/scratch/romanov/test_slurm/%j.err
```


## Run eic_shell on slurm 


There are several approaches how to run eic_shell under the slurm on ifarm. 

For Meson-Structure campaigns we create 2 scripts: one for batch submission and another one for what to do in the container (listed below). It is also possible to run just one script with slurm command. 


`eic_shell` is a slim wrapper around singularity (or now apptainer) containers. Instead of eic_shell direct singularity command could be used. 

```bash
singularity exec -B /host/dir:/container/dir {image} script_to_run.sh
```

Where: 

- `-B` is binding of existing directory to some path in container. One needs to bind all paths that are used. And also container doesn't follow links if they point to something that is not bound
- `{image}` - images avialable on ifarm on CVMFS at folder: 

   ```bash
   # eic_shell images location: 
   ls /cvmfs/singularity.opensciencegrid.org/eicweb/

   # the latest `nightly` image:
   /cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:nightly

   # release or stable images are available by names like: 
   /cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:25.07-stable
   ```
- `script_to_run.sh` your script to run in the eic shell

Here is an example (it is wordy but it illustrates real ifarm paths and images)

```bash
singularity exec \
-B /volatile/eic/romanov/meson-structure-2025-07:/volatile/eic/romanov/meson-structure-2025-07 \
/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:25.07-stable \
/volatile/eic/romanov/meson-structure-2025-07/reco/k_lambda_18x275_5000evt_073.container.sh
```

Instead of `script_to_run.sh` one can put commands directly, but it might be tricky in terms of quotes, special symbols, etc. Here is an example from [csv_convert/convert_campaign.10x100.slurm.sh](https://github.com/JeffersonLab/meson-structure/blob/main/csv_convert/convert_campaign.10x100.slurm.sh):

```bash
singularity exec -B "$CAMPAIGN":/work -B "$CSV_CONVERT_DIR":/code "$IMG" \
   bash -c 'cd /code && python3 convert_campaign.py /work && cd /work && for f in *.csv; do zip "${f}.zip" "$f"; done'
```

For simulation campaign [full-sim-pipeline/](https://github.com/JeffersonLab/meson-structure/tree/main/full-sim-pipeline) scripts create such jobs for each hepmc file.


### Full scripts example

Full script to start a slurm job (still be run under bash for debug purposes) 

```bash
#!/bin/bash
#SBATCH --account=eic
#SBATCH --partition=production
#SBATCH --job-name=k_lambda_18x275_5000evt_073
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=5G
#SBATCH --output=/volatile/eic/romanov/meson-structure-2025-07/reco/k_lambda_18x275_5000evt_073.slurm.log
#SBATCH --error=/volatile/eic/romanov/meson-structure-2025-07/reco/k_lambda_18x275_5000evt_073.slurm.err

set -e

# Ensure singularity is available
if ! command -v singularity &> /dev/null; then
  echo "singularity not found. Please load the module or install singularity."
  exit 1
fi

echo "Running job k_lambda_18x275_5000evt_073 on $(hostname)"
echo "Using container image: /cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:25.07-stable"
echo "Executing container-run script: /volatile/eic/romanov/meson-structure-2025-07/reco/k_lambda_18x275_5000evt_073.container.sh"

# Execute the container-run script inside the container.
singularity exec -B /volatile/eic/romanov/meson-structure-2025-07:/volatile/eic/romanov/meson-structure-2025-07 /cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:25.07-stable /volatile/eic/romanov/meson-structure-2025-07/reco/k_lambda_18x275_5000evt_073.container.sh

echo "Slurm job finished for k_lambda_18x275_5000evt_073!"
```

Script of what to do in containers

```bash
#!/bin/bash
set -e
# This script is intended to run INSIDE the Singularity container.

echo "Sourcing EIC environment..."
# Adjust the path if needed:
source /opt/detector/epic-main/bin/thisepic.sh

echo ">"
echo "=ABCONV===================================================================="
echo "==========================================================================="
echo "  Running afterburner on:"
echo "    /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc-priority-18x275/k_lambda_18x275_5000evt_074.hepmc"
echo "  Resulting files:"
echo "    /volatile/eic/romanov/meson-structure-2025-07/reco/k_lambda_18x275_5000evt_074.afterburner.*"
/usr/bin/time -v abconv /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc-priority-18x275/k_lambda_18x275_5000evt_074.hepmc --output /volatile/eic/romanov/meson-structure-2025-07/reco/k_lambda_18x275_5000evt_074.afterburner 2>&1

echo ">"
echo "=NPSIM====================================================================="
echo "==========================================================================="
echo "  Running npsim on:"
echo "    /volatile/eic/romanov/meson-structure-2025-07/reco/k_lambda_18x275_5000evt_074.afterburner.hepmc"
echo "  Resulting file:"
echo "    /volatile/eic/romanov/meson-structure-2025-07/reco/k_lambda_18x275_5000evt_074.edm4hep.root"
echo "  Events to process:"
echo "    5000"

/usr/bin/time -v npsim --compactFile=$DETECTOR_PATH/epic.xml --runType run --inputFiles /volatile/eic/romanov/meson-structure-2025-07/reco/k_lambda_18x275_5000evt_074.afterburner.hepmc --outputFile /volatile/eic/romanov/meson-structure-2025-07/reco/k_lambda_18x275_5000evt_074.edm4hep.root --numberOfEvents 5000 2>&1

echo ">"
echo "=EICRECON=================================================================="
echo "==========================================================================="
echo "  Running eicrecon on:"
echo "    /volatile/eic/romanov/meson-structure-2025-07/reco/k_lambda_18x275_5000evt_074.edm4hep.root"
echo "  Resulting files:"
echo "    /volatile/eic/romanov/meson-structure-2025-07/reco/k_lambda_18x275_5000evt_074.edm4eic.root"
/usr/bin/time -v eicrecon -Ppodio:output_file=/volatile/eic/romanov/meson-structure-2025-07/reco/k_lambda_18x275_5000evt_074.edm4eic.root /volatile/eic/romanov/meson-structure-2025-07/reco/k_lambda_18x275_5000evt_074.edm4hep.root 2>&1

echo "All steps completed for k_lambda_18x275_5000evt_074!"
```


## Running with a custom EICrecon branch

Sometimes you need a modified EICrecon — e.g. the
[reco/ff-lambda-multicalo](https://github.com/eic/EICrecon/tree/reco/ff-lambda-multicalo) branch
that adds far-forward Lambda reconstruction with multiple calorimeters.

The idea is simple: take the standard container image (which already has all dependencies),
build your EICrecon branch inside it, and override the environment so that
`eicrecon` picks up the new libraries and plugins instead of the ones shipped with the image.

There are two routes:
1. **Build on a shared filesystem** (e.g. `/volatile`) inside the stock singularity image — no new image needed.
2. **Build a new Docker image** on top of `eicweb/eic_xl:nightly`, push it to Docker Hub, then pull it as a singularity image.

### Route 1: Build on shared filesystem (recommended for ifarm)

This is the simplest approach. You build EICrecon once on `/volatile` (or `/work`)
and then every slurm job sources the new environment before running.

#### One-time build (interactive or in a slurm job)

```bash
#!/bin/bash
set -e

# Where to put the custom EICrecon build
EICRECON_SRC=/volatile/eic/$USER/EICrecon
EICRECON_INSTALL=/volatile/eic/$USER/EICrecon/install
IMG=/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:nightly

# Clone and checkout the branch (run on the host, /volatile is shared)
git clone https://github.com/eic/EICrecon.git "$EICRECON_SRC"
cd "$EICRECON_SRC"
git checkout reco/ff-lambda-multicalo

# Build inside the container so that all dependencies are found
singularity exec \
  -B /volatile/eic/$USER:/volatile/eic/$USER \
  "$IMG" \
  bash -c "
    set -e
    source /opt/detector/epic-main/bin/thisepic.sh
    cd $EICRECON_SRC
    cmake -B build -S . -DCMAKE_INSTALL_PREFIX=$EICRECON_INSTALL
    cmake --build build -j\$(nproc)
    cmake --install build
  "
```

#### Using the custom build in your container script

In the container script (the one that runs afterburner → npsim → eicrecon),
source the custom EICrecon environment **after** the standard epic environment:

```bash
#!/bin/bash
set -e

# Standard environment
source /opt/detector/epic-main/bin/thisepic.sh

# Override with custom EICrecon
EICRECON_INSTALL=/volatile/eic/$USER/EICrecon/install
source "$EICRECON_INSTALL/bin/eicrecon-this.sh"

# Verify
echo "Using eicrecon from: $(which eicrecon)"
echo "JANA_PLUGIN_PATH=$JANA_PLUGIN_PATH"

# Now run as usual — eicrecon will use the custom build
eicrecon -Ppodio:output_file=output.edm4eic.root input.edm4hep.root
```

`eicrecon-this.sh` prepends the install directory to `PATH`, `LD_LIBRARY_PATH`,
and `JANA_PLUGIN_PATH` so the custom build takes priority over the image defaults.

If for some reason `eicrecon-this.sh` is not available, you can set the variables manually:

```bash
export PATH="$EICRECON_INSTALL/bin:$PATH"
export LD_LIBRARY_PATH="$EICRECON_INSTALL/lib:$LD_LIBRARY_PATH"
export JANA_PLUGIN_PATH="$EICRECON_INSTALL/lib/EICrecon/plugins:$JANA_PLUGIN_PATH"
```


### Route 2: Build a new Docker image

If you want a self-contained image (useful when sharing with others or for reproducibility),
build a Docker image on top of the official one and then pull it as singularity.

#### Dockerfile

```dockerfile
FROM eicweb/eic_xl:nightly

RUN source /opt/detector/epic-main/bin/thisepic.sh && \
    git clone --branch reco/ff-lambda-multicalo --depth 1 \
        https://github.com/eic/EICrecon.git /opt/EICrecon && \
    cd /opt/EICrecon && \
    cmake -B build -S . -DCMAKE_INSTALL_PREFIX=/opt/EICrecon/install && \
    cmake --build build -j"$(nproc)" && \
    cmake --install build && \
    rm -rf build .git

# Source both environments on entry
RUN echo 'source /opt/detector/epic-main/bin/thisepic.sh' >> /etc/bash.bashrc && \
    echo 'source /opt/EICrecon/install/bin/eicrecon-this.sh' >> /etc/bash.bashrc
```

#### Build, push, and use on ifarm

```bash
# On a machine with Docker
docker build -t yourdockerhub/eic_xl_ff_lambda:latest .
docker push yourdockerhub/eic_xl_ff_lambda:latest

# On ifarm — pull as singularity image (one time)
singularity pull docker://yourdockerhub/eic_xl_ff_lambda:latest
# This creates eic_xl_ff_lambda_latest.sif

# Use in slurm jobs just like the standard image
singularity exec \
  -B /volatile/eic/$USER:/volatile/eic/$USER \
  eic_xl_ff_lambda_latest.sif \
  your_container_script.sh
```

With the Docker route the custom EICrecon is baked into the image,
so container scripts don't need to source anything extra — the environment
is already set up via `/etc/bash.bashrc`.