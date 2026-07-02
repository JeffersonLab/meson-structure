#!/usr/bin/env python3
"""Antonio's per-energy acceptance / reco-comparison plots.

Wraps four standalone scripts, feeding each the CSVs it needs. Per-chunk CSVs are
concatenated (header-stable) into merged files under `<outdir>/_merged/`:

  - vertex_plots.py          <- acceptance_ppim.csv                 (vertex/kinematics)
  - pimin_acceptance_plots.py<- acceptance_ppim.csv + *_pimin_hits.csv (pair)
  - prot_acceptance_plots.py <- acceptance_ppim.csv + *_prot_hits.csv  (pair)
  - compare_reco_methods.py  <- reco_dis.csv                        (reco-vs-truth)

The acceptance tables live in `csv_dd4hep`; reco_dis lives in `csv_reco`. Any
plotter whose input is missing/empty is skipped (2026-07 `reco_dis.csv` were
produced empty upstream, so compare_reco is skipped until they are regenerated).

Run standalone:
    python runner.py --energy 9x275 \
        --csv-dd4hep-dir /path/to/csv_dd4hep/9x275 \
        --csv-reco-dir   /path/to/csv_reco/9x275 \
        --outdir /tmp/test --max-files 20
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Optional

runner_dir = Path(__file__).resolve().parent


def non_empty(csv_dir: Path, pattern: str, max_files: Optional[int]) -> list[Path]:
    files = [p for p in sorted(csv_dir.glob(pattern))
             if p.suffix == ".csv" and p.stat().st_size > 0]
    if max_files and max_files > 0:
        files = files[:max_files]
    return files


def merge_csvs(files: list[Path], dest: Path) -> int:
    """Concatenate CSVs assuming identical headers. Returns total data rows."""
    dest.parent.mkdir(parents=True, exist_ok=True)
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


def prepare(csv_dir: Path, pattern: str, dest: Path, max_files: Optional[int],
            label: str) -> Optional[Path]:
    """Merge matching non-empty chunks into `dest`; return it, or None if none."""
    files = non_empty(csv_dir, pattern, max_files)
    if not files:
        print(f"[runner] skip {label}: no non-empty {pattern} in {csv_dir}",
              file=sys.stderr)
        return None
    rows = merge_csvs(files, dest)
    print(f"[runner] {label}: merged {len(files)} chunks ({rows} rows) -> {dest}",
          flush=True)
    return dest


def run(script: str, args_list: list[str], sub_outdir: Path) -> Optional[str]:
    sub_outdir.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(runner_dir / script), *args_list, "-o", str(sub_outdir)]
    print(f"[runner] {script} -> {sub_outdir}", flush=True)
    proc = subprocess.run(cmd, cwd=runner_dir)
    return script if proc.returncode != 0 else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--energy", required=True, help="Used for output naming.")
    parser.add_argument("--csv-dd4hep-dir", type=Path, required=True,
                        help="Directory with acceptance_ppim*.csv (csv_dd4hep).")
    parser.add_argument("--csv-reco-dir", type=Path, default=None,
                        help="Directory with reco_dis.csv (csv_reco); optional.")
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--max-files", type=int, default=0,
                        help="Cap on chunks merged per input (0 = no cap).")
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    merged = args.outdir / "_merged"
    mf = args.max_files or None
    failures: list[str] = []

    # Acceptance tables (csv_dd4hep).
    acc = prepare(args.csv_dd4hep_dir, "*.acceptance_ppim.csv",
                  merged / "acceptance_ppim.csv", mf, "acceptance_ppim")
    pimin_hits = prepare(args.csv_dd4hep_dir, "*.acceptance_ppim_pimin_hits.csv",
                         merged / "pimin_hits.csv", mf, "pimin_hits")
    prot_hits = prepare(args.csv_dd4hep_dir, "*.acceptance_ppim_prot_hits.csv",
                        merged / "prot_hits.csv", mf, "prot_hits")

    if acc is not None:
        failures.append(run("vertex_plots.py", [str(acc)], args.outdir / "vertex"))
        if pimin_hits is not None:
            failures.append(run("pimin_acceptance_plots.py",
                                 [str(acc), str(pimin_hits)], args.outdir / "pimin"))
        if prot_hits is not None:
            failures.append(run("prot_acceptance_plots.py",
                                 [str(acc), str(prot_hits)], args.outdir / "prot"))

    # Reco-vs-truth comparison (csv_reco/reco_dis.csv), if available and non-empty.
    if args.csv_reco_dir is not None:
        reco = prepare(args.csv_reco_dir, "*.reco_dis.csv",
                       merged / "reco_dis.csv", mf, "reco_dis")
        if reco is not None:
            failures.append(run("compare_reco_methods.py", [str(reco)],
                                 args.outdir / "compare_reco"))

    failures = [f for f in failures if f]
    if failures:
        print(f"[runner] failed: {failures}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
