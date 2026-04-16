#!/bin/bash
#SBATCH --account=eic
#SBATCH --partition=production
#SBATCH --job-name=MSCSV10x100
#SBATCH --time=1-00:00:00          # format days-hours:minutes:seconds
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G

set -euo pipefail

CAMPAIGN=/volatile/eic/romanov/meson-structure-2026-03/dd4hep/10x100-priority
CSV_CONVERT_DIR=/work/eic/users/romanov/meson-structure-work/meson-structure/analysis/edm4hep_mcpart_lambda
IMG=/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:nightly

echo "[INFO]  Running root in $(hostname)"
echo "[INFO]  Campaign directory : $CAMPAIGN"
echo "[INFO]  Container image    : $IMG"
echo "[INFO]  CSV_CONVERT_DIR    : $CSV_CONVERT_DIR"


# Bind the whole campaign so script sees reco/ inside /work.
# Input pattern uses a TChain wildcard — expanded inside the macro.
singularity exec -B "$CAMPAIGN":/work -B "$CSV_CONVERT_DIR":/code "$IMG" \
   bash -c 'cd /code && root -x -l -b -q '\''mcpart_lambda.cxx("/work/k_lambda_10x100_*.edm4hep.root", "results_10x100", 50000)'\'''

echo "[DONE]  Conversion job finished"