# Data
*(last update of July 2026 — [campaign 2026-07](https://jeffersonlab.github.io/meson-structure/campaign-2026-07/campaign-2026-07.html))*

## Location
Campaign 2026-07 introduces the new `9xN` energy scheme (5x41, 9x100, 9x130,
9x275 GeV) for the EIC early-science program. 

> For machine-background-mixed data, see the
> [Machine background (2026-06)](#machine-background-2026-06) section below.

Reconstruction-based analyses can use `reco` / `csv_reco` directly.

On JLab ifarm:

```bash
/work/eic3/users/romanov/meson-structure-2026-07
```

On XRootD (open for universities and public)

```bash
xrdfs root://dtn-eic.jlab.org
ls /work/eic3/users/romanov/meson-structure-2026-07
```


Subdirectories (per-energy dirs `5x41`, `9x100`, `9x130`, `9x275`; files named
`msf_ev1000_NNNN.*`) :

- `afterburner` — eg output with crossing-angle + beam effects
- `bg_merged`   — Afterburner + background merged
- `dd4hep`      — DD4hep full simulation (`*.edm4hep.root`; ~5.0 TB, ~1000 files/energy)
- `reco`        — EICrecon reconstruction of `dd4hep` (`*.edm4eic.root`; ~2.2 TB, ~1000 files/energy)
- `csv_dd4hep`  — acceptance / MC-truth CSVs from `dd4hep` (~21 GB)
- `csv_reco`    — reconstruction CSVs from `reco` (`*.mc_dis.csv`, `*.reco_dis.csv`, `*.mcpart_lambda.csv`, `*.reco_ff_lambda.csv`; ~1.2 GB)
- `eg-split`, `eg-hepmc`, `eg-original-2026-06` — event-generator inputs

1000 events per file (~1000 files per energy)

```bash
# available throuhg xrdfs root://dtn-eic.jlab.org
/work/eic/users/romanov/meson-structure-2026-07/eg-hepmc
/work/eic/users/romanov/meson-structure-2026-07/eg-original-2026-06
/work/eic/users/romanov/meson-structure-2026-07/eg-split
/work/eic/users/romanov/meson-structure-2026-07/afterburner
/work/eic/users/romanov/meson-structure-2026-07/bg_merged
/work/eic/users/romanov/meson-structure-2026-07/dd4hep
/work/eic/users/romanov/meson-structure-2026-07/reco
/work/eic/users/romanov/meson-structure-2026-07/csv_dd4hep
/work/eic/users/romanov/meson-structure-2026-07/csv_for_ai
/work/eic/users/romanov/meson-structure-2026-07/csv_reco
/work/eic/users/romanov/meson-structure-2026-07/analysis
/work/eic/users/romanov/meson-structure-2026-07/datasets-no-background
```

Per-energy `.root` counts / sizes:

| Energy | `dd4hep` (`.edm4hep.root`) | `reco` (`.edm4eic.root`) |
| ------ | ------------------------: | -----------------------: |
| 5x41   | 998 (647 GB)              | 998 (472 GB)             |
| 9x100  | 1000 (1.4 TB)             | 999 (718 GB)             |
| 9x130  | 1000 (1.7 TB)             | 1000 (421 GB)            |
| 9x275  | 1000 (1.4 TB)             | 1000 (630 GB)            |


## Machine background (2026-06)

Machine-background-mixed data comes from campaign
[2026-06](https://jeffersonlab.github.io/meson-structure/campaign-2026-06/campaign-2026-06.html),
where the afterburned signal is mixed with the official ePIC background cocktails
(`synrad`, `ebrems`, `ecoulomb`, `etouschek`) via `SignalBackgroundMerger` into
2 µs timeframes (one signal per frame), then run through npsim with status-offset
flags. See **[Backgrounds in ePIC simulation](./background.md)** for the full
mechanism.

> (!) The background datasets use the **old energy scheme** `10x100, 10x130,
> 18x275` (5x41 is skipped) and 5000 events per fil, named `k_lambda_{beam}_5000evt_NNNN.*`.

On JLab ifarm, under `/work/eic3/users/romanov/meson-structure-2026-06`:

- `bg_merged`             — `SignalBackgroundMerger` output (`*.bg.hepmc3.tree.root`; the merged input to npsim; ~5.0 TB, 200 files/energy)
- `dd4hep-background`     — DD4hep on the background-merged input (`*.edm4hep.root`; ~12 TB)
- `reco-background`       — EICrecon reconstruction of `dd4hep-background` (`*.edm4eic.root`; ~4.1 TB, partial)
- `csv_dd4hep-background` — acceptance / combinatorics CSVs from `dd4hep-background` (~9.1 GB)

Per-energy `.root` file counts (background):

| Energy | `bg_merged` | `dd4hep-background` | `reco-background` |
| ------ | ----------: | ------------------: | ----------------: |
| 10x100 | 200         | 133                 | 68                |
| 10x130 | 200         | 200                 | 43                |
| 18x275 | 200         | 200                 | 107               |

```bash
xrdfs root://dtn-eic.jlab.org
ls /work/eic3/users/romanov/meson-structure-2026-06/reco-background
```

> Campaign 2026-06 also produced non-background flavors (`dd4hep-official`,
> `dd4hep-saveall`, `dd4hep-stv`, and their `reco`/`csv`) — see the
> [campaign 2026-06](https://jeffersonlab.github.io/meson-structure/campaign-2026-06/campaign-2026-06.html)
> page.


## Accessing Data with XRootD

The data is available remoutly through XRootD via:  

```
root://dtn-eic.jlab.org
```

**To browse the available files** one can use `xrdfs` command:

```bash
xrdfs root://dtn-eic.jlab.org
ls /volatile/eic/romanov/meson-structure-2026-03/reco
```

**To download** files: 

```bash
xrdcp root://dtn-eic.jlab.org//volatile/eic/romanov/meson-structure-2026-03/reco/5x41-priority/k_lambda_5x41_5000evt_001.edm4eic.root ./
```

**To use directly in scripts**:

```python
# Both uproot and pyroot can work with links directly 
# if XRootD is installed in the system
import uproot
file = uproot.open("root://dtn-eic.jlab.org//volatile/eic/romanov/meson-structure-2026-03/reco/5x41-priority/k_lambda_5x41_5000evt_001.edm4eic.root")
```
