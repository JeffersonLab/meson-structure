# Data
*(last update of November 2026 — [campaign 2026-11](https://jeffersonlab.github.io/meson-structure/campaign-2026-11/campaign-2026-11.html))*

## Timeframe data (2026-11)

Campaign [2026-11](https://jeffersonlab.github.io/meson-structure/campaign-2026-11/campaign-2026-11.html)
is the streaming-readout study set: 40k K⁺Λ events per energy (9x100, 9x130,
9x275; 5x41 signal only) simulated alone through Geant4 and mixed after
Geant4 by TimeframeBuilder with the official ePIC background cocktails. It
stops at EDM4hep (no `reco`, no CSV). Image `eic_xl:26.11-stable`.

On JLab ifarm:

```bash
/work/eic3/users/romanov/meson-structure-2026-11
  dd4hep/<E>/           # signal only, 80 files x 500 events per energy (*.edm4hep.root)
  dd4hep-tfb2us/<E>/    # 2 us frames: one signal at a random crossing + background, 500 frames per file
  dd4hep-tfb200ns/<E>/  # 200 ns "found event" frames: signal pinned at t = 0 + background, 500 frames per file
/work/eic3/users/romanov/background-only-2026-11
  frames-2us/<E>/       # background-only 2 us frames, 80 files x 500 frames per energy
  pools/<E>/<source>/   # per-source Geant4 pools the frames are built from
```

Frame files carry the ePIC status offsets per background source (2000 SynRad,
3000 e-gas, 4000 Coulomb, 5000 Touschek, 6000 p-gas) and a `SubEventHeaders`
collection listing every sub-event with its time offset; see
[Backgrounds in ePIC simulation](./background.md). File counts and sizes are
filled in when the production finishes.

## Location (2026-07)
Campaign 2026-07 introduces the new `9xN` energy scheme (5x41, 9x100, 9x130,
9x275 GeV) for the EIC early-science program. 

> For machine-background-mixed data, see the
> [Machine background (2026-06)](#machine-background-2026-06) section below.

Reconstruction-based analyses can use `reco` / `csv_reco` directly.

On JLab ifarm:

```bash
/work/eic3/users/romanov/meson-structure-2026-07
```

XRootD: not exported from the new public door (see
[Accessing Data with XRootD](#accessing-data-with-xrootd)).


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
# on ifarm (not exported through XRootD, see below)
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


> Campaign 2026-06 also produced non-background flavors (`dd4hep-official`,
> `dd4hep-saveall`, `dd4hep-stv`, and their `reco`/`csv`) — see the
> [campaign 2026-06](https://jeffersonlab.github.io/meson-structure/campaign-2026-06/campaign-2026-06.html)
> page.


## Accessing Data with XRootD

> (!) `dtn-eic.jlab.org` is retired (it no longer resolves, checked 2026-10-14).
> The public JLab door is now `root://dtn2304.jlab.org:8443/` and it exports
> `/jlab-osdf-ro/eic/EPIC/{volatile,cache,work}` only — the user campaign
> directories under `/work/eic3/users/romanov` are **not** reachable through
> it. Use the ifarm paths above on the JLab farm, or ask for a copy. The
> `xrdfs`/`xrdcp` examples below are kept for the exported ePIC directories.
> The door needs an XRootD 5.9+ client (the `eic_xl` images have it).

**To browse the exported files** one can use `xrdfs` command:

```bash
xrdfs root://dtn2304.jlab.org:8443/
ls /jlab-osdf-ro/eic/EPIC/volatile/EVGEN/BACKGROUNDS
```

**To download** files: 

```bash
xrdcp root://dtn2304.jlab.org:8443//jlab-osdf-ro/eic/EPIC/volatile/EVGEN/BACKGROUNDS/BEAMGAS/electron/coulomb/EIC_ESR_Xsuite/dataprod_rel_1.0.1/10x275/10000Ahr/MachineRuntime50s/dataprod_rel_1.0.1_electron_coulomb_10x275_10000Ahr.hepmc3.tree.root ./
```

**To use directly in scripts**:

```python
# Both uproot and pyroot can work with links directly 
# if XRootD is installed in the system
import uproot
file = uproot.open("root://dtn2304.jlab.org:8443//jlab-osdf-ro/eic/EPIC/volatile/EVGEN/BACKGROUNDS/BEAMGAS/electron/coulomb/EIC_ESR_Xsuite/dataprod_rel_1.0.1/10x275/10000Ahr/MachineRuntime50s/dataprod_rel_1.0.1_electron_coulomb_10x275_10000Ahr.hepmc3.tree.root")
```
