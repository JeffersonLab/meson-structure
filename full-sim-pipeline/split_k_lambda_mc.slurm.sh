#!/bin/bash
#SBATCH --account=eic
#SBATCH --partition=production
#SBATCH --job-name=processMC
#SBATCH --time=2-00:00:00          # format days-hours:minutes:seconds
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=/volatile/eic/romanov/meson-structure-2025-07/eg_tohepmc.%j.log
#SBATCH --error=/volatile/eic/romanov/meson-structure-2025-07/eg_tohepmc.%j.err

set -euo pipefail

# split 5x41
python root_hepmc_converter.py \
      --input-files /volatile/eic/romanov/meson-structure-2025-07/mc_kaon_lambda_2025-07/k_lambda_crossing_0_5.0on41.0_x0.0001-1.0000_q1.0-500.0.root \
      --output-prefix /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc/k_lambda_5x41_5000evt \
      --events-per-file 5000

# split 10x100
python root_hepmc_converter.py \
      --input-files /volatile/eic/romanov/meson-structure-2025-07/mc_kaon_lambda_2025-07/k_lambda_crossing_0_10.0on100.0_x0.0001-1.0000_q1.0-500.0.root \
      --output-prefix /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc/k_lambda_10x100_5000evt \
      --events-per-file 5000

# split 10x130
python root_hepmc_converter.py \
      --input-files /volatile/eic/romanov/meson-structure-2025-07/mc_kaon_lambda_2025-07/k_lambda_crossing_0_10.0on130.0_x0.0001-1.0000_q1.0-500.0.root \
      --output-prefix /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc/k_lambda_10x130_5000evt \
      --events-per-file 5000

# split 18x275
python root_hepmc_converter.py \
      --input-files /volatile/eic/romanov/meson-structure-2025-07/mc_kaon_lambda_2025-07/k_lambda_crossing_0_18.0on275.0_x0.0001-1.0000_q1.0-500.0.root \
      --output-prefix /volatile/eic/romanov/meson-structure-2025-07/eg-hepmc/k_lambda_18x275_5000evt \
      --events-per-file 5000
