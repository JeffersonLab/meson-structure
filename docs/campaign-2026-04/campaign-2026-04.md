# Campaign 2026-04

Unlike the other campaigns, this one is not a full production run. It is a
focused investigation into two Lambda-related MCParticle bugs affecting the
ePIC + DD4hep simulation chain.

## Bugs under investigation

1. **MCParticle endpoints / daughter tree wrong for Lambdas**
   [eic/epic#1069](https://github.com/eic/epic/issues/1069)

2. **Tracking-volume G4 handler drops Lambda decay info**
   [eic/epic#1081 (review)](https://github.com/eic/epic/pull/1081#pullrequestreview-4143804432)

The symptom in both cases is the same: primary Lambdas in the output MC record
either have no daughters, have wrong endpoint coordinates, or are replaced by a
shower-like daughter list — which breaks any downstream analysis that follows
the `Λ -> p π-` or `Λ -> n π0` decay chain.

## Variants produced

Only DD4hep + afterburner were re-run; no full reconstruction. The runs differ
only in how the Geant4 tracking-volume handler and the `--part.keepAllParticles`
flag are configured:

| Folder tag   | What was changed                                                        |
|--------------|-------------------------------------------------------------------------|
| `saveall`    | `--part.keepAllParticles=True` (does not actually work due to DD4hep bug) |
| `notv2`      | Tracking-volume G4 handler switched off -> true "save all" behaviour    |
| `notw`       | Same as `notv2` (handler off)                                           |
| `longtv`     | Updated, longer tracking volume from the issue above                    |

## Data location (ifarm)

```
/work/eic/users/romanov/meson-structure-2026-04-check/
    afterburner/
    dd4hep_2026-03/
    dd4hep_26-04/
    dd4hep_26-04_notv2/
    dd4hep_26-04_saveall/
    dd4hep_26-04_longtv/
    dd4hep_26-04_notw/
    dd4hep_26-03_saveall/
    ana_26-04/
    ana_26-04_notv2/
    csv_dd4hep_26-04_notv2/
```

## Reports

- [Tracking volume (saveall variant)](./tracking-volume.md)
- [Tracking volume comparison — saveall vs longtv](./tracking-volume-comparison.md) *(pending data regen)*
