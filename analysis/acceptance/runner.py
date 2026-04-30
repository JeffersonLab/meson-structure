#!/usr/bin/env python3
"""Per-energy detector-acceptance plots.

Each per-energy CSV directory contains hundreds of per-chunk files. The
plotters each take ONE CSV, so this runner concatenates the matching
chunks (header-stable text concat) into `<outdir>/<plotter>/_merged.csv`
and feeds that to the plotter.

Wraps three plotters that share the same `<csv> -o <dir>` CLI:
  - plot_detector_acceptance.py  <- *.acceptance_ppim.csv
  - plot_proton_hits.py          <- *.acceptance_ppim_prot_hits.csv
  - plot_pion_hits.py            <- *.acceptance_ppim_pimin_hits.csv

Run standalone:
    python runner.py --energy 10x100 \
        --csv-dir /path/to/csv_dd4hep_saveall/10x100 \
        --outdir /tmp/test --max-files 20
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

runner_dir = Path(__file__).resolve().parent

# script_filename -> CSV glob to feed it (per docs/data-csv.md)
SCRIPTS: dict[str, str] = {
    "plot_detector_acceptance.py": "*.acceptance_ppim.csv",
    "plot_proton_hits.py":         "*.acceptance_ppim_prot_hits.csv",
    "plot_pion_hits.py":           "*.acceptance_ppim_pimin_hits.csv",
}


def find_csvs(csv_dir: Path, pattern: str, max_files: Optional[int]) -> list[Path]:
    """Return matching CSVs, excluding .zip companions, capped at max_files."""
    matches = [p for p in sorted(csv_dir.glob(pattern)) if p.suffix == ".csv"]
    if max_files is not None and max_files > 0:
        matches = matches[:max_files]
    return matches


def merge_csvs(files: list[Path], dest: Path) -> int:
    """Concatenate CSVs assuming identical headers. Returns total data rows."""
    rows = 0
    with dest.open("w", encoding="utf-8", newline="") as out:
        for i, src in enumerate(files):
            with src.open("r", encoding="utf-8", newline="") as f:
                header = f.readline()
                if i == 0:
                    out.write(header)
                for line in f:
                    out.write(line)
                    rows += 1
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--energy", required=True)
    parser.add_argument("--csv-dir", type=Path, required=True,
                        help="Directory with per-chunk acceptance_ppim*.csv files.")
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--only", default="all",
                        help="Comma-separated subset (plot_detector_acceptance, "
                             "plot_proton_hits, plot_pion_hits) or 'all'.")
    parser.add_argument("--max-files", type=int, default=0,
                        help="Cap on chunks to merge per plotter (0 = no cap).")
    parser.add_argument("--keep-merged", action="store_true",
                        help="Keep the merged CSV after plotting (for debugging).")
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)

    if args.only == "all":
        wanted = set(SCRIPTS.keys())
    else:
        requested = {s.strip() for s in args.only.split(",") if s.strip()}
        wanted = {s for s in SCRIPTS
                  if Path(s).stem in requested or s in requested}
        if not wanted:
            print(f"[runner] --only={args.only!r} matched none of: "
                  f"{sorted(Path(s).stem for s in SCRIPTS)}", file=sys.stderr)
            sys.exit(2)

    max_files = args.max_files or None
    failures: list[str] = []

    for script, pattern in SCRIPTS.items():
        if script not in wanted:
            continue

        files = find_csvs(args.csv_dir, pattern, max_files)
        if not files:
            print(f"[runner] skip {script}: no CSV matching {pattern} in {args.csv_dir}",
                  file=sys.stderr)
            continue

        sub_outdir = args.outdir / Path(script).stem
        sub_outdir.mkdir(parents=True, exist_ok=True)
        merged = sub_outdir / "_merged.csv"

        print(f"[runner] {script}: merging {len(files)} chunks -> {merged}", flush=True)
        rows = merge_csvs(files, merged)
        print(f"[runner]   {rows} data rows", flush=True)

        cmd = [sys.executable, str(runner_dir / script),
               str(merged), "-o", str(sub_outdir)]
        print(f"[runner] {' '.join(cmd)}", flush=True)
        proc = subprocess.run(cmd, cwd=runner_dir)

        if not args.keep_merged:
            try:
                merged.unlink()
            except OSError:
                pass

        if proc.returncode != 0:
            failures.append(script)

    if failures:
        print(f"[runner] failed: {failures}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
