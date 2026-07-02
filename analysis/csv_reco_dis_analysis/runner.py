#!/usr/bin/env python3
"""Reco DIS analyses from per-energy `*.reco_dis.csv`.

Wraps the standalone plotters in this folder that share the same
`<csv> ... -o <dir>` CLI and read `*.reco_dis.csv`:
  - reco_dis_all.py          all-column histograms
  - scattered_electron.py    scattered-electron kinematics
  - t_analysis.py            t-value focused analysis
  - csv_reco_dis_analysis.py generic histograms from csv_reco_dis.cxx output
  - beam_t_error.py          beam-angle / t-error analysis

`csv_gregory.py` is intentionally NOT run here: it needs matched
`mc_dis.csv`/`reco_dis.csv` pairs and validates the pairing strictly; run it
standalone when both tables are complete.

Empty CSV chunks are skipped. If no non-empty `*.reco_dis.csv` exist, the runner
exits 0 with a message (nothing to do) rather than failing — the 2026-07
`reco_dis.csv` tables were produced empty upstream and need regenerating.

Run standalone:
    python runner.py --energy 9x275 \
        --csv-dir /path/to/csv_reco/9x275 --outdir /tmp/test
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

runner_dir = Path(__file__).resolve().parent

SCRIPTS: list[str] = [
    "reco_dis_all.py",
    "scattered_electron.py",
    "t_analysis.py",
    "csv_reco_dis_analysis.py",
    "beam_t_error.py",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--energy", required=True, help="Used for output naming.")
    parser.add_argument("--csv-dir", type=Path, required=True,
                        help="Directory with *.reco_dis.csv files (csv_reco).")
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--max-files", type=int, default=0,
                        help="Cap on input CSVs (0 = no cap).")
    parser.add_argument("--only", default="all",
                        help="Comma-separated subset of script stems, or 'all'.")
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)

    # Only non-empty chunks (2026-07 reco_dis.csv were written empty upstream).
    files = [p for p in sorted(args.csv_dir.glob("*.reco_dis.csv")) if p.stat().st_size > 0]
    if args.max_files and args.max_files > 0:
        files = files[: args.max_files]

    if not files:
        print(f"[runner] no non-empty *.reco_dis.csv in {args.csv_dir} — nothing to do "
              f"(regenerate csv_reco?)", file=sys.stderr)
        return

    if args.only == "all":
        wanted = list(SCRIPTS)
    else:
        req = {s.strip() for s in args.only.split(",") if s.strip()}
        wanted = [s for s in SCRIPTS if Path(s).stem in req or s in req]

    print(f"[runner] {args.energy}: {len(files)} non-empty reco_dis.csv files", flush=True)
    failures: list[str] = []
    for script in wanted:
        sub_outdir = args.outdir / Path(script).stem
        sub_outdir.mkdir(parents=True, exist_ok=True)
        cmd = [sys.executable, str(runner_dir / script),
               *map(str, files), "-o", str(sub_outdir)]
        print(f"[runner] {script} -> {sub_outdir}", flush=True)
        proc = subprocess.run(cmd, cwd=runner_dir)
        if proc.returncode != 0:
            failures.append(script)

    if failures:
        print(f"[runner] failed: {failures}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
