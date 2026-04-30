#!/usr/bin/env python3
"""Per-energy detector-acceptance plots.

Wraps three plotting scripts that each consume one CSV and produce plots:
  - plot_detector_acceptance.py    (acceptance/hits flags per event)
  - plot_pion_hits.py              (pion z vs x hit positions)
  - plot_proton_hits.py            (proton z vs x hit positions)

Each script gets the CSV that matches its filename glob in --csv-dir. If a
glob matches nothing, that script is skipped with a warning rather than
failing the whole run.

Run standalone:
    python runner.py --energy 10x100 \
        --csv-dir /path/to/csv_dd4hep/10x100 --outdir /tmp/test
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Optional

runner_dir = Path(__file__).resolve().parent

# script_filename -> default CSV glob to feed it
SCRIPTS: dict[str, str] = {
    "plot_detector_acceptance.py": "*acceptance*.csv",
    "plot_pion_hits.py":           "*pion*hits*.csv",
    "plot_proton_hits.py":         "*proton*hits*.csv",
}


def pick_csv(csv_dir: Path, pattern: str) -> Optional[Path]:
    matches = sorted(csv_dir.glob(pattern))
    if not matches:
        return None
    if len(matches) > 1:
        print(f"[runner] {pattern}: {len(matches)} matches, using {matches[0].name}",
              file=sys.stderr)
    return matches[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--energy", required=True)
    parser.add_argument("--csv-dir", type=Path, required=True,
                        help="Directory containing the per-energy acceptance/hit CSVs.")
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--only", default="all",
                        help="Comma-separated subset of script names "
                             "(plot_detector_acceptance, plot_pion_hits, plot_proton_hits) or 'all'.")
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)

    if args.only == "all":
        wanted = set(SCRIPTS.keys())
    else:
        requested = {s.strip() for s in args.only.split(",") if s.strip()}
        wanted = {s for s in SCRIPTS if Path(s).stem in requested or s in requested}
        if not wanted:
            print(f"[runner] --only={args.only!r} matched no known scripts: "
                  f"{list(SCRIPTS)}", file=sys.stderr)
            sys.exit(2)

    failures: list[str] = []
    for script, pattern in SCRIPTS.items():
        if script not in wanted:
            continue
        csv = pick_csv(args.csv_dir, pattern)
        if csv is None:
            print(f"[runner] skip {script}: no CSV matching {pattern} in {args.csv_dir}",
                  file=sys.stderr)
            continue

        sub_outdir = args.outdir / Path(script).stem
        sub_outdir.mkdir(parents=True, exist_ok=True)
        cmd = [sys.executable, str(runner_dir / script),
               str(csv), "-o", str(sub_outdir)]
        print(f"[runner] {' '.join(cmd)}", flush=True)
        proc = subprocess.run(cmd, cwd=runner_dir)
        if proc.returncode != 0:
            failures.append(script)

    if failures:
        print(f"[runner] failed: {failures}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
