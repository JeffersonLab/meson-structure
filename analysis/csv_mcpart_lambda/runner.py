#!/usr/bin/env python3
"""MC-truth Lambda plots from per-energy mcpart_lambda CSVs.

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
    parser.add_argument("--energy", required=True)
    parser.add_argument("--csv-dir", type=Path, required=True,
                        help="Directory with *.mcpart_lambda.csv (or fallback via --glob).")
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--events", "-n", type=int, default=None)
    parser.add_argument("--glob", dest="glob_pattern", default="*.mcpart_lambda.csv")
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    files = sorted(args.csv_dir.glob(args.glob_pattern))
    if not files:
        print(f"[runner] no {args.glob_pattern} in {args.csv_dir}", file=sys.stderr)
        sys.exit(1)

    cmd = [
        sys.executable, str(runner_dir / "lambda_decay.py"),
        "--output", str(args.outdir),
        "--beam", args.energy,
    ]
    if args.events is not None:
        cmd += ["--events", str(args.events)]
    cmd += [str(f) for f in files]

    print(f"[runner] running on {len(files)} files", flush=True)
    subprocess.run(cmd, check=True, cwd=runner_dir)


if __name__ == "__main__":
    main()
