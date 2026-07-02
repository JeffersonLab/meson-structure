from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
import math

# =============================================================================
# Paths
# =============================================================================

@dataclass(frozen=True)
class Paths:
    inputs: Path = Path("/work/eic3/users/fraisse/meson-structure/data/")
    outputs: Path = Path("./outputs")
    base_dir: Path = Path("/work/eic3/users/fraisse/meson-structure/data/")
    afterburner_pattern: str = (
        "/work/eic3/users/romanov/meson-structure-2026-02/afterburner/{beam}-priority/"
        "k_lambda_{beam}_5000evt_{idx:04d}.afterburner.hepmc"
    )
    gen_base_dir: Path = Path("/work/eic3/users/romanov/eg-orig-kaon-lambda-2025-08/")

PATHS = Paths()
PATHS.outputs.mkdir(parents=True, exist_ok=True)

# =============================================================================
# Physics constants (global run settings)
# =============================================================================

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

CONST = PhysicsConstants()

# =============================================================================
# LHAPDF setup
# =============================================================================

DEFAULT_LHAPDF_DATA_PATH = "/work/eic3/users/fraisse/lhapdf"

def setup_lhapdf_env() -> str:
    """
    Ensure LHAPDF_DATA_PATH is set before importing python lhapdf.
    Returns the resolved LHAPDF path.
    """
    lhapdf_path = os.environ.get("LHAPDF_DATA_PATH", DEFAULT_LHAPDF_DATA_PATH)
    os.environ["LHAPDF_DATA_PATH"] = lhapdf_path
    return lhapdf_path

PION_PDFSET_DEFAULT = "JAM21PionPDFnlo"
PION_PDFMEMBER_DEFAULT = 0

def get_pion_pdfset() -> str:
    return os.environ.get("PION_PDFSET", PION_PDFSET_DEFAULT)

def get_pion_pdfmember() -> int:
    return int(os.environ.get("PION_PDFMEMBER", str(PION_PDFMEMBER_DEFAULT)))

# =============================================================================
# Default grid settings for structure function evaluation
# =============================================================================

GRID_DEFAULTS = dict(
    x_min=0.0, x_max=1.0,
    q2_min=1.0, q2_max=500.0,
    nx=20, nq2=20,
)


