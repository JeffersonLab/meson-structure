# Analysis

Analyses live in [`analysis/`](https://github.com/JeffersonLab/meson-structure/tree/main/analysis),
one folder per analysis.

## Setup

```bash
pip install --user uv          # if you don't have uv
uv sync                        # install deps from pyproject.toml
```

## Running

```bash
uv run analysis/run.py list                                 # registered analyses
uv run analysis/run.py run eg-kinematics --energy 10x100    # one energy, local
uv run analysis/run.py run eg-kinematics                    # all energies, local
uv run analysis/run.py run eg-kinematics --mode slurm       # fan out per energy
uv run analysis/run.py run-all --mode slurm                 # everything
```

The launcher resolves campaign paths from `analysis/campaign.yaml`, builds an
argv, runs it locally or submits via SLURM. No DAG, no I/O tracking.

## Adding your analysis

Drop two files into your folder:

```
analysis/<your-name>/
    runner.py             # what the launcher invokes
    meta.yaml             # how to invoke it
    your_real_script.py   # your code (Python, ROOT macro, ...)
```

`analysis/run.py list` picks it up automatically. Folders without both files
are ignored.

### `meta.yaml`

```yaml
mode: per-energy            # per-energy | once
use_container: false        # true: wrap python call in `singularity exec`
inputs:
  csv_dir: csv_dd4hep_dir   # runner kwarg name -> key in campaign.yaml
sbatch:                     # only used by --mode slurm
  time: "04:00:00"
  mem_gb: 5
```

Optional: `extra_params` (static defaults), `container` (override campaign
container), `command` (Typer subcommand on runner).

### `runner.py`

Stdlib-only at import time (`argparse`, `subprocess`, `pathlib`) so it runs
inside any container Python. Defer heavy imports inside `main()`.

```python
#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

runner_dir = Path(__file__).resolve().parent

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--energy", required=True)
    parser.add_argument("--csv-dir", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--max-events", type=int, default=None)
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    files = sorted(args.csv_dir.glob("*.your_pattern.csv"))
    if not files:
        sys.exit(f"no inputs in {args.csv_dir}")

    cmd = [sys.executable, str(runner_dir / "your_real_script.py"),
           "-o", str(args.outdir), "--beam", args.energy, *map(str, files)]
    if args.max_events is not None:
        cmd += ["--events", str(args.max_events)]
    subprocess.run(cmd, check=True, cwd=runner_dir)


if __name__ == "__main__":
    main()
```

Must be runnable standalone:

```bash
uv run analysis/<your-name>/runner.py --energy 10x100 --csv-dir <path> --outdir /tmp/test
```

The launcher uses the same code path.

### Parameter resolution

Last wins:

1. `meta.extra_params` — static kwargs.
2. `meta.inputs` — runner kwarg ← `campaign.yaml` key (with `${energy}`,
   `${energy_num}`, `${proton_num}` interpolated).
3. Derived: `--energy <e>`, `--outdir <analysis_output>/<name>/<energy>`.
4. `--set key=value` on `analysis/run.py` (repeatable).

Final invocation:

```
python <folder>/runner.py --energy ... --outdir ... [meta.inputs] [overrides]
```

If `use_container: true`, wrapped in `singularity exec -B <bind_dirs> <container> ...`.

## Conventions for the underlying script

Optional. Recommended shape — yields a ~20-line `runner.py`:

```bash
script.py input1.csv input2.csv ... --beam 10x100 -o output_folder
```

1. Multiple input files via positional args. Don't OOM on ~200 chunks / 1M events.
2. `-o, --output` — output directory.
3. `-b, --beam` — `<eE>x<pE>` (e.g. `10x100`). Launcher always passes it.
4. `-e, --events` (optional) — max events; `None` = all.

If your script handles multiple CSV types per chunk (e.g. `*.type1.csv` +
`*.type2.csv`), match files by chunk number inside the script.

If your script takes one CSV but the campaign produces many chunks, concat
in the runner — see [`analysis/acceptance/runner.py`](https://github.com/JeffersonLab/meson-structure/tree/main/analysis/acceptance)
for the header-stable text-concat pattern.

Reference: [`analysis/csv_reco_dis_analysis/scattered_electron.py`](https://github.com/JeffersonLab/meson-structure/tree/main/analysis/csv_reco_dis_analysis/scattered_electron.py).

## Containers

`use_container: true` wraps the python call in:

```
singularity exec -B <campaign.bind_dirs> -B <repo_root> <container> python runner.py ...
```

Use it for ROOT macros, edm4hep/edm4eic dictionaries, eicrecon. Pure-Python
analyses (uproot, awkward, hist, matplotlib) leave it `false` and use the
host Python.

## `campaign.yaml`

Independent of `full-sim-pipeline/config-campaign-*.yaml`. Edit
`analysis/campaign.yaml` to point at the active campaign:

```yaml
base_dir: "/work/eic3/users/romanov/meson-structure-2026-05"
csv_dd4hep_dir: "${base_dir}/csv_dd4hep_saveall/${energy}"
```

`${energy}` resolves per energy at submit time.

## Debugging

- `--dry-run` — print argv, don't submit.
- `uv run analysis/<name>/runner.py --help` — standalone, no launcher involved.
- `--set max_events=5000` — fast iteration.
- `--mode slurm` logs: `<analysis_output>/<name>/_logs/`.
- `--mode local` streams to terminal; Ctrl-C aborts.

EIC plot-style template:
[ResultsCommittee templates](https://github.com/eic/ResultsCommittee_templates/tree/main/plot_macro).
