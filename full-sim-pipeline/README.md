# Meson Structure Priority Processing Pipeline

Simplified Snakemake workflow for processing priority files (first 500 files per energy) for the EIC Lambda decay studies.

## Quick Fix for Snakemake Error

If you get the `AttributeError: module 'pulp' has no attribute 'list_solvers'` error:

```bash
# Run the fix script
chmod +x fix_and_test.sh
./fix_and_test.sh

# Or manually:
pip uninstall -y pulp
# If that doesn't work, try:
pip install 'pulp<2.8'
```

## Quick Start

### 1. Check available HEPMC files
```bash
snakemake -s Snakefile.smk list_hepmc
```

### 2. Test mode (dry run)
```bash
snakemake -s Snakefile.smk -n
```

### 3. Create jobs only (no submission)
```bash
snakemake -s Snakefile.smk create_only -j 4
```

### 4. Submit already created jobs
```bash
snakemake -s Snakefile.smk submit_only -j 4
```

### 5. Monitor progress
```bash
# One-time status check
snakemake -s Snakefile.smk check_status

# Continuous monitoring (updates every 30s)
snakemake -s Snakefile.smk monitor
```

## Complete Workflow

```bash
# Step 1: List files to verify setup
snakemake -s Snakefile.smk list_hepmc

# Step 2: Create and submit all jobs at once
snakemake -s Snakefile.smk -j 4

# Step 3: Monitor
snakemake -s Snakefile.smk monitor
```

## Test Mode

To test without submitting jobs:
```bash
# Edit config.yaml
vim config.yaml
# Set: test_mode: true

# Run the workflow
snakemake -s Snakefile.smk -j 4

# This will create all job files but won't submit to SLURM
```

## Directory Structure

```
meson-structure-2025-08/
├── eg-hepmc/
│   ├── 5x41-priority/      # Input HEPMC files
│   ├── 5x41-rest/          # (not processed yet)
│   ├── 10x100-priority/
│   ├── 10x100-rest/
│   ├── 10x130-priority/
│   ├── 10x130-rest/
│   ├── 18x275-priority/
│   └── 18x275-rest/
├── reco/
│   ├── 5x41-priority/      # Output files
│   │   ├── *.slurm.sh      # SLURM job scripts
│   │   ├── *.container.sh  # Container scripts
│   │   ├── *.afterburner.hepmc
│   │   ├── *.edm4hep.root
│   │   └── *.edm4eic.root
│   └── ...
└── logs/                   # Snakemake logs
```

## Configuration

Edit `config.yaml` to adjust settings:

```yaml
base_dir: "/volatile/eic/romanov/meson-structure-2025-08"
test_mode: false  # Set to true for testing without submission
```

## Useful Commands

```bash
# Clean and restart
snakemake -s Snakefile.smk clean_flags  # Remove flag files
snakemake -s Snakefile.smk clean_logs   # Remove log files

# Check what will be done
snakemake -s Snakefile.smk -n -r        # Dry run with reasons

# Force re-run of specific rule
snakemake -s Snakefile.smk create_priority_jobs -f

# Check logs
tail -f logs/create_jobs_5x41_priority.log
tail -f logs/submit_jobs_10x100_priority.log

# Check SLURM queue
squeue -u $USER

# Cancel all your jobs
scancel -u $USER
```

## Troubleshooting

### No HEPMC files found
- Check that files exist: `ls -la /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc/5x41-priority/`
- Verify correct paths in `config.yaml`

### Jobs not submitting
- Check SLURM availability: `sinfo`
- Review submission logs: `cat logs/submit_jobs_*_priority.log`
- Verify test_mode is false in config.yaml

### Want to re-run everything
```bash
snakemake -s Snakefile.smk clean_flags
snakemake -s Snakefile.smk -j 4
```

### Snakemake not working
```bash
./fix_and_test.sh  # Run the fix script
```

## Output Files

Each HEPMC file will produce:
- `*.afterburner.hepmc` - After afterburner processing
- `*.edm4hep.root` - After detector simulation (NPSIM)
- `*.edm4eic.root` - After reconstruction (EICRECON)

Plus job management files:
- `*.slurm.sh` - SLURM submission script
- `*.container.sh` - Container execution script
- `*.slurm.log` - Job output log
- `*.slurm.err` - Job error log
- `*.info.yaml` - Job metadata
