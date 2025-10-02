# Simple Python Pipeline - No Snakemake!

A straightforward Python script that handles priority reconstruction without any overcomplicated workflow managers.

## Usage

```bash
# Make it executable
chmod +x pipeline.py

# List HEPMC files
./pipeline.py list

# Create jobs for all energies
./pipeline.py create

# Submit jobs
./pipeline.py submit

# Do everything (create + submit)
./pipeline.py run

# Check status
./pipeline.py status

# Monitor progress (real-time)
./pipeline.py monitor

# Clean flags to re-run
./pipeline.py clean
```

## Process Specific Energy

```bash
# Create jobs for just 5x41
./pipeline.py create --energy 5x41

# Submit just 10x100
./pipeline.py submit --energy 10x100

# Run everything for 18x275
./pipeline.py run --energy 18x275
```

## Test Mode

Test without actually submitting to SLURM:
```bash
# Test create and submit
./pipeline.py run --test

# Test specific energy
./pipeline.py run --energy 5x41 --test
```

## Complete Workflow Example

```bash
# 1. Check what you have
./pipeline.py list

# 2. Test first
./pipeline.py run --test

# 3. Run for real
./pipeline.py run

# 4. Monitor
./pipeline.py monitor
```

## What It Does

1. **Creates jobs** using your existing `create_jobs.py` script
2. **Submits to SLURM** using the generated submit scripts
3. **Tracks progress** with simple flag files
4. **Monitors** job completion

## Files Created

```
reco/
├── 5x41-priority/
│   ├── .jobs_created       # Flag: jobs were created
│   ├── .jobs_submitted     # Flag: jobs were submitted
│   ├── *.slurm.sh         # SLURM job scripts
│   ├── *.container.sh     # Container scripts
│   └── *.edm4eic.root     # Output files
└── logs/
    ├── create_jobs_*.log
    └── submit_jobs_*.log
```

## No Dependencies!

- No Snakemake
- No PuLP  
- No complex DAGs
- Just Python 3 and subprocess

## Customize

Edit the configuration at the top of `pipeline.py`:
```python
BASE_DIR = "/volatile/eic/romanov/meson-structure-2025-08"
CONTAINER = "/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:25.07-stable"
ENERGIES = ["5x41", "10x100", "10x130", "18x275"]
```

## That's it!

Simple, straightforward, and it just works.
