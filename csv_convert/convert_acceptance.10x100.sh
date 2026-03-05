#!/bin/bash
#SBATCH --account=eic
#SBATCH --partition=production
#SBATCH --job-name=MSCSV10x100
#SBATCH --time=1-00:00:00          # format days-hours:minutes:seconds
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=/volatile/eic/romanov/meson-structure-2026-02/convert_csv_10x100.%j.log
#SBATCH --error=/volatile/eic/romanov/meson-structure-2026-02/convert_csv_10x100.%j.err

set -euo pipefail

CAMPAIGN=/volatile/eic/romanov/meson-structure-2026-02/dd4hep/10x100-priority
CSV_CONVERT_DIR=/work/eic/users/romanov/meson-structure-work/meson-structure/csv_convert
IMG=/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:nightly

echo "[INFO]  Running root in $(hostname)"
echo "[INFO]  Campaign directory : $CAMPAIGN"
echo "[INFO]  Container image    : $IMG"
echo "[INFO]  CSV_CONVERT_DIR    : $CSV_CONVERT_DIR"


# Bind the whole campaign so script sees reco/ inside /work
#singularity exec -B "$CAMPAIGN":/work -B "$CSV_CONVERT_DIR":/code "$IMG" \
#   bash -c 'cd /code &&root -x -l -b -q '\''csv_edm4hep_acceptance_ppim.cxx("/work/k_lambda_10x100_5000evt_0001.edm4hep.root", "k_lambda_10x100_5000evt_0001.acceptance.csv", 5000)'\'''

singularity exec -B "$CAMPAIGN":/work -B "$CSV_CONVERT_DIR":/code "$IMG" \
   bash -c 'cd /code &&root -x -l -b -q '\''csv_edm4hep_acceptance_npi0.cxx("/work/k_lambda_10x100_5000evt_0001.edm4hep.root", "csv_edm4hep_acceptance_npi0.acceptance_npi0.csv", 5000)'\'''

echo "[DONE]  Conversion job finished"