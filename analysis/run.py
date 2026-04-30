#!/usr/bin/env python3
"""Top-level analysis dispatcher.

Examples:
    # list registered analyses
    python analysis/run.py list

    # debug one analysis, one energy, locally
    python analysis/run.py run eg-kinematics --energy 10x100

    # all energies (per-energy mode), locally, sequential
    python analysis/run.py run eg-kinematics

    # submit to SLURM, fan out one job per energy
    python analysis/run.py run eg-kinematics --mode slurm

    # preview without submitting
    python analysis/run.py run eg-kinematics --mode slurm --dry-run

    # forward extra runner kwargs (repeat --set as needed)
    python analysis/run.py run eg-kinematics --energy 10x100 \\
        --set max_events=5000 --set chunk_size=50000

    # everything at once
    python analysis/run.py run-all --mode slurm
    python analysis/run.py run-all --mode slurm --only eg-kinematics,csv_mc_dis_analysis
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import typer

analysis_dir = Path(__file__).resolve().parent
repo_root = analysis_dir.parent
sys.path.insert(0, str(analysis_dir))

from launcher import (  # noqa: E402
    build_argv,
    discover_analyses,
    load_campaign,
    load_meta,
    resolve_params,
    submit,
)

app = typer.Typer(add_completion=False, no_args_is_help=True)


def _parse_overrides(set_args: list[str]) -> dict[str, str]:
    """Parse `--set key=value --set flag=true` into a dict."""
    out: dict[str, str] = {}
    for item in set_args or []:
        if "=" not in item:
            raise typer.BadParameter(f"--set expects key=value, got {item!r}")
        key, value = item.split("=", 1)
        out[key.strip()] = value.strip()
    return out


def _campaign_or_default(campaign: Optional[Path]) -> Path:
    if campaign is not None:
        return campaign
    default = analysis_dir / "campaign.yaml"
    if not default.is_file():
        raise typer.BadParameter(f"no --campaign given and {default} does not exist")
    return default


def _run_one_analysis(
    name: str,
    energy: Optional[str],
    mode: str,
    campaign_path: Path,
    output_root: Optional[Path],
    overrides: dict[str, str],
) -> None:
    """Submit one analysis (one or all energies). Plain function, no Typer."""
    folder = analysis_dir / name
    if not (folder / "runner.py").is_file():
        raise typer.BadParameter(f"{folder}/runner.py not found")

    campaign = load_campaign(campaign_path)
    meta = load_meta(folder)

    out_root = output_root or Path(campaign.get("analysis_output", str(analysis_dir / "out")))
    log_dir = out_root / meta.name / "_logs"

    if meta.mode == "once":
        energies: list[Optional[str]] = [None]
    elif energy is not None:
        energies = [energy]
    else:
        energies = list(campaign.energies)

    sbatch_defaults = dict(campaign.get("sbatch_defaults") or {})
    sbatch = {**sbatch_defaults, **dict(meta.sbatch)}

    submitted_jobs = []
    for selected_energy in energies:
        params = resolve_params(campaign, meta, selected_energy, out_root, overrides)
        argv = build_argv(folder, meta, campaign, params, repo_root)
        job_name = f"{meta.name}_{selected_energy}" if selected_energy else meta.name
        result = submit(argv, mode=mode, log_dir=log_dir, job_name=job_name,
                        sbatch=sbatch, cwd=folder)
        if mode == "slurm" and result is not None:
            typer.echo(f"submitted: {job_name}  job_id={getattr(result, 'job_id', '?')}")
            submitted_jobs.append((job_name, result))

    if mode == "slurm" and submitted_jobs:
        typer.echo(f"\n{len(submitted_jobs)} SLURM job(s) submitted. "
                   f"Check status with `squeue -u $USER` or watch the log dir:")
        typer.echo(f"  {log_dir}")


@app.command("list")
def list_cmd(
    campaign: Optional[Path] = typer.Option(None, "--campaign", "-c"),
):
    """List analyses that have a runner.py + meta.yaml."""
    names = discover_analyses(analysis_dir)
    if not names:
        typer.echo("no analyses registered (looking for runner.py + meta.yaml)")
        return
    campaign_path = _campaign_or_default(campaign)
    cfg = load_campaign(campaign_path)
    typer.echo(f"campaign: {campaign_path}")
    typer.echo(f"energies: {list(cfg.energies)}")
    typer.echo("")
    typer.echo("registered analyses:")
    for name in names:
        meta = load_meta(analysis_dir / name)
        typer.echo(f"  {name:30s}  mode={meta.mode}  container={meta.use_container}")


@app.command("run")
def run_cmd(
    name: str = typer.Argument(..., help="Analysis folder name."),
    energy: Optional[str] = typer.Option(
        None, "--energy", "-e",
        help="One energy (e.g. 10x100). Omit for all (per-energy analyses).",
    ),
    mode: str = typer.Option("local", "--mode", "-m", help="local | slurm | dry-run"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Alias for --mode dry-run."),
    campaign: Optional[Path] = typer.Option(None, "--campaign", "-c"),
    output_root: Optional[Path] = typer.Option(None, "--output-root", "-o"),
    set_args: list[str] = typer.Option(
        None, "--set",
        help="Override runner kwargs: --set key=value (repeat as needed).",
    ),
):
    """Run one analysis (one energy or all)."""
    effective_mode = "dry-run" if dry_run else mode
    overrides = _parse_overrides(set_args or [])
    _run_one_analysis(
        name=name,
        energy=energy,
        mode=effective_mode,
        campaign_path=_campaign_or_default(campaign),
        output_root=output_root,
        overrides=overrides,
    )


@app.command("run-all")
def run_all_cmd(
    mode: str = typer.Option("local", "--mode", "-m"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    campaign: Optional[Path] = typer.Option(None, "--campaign", "-c"),
    output_root: Optional[Path] = typer.Option(None, "--output-root", "-o"),
    only: Optional[str] = typer.Option(None, "--only",
                                        help="Comma-separated subset to run."),
    set_args: list[str] = typer.Option(None, "--set"),
):
    """Run every registered analysis."""
    effective_mode = "dry-run" if dry_run else mode
    overrides = _parse_overrides(set_args or [])
    campaign_path = _campaign_or_default(campaign)

    names = discover_analyses(analysis_dir)
    if only:
        keep = {s.strip() for s in only.split(",") if s.strip()}
        names = [n for n in names if n in keep]

    for name in names:
        typer.echo(f"\n=== {name} ===")
        _run_one_analysis(
            name=name,
            energy=None,
            mode=effective_mode,
            campaign_path=campaign_path,
            output_root=output_root,
            overrides=overrides,
        )


if __name__ == "__main__":
    app()
