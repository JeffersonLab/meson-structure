# JSON Histogram Serialization for EIC Kinematics Analysis

## Overview

The `eg-kinematics.py` script has been updated to save histograms in JSON format alongside the PNG files, making them suitable for use with Apache ECharts or other web-based visualization tools.

## New Features

### JSON Serialization

When you run the analysis script, it now creates JSON files with the same names as the PNG files:

- `inc_p_pt.png` → `inc_p_pt.json`
- `scat_e_theta.png` → `scat_e_theta.json`
- etc.

### JSON Structure

Each histogram JSON file contains a simple, clean structure:

```json
{
  "particle": "particle_name",
  "variable": "variable_name",
  "title": "Full Title for Display",
  "x_label": "Axis Label [units]",
  "bins": {
    "edges": [...],      // Array of bin edges
    "centers": [...],    // Array of bin centers
    "counts": [...]      // Array of counts per bin
  },
  "stats": {
    "entries": 12345,    // Total number of entries
    "mean": 1.234,       // Mean value
    "std": 0.567         // Standard deviation
  }
}
```

## Usage

### Running the Analysis

```bash
python eg-kinematics.py --input-file your_root_file.root --energy 10x100 --max-events 100000
```

This will create in the `plots/` directory:
- PNG files (as before)
- JSON files with the same names (new)

### Using with Apache ECharts

An example HTML viewer (`echarts_histogram_viewer.html`) is provided. To use it:

1. Run the analysis to generate JSON files
2. Open `echarts_histogram_viewer.html` in a web browser
3. Select a histogram from the dropdown menu

Note: You may need to serve the files through a web server due to CORS restrictions when loading local JSON files.

### Simple Python Web Server

```bash
cd C:\dev\meson-structure\analysis\eg-kinematics
python -m http.server 8000
```

Then open: http://localhost:8000/echarts_histogram_viewer.html

## Integration with Your Application

To use the JSON data in your own application:

```javascript
// Load specific histogram
fetch('plots/inc_p_pt.json')
  .then(response => response.json())
  .then(histData => {
    // Create bar data for ECharts
    const barData = histData.bins.centers.map((center, i) => 
      [center, histData.bins.counts[i]]
    );
    
    // Use with ECharts
    const option = {
      xAxis: { type: 'value', name: histData.x_label },
      yAxis: { type: 'value', name: 'Counts' },
      series: [{ type: 'bar', data: barData }]
    };
  });
```

## Benefits

1. **Web Integration**: Easy to integrate with web-based dashboards
2. **Interactivity**: ECharts provides zoom, pan, and hover tooltips
3. **Portability**: JSON files can be used with any visualization library
4. **Metadata Preservation**: All histogram information is preserved
5. **Statistics**: Mean, std dev, and entry count are pre-calculated

## Notes for EIC Analysis

- The JSON files preserve all the kinematic information for:
  - Incident particles (proton, electron): pT, pz, p, angle with Z-axis
  - Scattered particles (electron, kaon, lambda): pT, pz, p, theta, phi, eta
- The histogram binning is optimized for the beam energy configuration
- All units are preserved in the axis labels
