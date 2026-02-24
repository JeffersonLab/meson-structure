from __future__ import annotations
import numpy as np
from .config import PhysicsConstants, DEFAULT_CONST


def parse_proton_energy(beam_str: str) -> float:
    s = str(beam_str)
    if "x" in s:
        return float(s.split("x")[-1])
    return float(s)


def direct_energy_window(beam: str) -> tuple[float, float]:
    if beam == "5x41":
        return 20.0, 41.0
    if beam == "10x100":
        return 50.0, 100.0
    if beam == "18x275":
        return 130.0, 275.0
    raise ValueError(f"Unknown beam config: {beam}")


def E_to_L(E_GeV: np.ndarray | float, c: PhysicsConstants = DEFAULT_CONST) -> np.ndarray:
    E = np.asarray(E_GeV, dtype=np.float64)
    m = c.m_lambda_gev
    # <L> = (sqrt(E^2 - m^2)/m) * c*tau
    return c.ctau_lambda_m * np.sqrt(np.maximum(E * E - m * m, 0.0)) / m


def L_to_E(L_m: np.ndarray | float, c: PhysicsConstants = DEFAULT_CONST) -> np.ndarray:
    L = np.asarray(L_m, dtype=np.float64)
    m = c.m_lambda_gev
    # E = sqrt((m*L/ctau)^2 + m^2)
    return np.sqrt((m * L / c.ctau_lambda_m) ** 2 + m * m)


def proton_kinematics_for_beam(beam: str, c: PhysicsConstants = DEFAULT_CONST) -> dict[str, float | np.ndarray]:
    """
    Returns:
      - Ep, p_mag, nhat, pplus_p
      - proton 4-vector components (ppx,ppy,ppz,ppE) for t computation
    """
    Ep = parse_proton_energy(beam)
    p_mag = np.sqrt(max(Ep * Ep - c.mp_gev * c.mp_gev, 0.0))
    th = c.theta_proton_rad
    nhat = np.array([np.sin(th), 0.0, np.cos(th)], dtype=np.float64)
    pplus_p = Ep + p_mag
    ppx = p_mag * np.sin(th)
    ppy = 0.0
    ppz = p_mag * np.cos(th)
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
    denom = 1.0 - xl
    xk = np.full_like(xb, np.nan, dtype=np.float64)
    ok = np.isfinite(xb) & np.isfinite(denom) & (denom > 0)
    xk[ok] = xb[ok] / denom[ok]
    return xk