"""Build runner argv lists and dispatch them via submitit."""
from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional, Sequence

import submitit
from omegaconf import DictConfig, OmegaConf


def build_argv(
    analysis_dir: Path,
    meta: DictConfig,
    campaign: DictConfig,
    params: dict[str, Any],
    repo_root: Path,
) -> list[str]:
    """Construct the argv that runs the analysis (host or singularity-wrapped).

    Always ends with: python <analysis_dir>/<entry> [<command>] --kwargs...
    Booleans -> --flag / omitted (Typer convention). None -> omitted.
    """
    runner_path = analysis_dir / meta.entry
    argv: list[str] = ["python", str(runner_path)]
    if meta.command:
        argv.append(str(meta.command))
    argv.extend(_kwargs_to_flags(params))

    if not meta.use_container:
        return argv

    container = meta.container or campaign.get("container")
    if not container:
        return argv

    bind_dirs = list(campaign.get("bind_dirs", [])) + [str(repo_root)]
    bind_args: list[str] = []
    seen: set[str] = set()
    for path in bind_dirs:
        path = str(path)
        if path and path not in seen:
            bind_args.extend(["-B", f"{path}:{path}"])
            seen.add(path)
    return ["singularity", "exec", *bind_args, str(container), *argv]


def _kwargs_to_flags(params: dict[str, Any]) -> list[str]:
    """Convert {key: value} -> ['--key', 'value', ...] using Typer conventions."""
    out: list[str] = []
    for key, value in params.items():
        if value is None or value is False:
            continue
        flag = f"--{key.replace('_', '-')}"
        if value is True:
            out.append(flag)
        else:
            out.extend([flag, str(value)])
    return out


def submit(
    argv: Sequence[str],
    *,
    mode: str,                       # local | slurm | dry-run
    log_dir: Path,
    job_name: str,
    sbatch: dict[str, Any],
    cwd: Optional[Path] = None,
) -> Optional["submitit.Job"]:
    """Submit `argv` via submitit."""
    if mode == "dry-run":
        cwd_str = str(cwd) if cwd else "."
        print(f"[dry-run] {job_name}")
        print(f"          cwd: {cwd_str}")
        print(f"          cmd: {' '.join(shlex.quote(a) for a in argv)}")
        return None

    log_dir.mkdir(parents=True, exist_ok=True)

    if mode == "local":
        executor = submitit.LocalExecutor(folder=str(log_dir))
    elif mode == "slurm":
        executor = submitit.AutoExecutor(folder=str(log_dir), cluster="slurm")
        executor.update_parameters(
            name=job_name,
            timeout_min=_walltime_minutes(sbatch.get("time", "04:00:00")),
            mem_gb=int(sbatch.get("mem_gb", 5)),
            cpus_per_task=int(sbatch.get("cpus_per_task", 1)),
            slurm_account=sbatch.get("account", "eic"),
            slurm_partition=sbatch.get("partition", "production"),
            stderr_to_stdout=False,
        )
    else:
        raise ValueError(f"unknown mode: {mode!r}")

    return executor.submit(_run_argv, list(argv), cwd)


def _run_argv(argv: Sequence[str], cwd: Optional[Path]) -> int:
    """Worker entrypoint executed by submitit on the target host."""
    print(f"[launcher] cwd: {cwd or Path.cwd()}", flush=True)
    print(f"[launcher] cmd: {' '.join(shlex.quote(a) for a in argv)}", flush=True)
    proc = subprocess.run(list(argv), cwd=str(cwd) if cwd else None)
    if proc.returncode != 0:
        sys.exit(proc.returncode)
    return 0


def _walltime_minutes(walltime: str) -> int:
    """Parse `D-HH:MM:SS`, `HH:MM:SS`, or `MM:SS` into total minutes."""
    days = 0
    if "-" in walltime:
        d, walltime = walltime.split("-", 1)
        days = int(d)
    parts = [int(p) for p in walltime.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    hours, minutes, seconds = parts
    return days * 1440 + hours * 60 + minutes + (1 if seconds else 0)
