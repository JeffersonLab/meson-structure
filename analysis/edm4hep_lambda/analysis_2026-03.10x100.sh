#!/bin/bash
#SBATCH --account=eic
#SBATCH --partition=production
#SBATCH --job-name=MSCSV10x100
#SBATCH --time=1-00:00:00          # format days-hours:minutes:seconds
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=/work/eic3/users/romanov/meson-structure-2026-04-check/ana_2026-03_10x100.%j.log
#SBATCH --error=/work/eic3/users/romanov/meson-structure-2026-04-check/ana_2026-03_10x100.%j.err

set -euo pipefail

CAMPAIGN=/work/eic3/users/romanov/meson-structure-2026-04-check/dd4hep_2026-03/10x100
OUTPUT_DIR=/work/eic3/users/romanov/meson-structure-2026-04-check
CSV_CONVERT_DIR=/work/eic/users/romanov/meson-structure-work/meson-structure/analysis/edm4hep_lambda
IMG=/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:26.03.1-stable

echo "[INFO]  Running root in $(hostname)"
echo "[INFO]  Campaign directory : $CAMPAIGN"
echo "[INFO]  Container image    : $IMG"
echo "[INFO]  CSV_CONVERT_DIR    : $CSV_CONVERT_DIR"
echo "[INFO]  OUTPUT_DIR         : $OUTPUT_DIR"


# Bind the whole campaign so script sees reco/ inside /work
#singularity exec -B "$CAMPAIGN":/work -B "$CSV_CONVERT_DIR":/code "$IMG" \
#   bash -c 'cd /code &&root -x -l -b -q '\''csv_edm4hep_acceptance_ppim.cxx("/work/k_lambda_10x100_5000evt_0001.edm4hep.root", "k_lambda_10x100_5000evt_0001.acceptance.csv", 5000)'\'''

singularity exec -B "$CAMPAIGN":/work -B "$CSV_CONVERT_DIR":/code -B "$OUTPUT_DIR":/output "$IMG" \
   bash -c 'cd /code &&root -x -l -b -q '\''mcpart_lambda.cxx("/work/k_lambda_10x100_5000evt_0001.edm4hep.root,/work/k_lambda_10x100_5000evt_0005.edm4hep.root,/work/k_lambda_10x100_5000evt_0009.edm4hep.root,/work/k_lambda_10x100_5000evt_0002.edm4hep.root,/work/k_lambda_10x100_5000evt_0006.edm4hep.root,/work/k_lambda_10x100_5000evt_0010.edm4hep.root,/work/k_lambda_10x100_5000evt_0003.edm4hep.root,/work/k_lambda_10x100_5000evt_0007.edm4hep.root,/work/k_lambda_10x100_5000evt_0004.edm4hep.root,/work/k_lambda_10x100_5000evt_0008.edm4hep.root", "/output/ana_2026-03_10x100", 5000)'\'''

echo "[DONE]  Conversion job finished"

