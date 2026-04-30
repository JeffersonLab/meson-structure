#!/usr/bin/env python3
"""Per-energy multi-calo Lambda / Kaon-SF studies.

Run standalone:
    python runner.py --energy 10x100 \
        --inputs /path/to/reco --outdir /tmp/test --nfiles 2
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
    inputs: Path = typer.Option(..., help="Reco/eicrecon base directory."),
    outdir: Path = typer.Option(...),
    nfiles: int = typer.Option(1),
    bins: int = typer.Option(50),
    task: str = typer.Option("all"),
    with_beta: bool = typer.Option(False, "--with-beta"),
    tmax: Optional[float] = typer.Option(None, "--tmax"),
    lumin_fb: float = typer.Option(1.0, "--lumin-fb"),
    log_q2: bool = typer.Option(False, "--logQ2"),
    suffix: str = typer.Option("testall_calocalib_verification"),
    gen_dir: Optional[Path] = typer.Option(None, "--gen-dir"),
):
    outdir.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable, str(runner_dir / "run.py"),
        "--inputs", str(inputs),
        "--outputs", str(outdir),
        "--suffix", suffix,
        "--nfiles", str(nfiles),
        "--bins", str(bins),
        "--beam", energy,
        "--task", task,
        "--lumin-fb", str(lumin_fb),
    ]
    if with_beta:
        cmd.append("--with-beta")
    if tmax is not None:
        cmd += ["--tmax", str(tmax)]
    if log_q2:
        cmd.append("--logQ2")
    if gen_dir is not None:
        cmd += ["--gen-dir", str(gen_dir)]

    print(f"[runner] {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, check=True, cwd=runner_dir)


if __name__ == "__main__":
    app()
