# Dynamic Histogram Plots

This page demonstrates interactive histogram visualization using Apache ECharts. You can select different histograms from the dropdown menu to explore the kinematics data.

## 10x100 GeV Analysis

The following interactive viewer displays histograms from the 10x100 GeV beam configuration analysis. Select a histogram from the dropdown to view:

<HistogramViewer 
  base-path="/analysis/campaign-2025-07/eg-kinematics/10x100" 
  energy="10x100"
/>

## Features

- **Interactive Selection**: Choose from different particles and kinematic variables
- **Statistics Display**: View entries, mean, and standard deviation for each histogram
- **Zoom and Pan**: Use mouse wheel to zoom, drag to pan
- **Tooltips**: Hover over bars to see detailed bin information
- **Dark Mode Support**: Automatically adapts to VitePress theme

## Available Histograms

### Incident Particles
- **Incident Proton**: pT, px, py, pz, p, angle with Z-axis
- **Incident Electron**: pT, px, py, pz, p, angle with Z-axis

### Scattered Particles
- **Scattered Electron**: pT, pz, p, theta, phi, pseudorapidity (η)
- **Kaon**: pT, pz, p, theta, phi, pseudorapidity (η)
- **Lambda**: pT, px, py, pz, p, angle with Z-axis

## Technical Details

The histograms are generated from the EIC simulation data and stored as JSON files. Each file contains:

- Bin edges and centers
- Counts per bin
- Statistical information (entries, mean, standard deviation)
- Axis labels and titles

The interactive visualization uses Apache ECharts to render the histograms with full interactivity in the browser.
