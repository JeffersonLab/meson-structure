#!/usr/bin/env python3
"""MC-truth Lambda plots from per-energy mcpart_lambda CSVs.

Run standalone:
    python runner.py --energy 10x100 \
        --csv-dir /path/to/csv_dd4hep/10x100 --outdir /tmp/test
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer

runner_dir = Path(__file__).resolve().parent
app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def run(
    energy: str = typer.Option(...),
    csv_dir: Path = typer.Option(..., help="Directory with *.mcpart_lambda.csv (or fallback to *.csv)."),
    outdir: Path = typer.Option(...),
    events: Optional[int] = typer.Option(None, "--events", "-n"),
    glob_pattern: str = typer.Option("*.mcpart_lambda.csv", "--glob"),
):
    outdir.mkdir(parents=True, exist_ok=True)
    files = sorted(csv_dir.glob(glob_pattern))
    if not files:
        print(f"[runner] no {glob_pattern} in {csv_dir}", file=sys.stderr)
        raise typer.Exit(code=1)

    cmd = [
        sys.executable, str(runner_dir / "lambda_decay.py"),
        "--output", str(outdir),
        "--beam", energy,
    ]
    if events is not None:
        cmd += ["--events", str(events)]
    cmd += [str(f) for f in files]

    print(f"[runner] running on {len(files)} files", flush=True)
    subprocess.run(cmd, check=True, cwd=runner_dir)


if __name__ == "__main__":
    app()
