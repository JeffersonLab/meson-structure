#!/usr/bin/env python3
"""MC DIS plots from per-energy CSV.

Run standalone:
    python runner.py --energy 10x100 \
        --csv-dir /path/to/csv_dd4hep/10x100 --outdir /tmp/test
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

runner_dir = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--energy", required=True,
                        help="Used for output naming; the script regex-extracts it.")
    parser.add_argument("--csv-dir", type=Path, required=True,
                        help="Directory containing *.mc_dis.csv files.")
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--bins", type=int, default=500)
    parser.add_argument("--dpi", type=int, default=150)
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    files = sorted(args.csv_dir.glob("*.mc_dis.csv"))
    if not files:
        print(f"[runner] no *.mc_dis.csv in {args.csv_dir}", file=sys.stderr)
        sys.exit(1)

    cmd = [
        sys.executable, str(runner_dir / "plot_mc.py"),
        "--outdir", str(args.outdir),
        "--bins", str(args.bins),
        "--dpi", str(args.dpi),
        *map(str, files),
    ]
    print(f"[runner] running on {len(files)} files", flush=True)
    subprocess.run(cmd, check=True, cwd=runner_dir)


if __name__ == "__main__":
    main()
