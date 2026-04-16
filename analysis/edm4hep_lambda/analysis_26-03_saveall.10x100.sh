#!/bin/bash
#SBATCH --account=eic
#SBATCH --partition=production
#SBATCH --job-name=MS-26-03-sa
#SBATCH --time=1-00:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=/work/eic3/users/romanov/meson-structure-2026-04-check/ana_26-03_saveall_10x100.%j.log
#SBATCH --error=/work/eic3/users/romanov/meson-structure-2026-04-check/ana_26-03_saveall_10x100.%j.err

set -euo pipefail

CAMPAIGN=/work/eic3/users/romanov/meson-structure-2026-04-check/dd4hep_26-03_saveall/10x100
OUTPUT_DIR=/work/eic3/users/romanov/meson-structure-2026-04-check
CODE_DIR=/work/eic/users/romanov/meson-structure-work/meson-structure/analysis/edm4hep_lambda
IMG=/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:26.03.1-stable

echo "[INFO]  Running root in $(hostname)"
echo "[INFO]  Campaign directory : $CAMPAIGN"
echo "[INFO]  Container image    : $IMG"
echo "[INFO]  CODE_DIR           : $CODE_DIR"
echo "[INFO]  OUTPUT_DIR         : $OUTPUT_DIR"

singularity exec \
    -B "$CAMPAIGN":/work \
    -B "$CODE_DIR":/code \
    -B "$OUTPUT_DIR":/output \
    "$IMG" \
    bash -c 'cd /code && root -x -l -b -q '"'"'mcpart_lambda.cxx("/work/*.edm4hep.root", "/output/ana_10x100_26-03_saveall")'"'"''

echo "[DONE]  Job finished"
