"""Kinematics and neutral decay candidate helpers."""
from __future__ import annotations
import numpy as np
import matplotlib
matplotlib.use("Agg")
from config import (DETECTORS, M_PI0, PROTON_DIRECTION, PROTON_E, PROTON_P, PROTON_PX, PROTON_PY, PROTON_PZ)


def beam_pt(row):
    """Momentum transverse to incident proton axis, in GeV."""
    v = np.array([row['px'], row['py'], row['pz']], dtype=float)
    return float(np.linalg.norm(v - np.dot(v, PROTON_DIRECTION) * PROTON_DIRECTION))


def lambda_transfer_and_xl(energy, px, py, pz):
    """Calculate t=(p_proton-p_lambda)^2 and beam-axis xL in lab coordinates."""
    delta_e = PROTON_E - energy
    delta_px = PROTON_PX - px
    delta_py = PROTON_PY - py
    delta_pz = PROTON_PZ - pz
    t = delta_e**2 - delta_px**2 - delta_py**2 - delta_pz**2
    p_parallel = px * PROTON_DIRECTION[0] + py * PROTON_DIRECTION[1] + pz * PROTON_DIRECTION[2]
    return -t, p_parallel / PROTON_P


def pi0_from_two_photons(g1, g2):
    """Reconstruct pi0 four-vector from two photon candidates (GeV units)."""
    E = g1['E'] + g2['E']
    px = g1['px'] + g2['px']
    py = g1['py'] + g2['py']
    pz = g1['pz'] + g2['pz']
    m2 = E*E - px*px - py*py - pz*pz
    if not np.isfinite(m2) or m2 < -1e-6:
        return None
    m = np.sqrt(max(0.0, m2))
    pt = np.hypot(px, py)
    mom = np.hypot(pt, pz)
    return {'E':E, 'px':px,'py':py,'pz':pz, 'p':mom,'pt':pt,
            'mass':m, 'theta_mrad':1000*np.arctan2(pt,pz),
            'eta':np.arcsinh(pz/pt) if pt>1e-12 else np.nan,
            'phi':np.arctan2(py,px)}


def collect_pi0_pairs(event_det):
    """All unique unordered photon pairs across the THREE detectors.

    No relation-based matching or cluster deduplication is available.
    """
    photons = [(name, k) for name in DETECTORS for k in event_det[name]
               if k['_pdg'] == 22]
    pairs = []
    for i in range(len(photons)):
        for j in range(i+1, len(photons)):
            cand = pi0_from_two_photons(photons[i][1], photons[j][1])
            if cand is not None:
                cand['detectors'] = (photons[i][0], photons[j][0])
                pairs.append(cand)
    return pairs


def select_best_pi0(pairs):
    """Select best pi0 candidates."""
    return min(pairs, key=lambda k:abs(k['mass']-M_PI0)) if pairs else None


def _mc_lambda_candidates(event):
    """Return Sullivan-source MC Lambdas, as in the earlier working study.

    Crucially, source=0 is the generator-status BLOCK (status//1000 == 0),
    not status==0. Do not veto on MC production vertex here: that veto was
    responsible for discarding otherwise matchable generator records.
    """
    return [r for r in event
            if r.get('_pdg') == 3122
            and 0 <= int(r.get('_status', -1)) < 1000
            and np.isfinite(r.get('E', np.nan))
            and np.isfinite(r.get('cos_theta', np.nan))]


def _primary_mc_lambda(event):
    """Compute primary mc lambda for the analysis."""
    candidates = _mc_lambda_candidates(event)
    if not candidates:
        return None
    forward = [r for r in candidates if r['cos_theta'] > 0.99]
    return max(forward or candidates, key=lambda r: r['E'])

