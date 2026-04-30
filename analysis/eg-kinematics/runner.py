#!/usr/bin/env python3
"""Per-energy kinematics over the EG ROOT file.

Run standalone for debugging:
    python runner.py --energy 10x100 \
        --eg-dir /work/eic/users/romanov/eg-orig-kaon-lambda-2025-08 \
        --outdir /tmp/test --max-events 5000

Stdlib-only (no typer/omegaconf imports) so this runs inside any container
that ships Python.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

runner_dir = Path(__file__).resolve().parent


def find_eg_file(eg_dir: Path, energy: str) -> Path:
    e_num, p_num = energy.split("x")
    pattern = f"k_lambda_crossing_*-{e_num}.0on{p_num}.0_*.root"
    matches = sorted(eg_dir.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"no EG file matching {pattern} in {eg_dir}")
    if len(matches) > 1:
        print(f"[runner] warning: multiple matches, using {matches[0].name}", file=sys.stderr)
    return matches[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--energy", required=True)
    parser.add_argument("--eg-dir", type=Path, required=True,
                        help="Directory containing the EG ROOT files.")
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--max-events", type=int, default=None)
    parser.add_argument("--chunk-size", type=int, default=100_000)
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    eg_file = find_eg_file(args.eg_dir, args.energy)

    cmd = [
        sys.executable, str(runner_dir / "eg_kinematics.py"),
        "--input-file", str(eg_file),
        "--energy", args.energy,
        "--outdir", str(args.outdir),
        "--chunk-size", str(args.chunk_size),
    ]
    if args.max_events is not None:
        cmd += ["--max-events", str(args.max_events)]

    print(f"[runner] {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, check=True, cwd=runner_dir)


if __name__ == "__main__":
    main()
