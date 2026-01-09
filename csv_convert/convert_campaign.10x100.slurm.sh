#!/bin/bash
#SBATCH --account=eic
#SBATCH --partition=production
#SBATCH --job-name=MSCSV10x100
#SBATCH --time=1-00:00:00          # format days-hours:minutes:seconds
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=/volatile/eic/romanov/meson-structure-2025-10/convert_csv_10x100.%j.log
#SBATCH --error=/volatile/eic/romanov/meson-structure-2025-10/convert_csv_10x100.%j.err

set -euo pipefail

CAMPAIGN=/volatile/eic/romanov/meson-structure-2025-10/reco/10x100-priority
CSV_CONVERT_DIR=/work/eic/users/romanov/meson-structure-work/meson-structure/csv_convert
IMG=/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:25.10-stable

echo "[INFO]  Running convert_campaign.py in $(hostname)"
echo "[INFO]  Campaign directory : $CAMPAIGN"
echo "[INFO]  Container image    : $IMG"
echo "[INFO]  CSV_CONVERT_DIR    : $CSV_CONVERT_DIR"


# Bind the whole campaign so script sees reco/ inside /work
singularity exec -B "$CAMPAIGN":/work -B "$CSV_CONVERT_DIR":/code "$IMG" \
   bash -c 'cd /code && python3 convert_campaign.py /work && cd /work && for f in *.csv; do python3 -m zipfile -c "$f.zip" "$f"; done'

echo "[DONE]  Conversion job finished"