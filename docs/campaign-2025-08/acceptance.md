<script setup>
const sources = {
  '5×41 GeV': '/analysis/campaign-2025-08/acceptance/5x41/',
  '10×100 GeV': '/analysis/campaign-2025-08/acceptance/10x100/',
  '10×130 GeV': '/analysis/campaign-2025-08/acceptance/10x130/',
  '18×275 GeV': '/analysis/campaign-2025-08/acceptance/18x275/'
}
</script>

# Acceptance Analysis

This page shows acceptance plots for Lambda decay products across different beam energies.

<PlotCompareViewer :sources="sources">

## Primary vs Secondary Particles

### Decay Points Distribution

<VerticalComparePlot
  plot-name="01_primary_vs_secondary_decay_points.png"
  title="Primary vs Secondary Decay Points"
  description="Spatial distribution of decay points for primary and secondary particles in the detector."
/>

### Birth Points Distribution

<VerticalComparePlot
  plot-name="02_primary_vs_secondary_birth_points.png"
  title="Primary vs Secondary Birth Points"
  description="Spatial distribution of birth points for primary and secondary particles."
/>

## Lambda Decay Analysis

### Primary Lambda Decay Z Distribution

<VerticalComparePlot
  plot-name="03_primary_lambda_decay_z_distribution.png"
  title="Primary Lambda Decay Z Distribution"
  description="Distribution of Lambda decay vertices along the beam axis (Z)."
/>

### Lambda Decay Points (3D)

<VerticalComparePlot
  plot-name="04_lambda_decay_points.png"
  title="Lambda Decay Points"
  description="Three-dimensional visualization of Lambda decay vertices in the detector."
/>

### Undecayed Primary Lambdas

<VerticalComparePlot
  plot-name="undecayed_primary_lambdas.png"
  title="Undecayed Primary Lambdas"
  description="Distribution of Lambda particles that did not decay within the detector acceptance."
/>

## Proton-Pion Decay Channel

### Decay Points

<VerticalComparePlot
  plot-name="05_proton_pion_decay_points.png"
  title="Proton-Pion Decay Points"
  description="Spatial distribution of proton-pion pairs from Lambda decay."
/>

### Trajectories

<VerticalComparePlot
  plot-name="06_proton_pion_trajectories.png"
  title="Proton-Pion Trajectories"
  description="Visualization of proton and pion trajectories from Lambda decay."
/>

## Proton Analysis

### End Points Distribution

<VerticalComparePlot
  plot-name="10_proton_end_points.png"
  title="Proton End Points"
  description="Spatial distribution where protons stop or exit the detector."
/>

### Trajectory Histogram

<VerticalComparePlot
  plot-name="08_proton_trajectory_histogram.png"
  title="Proton Trajectory Histogram"
  description="Histogram of proton trajectory lengths and angular distributions."
/>

## Pion Analysis

### End Points Distribution

<VerticalComparePlot
  plot-name="07_pion_end_points.png"
  title="Pion End Points"
  description="Spatial distribution where pions stop or exit the detector."
/>

### Trajectory Histogram

<VerticalComparePlot
  plot-name="09_pion_trajectory_histogram.png"
  title="Pion Trajectory Histogram"
  description="Histogram of pion trajectory lengths and angular distributions."
/>

## Neutron-Pi0 Decay Channel

### Decay Points

<VerticalComparePlot
  plot-name="11_neutron_pizero_decay_points.png"
  title="Neutron-Pi0 Decay Points"
  description="Spatial distribution of neutron-pi0 pairs from Lambda decay."
/>

### Trajectories

<VerticalComparePlot
  plot-name="12_neutron_pizero_trajectories.png"
  title="Neutron-Pi0 Trajectories"
  description="Visualization of neutron and pi0 trajectories from Lambda decay."
/>

### Pi0 Decay Points

<VerticalComparePlot
  plot-name="13_pizero_decay_points.png"
  title="Pi0 Decay Points"
  description="Spatial distribution of pi0 decay vertices."
/>

## Neutron Analysis

### End Points Distribution

<VerticalComparePlot
  plot-name="15_neutron_end_points.png"
  title="Neutron End Points"
  description="Spatial distribution where neutrons are absorbed or exit the detector."
/>

### Trajectory Histogram

<VerticalComparePlot
  plot-name="16_neutron_trajectory_histogram.png"
  title="Neutron Trajectory Histogram"
  description="Histogram of neutron trajectory lengths and angular distributions."
/>

## Pi0 Analysis

### Trajectory Histogram

<VerticalComparePlot
  plot-name="17_pizero_trajectory_histogram.png"
  title="Pi0 Trajectory Histogram"
  description="Histogram of pi0 trajectory lengths and angular distributions."
/>

## Photon Analysis

### End Points Distribution

<VerticalComparePlot
  plot-name="14_gamma_end_points.png"
  title="Photon End Points"
  description="Spatial distribution where photons are absorbed or exit the detector."
/>

</PlotCompareViewer>

## Notes

- Use the **global selector** at the top to view all plots for a specific energy or compare two energies
- Each plot also has an **individual selector** if you want to view different energies for different plots
- The comparison modes show plots side by side for easy comparison
- All plots are generated from Monte Carlo simulations of Lambda production and decay in the EIC detector
