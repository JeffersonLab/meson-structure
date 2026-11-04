"""ePIC pion Sullivan neutron analysis. See README.md for limitations."""
from __future__ import annotations
import math
import numpy as np
from config import BEAM_DIR, BEAM_MOM, NEUTRON_MASS, PROTON_ENERGY, PROTON_P

def vec_from_four(E, px, py, pz, mass=NEUTRON_MASS):
    """Compute vec from four for the analysis."""
    p = np.array([px, py, pz], float)
    if not np.all(np.isfinite(p)):
        return None
    pm = float(np.linalg.norm(p))
    if not np.isfinite(E):
        E = float(np.hypot(pm, mass))
    if not np.isfinite(E):
        return None
    pt = float(np.linalg.norm(p - np.dot(p, BEAM_DIR) * BEAM_DIR))
    parallel = float(np.dot(p, BEAM_DIR))
    minus_t = float((BEAM_MOM - p) @ (BEAM_MOM - p) - (PROTON_ENERGY - E) ** 2)
    angle_beam = 1000 * float(np.arctan2(pt, parallel))
    return {'E': float(E), 'px': float(px), 'py': float(py), 'pz': float(pz), 'p': pm, 'pt_beam': pt, 'theta_mrad': 1000 * math.atan2(math.hypot(px, py), pz), 'theta_beam_mrad': angle_beam, 'phi': math.atan2(py, px), 'eta': math.asinh(pz / max(math.hypot(px, py), 1e-15)), 'xL': parallel / PROTON_P, 'minus_t': minus_t, 'mass': float(mass) if np.isfinite(mass) else np.nan, 'delta_phi_pi': float(np.pi - abs(math.atan2(py, px))), 'W': np.nan, 'MX': np.nan}
