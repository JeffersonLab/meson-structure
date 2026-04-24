<script setup>
const sources = {
  'saveall 5x41':    '/analysis/campaign-2026-04/tracking-volume/saveall_5x41/',
  'longtv 5x41':     '/analysis/campaign-2026-04/tracking-volume/longtv_5x41/',
  'saveall 10x100':  '/analysis/campaign-2026-04/tracking-volume/saveall_10x100/',
  'longtv 10x100':   '/analysis/campaign-2026-04/tracking-volume/longtv_10x100/',
  'saveall 10x130':  '/analysis/campaign-2026-04/tracking-volume/saveall_10x130/',
  'longtv 10x130':   '/analysis/campaign-2026-04/tracking-volume/longtv_10x130/',
  'saveall 18x275':  '/analysis/campaign-2026-04/tracking-volume/saveall_18x275/',
  'longtv 18x275':   '/analysis/campaign-2026-04/tracking-volume/longtv_18x275/'
}
</script>

# Tracking volume comparison: saveall vs longtv

This page compares the two candidate fixes for the MCParticle Lambda bugs
(see the [campaign index](./campaign-2026-04.md) for bug links):

- **saveall** — runs with `--part.keepAllParticles=True` (tracking-volume
  handler ON, but the flag is supposed to preserve everything). Intended as
  the physics-correct baseline.
- **longtv** — runs with the new, extended tracking volume proposed in
  [eic/epic#1081](https://github.com/eic/epic/pull/1081#pullrequestreview-4143804432).
  Keeps the handler but makes the Λ decay region fit inside the volume so
  daughter particles are kept without the save-all crutch.

All plots are produced by
`analysis/acceptance/plot_lambda_endpoints.py` and show **primary Λ**
(`lam_is_first == 1`) endpoints, grouped by daughter count
`nd ∈ {0, 1, 2, ≥3, any}`.

> **How to read**
> Use the global selector at the top to switch everything to one energy or
> variant at once. Use the per-plot dropdown to pick any pair — in particular
> the `saveall X vs longtv X` comparisons show **saveall first, longtv below**,
> which is the intended reading order.

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
  description="Combined density of all primary Λ endpoints in the ZX plane."
/>

### 2-D histogram, nd = 0 (undecayed)

<VerticalComparePlot
  plot-name="lam_endpoints_zx_hist2d_nd0.png"
  title="ZX endpoint density — nd = 0"
  description="Primary Λ with no recorded daughters — indicates the particle left the simulated volume without decaying OR that the tracking-volume bug dropped its daughters."
/>

### 2-D histogram, nd = 1

<VerticalComparePlot
  plot-name="lam_endpoints_zx_hist2d_nd1.png"
  title="ZX endpoint density — nd = 1"
  description="Primary Λ with a single recorded daughter (partial-keep artefact)."
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
  description="Showering / re-interacting Λ endpoints."
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

## Notes

- The interesting regions to watch are (a) the **nd = 0** populations — ideally
  these concentrate far downstream or at world-volume boundaries, not inside
  the detector, and (b) the **nd ≥ 3** populations, which should be rare.
  A working fix moves events out of `nd = 0` and `nd ≥ 3` into `nd = 2`.
- The angular overlay is the cleanest sanity check: all variants must peak at
  25 mrad (hadron beam) and show consistent tails. Any big asymmetry between
  `saveall` and `longtv` there indicates a different kinematic pre-selection
  slipped in, not a tracking-volume effect.
