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

The idea is to build a new singularity/apptainer image on top of the standard `eic_xl`
image. The base image already ships all dependencies (ROOT, podio, EDM4hep, JANA, etc.).
We clone the custom EICrecon branch, build and install it over the stock one, and bake
the result into a new `.sif` image. After that, `singularity exec` or `singularity run`
just works — no extra environment setup in your scripts.


### Singularity definition file

Create a file `eicrecon_custom.def`:

```singularity
Bootstrap: docker
From: eicweb/eic_xl:nightly

%post
    # Source the full EIC/epic environment so cmake finds all dependencies
    . /opt/detector/epic-main/bin/thisepic.sh

    # Clone the custom EICrecon branch
    git clone --branch reco/ff-lambda-multicalo --depth 1 \
        https://github.com/eic/EICrecon.git /tmp/EICrecon
    cd /tmp/EICrecon

    # Build and install into /opt/EICrecon
    cmake -B build -S . -DCMAKE_INSTALL_PREFIX=/opt/EICrecon
    cmake --build build -j"$(nproc)"
    cmake --install build

    # Clean up build artifacts to keep the image small
    rm -rf /tmp/EICrecon

%environment
    # Prepend custom EICrecon paths so it takes priority over the stock version
    export PATH=/opt/EICrecon/bin:$PATH
    export LD_LIBRARY_PATH=/opt/EICrecon/lib:$LD_LIBRARY_PATH
    export JANA_PLUGIN_PATH=/opt/EICrecon/lib/EICrecon/plugins${JANA_PLUGIN_PATH:+:$JANA_PLUGIN_PATH}
```

The `%environment` section is automatically sourced by singularity/apptainer on every
`exec` / `run` / `shell`, so the custom EICrecon takes priority over the stock version
that ships with the base image.


### Build the image

Building requires either root access or `--fakeroot` (available on ifarm):

```bash
# On ifarm (with --fakeroot)
singularity build --fakeroot eicrecon_custom.sif eicrecon_custom.def

# Or on a machine where you have root
sudo singularity build eicrecon_custom.sif eicrecon_custom.def
```

This takes a while (EICrecon is a large C++ project). The resulting `.sif` file is
a self-contained, read-only image.


### Use in slurm jobs

The custom image is a drop-in replacement for the stock one. Use it exactly the same
way as described in the sections above:

```bash
# Instead of the stock image:
#   IMG=/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:nightly
# Use:
IMG=/path/to/eicrecon_custom.sif

singularity exec \
  -B /volatile/eic/$USER:/volatile/eic/$USER \
  "$IMG" \
  your_container_script.sh
```

Container scripts don't need any special sourcing — `eicrecon` inside the image
already points to the custom build:

```bash
#!/bin/bash
set -e
source /opt/detector/epic-main/bin/thisepic.sh

# This runs the custom EICrecon — no extra setup needed
eicrecon -Ppodio:output_file=output.edm4eic.root input.edm4hep.root
```