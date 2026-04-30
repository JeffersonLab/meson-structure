#!/usr/bin/env python3
"""ROOT-macro analyses over edm4hep files.

Runs both `mcpart_lambda.cxx` and `acceptance.cxx` ROOT macros against the
`*.edm4hep.root` files for one energy. Expects to be invoked inside a
container that has ROOT + edm4hep/edm4eic dictionaries.

Run standalone (inside container):
    python runner.py --energy 10x100 \
        --edm4hep-dir /path/to/dd4hep/10x100 \
        --outdir /tmp/test --n-events 5000
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Iterable

import typer

runner_dir = Path(__file__).resolve().parent
app = typer.Typer(add_completion=False, no_args_is_help=True)


def _run_macro(macro: str, args: Iterable[str], cwd: Path) -> None:
    arg_str = ",".join(f'"{a}"' if not a.lstrip("-").isdigit() else a for a in args)
    invocation = f'{macro}({arg_str})'
    cmd = ["root", "-x", "-l", "-b", "-q", invocation]
    print(f"[runner] {' '.join(cmd)}", flush=True)
    proc = subprocess.run(cmd, cwd=str(cwd))
    if proc.returncode != 0:
        sys.exit(proc.returncode)


@app.command()
def run(
    energy: str = typer.Option(...),
    edm4hep_dir: Path = typer.Option(..., help="Dir with *.edm4hep.root for this energy."),
    outdir: Path = typer.Option(...),
    n_events: int = typer.Option(5000, "--n-events"),
    only: str = typer.Option(
        "all",
        help="Which macro(s) to run: all | mcpart_lambda | acceptance",
    ),
):
    outdir.mkdir(parents=True, exist_ok=True)
    pattern = str(edm4hep_dir / "*.edm4hep.root")

    if only in ("all", "mcpart_lambda"):
        _run_macro(
            "mcpart_lambda.cxx",
            [pattern, str(outdir / "mcpart_lambda"), str(n_events)],
            cwd=runner_dir,
        )
    if only in ("all", "acceptance"):
        _run_macro(
            "acceptance.cxx",
            [pattern, str(outdir / "acceptance"), str(n_events)],
            cwd=runner_dir,
        )


if __name__ == "__main__":
    app()
