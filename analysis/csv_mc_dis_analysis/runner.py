#!/usr/bin/env python3
"""MC DIS plots from per-energy CSV.

Run standalone:
    python runner.py --energy 10x100 \
        --csv-dir /path/to/csv_dd4hep/10x100 --outdir /tmp/test
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import typer

runner_dir = Path(__file__).resolve().parent
app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def run(
    energy: str = typer.Option(..., help="Used for output naming; the script regex-extracts it."),
    csv_dir: Path = typer.Option(..., help="Directory containing *.mc_dis.csv files."),
    outdir: Path = typer.Option(...),
    bins: int = typer.Option(500),
    dpi: int = typer.Option(150),
):
    outdir.mkdir(parents=True, exist_ok=True)
    files = sorted(csv_dir.glob("*.mc_dis.csv"))
    if not files:
        print(f"[runner] no *.mc_dis.csv in {csv_dir}", file=sys.stderr)
        raise typer.Exit(code=1)

    cmd = [
        sys.executable, str(runner_dir / "plot_mc.py"),
        "--outdir", str(outdir),
        "--bins", str(bins),
        "--dpi", str(dpi),
        *map(str, files),
    ]
    print(f"[runner] running on {len(files)} files", flush=True)
    subprocess.run(cmd, check=True, cwd=runner_dir)


if __name__ == "__main__":
    app()
