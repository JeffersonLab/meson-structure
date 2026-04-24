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

BASE_EG_DIR="/work/eic/users/romanov/eg-orig-kaon-lambda-2025-08"
OUTPUT_DIR="/work/eic3/users/romanov/meson-structure-2026-04-check/ana/eg-kinematics"
CODE_DIR="/work/eic/users/romanov/meson-structure-work/meson-structure/analysis/eg-kinematics"

declare -A EG_MAP

# Assign keys and values
EG_MAP["5x41"]="$BASE_EG_DIR/k_lambda_crossing_0.000-5.0on41.0_x0.0001-1.0000_q1.0-500.0.root"
EG_MAP["10x100"]="$BASE_EG_DIR/k_lambda_crossing_0.000-10.0on100.0_x0.0001-1.0000_q1.0-500.0.root"
EG_MAP["10x130"]="$BASE_EG_DIR/k_lambda_crossing_0.000-10.0on130.0_x0.0001-1.0000_q1.0-500.0.root"
EG_MAP["18x275"]="$BASE_EG_DIR/k_lambda_crossing_0.000-18.0on275.0_x0.0001-1.0000_q1.0-500.0.root"

energies=("5x41" "10x100" "10x130" "18x275")

mkdir -p "$OUTPUT_DIR"
cd "$CODE_DIR"

for energy in "${energies[@]}"; do
    current_file="${EG_MAP[$energy]}"
    
    # Create a specific output directory for the current energy configuration
    energy_outdir="$OUTPUT_DIR/$energy"
    mkdir -p "$energy_outdir"

    echo "====================================================="
    echo "[START] Processing energy: $energy"
    echo "        Input file: $current_file"
    echo "        Output dir: $energy_outdir"
    echo "====================================================="

    # Run the script using the dynamic loop variables
    uv run "$CODE_DIR/eg-kinematics.py" \
        --input-file "$current_file" \
        --outdir "$energy_outdir" \
        -e "$energy"

    echo "[DONE]  Energy $energy finished"
done

echo "====================================================="
echo "[DONE]  Job finished"