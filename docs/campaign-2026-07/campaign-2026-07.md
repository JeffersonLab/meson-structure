# Campaign 2026-06

This page documents the 2026-07 meson structure simulation campaign.

> (!) For the list of files go to [DATA PAGE](../data.md)


## Overview

The July 2026 campaign introduces new energy ranges
in compliance to EIC early science program
Energy ranges (all variants):

1. 5x41 GeV
2. 9x100 GeV
3. 9x130 GeV
4. 9x275 GeV

Statistics: 1000 events per job.

> (!) The `-background` variant skips 5x41 (no official 5x41 cocktail is
> published); see the cocktail table below.


## Variants in detail

Commands log 

```bash

# EG originals 


/w/eic-scshelf2104/users/romanov/meson-structure-2026-07/eg-original-2026-06/k_lambda_crossing_0.000-9.0on100.0_x0.0001-1.0000_q1.0-500.0.root  

/w/eic-scshelf2104/users/romanov/meson-structure-2026-07/eg-original-2026-06/k_lambda_crossing_0.000-9.0on130.0_x0.0001-1.0000_q1.0-500.0.root

/w/eic-scshelf2104/users/romanov/meson-structure-2026-07/eg-original-2026-06/k_lambda_crossing_0.000-9.0on275.0_x0.0001-1.0000_q1.0-500.0.root

# EG splitting section
/w/eic-scshelf2104/users/romanov/meson-structure-2026-07/eg-split/9x100
/w/eic-scshelf2104/users/romanov/meson-structure-2026-07/eg-split/9x130
/w/eic-scshelf2104/users/romanov/meson-structure-2026-07/eg-split/9x275

uv run 01_root_hepmc_klam_convert.py \
      --input-files /w/eic-scshelf2104/users/romanov/meson-structure-2026-07/eg-original-2026-06/k_lambda_crossing_0.000-9.0on100.0_x0.0001-1.0000_q1.0-500.0.root \
      --chunk-size 1000 \
      --events 10000000 \
      --output-prefix /w/eic-scshelf2104/users/romanov/meson-structure-2026-07/eg-split/9x100/msf_ev1000 \
      --events-per-file 1000

uv run 01_root_hepmc_klam_convert.py \
      --input-files /w/eic-scshelf2104/users/romanov/meson-structure-2026-07/eg-original-2026-06/k_lambda_crossing_0.000-9.0on130.0_x0.0001-1.0000_q1.0-500.0.root \
      --chunk-size 1000 \
      --events 10000000 \
      --output-prefix /w/eic-scshelf2104/users/romanov/meson-structure-2026-07/eg-split/9x130/msf_ev1000 \
      --events-per-file 1000

uv run 01_root_hepmc_klam_convert.py \
      --input-files /w/eic-scshelf2104/users/romanov/meson-structure-2026-07/eg-original-2026-06/k_lambda_crossing_0.000-9.0on275.0_x0.0001-1.0000_q1.0-500.0.root \
      --chunk-size 1000 \
      --events 10000000 \
      --output-prefix /w/eic-scshelf2104/users/romanov/meson-structure-2026-07/eg-split/9x275/msf_ev1000 \
      --events-per-file 1000
```
