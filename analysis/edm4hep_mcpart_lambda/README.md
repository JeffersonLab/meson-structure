# edm4hep_mcpart_lambda

MC truth Lambda decay analysis directly from EDM4HEP/EDM4EIC files.
Produces a ROOT file with histograms and a flat `TTree`, plus PNG images of every histogram — no CSV step required.

This is the ROOT-native counterpart of [`csv_convert/csv_mcpart_lambda.cxx`](../../csv_convert/csv_mcpart_lambda.cxx) + [`analysis/csv_mcpart_lambda/lambda_decay.py`](../csv_mcpart_lambda/lambda_decay.py).

## Output

All output goes into a single directory:

```
<output_dir>/
  mcpart_lambda.root   # TTree (lambda_decays) + all histograms
  h_lam_p.png
  h_lam_pt.png
  h_lam_decay_rz.png
  ...                  # ~30 PNGs total
```

### TTree columns

Same schema as `*.mcpart_lambda.csv`. One row per Lambda found in MCParticles.
Columns: `event`, `lam_is_first`, `lam_decay`, then 15 fields per particle with prefixes
`lam`, `prot`, `pimin`, `neut`, `pizero`, `gamone`, `gamtwo`
(fields: `_id _pdg _gen _sim _px _py _pz _vx _vy _vz _epx _epy _epz _time _nd`).

`lam_decay` values: `0` = no decay, `1` = p+π⁻, `2` = n+π⁰, `3` = shower/recharge, `4` = other.

### Histograms

| Group | Histograms |
|---|---|
| Λ kinematics | \|p\|, pT, pz, η, φ, mass |
| Λ decay | decay type, N daughters |
| Λ decay vertex | z, r, r-vs-z (2D), x-vs-y (2D) |
| Λ correlations (2D) | \|p\| vs η, pT vs η, pz vs pT |
| Proton (p+π⁻) | \|p\|, pT, η |
| π⁻ (p+π⁻) | \|p\|, pT, η |
| Neutron (n+π⁰) | \|p\|, pT, η |
| π⁰ (n+π⁰) | \|p\|, pT |
| γ from π⁰ | energy, η |
| p+π⁻ derived | opening angle, invariant mass (peaks at Λ mass) |
| Λ generator status | status code distribution |

## Usage

### ROOT macro (no compilation needed)

```bash
# single file
root -x -l -b -q 'mcpart_lambda.cxx("input.edm4hep.root","output_dir")'

# multiple files, comma-separated, limit to 5000 events
root -x -l -b -q 'mcpart_lambda.cxx("f1.root,f2.root","output_dir",5000)'
```

### Compiled

```bash
mkdir build && cd build
cmake .. && make
./mcpart_lambda -o output_dir input1.root input2.root
./mcpart_lambda -n 5000 -o output_dir input1.root
```

### Dependencies

`ROOT`, `podio`, `EDM4HEP`, `EDM4EIC`, `fmt` — all available in `eicweb/eic_xl:nightly`.
