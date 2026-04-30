#!/usr/bin/env python3
"""Per-energy multi-calo Lambda / Kaon-SF studies.

Run standalone:
    python runner.py --energy 10x100 \
        --inputs /path/to/reco --outdir /tmp/test --nfiles 2
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
    parser.add_argument("--inputs", type=Path, required=True,
                        help="Reco/eicrecon base directory.")
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--nfiles", type=int, default=1)
    parser.add_argument("--bins", type=int, default=50)
    parser.add_argument("--task", default="all")
    parser.add_argument("--with-beta", action="store_true")
    parser.add_argument("--tmax", type=float, default=None)
    parser.add_argument("--lumin-fb", type=float, default=1.0)
    parser.add_argument("--logQ2", action="store_true", dest="log_q2")
    parser.add_argument("--suffix", default="testall_calocalib_verification")
    parser.add_argument("--gen-dir", type=Path, default=None)
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable, str(runner_dir / "run.py"),
        "--inputs", str(args.inputs),
        "--outputs", str(args.outdir),
        "--suffix", args.suffix,
        "--nfiles", str(args.nfiles),
        "--bins", str(args.bins),
        "--beam", args.energy,
        "--task", args.task,
        "--lumin-fb", str(args.lumin_fb),
    ]
    if args.with_beta:
        cmd.append("--with-beta")
    if args.tmax is not None:
        cmd += ["--tmax", str(args.tmax)]
    if args.log_q2:
        cmd.append("--logQ2")
    if args.gen_dir is not None:
        cmd += ["--gen-dir", str(args.gen_dir)]

    print(f"[runner] {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, check=True, cwd=runner_dir)


if __name__ == "__main__":
    main()
