# Analysis launcher — system requirements

User-facing tutorial: [docs/analysis.md](../docs/analysis.md). This file
records the requirements and design decisions the launcher must satisfy.

## Requirements

1. **Different people write different analyses.** The launcher does not
   force a uniform script CLI. Each folder owns its invocation.
2. **The "DAG" is upstream.** Analyses are an `analyses × energies` grid.
   No dependency graph between analyses, no input/output tracking.
3. **One unified way to launch** — laptop, ifarm interactive, JLab SLURM —
   without changing the analysis code. Switch backends with `--mode`.
4. **Per-folder mini-runner + global runner.** Each analysis ships its own
   small runner, debuggable directly. The global runner discovers and
   dispatches.
5. **Easy debug knobs.** Custom flags / fewer files / one energy must be a
   one-flag tweak, not a config edit.
6. **No Snakemake-style ceremony.** `rule all: [f"out/..." for ...]` is not
   acceptable for "test-run with custom flag". No DAG-build wait.
7. **Scratch and personal folders coexist.** Folders without an explicit
   opt-in are ignored. Not every analysis is pipeline-ready.
8. **Container support per analysis.** Some analyses need ROOT / edm4hep
   inside singularity; some need host Python. Per-folder declaration.
9. **Runners must work inside the campaign container.** Container Python
   has no `typer` / `omegaconf` / `numpy` at startup.
10. **Pip-installable, easy on farm nodes.** No JVM (rules out Nextflow),
    no server component (rules out Prefect), no Java daemon.
11. **Campaign config decoupled from `full-sim-pipeline/`.** Pipeline-stage
    flags don't bleed into analyses.
12. **Snakemake → no.** Slow DAG, flag soup, fights us on dev/debug.
13. **Custom DSL → no.** Don't reinvent Snakemake.

## Decisions

| Choice | Why |
|---|---|
| **Backend: [submitit](https://github.com/facebookincubator/submitit) for SLURM, plain `subprocess.run` for local** | Pip-installable, native SLURM, zero ceremony. `LocalExecutor` was tried and dropped: enforced walltime + silent parallelism on the login node. |
| **Per-folder `runner.py` + `meta.yaml` opt-in contract** | Authors keep autonomy; launcher stays minimal. Folders without both files are ignored. |
| **`runner.py` is stdlib-only at import time** | Same code runs on host and inside container. Heavy imports go inside `main()`. |
| **`runner.py` shells out to the analysis script** | Author's CLI / language stays free (Python, ROOT macro, C++). Launcher doesn't import or understand it. |
| **`meta.yaml` declares `inputs:` mapping kwarg → campaign key** | One indirection, no templating language. OmegaConf interpolates `${energy}`, `${energy_num}`, `${proton_num}`. |
| **Container wrap is whole-runner** | Matches the pre-existing pipeline pattern (`50_create_analysis_jobs.py`). One place handles `singularity exec -B ... <container>`. |
| **`--set key=value` for CLI overrides** | Repeatable, unambiguous, no `--` magic. |
| **`mode: per-energy` vs `once`** | Most analyses fan out per energy; cross-energy comparisons run once. No DAG required to express this. |
| **`analysis/campaign.yaml` is the only config** | Independent of `full-sim-pipeline/config-campaign-*.yaml`. One file to edit per campaign. |
| **Top-level `analysis/run.py` keeps Typer; runners use argparse** | Top-level is host-only; runners must work in container. |

## Non-goals

- Incremental rebuilds / "skip if output exists". Authors handle re-runs.
- File-level dependency tracking. The campaign DAG already ran.
- Workflow visualization, retries, monitoring dashboards.
- Sharing rules with EIC-wide Snakemake pipelines (lingua-franca argument
  was weighed and rejected — daily UX won).

## Layout

```
analysis/
    campaign.yaml         # paths, energies, container — edit per campaign
    run.py                # CLI: list / run / run-all
    launcher/             # config, dispatch, discovery
    <name>/
        runner.py         # stdlib-only, standalone-runnable
        meta.yaml         # mode, inputs, sbatch hints
        ...               # actual analysis code
```

## Install

The repo uses `uv` + `pyproject.toml` at the root. Dependencies (`submitit`,
`omegaconf`, `typer`, plus the analysis stack: `uproot`, `awkward`, `hist`,
`matplotlib`, ...) are declared there.

```bash
pip install --user uv          # if you don't have uv
uv sync                        # creates/updates .venv from pyproject.toml
uv run python analysis/run.py list
```

Per-folder runners are stdlib-only at import time, so they also work inside
the campaign container without extra deps.
