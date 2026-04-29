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
only in how the Geant4 tracking-volume handler and the `--part.userParticleHandler=""`
flag are configured:

| Folder tag   | What was changed                                                        |
|--------------|-------------------------------------------------------------------------|
| `dd4hep_saveall`    | Save all particles |
| `dd4hep_26-03`    | Old (bugged) behavior    |
| `dd4hep`     | Updated (fixed), longer tracking volume from the issue above                    |

Directories `ana`,  `csv_dd4hep`, `csv_reco`, `reco` correspond to 
results from `dd4hep`, i.e. new fixed tracking volume data. 

## Data location (ifarm)

```
/work/eic/users/romanov/meson-structure-2026-04-check/
 
```

## Reports

- [Tracking volume (saveall variant)](./tracking-volume.md)

