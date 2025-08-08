#!/bin/bash
#SBATCH --account=eic
#SBATCH --partition=production
#SBATCH --job-name=SplitEG
#SBATCH --time=2-00:00:00          # format days-hours:minutes:seconds
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=/volatile/eic/romanov/meson-structure-2025-08/eg_split.%j.log
#SBATCH --error=/volatile/eic/romanov/meson-structure-2025-09/eg_split.%j.err

set -euo pipefail

IN_FILES_DIR="/volatile/eic/romanov/meson-structure-2025-08/eg-orig-kaon-lambda"
OUT_FILES_DIR="/volatile/eic/romanov/meson-structure-2025-08/eg-hepmc"
mkdir -p $OUT_FILES_DIR

# split 5x41
python root_hepmc_converter.py \
      --input-files $IN_FILES_DIR/k_lambda_crossing_0.000-5.0on41.0_x0.0001-1.0000_q1.0-500.0.root \
      --output-prefix $OUT_FILES_DIR/k_lambda_5x41_5000evt \
      --events-per-file 5000

# split 10x100
python root_hepmc_converter.py \
      --input-files $IN_FILES_DIR/k_lambda_crossing_0.000-10.0on100.0_x0.0001-1.0000_q1.0-500.0.root \
      --output-prefix $OUT_FILES_DIR/k_lambda_10x100_5000evt \
      --events-per-file 5000

# split 10x130
python root_hepmc_converter.py \
      --input-files $IN_FILES_DIR/k_lambda_crossing_0.000-10.0on130.0_x0.0001-1.0000_q1.0-500.0.root \
      --output-prefix $OUT_FILES_DIR/k_lambda_10x130_5000evt \
      --events-per-file 5000

# split 18x275
python root_hepmc_converter.py \
      --input-files $IN_FILES_DIR/k_lambda_crossing_0.000-18.0on275.0_x0.0001-1.0000_q1.0-500.0.root \
      --output-prefix $OUT_FILES_DIR/k_lambda_18x275_5000evt \
      --events-per-file 5000
