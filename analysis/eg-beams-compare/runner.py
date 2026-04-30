#!/usr/bin/env python3
"""Cross-energy comparison of EG kinematics.

This is a `mode: once` analysis — it consumes ALL energies in a single run
and produces overlay plots. It does not get fanned out per energy.

Run standalone:
    python runner.py \
        --eg-dir /work/eic/users/romanov/eg-orig-kaon-lambda-2025-08 \
        --outdir /tmp/test
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Optional

import typer

runner_dir = Path(__file__).resolve().parent
app = typer.Typer(add_completion=False, no_args_is_help=True)


def _load_module():
    """Import eg-beam-compare-analysis.py despite the dash in its filename."""
    src = runner_dir / "eg-beam-compare-analysis.py"
    spec = importlib.util.spec_from_file_location("eg_beam_compare", str(src))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def _resolve_files(eg_dir: Path, energies: list[str]) -> dict[str, str]:
    """Resolve {energy: filepath} for each requested energy."""
    out: dict[str, str] = {}
    for e in energies:
        e_num, p_num = e.split("x")
        pattern = f"k_lambda_crossing_*-{e_num}.0on{p_num}.0_*.root"
        matches = sorted(eg_dir.glob(pattern))
        if matches:
            out[e] = str(matches[0])
        else:
            print(f"[runner] WARN: no EG file for {e} in {eg_dir}", file=sys.stderr)
    return out


@app.command()
def run(
    eg_dir: Path = typer.Option(...),
    outdir: Path = typer.Option(...),
    energies: str = typer.Option(
        "5x41,10x100,10x130,18x275",
        help="Comma-separated energies to overlay.",
    ),
    chunk_size: int = typer.Option(100_000, "--chunk-size"),
    max_events: Optional[int] = typer.Option(None, "--max-events"),
):
    outdir.mkdir(parents=True, exist_ok=True)
    energy_list = [e.strip() for e in energies.split(",") if e.strip()]
    files = _resolve_files(eg_dir, energy_list)
    if not files:
        raise typer.Exit(code=1)

    mod = _load_module()
    hists_by_energy: dict[str, dict] = {}
    for energy, path in files.items():
        print(f"[runner] processing {energy}: {path}", flush=True)
        hists_by_energy[energy] = mod.process_file(
            filename=path,
            chunk_size=chunk_size,
            max_events=max_events,
        )
    mod.make_all_comparison_plots(hists_by_energy, outdir=str(outdir))
    print(f"[runner] done -> {outdir}")


if __name__ == "__main__":
    app()
