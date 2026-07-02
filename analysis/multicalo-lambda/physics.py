from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import numpy as np

from config import PhysicsConstants, CONST


# =============================================================================
# Beam helpers
# =============================================================================

def parse_proton_energy(beam_str: str) -> float:
    """
    Extract proton energy (GeV) from a beam string like '5x41', '10x100', '18x275'.
    If the string doesn't contain 'x', it is interpreted as a float.
    """
    s = str(beam_str)
    if "x" in s:
        return float(s.split("x")[-1])
    return float(s)


def direct_energy_window(beam: str) -> tuple[float, float]:
    """
    Energy window (GeV) used for direct-energy selections in afterburner studies.
    """
    if beam == "5x41":
        return 20.0, 41.0
    if beam == "10x100":
        return 50.0, 100.0
    if beam == "18x275":
        return 130.0, 275.0
    raise ValueError(f"Unknown beam config: {beam}")


# =============================================================================
# Lambda/proton kinematics utilities
# =============================================================================

def E_to_L(E_GeV: np.ndarray | float, c: PhysicsConstants = CONST) -> np.ndarray:
    """
    Convert Lambda energy E (GeV) to average decay length <L> in meters:
      <L> = (p/m) * c*tau = ctau * sqrt(E^2 - m^2) / m
    """
    E = np.asarray(E_GeV, dtype=np.float64)
    m = float(c.m_lambda_gev)
    return float(c.ctau_lambda_m) * np.sqrt(np.maximum(E * E - m * m, 0.0)) / m


def L_to_E(L_m: np.ndarray | float, c: PhysicsConstants = CONST) -> np.ndarray:
    """
    Inverse of E_to_L:
      E = sqrt((m*L/ctau)^2 + m^2)
    """
    L = np.asarray(L_m, dtype=np.float64)
    m = float(c.m_lambda_gev)
    return np.sqrt((m * L / float(c.ctau_lambda_m)) ** 2 + m * m)


def proton_kinematics_for_beam(beam: str, c: PhysicsConstants = CONST) -> dict[str, float | np.ndarray]:
    """
    Compute basic proton kinematics given a beam string (e.g. '18x275').

    Returns a dict with:
      Ep      : proton energy (GeV)
      p_mag   : proton momentum magnitude (GeV)
      nhat    : unit direction vector (3,)
      pplus_p : E + |p| (GeV)
      ppx,ppy,ppz,ppE : proton 4-vector components (GeV)
    """
    Ep = parse_proton_energy(beam)
    mp = float(c.mp_gev)
    p_mag = math.sqrt(max(Ep * Ep - mp * mp, 0.0))

    th = float(c.theta_proton_rad)
    sin_th = math.sin(th)
    cos_th = math.cos(th)

    nhat = np.array([sin_th, 0.0, cos_th], dtype=np.float64)
    pplus_p = Ep + p_mag

    ppx = p_mag * sin_th
    ppy = 0.0
    ppz = p_mag * cos_th
    ppE = Ep

    return dict(
        Ep=Ep,
        p_mag=p_mag,
        nhat=nhat,
        pplus_p=pplus_p,
        ppx=ppx,
        ppy=ppy,
        ppz=ppz,
        ppE=ppE,
    )


def xk_from_xb_xl(xb: np.ndarray, xl: np.ndarray) -> np.ndarray:
    """
    Compute x_K from x_B and x_L:
      x_K = x_B / (1 - x_L)

    Returns NaN where undefined/invalid.
    """
    xb = np.asarray(xb, dtype=np.float64)
    xl = np.asarray(xl, dtype=np.float64)

    denom = 1.0 - xl
    xk = np.full_like(xb, np.nan, dtype=np.float64)

    ok = np.isfinite(xb) & np.isfinite(denom) & (denom > 0.0)
    xk[ok] = xb[ok] / denom[ok]
    return xk

# =============================================================================
# Kaon SF model parameters
# =============================================================================

@dataclass(frozen=True)
class ToyParams:
    a: float = 0.5
    b: float = 1.5
    Q0: float = 0.5

@dataclass(frozen=True)
class KaonModelParams:
    db_hard_valence: float = -0.5
    db_soft_valence: float = +0.5
    da_sbar_su3_break: float = +0.2
    db_sbar_su3_break: float = -0.4
    sea_amp: float = 0.05
    sea_a: float = 0.2
    sea_b: float = 4.0

# =============================================================================
# Kaon structure function (LO)
# =============================================================================

# e_f^2
_E2 = {
    1: 1.0 / 9.0,  # d
    2: 4.0 / 9.0,  # u
    3: 1.0 / 9.0,  # s
    4: 4.0 / 9.0,  # c
    5: 1.0 / 9.0,  # b
    6: 4.0 / 9.0,  # t
}


def beta_func(p: float, q: float) -> float:
    """Euler beta function: B(p,q) = Γ(p) Γ(q) / Γ(p+q)."""
    return math.gamma(p) * math.gamma(q) / math.gamma(p + q)


def toy_norm(a: float, b: float) -> float:
    """Normalization so that ∫_0^1 norm * x^a (1-x)^b dx = 1."""
    return 1.0 / beta_func(a + 1.0, b + 1.0)


def toy_shape_x(x: float, a: float, b: float, norm: float) -> float:
    """Normalized x-shape: norm * x^a (1-x)^b."""
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return norm * (x**a) * ((1.0 - x) ** b)


def F2_from_pdf_func(pdf_func: Callable[[int, float, float], float], x: float, Q2: float) -> float:
    """
    Generic LO F2:
      F2(x,Q2) = x * Σ_f e_f^2 [ q_f(x,Q2) + qbar_f(x,Q2) ]
    using flavors 1..6.

    pdf_func(pid, x, Q2) must return f(x,Q2) (not x*f).
    """
    s = 0.0
    for flav in range(1, 7):
        q = pdf_func(+flav, x, Q2)
        qb = pdf_func(-flav, x, Q2)
        s += _E2[flav] * (q + qb)
    return x * s