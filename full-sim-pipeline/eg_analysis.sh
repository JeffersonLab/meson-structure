#!/bin/bash

# Directory variables
SCRIPT="/home/romanov/meson-structure-work/meson-structure/analysis/eg-kinematics/eg-kinematics.py"
INPUT_DIR="/w/eic-scshelf2104/users/singhav/EIC_mesonsf_generator/OUTPUTS/kaon_lambda_v2"
OUTPUT_DIR="/home/romanov/meson-structure-work/meson-structure/docs/public/analysis/campaign-2025-08/eg-kinematics"
MAX_EVENTS=50000

# Process 5 GeV on 41 GeV
mkdir -p $OUTPUT_DIR/5x41
python3 $SCRIPT \
    --input-file $INPUT_DIR/k_lambda_crossing_0.000-5.0on41.0_x0.0001-1.0000_q1.0-500.0.root \
    --outdir $OUTPUT_DIR/5x41 \
    --energy=5x41 \
    --max-events $MAX_EVENTS

# Process 10 GeV on 100 GeV
mkdir -p $OUTPUT_DIR/10x100
python3 $SCRIPT \
    --input-file $INPUT_DIR/k_lambda_crossing_0.000-10.0on100.0_x0.0001-1.0000_q1.0-500.0.root \
    --outdir $OUTPUT_DIR/10x100 \
    --energy=10x100 \
    --max-events $MAX_EVENTS

# Process 10 GeV on 130 GeV
mkdir -p $OUTPUT_DIR/10x130
python3 $SCRIPT \
    --input-file $INPUT_DIR/k_lambda_crossing_0.000-10.0on130.0_x0.0001-1.0000_q1.0-500.0.root \
    --outdir $OUTPUT_DIR/10x130 \
    --energy=10x130 \
    --max-events $MAX_EVENTS

# Process 18 GeV on 275 GeV
mkdir -p $OUTPUT_DIR/18x275
python3 $SCRIPT \
    --input-file $INPUT_DIR/k_lambda_crossing_0.000-18.0on275.0_x0.0001-1.0000_q1.0-500.0.root \
    --outdir $OUTPUT_DIR/18x275 \
    --energy=18x275 \
    --max-events $MAX_EVENTS



echo "All energy configurations processed!"