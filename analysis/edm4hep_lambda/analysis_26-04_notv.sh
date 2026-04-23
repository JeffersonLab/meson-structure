#!/bin/bash
#SBATCH --account=eic
#SBATCH --partition=production
#SBATCH --job-name=MS-26-04-sa
#SBATCH --time=1-00:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=/work/eic3/users/romanov/meson-structure-2026-04-check/ana_26-04_notw.%j.log
#SBATCH --error=/work/eic3/users/romanov/meson-structure-2026-04-check/ana_26-04_notw.%j.err

set -euo pipefail

BASE_CAMPAIGN=/work/eic3/users/romanov/meson-structure-2026-04-check/dd4hep_26-04_notv2
OUTPUT_DIR=/work/eic3/users/romanov/meson-structure-2026-04-check/ana_26-04_notv2
CODE_DIR=/work/eic/users/romanov/meson-structure-work/meson-structure/analysis/edm4hep_lambda
IMG=/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:nightly

energies=("5x41" "10x100" "10x130" "18x275")

echo "[INFO]  Running root on $(hostname)"
echo "[INFO]  Base campaign dir  : $BASE_CAMPAIGN"
echo "[INFO]  Container image    : $IMG"
echo "[INFO]  CODE_DIR           : $CODE_DIR"
echo "[INFO]  OUTPUT_DIR         : $OUTPUT_DIR"
echo "[INFO]  Energies           : ${energies[*]}"

for energy in "${energies[@]}"; do
    CAMPAIGN="$BASE_CAMPAIGN/$energy"

    echo "[INFO]  =========================================================="
    echo "[INFO]  Processing energy  : $energy"
    echo "[INFO]  Campaign directory : $CAMPAIGN"
    echo "[INFO]  =========================================================="

    # --- mcpart_lambda ---
    singularity exec \
        -B "$CAMPAIGN":/work \
        -B "$CODE_DIR":/code \
        -B "$OUTPUT_DIR":/output \
        "$IMG" \
        bash -c "cd /code && root -x -l -b -q 'mcpart_lambda.cxx(\"/work/*.edm4hep.root\", \"/output/${energy}_lambda\", 5000)'"

    # --- acceptance ---
    singularity exec \
        -B "$CAMPAIGN":/work \
        -B "$CODE_DIR":/code \
        -B "$OUTPUT_DIR":/output \
        "$IMG" \
        bash -c "cd /code && root -x -l -b -q 'acceptance.cxx(\"/work/*.edm4hep.root\", \"/output/${energy}_acceptance\", 5000)'"

    echo "[DONE]  Energy $energy finished"
done

echo "[DONE]  Job finished"