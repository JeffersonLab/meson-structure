"""Minimal EDM4eIC event-wise arrays for yield projections."""
from __future__ import annotations
import awkward as ak
import numpy as np

def branch(tree, coll, field, *, required=True):
    """Read an EDM4eIC collection field, accepting common ROOT branch layouts."""
    for key in (f'{coll}/{coll}.{field}', f'{coll}.{field}', f'{coll}/{field}'):
        if key in tree:
            return tree[key].array(library='ak')
    if required:
        raise KeyError(f'Missing {coll}.{field} in ROOT tree')
    return None

def first(array, n=None):
    """Convert an event-wise array to one scalar per event."""
    if n is not None:
        array = array[:n]
    if array is None:
        return None
    if array.ndim > 1:
        array = ak.firsts(array)
    return np.asarray(ak.to_numpy(ak.fill_none(array, np.nan)), dtype=float)

def leading(tree, collection, *, pdg=None, status=None, energy_from_mass=None):
    """Select highest-energy particle per event from a jagged collection."""
    px = branch(tree, collection, 'momentum.x')
    py = branch(tree, collection, 'momentum.y')
    pz = branch(tree, collection, 'momentum.z')
    E = branch(tree, collection, 'energy', required=False)
    if E is None:
        mass = branch(tree, collection, 'mass', required=False)
        if mass is None:
            mass = energy_from_mass
        if mass is None:
            raise KeyError(f'{collection}: neither energy nor mass available')
        E = np.sqrt(px * px + py * py + pz * pz + mass * mass)
    mask = ak.ones_like(px, dtype=bool)
    if pdg is not None:
        mask = mask & (branch(tree, collection, 'PDG') == pdg)
    if status is not None:
        mask = mask & (branch(tree, collection, 'generatorStatus') == status)
    E, px, py, pz = (a[mask] for a in (E, px, py, pz))
    order = ak.argsort(E, axis=1, ascending=False)
    return np.stack([first(a[order][:, :1]) for a in (E, px, py, pz)], axis=1)

def dis(tree, method):
    """Read the event-level Bjorken x and Q² for a reconstruction method."""
    collection = f'InclusiveKinematics{method}'
    return (first(branch(tree, collection, 'x')), first(branch(tree, collection, 'Q2')))

def beam_xl(particle, proton):
    """Light-cone energy fraction (E+p_parallel)/(E_beam+|p_beam|)."""
    p = proton[:, 1:]
    pmag = np.linalg.norm(p, axis=1)
    axis = np.divide(p, pmag[:, None], out=np.full_like(p, np.nan), where=pmag[:, None] > 0)
    ppar = np.sum(particle[:, 1:] * axis, axis=1)
    xl = (particle[:, 0] + ppar) / (proton[:, 0] + pmag)
    pt = np.linalg.norm(particle[:, 1:] - ppar[:, None] * axis, axis=1)
    return (xl, pt)

def meson_x(xb, xl):
    """Compute Sullivan meson momentum fraction from Bjorken x and x_L."""
    den = 1 - xl
    return np.divide(xb, den, out=np.full_like(xb, np.nan), where=den > 0)

def hist2(x, q, mask, xedges, qedges):
    """Count selected events in a two-dimensional kinematic histogram."""
    return np.histogram2d(x[mask], q[mask], bins=(xedges, qedges))[0]

def transitions(tx, tq, rx, rq, mask, src_edges, dst_edges, q_edges):
    """Count truth-to-reconstruction transitions between kinematic bins."""
    counts = np.zeros((len(dst_edges) - 1, len(q_edges) - 1, len(src_edges) - 1, len(q_edges) - 1))
    ids = [np.searchsorted(e, v[mask], side='right') - 1 for e, v in ((dst_edges, rx), (q_edges, rq), (src_edges, tx), (q_edges, tq))]
    good = np.logical_and.reduce([(a >= 0) & (a < n) for a, n in zip(ids, counts.shape)])
    np.add.at(counts, tuple((a[good] for a in ids)), 1)
    return counts
