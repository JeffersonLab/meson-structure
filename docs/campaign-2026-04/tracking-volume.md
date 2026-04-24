<script setup>
const sources = {
  '10x100 GeV':  '/analysis/campaign-2026-04/tracking-volume/longtv-10x100/',
  '10x130 GeV':  '/analysis/campaign-2026-04/tracking-volume/longtv-10x130/',
  '18x275 GeV':  '/analysis/campaign-2026-04/tracking-volume/longtv-18x275/'
}
</script>

# New tracking volume Λ decays

Test of new tracking volume setting.

See the [campaign index](./campaign-2026-04.md) for bug context and variant
definitions.

All plots are produced by `analysis/acceptance/plot_lambda_endpoints.py`,
filtered to `lam_is_first == 1` (primary = Sullivan lambdas), and grouped by daughter count
`nd ∈ {0, 1, 2, ≥3, any}`.

<PlotCompareViewer :sources="sources">

## I.The most explanatory plots

### Decay types

Decay types are determined by MCParticle daughters of the primary lambdas coming from the interaction point. 
(Primary = from Sullivan process)

During analysis we calculate daughters and what are the daughters: 

- `0` no daughters
- `1`&`2` 2 daughters pπ- or nπ0 - anticipated lambda decays
- `3` >2 daughters
- `4/5/6/7` 1 daughter p / π+ / n / π0
- `8` other - non-standard 1- or 2-daughter combination

<VerticalComparePlot
  plot-name="lam_decay_counts.png"
  title="Primary Λ decay codes — counts per category"
/>

### Endpoint Z & Angle

<VerticalComparePlot
  plot-name="lam_endpoints_z1d_overlay.png"
  title="Λ endpoint Z — by number of daughters"
  description="Step histograms per daughter-count category plus a dashed outline for the combined sample."
/>

<VerticalComparePlot
  plot-name="lam_endpoints_z1d_nd2.png"
  title="Λ endpoint Z for lambdas with 2 daughters"
/>

<VerticalComparePlot
  plot-name="lam_angle_theta.png"
  title="Λ angle θ with Z+ (mrad)"
/>

### Endpoint in ZX and ZY

<VerticalComparePlot
  plot-name="lam_endpoints_zx_scatter.png"
  title="Scatter. Primary Λ endpoint ZX — coloured by n daughters"
  description="Per-event scatter of Λ endpoints in the ZX plane. Colour encodes number of recorded daughters (0, 1, 2, ≥3)."
/>

<VerticalComparePlot
  plot-name="lam_endpoints_zy_scatter.png"
  title="Scatter. Primary Λ endpoint ZY — coloured by n daughters"
/>

## II. 1-D Λ endpoint Z distributions

Λ endpoint Z corresponds to `MCParticle.endpoint.z` of lambdas. 
I.e. the point where Geant4 decayed lambdas. 

These plots just use number of daughters, not categories like above. 

### Λ endpoint Z 1D (all)

<VerticalComparePlot
  plot-name="lam_endpoints_z1d_overlay.png"
  title="Λ endpoint Z — categories overlaid"
  description="Step histograms per daughter-count category plus a dashed outline for the combined sample."
/>


### Λ endpoint Z 1D by N-daughters

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


## IV. ZX plane (EIC detector overlay)

### ZX Scatter — by daughter count

<VerticalComparePlot
  plot-name="lam_endpoints_zx_scatter.png"
  title="Scatter. Primary Λ endpoint ZX — coloured by n daughters"
  description="Per-event scatter of Λ endpoints in the ZX plane. Colour encodes number of recorded daughters (0, 1, 2, ≥3)."
/>


### ZX 2D histograms

<VerticalComparePlot
  plot-name="lam_endpoints_zx_hist2d_ndany.png"
  title="ZX endpoint density — any nd"
/>


<VerticalComparePlot
  plot-name="lam_endpoints_zx_hist2d_nd0.png"
  title="ZX endpoint density — nd = 0 (undecayed)"
  description="Primary Λ with no recorded daughters."
/>



<VerticalComparePlot
  plot-name="lam_endpoints_zx_hist2d_nd1.png"
  title="ZX endpoint density — nd = 1"
/>


<VerticalComparePlot
  plot-name="lam_endpoints_zx_hist2d_nd2.png"
  title="ZX endpoint density — nd = 2"
  description="Canonical two-body Λ decay topology (p π- or n π0)."
/>



<VerticalComparePlot
  plot-name="lam_endpoints_zx_hist2d_nd3plus.png"
  title="ZX endpoint density — nd ≥ 3"
/>

## V. ZY plane

### ZY 2D Scatter

<VerticalComparePlot
  plot-name="lam_endpoints_zy_scatter.png"
  title="Scatter. Primary Λ endpoint ZY — coloured by n daughters"
/>

### ZY 2D Histograms

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

### ZR 2D Scatter

<VerticalComparePlot
  plot-name="lam_endpoints_zr_scatter.png"
  title="Primary Λ endpoint Z vs. -R — coloured by n daughters"
/>

### ZR 2D Histograms

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
