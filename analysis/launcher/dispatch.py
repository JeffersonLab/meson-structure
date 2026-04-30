"""Build runner argv lists and dispatch them locally or via submitit (slurm)."""
from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional, Sequence

from omegaconf import DictConfig


def build_argv(
    analysis_dir: Path,
    meta: DictConfig,
    campaign: DictConfig,
    params: dict[str, Any],
    repo_root: Path,
) -> list[str]:
    """Construct argv that runs the analysis (host or singularity-wrapped)."""
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
) -> Optional[Any]:
    """Dispatch `argv` according to `mode`.

    - dry-run: print and return None.
    - local:   run synchronously via subprocess. No timeout, no parallelism.
               Stdout/stderr stream to the caller's terminal.
    - slurm:   submit via submitit AutoExecutor; returns the Job for polling.
    """
    if mode == "dry-run":
        print(f"[dry-run] {job_name}")
        print(f"          cwd: {cwd or '.'}")
        print(f"          cmd: {_quote_cmd(argv)}")
        return None

    if mode == "local":
        return _run_local_sync(argv, cwd=cwd, job_name=job_name)

    if mode == "slurm":
        return _submit_slurm(argv, log_dir=log_dir, job_name=job_name,
                             sbatch=sbatch, cwd=cwd)

    raise ValueError(f"unknown mode: {mode!r}")


def _run_local_sync(
    argv: Sequence[str], *, cwd: Optional[Path], job_name: str
) -> int:
    """Run synchronously, streaming output. Raises CalledProcessError on failure."""
    print(f"[local] {job_name}")
    print(f"        cwd: {cwd or Path.cwd()}")
    print(f"        cmd: {_quote_cmd(argv)}", flush=True)
    proc = subprocess.run(list(argv), cwd=str(cwd) if cwd else None)
    print(f"[local] {job_name} exit={proc.returncode}")
    if proc.returncode != 0:
        sys.exit(proc.returncode)
    return 0


def _submit_slurm(
    argv: Sequence[str],
    *,
    log_dir: Path,
    job_name: str,
    sbatch: dict[str, Any],
    cwd: Optional[Path],
):
    import submitit  # imported lazily so `local` doesn't pay for it

    log_dir.mkdir(parents=True, exist_ok=True)
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
    return executor.submit(_slurm_worker, list(argv), cwd)


def _slurm_worker(argv: Sequence[str], cwd: Optional[Path]) -> int:
    """Entry point pickled and run on a SLURM compute node."""
    print(f"[slurm-worker] cwd: {cwd or Path.cwd()}", flush=True)
    print(f"[slurm-worker] cmd: {_quote_cmd(argv)}", flush=True)
    proc = subprocess.run(list(argv), cwd=str(cwd) if cwd else None)
    if proc.returncode != 0:
        sys.exit(proc.returncode)
    return 0


def _quote_cmd(argv: Sequence[str]) -> str:
    return " ".join(shlex.quote(a) for a in argv)


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
