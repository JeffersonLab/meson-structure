<script setup>
const sources = {
  '10x100 GeV':  '/analysis/campaign-2026-04/tracking-volume/longtv_10x100/',
  '10x130 GeV':  '/analysis/campaign-2026-04/tracking-volume/longtv_10x130/',
  '18x275 GeV':  '/analysis/campaign-2026-04/tracking-volume/longtv_18x275/'
}
</script>

# Tracking volume — `saveall` variant

Test of new tracking volume setting. 

See the [campaign index](./campaign-2026-04.md) for bug context and variant
definitions.

All plots are produced by `analysis/acceptance/plot_lambda_endpoints.py`,
filtered to `lam_is_first == 1`, and grouped by daughter count
`nd ∈ {0, 1, 2, ≥3, any}`.

<PlotCompareViewer :sources="sources">

## I. ZX plane (EIC detector overlay)

### Scatter — coloured by daughter count

<VerticalComparePlot
  plot-name="lam_endpoints_zx_scatter.png"
  title="Primary Λ endpoint ZX — coloured by n daughters"
  description="Per-event scatter of Λ endpoints in the ZX plane. Colour encodes number of recorded daughters (0, 1, 2, ≥3)."
/>

### 2-D histogram, all categories (any nd)

<VerticalComparePlot
  plot-name="lam_endpoints_zx_hist2d_ndany.png"
  title="ZX endpoint density — any nd"
/>

### 2-D histogram, nd = 0 (undecayed)

<VerticalComparePlot
  plot-name="lam_endpoints_zx_hist2d_nd0.png"
  title="ZX endpoint density — nd = 0"
  description="Primary Λ with no recorded daughters."
/>

### 2-D histogram, nd = 1

<VerticalComparePlot
  plot-name="lam_endpoints_zx_hist2d_nd1.png"
  title="ZX endpoint density — nd = 1"
/>

### 2-D histogram, nd = 2 (canonical two-body)

<VerticalComparePlot
  plot-name="lam_endpoints_zx_hist2d_nd2.png"
  title="ZX endpoint density — nd = 2"
  description="Canonical two-body Λ decay topology (p π- or n π0)."
/>

### 2-D histogram, nd ≥ 3 (showering)

<VerticalComparePlot
  plot-name="lam_endpoints_zx_hist2d_nd3plus.png"
  title="ZX endpoint density — nd ≥ 3"
/>

## II. ZY plane

### Scatter

<VerticalComparePlot
  plot-name="lam_endpoints_zy_scatter.png"
  title="Primary Λ endpoint ZY — coloured by n daughters"
/>

### 2-D histograms

<VerticalComparePlot
  plot-name="lam_endpoints_zy_hist2d_ndany.png"
  title="ZY endpoint density — any nd"
/>

<VerticalComparePlot
  plot-name="lam_endpoints_zy_hist2d_nd0.png"
  title="ZY endpoint density — nd = 0"
/>

<VerticalComparePlot
  plot-name="lam_endpoints_zy_hist2d_nd1.png"
  title="ZY endpoint density — nd = 1"
/>

<VerticalComparePlot
  plot-name="lam_endpoints_zy_hist2d_nd2.png"
  title="ZY endpoint density — nd = 2"
/>

<VerticalComparePlot
  plot-name="lam_endpoints_zy_hist2d_nd3plus.png"
  title="ZY endpoint density — nd ≥ 3"
/>

## III. ZR plane (EIC detector overlay, R = sqrt(X²+Y²))

### Scatter

<VerticalComparePlot
  plot-name="lam_endpoints_zr_scatter.png"
  title="Primary Λ endpoint ZR — coloured by n daughters"
  description="Radial view. Since R ≥ 0, only the upper half of the overlaid detector cross-section receives data points."
/>

### 2-D histograms

<VerticalComparePlot
  plot-name="lam_endpoints_zr_hist2d_ndany.png"
  title="ZR endpoint density — any nd"
/>

<VerticalComparePlot
  plot-name="lam_endpoints_zr_hist2d_nd0.png"
  title="ZR endpoint density — nd = 0"
/>

<VerticalComparePlot
  plot-name="lam_endpoints_zr_hist2d_nd1.png"
  title="ZR endpoint density — nd = 1"
/>

<VerticalComparePlot
  plot-name="lam_endpoints_zr_hist2d_nd2.png"
  title="ZR endpoint density — nd = 2"
/>

<VerticalComparePlot
  plot-name="lam_endpoints_zr_hist2d_nd3plus.png"
  title="ZR endpoint density — nd ≥ 3"
/>

## IV. 1-D Λ endpoint Z distributions

### Overlay (all categories on one figure)

<VerticalComparePlot
  plot-name="lam_endpoints_z1d_overlay.png"
  title="Λ endpoint Z — categories overlaid"
  description="Step histograms per daughter-count category plus a dashed outline for the combined sample."
/>

<VerticalComparePlot
  plot-name="lam_endpoints_z1d_overlay_log.png"
  title="Λ endpoint Z — categories overlaid (log y)"
/>

### Per category, with EIC image as a Z-landmark ribbon

<VerticalComparePlot
  plot-name="lam_endpoints_z1d_ndany.png"
  title="Λ endpoint Z — any nd"
/>

<VerticalComparePlot
  plot-name="lam_endpoints_z1d_nd0.png"
  title="Λ endpoint Z — nd = 0"
/>

<VerticalComparePlot
  plot-name="lam_endpoints_z1d_nd1.png"
  title="Λ endpoint Z — nd = 1"
/>

<VerticalComparePlot
  plot-name="lam_endpoints_z1d_nd2.png"
  title="Λ endpoint Z — nd = 2"
/>

<VerticalComparePlot
  plot-name="lam_endpoints_z1d_nd3plus.png"
  title="Λ endpoint Z — nd ≥ 3"
/>

## V. Λ polar angle with respect to +Z

The EIC hadron-beam crossing angle (25 mrad) is marked on both plots.

<VerticalComparePlot
  plot-name="lam_angle_theta.png"
  title="Primary Λ polar angle θ (mrad), categories overlaid"
/>

<VerticalComparePlot
  plot-name="lam_angle_theta_log.png"
  title="Primary Λ polar angle θ (mrad), log y"
/>

</PlotCompareViewer>
