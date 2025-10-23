# Campaign 2025-10

This page documents the 2025-10 meson structure simulation campaign.

> (!) For the list of files go to [DATA PAGE](../data.md) 


### Overview

This campaign:

- Includes 2025-10 EIC EPIC software stack


Energy ranges:

1. 5x41 GeV
2. 10x100 GeV
2. 10x130 GeV
3. 18x275 GeV

DIS parameters:

- `x= 0.0001 - 1.0000`
- `q2=1 - 500`

```bash
# Root directory
/volatile/eic/romanov/meson-structure-2025-10/

# Event generator root files
/volatile/eic/romanov/meson-structure-2025-08/eg-orig-kaon-lambda

# Event generator files in HepMC (split to 5000k events)
/volatile/eic/romanov/meson-structure-2025-08/eg-hepmc
```

Commands log

```bash
mkdir -p /volatile/eic/romanov/meson-structure-2025-10/
cp -r /volatile/eic/romanov/meson-structure-2025-08/eg-orig-kaon-lambda /volatile/eic/romanov/meson-structure-2025-10/
cp -r /volatile/eic/romanov/meson-structure-2025-08/eg-hepmc /volatile/eic/romanov/meson-structure-2025-10/

```
