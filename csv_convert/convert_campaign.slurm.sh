#!/bin/bash
#SBATCH --account=eic
#SBATCH --partition=production
#SBATCH --job-name=convertCSV
#SBATCH --time=02:00:00          # adjust as needed
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=/volatile/eic/romanov/meson-structure-2025-06/convert_csv.%j.log
#SBATCH --error=/volatile/eic/romanov/meson-structure-2025-06/convert_csv.%j.err

set -euo pipefail

CAMPAIGN=/volatile/eic/romanov/meson-structure-2025-06/reco
CSV_CONVERT_DIR=/work/eic/users/romanov/meson-structure-work/meson-structure/csv_convert
IMG=/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:nightly

echo "[INFO]  Running convert_campaign.py in $(hostname)"
echo "[INFO]  Campaign directory : $CAMPAIGN"
echo "[INFO]  Container image    : $IMG"
echo "[INFO]  CSV_CONVERT_DIR    : $CSV_CONVERT_DIR"


# Bind the whole campaign so script sees reco/ inside /work
singularity exec -B "$CAMPAIGN":/work -B "$CSV_CONVERT_DIR":/code "$IMG" \
   bash -c 'cd /code && python3 convert_campaign.py /work'

echo "[DONE]  Conversion job finished"