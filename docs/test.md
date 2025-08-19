# JsonHistogram Component Test

This page demonstrates the `JsonHistogram` component, which allows you to embed individual histograms directly in markdown pages.

## Basic Usage

Simply provide the path to a JSON histogram file:

<JsonHistogram path="/analysis/campaign-2025-07/eg-kinematics/10x100/inc_e_p.json" />

## Multiple Histograms

You can easily display multiple histograms on the same page:

### Incident Electron - Transverse Momentum

<JsonHistogram path="/analysis/campaign-2025-07/eg-kinematics/10x100/inc_e_pt.json" />

### Incident Electron - Angle with Z-axis

<JsonHistogram path="/analysis/campaign-2025-07/eg-kinematics/10x100/inc_e_angle_z_mrad.json" />

## Customization Options

### Custom Height

You can adjust the height of the histogram:

<JsonHistogram 
  path="/analysis/campaign-2025-07/eg-kinematics/10x100/scat_e_theta.json" 
  height="300px" 
/>

### Without Statistics

Hide the statistics bar by setting `show-stats` to false:

<JsonHistogram 
  path="/analysis/campaign-2025-07/eg-kinematics/10x100/kaon_eta.json" 
  :show-stats="false" 
/>

### Custom Title

Override the title from the JSON file:

<JsonHistogram 
  path="/analysis/campaign-2025-07/eg-kinematics/10x100/lambda_pz.json" 
  title="Lambda Longitudinal Momentum Distribution" 
/>

## Grid Layout

You can use CSS grid to display multiple histograms side by side:

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
  <div>
    <h4>Incident Proton pT</h4>
    <JsonHistogram 
      path="/analysis/campaign-2025-07/eg-kinematics/10x100/inc_p_pt.json" 
      height="350px"
      :show-stats="false"
    />
  </div>
  <div>
    <h4>Incident Electron pT</h4>
    <JsonHistogram 
      path="/analysis/campaign-2025-07/eg-kinematics/10x100/inc_e_pt.json" 
      height="350px"
      :show-stats="false"
    />
  </div>
</div>

## Component Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `path` | `string` | required | Path to the JSON histogram file |
| `height` | `string` | `'400px'` | Height of the chart container |
| `show-stats` | `boolean` | `true` | Whether to show statistics (entries, mean, std) |
| `title` | `string` | from JSON | Override the histogram title |

## Features

- **Auto-loading**: Histograms load automatically when the component mounts
- **Dark mode support**: Automatically adapts to VitePress theme
- **Interactive**: Zoom with mouse wheel, hover for tooltips
- **Responsive**: Adjusts to container width
- **Error handling**: Shows clear error messages if loading fails
