"""Binned event-yield projections and uncertainty CSV exports (no model fitting)."""
from __future__ import annotations
import csv
import json
from pathlib import Path
import numpy as np

NB_PER_FB = 1_000_000.0


def centers(edges):
    """Return geometric bin centers from bin boundaries."""
    edges = np.asarray(edges, float)
    if edges.ndim != 1 or len(edges) < 2 or not np.all(np.diff(edges) > 0):
        raise ValueError('Bin edges must be strictly increasing')
    return np.sqrt(edges[:-1] * edges[1:]) if np.all(edges > 0) else (edges[:-1] + edges[1:]) / 2


def safe_divide(num, den, *, missing=np.nan):
    """Divide arrays, returning NaN where the denominator is invalid."""
    num, den = np.broadcast_arrays(np.asarray(num, float), np.asarray(den, float))
    result = np.full(num.shape, missing, dtype=float)
    np.divide(num, den, out=result, where=np.isfinite(den) & (den > 0) & np.isfinite(num))
    return result


def efficiency_and_response(truth_hist, tagged_hist, transitions):
    """Response conditional on having a tag; out-of-range destinations remain losses."""
    if np.any(tagged_hist > truth_hist):
        raise ValueError('Tagged counts exceed truth counts')
    efficiency = safe_divide(tagged_hist, truth_hist)
    response = safe_divide(transitions, tagged_hist[None, None, :, :], missing=0.0)
    if np.any(response.sum(axis=(0, 1)) > 1 + 1e-10):
        raise ValueError('Migration probabilities exceed one')
    return efficiency, response


def expected_yield(sigma_nb, efficiency, response, luminosity_fb):
    """sigma(source) -> tag efficiency(source) -> response(destination|tag,source)."""
    if luminosity_fb <= 0 or not np.isfinite(luminosity_fb):
        raise ValueError('Luminosity must be positive')
    tagged = NB_PER_FB * luminosity_fb * np.nan_to_num(sigma_nb * efficiency, nan=0.0)
    return np.einsum('abij,ij->ab', response, tagged)


def purity_rate_proxy(signal_counts, signal_events, mixed_counts, mixed_events):
    """Ratio of per-frame candidate rates, NOT an MC-ancestry purity measurement."""
    if min(signal_events, mixed_events) <= 0:
        raise ValueError('Both frame counts must be positive')
    s = np.asarray(signal_counts, float) / signal_events
    m = np.asarray(mixed_counts, float) / mixed_events
    raw = safe_divide(s, m)
    # A zero-denominator bin is unknown, even if signal-only contains entries.
    return np.where(np.isfinite(raw), np.clip(raw, 0, 1), np.nan)


def relative_statistical_error(signal, purity=None):
    """Counting-only: 1/sqrt(S); proxy background: sqrt(S+B)/S.

    The latter assumes a known background expectation and Poisson count variance;
    background-normalization and time-overlay uncertainties are NOT included.
    """
    signal = np.asarray(signal, float)
    effective = signal if purity is None else signal * np.asarray(purity, float)
    stat = np.full(signal.shape, np.nan)
    valid = np.isfinite(effective) & (effective > 0) & np.isfinite(signal) & (signal > 0)
    stat[valid] = 1 / np.sqrt(effective[valid])
    return stat, effective


def export_uncertainties(outdir, channel, beam, method, luminosity, x_edges, q_edges,
                         signal, *, purity=None, scenario='signal_only', min_events=1.0,
                         metadata=None):
    """Export full-bin 2D and Q2-integrated 1D CSV with stable column names."""
    xcent, qcent = centers(x_edges), centers(q_edges)
    signal = np.asarray(signal, float)
    if signal.shape != (len(xcent), len(qcent)):
        raise ValueError(f'Yield shape mismatch: {signal.shape}')
    if purity is not None and np.asarray(purity).shape != signal.shape:
        raise ValueError('Purity map has incompatible shape')
    stat, effective = relative_statistical_error(signal, purity)
    stat = np.where(effective >= min_events, stat, np.nan)
    folder = Path(outdir) / 'uq_csv' / scenario / method.lower()
    folder.mkdir(parents=True, exist_ok=True)
    tag = f'{channel}_stat_uq_{beam}_L{luminosity:g}fb'.replace('L0.', 'L0p')
    fields = ['x', 'Q2', 'Nexpected', 'N_effective', 'stat_rel', 'stat_rel_percent',
              'purity_proxy', 'x_min', 'x_max', 'Q2_min', 'Q2_max']
    path2 = folder / f'{tag}_2D.csv'
    with path2.open('w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields); writer.writeheader()
        for ix, x in enumerate(xcent):
            for iq, q in enumerate(qcent):
                u = stat[ix, iq]
                writer.writerow(dict(x=x, Q2=q, Nexpected=signal[ix, iq],
                                     N_effective=effective[ix, iq], stat_rel=u,
                                     stat_rel_percent=100*u, purity_proxy=np.nan if purity is None else purity[ix, iq],
                                     x_min=x_edges[ix], x_max=x_edges[ix+1],
                                     Q2_min=q_edges[iq], Q2_max=q_edges[iq+1]))
    total = np.sum(signal, axis=1)
    # For integrated uncertainty combine signal + background variances over Q2 bins.
    if purity is None:
        effective_1d = total.copy()
    else:
        valid = (np.asarray(purity) > 0) & np.isfinite(purity)
        # Unknown contamination in a populated bin makes the Q2-integrated result undefined.
        unknown = np.any((signal > 0) & ~valid, axis=1)
        variance = np.sum(np.divide(signal, purity, out=np.zeros_like(signal), where=valid), axis=1)
        effective_1d = safe_divide(total**2, variance)
        effective_1d[unknown] = np.nan
    stat1 = np.full(total.shape, np.nan)
    valid1 = np.isfinite(effective_1d) & (effective_1d >= min_events) & (effective_1d > 0)
    stat1[valid1] = 1 / np.sqrt(effective_1d[valid1])
    path1 = folder / f'{tag}.csv'
    with path1.open('w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['x','Nexpected','N_effective','stat_rel','stat_rel_percent','x_min','x_max'])
        writer.writeheader()
        for i, x in enumerate(xcent):
            writer.writerow(dict(x=x,Nexpected=total[i],N_effective=effective_1d[i],
                                 stat_rel=stat1[i],stat_rel_percent=100*stat1[i],
                                 x_min=x_edges[i],x_max=x_edges[i+1]))
    return path1, path2
