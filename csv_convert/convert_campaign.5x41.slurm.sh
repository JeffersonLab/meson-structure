#!/bin/bash
#SBATCH --account=eic
#SBATCH --partition=production
#SBATCH --job-name=MSCSV5x41
#SBATCH --time=1-00:00:00          # format days-hours:minutes:seconds
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=/volatile/eic/romanov/meson-structure-2025-08/convert_csv_5x41.%j.log
#SBATCH --error=/volatile/eic/romanov/meson-structure-2025-08/convert_csv_5x41.%j.err

set -euo pipefail

CAMPAIGN=/volatile/eic/romanov/meson-structure-2025-08/reco/5x41-priority
CSV_CONVERT_DIR=/work/eic/users/romanov/meson-structure-work/meson-structure/csv_convert
IMG=/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:25.08-stable

echo "[INFO]  Running convert_campaign.py in $(hostname)"
echo "[INFO]  Campaign directory : $CAMPAIGN"
echo "[INFO]  Container image    : $IMG"
echo "[INFO]  CSV_CONVERT_DIR    : $CSV_CONVERT_DIR"


# Bind the whole campaign so script sees reco/ inside /work
singularity exec -B "$CAMPAIGN":/work -B "$CSV_CONVERT_DIR":/code "$IMG" \
   bash -c 'cd /code && python3 convert_campaign.py /work && cd /work && for f in *.csv; do python3 -m zipfile -c "$f.zip" "$f"; done'

echo "[DONE]  Conversion job finished"