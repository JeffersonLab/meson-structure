"""Campaign + meta.yaml loading and per-energy parameter resolution."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from omegaconf import DictConfig, OmegaConf


def load_campaign(campaign_path: Path) -> DictConfig:
    """Load the top-level campaign config (paths, energies, container)."""
    cfg = OmegaConf.load(str(campaign_path))
    if not isinstance(cfg, DictConfig):
        raise TypeError(f"campaign config at {campaign_path} is not a mapping")
    return cfg


_META_DEFAULTS = {
    "name": None,
    "mode": "per-energy",           # per-energy | once
    "entry": "runner.py",
    "command": None,                # optional Typer subcommand
    "inputs": {},                   # runner kwarg -> campaign key
    "extra_params": {},             # static kwargs forwarded to runner
    "container": None,              # override campaign.container
    "use_container": True,
    "sbatch": {
        "time": "04:00:00",
        "mem_gb": 5,
        "cpus_per_task": 1,
        "account": "eic",
        "partition": "production",
    },
}


def load_meta(analysis_dir: Path) -> DictConfig:
    """Load `meta.yaml` from an analysis folder, merged with defaults."""
    meta_path = analysis_dir / "meta.yaml"
    if not meta_path.is_file():
        raise FileNotFoundError(f"no meta.yaml in {analysis_dir}")
    user = OmegaConf.load(str(meta_path))
    if not isinstance(user, DictConfig):
        raise TypeError(f"{meta_path} is not a mapping")
    defaults = OmegaConf.create({**_META_DEFAULTS, "name": analysis_dir.name})
    return OmegaConf.merge(defaults, user)


def resolve_params(
    campaign: DictConfig,
    meta: DictConfig,
    energy: Optional[str],
    output_root: Path,
    overrides: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Build the kwargs to pass to the runner.

    Order (last wins):
      1. meta.extra_params  (static defaults declared by the analysis)
      2. meta.inputs        (runner kwarg <- campaign[key], with ${energy} resolved)
      3. derived            (energy, outdir)
      4. overrides          (CLI-supplied kwargs)
    """
    params: dict[str, Any] = {}

    static = OmegaConf.to_container(meta.extra_params, resolve=True) or {}
    params.update(static)

    view = _resolve_campaign_for_energy(campaign, energy)
    inputs = OmegaConf.to_container(meta.inputs, resolve=True) or {}
    for kwarg_name, campaign_key in inputs.items():
        if isinstance(campaign_key, str) and campaign_key in view:
            params[kwarg_name] = str(view[campaign_key])
        else:
            params[kwarg_name] = campaign_key

    if energy is not None:
        params["energy"] = energy
        params["outdir"] = str(output_root / meta.name / energy)
    else:
        params["outdir"] = str(output_root / meta.name)

    if overrides:
        params.update(overrides)

    return params


def _resolve_campaign_for_energy(
    campaign: DictConfig, energy: Optional[str]
) -> DictConfig:
    """Return campaign config with `${energy}` interpolated for one energy."""
    raw = OmegaConf.to_container(campaign, resolve=False)
    if energy is not None:
        electron, proton = energy.split("x")
        raw["energy"] = energy
        raw["energy_num"] = electron
        raw["proton_num"] = proton
    view = OmegaConf.create(raw)
    try:
        OmegaConf.resolve(view)
    except Exception:
        pass
    return view
