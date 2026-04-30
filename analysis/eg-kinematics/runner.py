#!/usr/bin/env python3
"""Per-energy kinematics over the EG ROOT file.

Run standalone for debugging:
    python runner.py --energy 10x100 \
        --eg-dir /work/eic/users/romanov/eg-orig-kaon-lambda-2025-08 \
        --outdir /tmp/test --max-events 5000
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer

runner_dir = Path(__file__).resolve().parent
app = typer.Typer(add_completion=False, no_args_is_help=True)


def _find_eg_file(eg_dir: Path, energy: str) -> Path:
    e_num, p_num = energy.split("x")
    pattern = f"k_lambda_crossing_*-{e_num}.0on{p_num}.0_*.root"
    matches = sorted(eg_dir.glob(pattern))
    if not matches:
        raise FileNotFoundError(
            f"no EG file matching {pattern} in {eg_dir}"
        )
    if len(matches) > 1:
        print(f"[runner] warning: multiple matches, using {matches[0].name}", file=sys.stderr)
    return matches[0]


@app.command()
def run(
    energy: str = typer.Option(...),
    eg_dir: Path = typer.Option(..., help="Directory containing the EG ROOT files."),
    outdir: Path = typer.Option(...),
    max_events: Optional[int] = typer.Option(None, "--max-events"),
    chunk_size: int = typer.Option(100_000, "--chunk-size"),
):
    outdir.mkdir(parents=True, exist_ok=True)
    eg_file = _find_eg_file(eg_dir, energy)

    cmd = [
        sys.executable, str(runner_dir / "eg-kinematics.py"),
        "--input-file", str(eg_file),
        "--energy", energy,
        "--outdir", str(outdir),
        "--chunk-size", str(chunk_size),
    ]
    if max_events is not None:
        cmd += ["--max-events", str(max_events)]

    print(f"[runner] {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, check=True, cwd=runner_dir)


if __name__ == "__main__":
    app()
