<script setup>
const sources = {
  '10x100 GeV':  '/analysis/campaign-2026-04/tracking-volume/longtv-10x100/',
  '10x130 GeV':  '/analysis/campaign-2026-04/tracking-volume/longtv-10x130/',
  '18x275 GeV':  '/analysis/campaign-2026-04/tracking-volume/longtv-18x275/'
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

## I. Λ decay classification

Column chart of primary-Λ decay codes as written by the converter.
Codes match `csv_mcpart_lambda.cxx`:
`0` no daughters · `1` p π- · `2` n π0 · `3` >2 daughters ·
`4/5/6/7` single p / π+ / n / π0 · `8` other (non-standard 1- or 2-daughter
combination).

<VerticalComparePlot
  plot-name="lam_decay_counts.png"
  title="Primary Λ decay codes — counts per category"
/>

<VerticalComparePlot
  plot-name="lam_decay_counts_log.png"
  title="Primary Λ decay codes — counts per category (log y)"
/>

## II. 1-D Λ endpoint Z distributions

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

## III. Λ polar angle with respect to +Z

The EIC hadron-beam crossing angle (25 mrad) is marked on both plots.

<VerticalComparePlot
  plot-name="lam_angle_theta.png"
  title="Primary Λ polar angle θ (mrad), categories overlaid"
/>

<VerticalComparePlot
  plot-name="lam_angle_theta_log.png"
  title="Primary Λ polar angle θ (mrad), log y"
/>

## IV. ZX plane (EIC detector overlay)

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

### 2-D histogram, nd ≥ 3

<VerticalComparePlot
  plot-name="lam_endpoints_zx_hist2d_nd3plus.png"
  title="ZX endpoint density — nd ≥ 3"
/>

## V. ZY plane

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

## VI. Z vs. -R plane (EIC detector overlay, lower half)

R = sqrt(X² + Y²) is plotted with a minus sign so that points fall into the
lower half of the detector cross-section, which is where the hadron-beam
pipe bends.

### Scatter

<VerticalComparePlot
  plot-name="lam_endpoints_zr_scatter.png"
  title="Primary Λ endpoint Z vs. -R — coloured by n daughters"
/>

### 2-D histograms

<VerticalComparePlot
  plot-name="lam_endpoints_zr_hist2d_ndany.png"
  title="Z vs. -R endpoint density — any nd"
/>

<VerticalComparePlot
  plot-name="lam_endpoints_zr_hist2d_nd0.png"
  title="Z vs. -R endpoint density — nd = 0"
/>

<VerticalComparePlot
  plot-name="lam_endpoints_zr_hist2d_nd1.png"
  title="Z vs. -R endpoint density — nd = 1"
/>

<VerticalComparePlot
  plot-name="lam_endpoints_zr_hist2d_nd2.png"
  title="Z vs. -R endpoint density — nd = 2"
/>

<VerticalComparePlot
  plot-name="lam_endpoints_zr_hist2d_nd3plus.png"
  title="Z vs. -R endpoint density — nd ≥ 3"
/>

</PlotCompareViewer>
