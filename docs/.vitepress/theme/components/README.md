# Histogram Visualization Components

This directory contains Vue components for displaying histograms in VitePress documentation.

## Components

### JsonHistogram

A simple component for embedding individual histograms from JSON files.

**Usage:**
```vue
<JsonHistogram path="/path/to/histogram.json" />
```

**Props:**
- `path` (string, required): Path to the JSON file
- `height` (string): Chart height (default: '400px')
- `showStats` (boolean): Show statistics bar (default: true)
- `title` (string): Override the histogram title

**Example:**
```vue
<JsonHistogram 
  path="/analysis/campaign-2025-07/eg-kinematics/10x100/inc_e_p.json"
  height="350px"
  :show-stats="false"
  title="Custom Title"
/>
```

### HistogramViewer

An interactive histogram viewer with a dropdown selector for multiple histograms.

**Usage:**
```vue
<HistogramViewer 
  base-path="/analysis/campaign-2025-07/eg-kinematics/10x100" 
  energy="10x100"
/>
```

**Props:**
- `basePath` (string, required): Base path to the histogram files
- `energy` (string): Energy configuration label

## JSON Format

Both components expect JSON files with the following structure:

```json
{
  "particle": "inc_e",
  "variable": "p",
  "title": "Incident Electron - p",
  "x_label": "P [GeV/c]",
  "bins": {
    "edges": [9.0, 9.1, 9.2, ...],
    "centers": [9.05, 9.15, 9.25, ...],
    "counts": [0, 12, 45, ...]
  },
  "stats": {
    "entries": 100000,
    "mean": 9.999,
    "std": 0.012
  }
}
```

## Features

- **Apache ECharts**: Uses ECharts for rendering
- **Dark Mode**: Automatically adapts to VitePress theme
- **Interactive**: Zoom, pan, and hover tooltips
- **Responsive**: Works on all device sizes
- **TypeScript**: Fully typed components

## Installation

These components are automatically registered in `.vitepress/theme/index.ts`:

```typescript
import JsonHistogram from "./components/JsonHistogram.vue";
import HistogramViewer from "./components/HistogramViewer.vue";

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('JsonHistogram', JsonHistogram);
    app.component('HistogramViewer', HistogramViewer);
  }
};
```

## Dependencies

Make sure to install ECharts:

```bash
npm install echarts
```
