# Analysis launcher

Small dispatcher for running campaign analyses locally, on the JLab interactive
farm, or via SLURM. Backend: [submitit](https://github.com/facebookincubator/submitit).

It does **one** thing: take a per-folder `runner.py` + `meta.yaml`, resolve
inputs from `campaign.yaml`, and submit. No DAG, no input/output tracking, no
Snakefile.

## Layout

```
analysis/
    campaign.yaml             # paths, energies, container — edit to your setup
    run.py                    # top-level CLI: list / run / run-all
    launcher/                 # library (config, dispatch, discovery)
        config.py
        dispatch.py
        discover.py
    eg-kinematics/
        runner.py             # standalone Typer CLI
        meta.yaml             # mode, inputs, sbatch hints
        eg-kinematics.py      # original analysis script (untouched)
    eg-beams-compare/         # mode: once (cross-energy)
    edm4hep_lambda/           # use_container: true (ROOT macros)
    csv_mc_dis_analysis/
    csv_mcpart_lambda/
    multicalo-lambda/
    ...                       # folders without runner.py+meta.yaml are ignored
```

## Daily commands

```bash
# what's registered?
python analysis/run.py list

# debug one analysis, one energy, locally
python analysis/run.py run eg-kinematics --energy 10x100

# fan out across all campaign energies, locally (sequential)
python analysis/run.py run eg-kinematics

# submit to SLURM, one job per energy
python analysis/run.py run eg-kinematics --mode slurm

# preview, do nothing
python analysis/run.py run eg-kinematics --mode slurm --dry-run

# override runner kwargs (repeatable)
python analysis/run.py run eg-kinematics --energy 10x100 \
    --set max_events=5000 --set chunk_size=50000

# everything
python analysis/run.py run-all --mode slurm
python analysis/run.py run-all --mode slurm --only eg-kinematics,csv_mc_dis_analysis

# `python -m analysis ...` works too
```

## Debug a folder directly (no top-level runner)

Each `runner.py` is a standalone Typer CLI. Useful when iterating on a single
analysis on the farm:

```bash
cd analysis/eg-kinematics
python runner.py \
    --energy 10x100 \
    --eg-dir /work/eic/users/romanov/eg-orig-kaon-lambda-2025-08 \
    --outdir /tmp/test --max-events 5000
```

Same code path the launcher uses → if it works here, SLURM works.

## Adding a new analysis

1. Create `analysis/<name>/runner.py` — a Typer app whose default command takes
   `--energy`, `--outdir`, plus whatever campaign inputs you need
   (`--csv-dir`, `--edm4hep-dir`, ...).
2. Create `analysis/<name>/meta.yaml`:

   ```yaml
   mode: per-energy           # or `once` for cross-energy analyses
   use_container: true        # set false for pure-Python (uproot/uv) analyses
   inputs:
     csv_dir: csv_dd4hep_dir  # runner kwarg name -> campaign.yaml key
   sbatch:
     time: "04:00:00"
     mem_gb: 5
   ```

3. The launcher discovers it automatically.

## How parameters reach the runner

Resolution order (last wins):

1. `meta.extra_params` — static defaults declared in `meta.yaml`.
2. `meta.inputs` — runner kwarg ← `campaign.yaml` key, with `${energy}` interpolated.
3. Derived: `--energy <e>`, `--outdir <output_root>/<name>/<energy>`.
4. CLI overrides: `--set key=value`.

The runner is invoked as:

```
python <folder>/runner.py [<command>] --key value --flag ...
```

Bools become `--flag` (true) or are omitted (false). `None` is omitted.
If `meta.use_container: true`, the whole `python ...` call is wrapped in
`singularity exec -B ... <container> ...`.

## `campaign.yaml`

Single source of truth for the launcher. Independent of `full-sim-pipeline/`
configs by design (decouples analyses from pipeline-stage flags).

Per-energy paths use OmegaConf interpolation:

```yaml
dd4hep_dir: "${base_dir}/dd4hep/${energy}"
```

`${energy}` resolves at submit time. `${energy_num}` (electron) and
`${proton_num}` (proton) are also available.

## Modes

| `--mode`   | Backend                                | Use case                  |
|------------|----------------------------------------|---------------------------|
| `local`    | `submitit.LocalExecutor`               | laptop, interactive farm  |
| `slurm`    | `submitit.AutoExecutor` cluster=slurm  | batch on JLab farm        |
| `dry-run`  | print only                              | preview commands          |

## Install

The **top-level launcher** (host-side) needs:

```bash
pip install submitit omegaconf typer
```

Per-folder `runner.py` files use **stdlib only** (argparse + subprocess) so
they work inside any container Python without extra deps. Each runner shells
out to the analysis script which has its own deps (uproot, ROOT, etc.).
