from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class Paths:
    inputs: Path = Path("/work/eic3/users/fraisse/meson-structure/data/")
    outputs: Path = Path("./outputs")
    base_dir: Path = Path("/work/eic3/users/fraisse/meson-structure/data/")
    afterburner_pattern: str = (
        "/work/eic3/users/romanov/meson-structure-2026-02/afterburner/{beam}-priority/"
        "k_lambda_{beam}_5000evt_{idx:04d}.afterburner.hepmc"
    )
    gen_base_dir: Path = Path("/work/eic3/users/romanov/meson-structure-2026-02/eg-orig-kaon-lambda/")


@dataclass(frozen=True)
class PhysicsConstants:
    energies: Sequence[str] = ("5x41", "10x100", "18x275")
    events_per_chunk: int = 5000
    m_lambda_gev: float = 1.11568
    ctau_lambda_m: float = 0.0789
    pid_lambda: int = 3122
    beta: float = 0.358
    theta_proton_rad: float = 25e-3
    mp_gev: float = 0.9382720813


DEFAULT_PATHS = Paths()
DEFAULT_CONST = PhysicsConstants()