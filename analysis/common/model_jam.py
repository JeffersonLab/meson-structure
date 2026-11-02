"""LHAPDF replica observables and covariance-based pseudo-data reweighting."""
from __future__ import annotations
import numpy as np

CHARGES2 = {1: 1 / 9, 2: 4 / 9, 3: 1 / 9, 4: 4 / 9}


def load_replicas(set_name, extra_path=None):
    """Load LHAPDF replicas excluding central member zero; return replica objects.

    Args:
        set_name, extra_path: Inputs and configuration for this operation.
    Returns:
        Computed data or saved file paths, as described above.
    """
    try:
        import lhapdf  # pylint: disable=import-outside-toplevel
    except ImportError as exc:
        raise RuntimeError('JAM plotting requires LHAPDF6 Python bindings') from exc
    if extra_path:
        lhapdf.setPaths([str(extra_path), *[p for p in lhapdf.paths() if p != str(extra_path)]])
    replicas = lhapdf.getPDFSet(set_name).mkPDFs()[1:]
    if len(replicas) < 2:
        raise ValueError(f'{set_name}: expected at least two replica members after member 0')
    return replicas


def evaluate(pdfs, x, component, q2):
    """Evaluate LO F2, valence contribution, or scaled xg for each replica and x.

    Args:
        pdfs, x, component, q2: Inputs and configuration for this operation.
    Returns:
        Computed data or saved file paths, as described above.
    """
    result = np.empty((len(pdfs), len(x)), dtype=float)
    for i, pdf in enumerate(pdfs):
        for j, xx in enumerate(x):
            xx = float(xx)
            if component == 'glue':
                result[i, j] = pdf.xfxQ2(21, xx, q2) * (10 * xx) ** 2
                continue
            pairs = [(pdf.xfxQ2(pid, xx, q2), pdf.xfxQ2(-pid, xx, q2), e2)
                     for pid, e2 in CHARGES2.items()]
            result[i, j] = sum(e2 * (abs(q - qb) if component == 'valence' else q + qb)
                               for q, qb, e2 in pairs)
    return result


def weighted_statistics(values, weights):
    """Return weighted mean and population standard deviation across replicas.

    Args:
        values, weights: Inputs and configuration for this operation.
    Returns:
        Computed data or saved file paths, as described above.
    """
    mean = weights @ values
    variance = weights @ (values - mean) ** 2
    return mean, np.sqrt(np.maximum(variance, 0))


def reweight_f2(f2_replicas, stat_rel, p2p_rel, flux_rel):
    """Fit replica weights to mean F2 pseudo-data with correlated flux covariance.

    Args:
        f2_replicas, stat_rel, p2p_rel, flux_rel: Inputs and configuration for this operation.
    Returns:
        Computed data or saved file paths, as described above.
    """
    f2 = np.asarray(f2_replicas, float)
    relative = np.asarray(stat_rel, float)
    center = np.mean(f2, axis=0)
    uncorr = center * np.hypot(relative, p2p_rel)
    valid = np.isfinite(center) & (center > 0) & np.isfinite(uncorr) & (uncorr > 0)
    if not np.any(valid):
        raise ValueError('No valid F2 pseudo-data bins for replica reweighting')
    central, err = center[valid], uncorr[valid]
    cov = np.diag(err ** 2) + flux_rel ** 2 * np.outer(central, central)
    inv = np.linalg.pinv(cov, hermitian=True)
    residual = f2[:, valid] - central
    chi2 = np.einsum('ni,ij,nj->n', residual, inv, residual)
    weights = np.exp(-.5 * (chi2 - np.min(chi2)))
    weights /= weights.sum()
    return weights, 1 / np.sum(weights ** 2)
