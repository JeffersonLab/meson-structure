"""Histogram and map rendering for Lambda reconstruction.

Histograms preserve zero bins; event tagging maps are not truth matched efficiencies.
"""
from __future__ import annotations
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from config import (
    XB_EDGES, Q2_EDGES, COLOR_MC, COLOR_NO_BACKGROUND,
    COLOR_WITH_BACKGROUND, COLOR_COMMON_LAMBDA, COLOR_AUXILIARY,
    PLOT_LOG_COUNTS, PLOT_FULL_DATA_RANGE, PLOT_Y_HEADROOM,
    PLOT_AUTO_LOG_X, PLOT_AUTO_SYMLOG_X, PLOT_LOG_X_DYNAMIC_RANGE,
)

plt.rcParams.update({
    "font.family": "STIXGeneral",
    "mathtext.fontset": "stix",
    "font.size": 13,
    "axes.titlesize": 15,
    "axes.labelsize": 14,
    "legend.fontsize": 10.5,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "axes.linewidth": 1.2,
    "axes.grid": False,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.major.size": 6,
    "ytick.major.size": 6,
    "xtick.minor.size": 3,
    "ytick.minor.size": 3,
    "xtick.major.width": 1.1,
    "ytick.major.width": 1.1,
    "xtick.minor.width": 0.9,
    "ytick.minor.width": 0.9,
    "legend.frameon": False,
    "figure.dpi": 120,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

from common.data import finite, percent_weights as _percent_weights


def _log_norm_from_positive(values, floor=None):
    """LogNorm spanning strictly positive finite values."""
    a = np.asarray(values, dtype=float)
    positive = a[np.isfinite(a) & (a > 0)]
    if not positive.size:
        return None
    vmin = float(positive.min()) if floor is None else max(float(floor), float(positive.min()))
    vmax = float(positive.max())
    if vmax <= vmin:
        return None
    return LogNorm(vmin=vmin, vmax=vmax)


def _style_hist_axes(ax, *, values=None, xlabel='', log_y=True, log_x='auto'):
    """Style axes without replacing zero with a positive plotting floor."""
    if log_y and PLOT_LOG_COUNTS:
        # A true log scale cannot display zero; symlog keeps the REAL zero.
        threshold = getattr(ax, '_hist_linthresh', 1e-2)
        ax.set_yscale('symlog', linthresh=threshold, linscale=0.5)
        ax.set_ylim(bottom=0)
    elif not PLOT_LOG_COUNTS:
        ax.set_yscale('linear')
        ax.set_ylim(bottom=0)
    if values is not None and PLOT_AUTO_LOG_X:
        v = finite(values)
        if v.size:
            nonzero = np.abs(v[np.abs(v) > 0])
            signed = bool(np.any(v < 0))
            if not signed and v.min() > 0 and ax.get_xlim()[0] > 0 and v.max()/v.min() >= PLOT_LOG_X_DYNAMIC_RANGE:
                ax.set_xscale('log')
            elif (signed and PLOT_AUTO_SYMLOG_X and nonzero.size > 0 and
                  np.max(nonzero)/np.min(nonzero) >= PLOT_LOG_X_DYNAMIC_RANGE):
                if not any(token in xlabel.lower() for token in ('mass', 'm_{', 'eta', 'phi', 'fraction')):
                    ax.set_xscale('symlog', linthresh=float(np.quantile(nonzero, .05)))
    ax.minorticks_on()
    ax.tick_params(which='both', direction='in', top=True, right=True)


def plot_stairs(ax, values, edges, *, weights=None, color=None, label=None,
                linewidth=2.0, log_floor=True):
    """Conventional, SINGLE CONTINUOUS step histogram, including TRUE zero bins.

    Symlog is logarithmic for positive populations above linthresh and linear
    near the origin, making zero mathematically representable. No counts are
    modified; in particular, no artificial positive floor is introduced.
    """
    v = np.asarray(values, dtype=float)
    good = np.isfinite(v)
    v = v[good]
    if not v.size:
        return None
    w = None if weights is None else np.asarray(weights, dtype=float)[good]
    counts, boundaries = np.histogram(v, bins=edges, weights=w)
    positive = counts[np.isfinite(counts) & (counts > 0)]
    if not positive.size:
        return counts
    # Draw ONE complete stair path: vertical walls down to genuine zero.
    ax.stairs(counts, boundaries, baseline=0, color=color, label=label,
              linewidth=linewidth)
    maxval = max(float(positive.max()), getattr(ax, '_hist_largest', 0.))
    ax._hist_largest = maxval
    if PLOT_LOG_COUNTS and log_floor:
        smallest = min(float(positive.min()), getattr(ax, '_hist_smallest', float('inf')))
        ax._hist_smallest = smallest
        # Display parameter only: not a replacement of empty bins.
        threshold = 0.5 * smallest
        ax._hist_linthresh = threshold
        ax.set_yscale('symlog', linthresh=threshold, linscale=0.5)
        ax.set_ylim(bottom=0, top=maxval * PLOT_Y_HEADROOM)
    else:
        ax.set_yscale('linear')
        ax.set_ylim(bottom=0, top=maxval * PLOT_Y_HEADROOM)
    return counts


def _square_figure():
    """Compute square figure for the analysis."""
    return plt.subplots(figsize=(6.0, 6.0))


def save_1d(values, path, label, title=None, bins=45, other=None, background=None,
            denominator=None, integral_label=None):
    """Publication-style 1D histogram.

    Each displayed distribution is normalized to 100%, so shapes can be
    compared independently of the number of simulated events.  For plots
    representing an event-level selection, denominator can be supplied to
    put the physically relevant integrated fraction in the title.
    """
    a = finite(values)
    b = finite(other) if other is not None else np.array([])
    c = finite(background) if background is not None else np.array([])
    if not len(a) and not len(b) and not len(c):
        return False

    joint = np.concatenate([v for v in (a, b, c) if len(v)])
    if label in ('eta',):
        edges = np.linspace(max(-1., (np.min(joint) if PLOT_FULL_DATA_RANGE else np.nanpercentile(joint, 1))-.2),
                            min(15., (np.max(joint) if PLOT_FULL_DATA_RANGE else np.nanpercentile(joint, 99))+.2), bins+1)
    elif label == 'mass' and 'lambda' in str(path).lower():
        edges = np.linspace(0.9, 1.4, bins+1)
    else:
        lo, hi = np.nanpercentile(joint, [0, 100])
        if hi <= lo:
            hi = lo + 1.
        edges = np.linspace(lo, hi, bins+1)

    fig, ax = plt.subplots(figsize=(6.0, 6.0))
    ax.set_yscale('log' if PLOT_LOG_COUNTS else 'linear')
    if len(a):
        plot_stairs(ax, a, edges, weights=_percent_weights(a), color=COLOR_MC,
                    label='MC truth' if (other is not None or background is not None) else 'Events')
    if len(b):
        plot_stairs(ax, b, edges, weights=_percent_weights(b), color=COLOR_NO_BACKGROUND,
                    label='Reco (signal only)')
    if len(c):
        plot_stairs(ax, c, edges, weights=_percent_weights(c), color=COLOR_WITH_BACKGROUND,
                    label='Reco + background')

    ax.set_xlabel(label)
    ax.set_ylabel('Fraction [%]')
    if denominator:
        parts = []
        if len(b):
            parts.append(f"signal: {100.0*len(b)/denominator:.2f}%")
        if len(c):
            parts.append(f"with bkg: {100.0*len(c)/denominator:.2f}%")
        prefix = integral_label or "Integrated"
        ax.set_title(prefix + " — " + ", ".join(parts))
    elif title:
        ax.set_title(title)

    if other is not None or background is not None:
        ax.legend()
    _style_hist_axes(ax, values=joint, xlabel=label)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)
    return True


def save_2d(x, y, path, xlabel, ylabel, title=None, edges=None, weights=None,
            normalize_percent=True):
    """Square 2D map with logarithmic colour scale.

    Unweighted occupancy maps are expressed as percent of entries. Weighted
    maps retain their physical weights unless normalize_percent=True.
    """
    x, y = np.asarray(x, float), np.asarray(y, float)
    mask = np.isfinite(x) & np.isfinite(y)
    if weights is not None:
        w = np.asarray(weights, float)
        mask &= np.isfinite(w)
        w = w[mask]
    else:
        w = None
    x, y = x[mask], y[mask]
    if not len(x):
        return False

    if edges is None:
        def axis(v):
            """Compute axis for the analysis."""
            lo, hi = np.percentile(v, [0.5, 99.5])
            if hi <= lo:
                hi = lo + 1.
            return np.linspace(lo, hi, 41)
        edges = (axis(x), axis(y))

    H, xe, ye = np.histogram2d(x, y, bins=edges, weights=w)
    if normalize_percent and H.sum() > 0:
        H = 100.0 * H / H.sum()
        cbar_label = 'Fraction [%]'
    else:
        cbar_label = 'Counts' if w is None else 'Weighted sum'

    z = np.ma.masked_where(~np.isfinite(H.T) | (H.T <= 0), H.T)
    norm = _log_norm_from_positive(H)
    fig, ax = plt.subplots(figsize=(6.2, 6.0))
    img = ax.pcolormesh(xe, ye, z, shading='auto', cmap='viridis', norm=norm)
    fig.colorbar(img, ax=ax, label=cbar_label)

    if np.min(xe) > 0 and np.max(xe)/np.min(xe) > PLOT_LOG_X_DYNAMIC_RANGE:
        ax.set_xscale('log')
    if np.min(ye) > 0 and np.max(ye)/np.min(ye) > PLOT_LOG_X_DYNAMIC_RANGE:
        ax.set_yscale('log')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.minorticks_on()
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)
    return True


def save_eff2d(x, y, numerator, denominator, path, xlabel='xB truth',
               ylabel='Q2 truth', title=None):
    """Compute save eff2d for the analysis."""
    x, y = np.asarray(x), np.asarray(y)
    numerator, denominator = np.asarray(numerator, bool), np.asarray(denominator, bool)
    sel = np.isfinite(x) & np.isfinite(y) & denominator
    total = np.histogram2d(x[sel], y[sel], bins=(XB_EDGES, Q2_EDGES))[0]
    passed = np.histogram2d(x[sel & numerator], y[sel & numerator],
                            bins=(XB_EDGES, Q2_EDGES))[0]
    fraction = np.divide(passed, total, out=np.full_like(total, np.nan), where=total>0)
    err = np.sqrt(np.divide(fraction*(1-fraction), total,
                            out=np.full_like(total,np.nan), where=total>0))

    n_den = int(np.count_nonzero(sel))
    n_num = int(np.count_nonzero(sel & numerator))
    integrated = n_num / n_den if n_den else np.nan

    path.parent.mkdir(parents=True, exist_ok=True)
    pass  # No intermediate data export.

    frac_pct = 100.0 * fraction
    z = np.ma.masked_where(~np.isfinite(frac_pct.T) | (frac_pct.T <= 0), frac_pct.T)
    norm = _log_norm_from_positive(frac_pct)
    fig, ax = plt.subplots(figsize=(6.2, 6.0))
    im = ax.pcolormesh(XB_EDGES, Q2_EDGES, z, shading='auto',
                       cmap='viridis', norm=norm)
    fig.colorbar(im, ax=ax, label='Event fraction [%]')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(f'Total: {100.0*integrated:.2f}% ({n_num}/{n_den})'
                 if np.isfinite(integrated) else 'Total: n/a')
    ax.minorticks_on()
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return fraction



def plot_structure_models(beam, uq_dir, output_dir, *, models=('DSE', 'JAM'),
                          components=('valence', 'glue'), scenarios=None):
    """Plot configured model scenarios using UQ CSV inputs; return output paths."""
    from common.model_plotting import SCENARIOS, plot_dse, plot_jam
    from config import (MODEL_POINT_TO_POINT_SYSTEMATIC, MODEL_JAM_SET,
                        MODEL_JAM_Q2_GEV2, MODEL_LHAPDF_PATH, MODEL_E615_DATA)
    scenarios = SCENARIOS if scenarios is None else scenarios
    saved = []
    for model in models:
        for component in components:
            for scenario in scenarios:
                folder = output_dir / 'models' / model.lower()
                if model == 'DSE':
                    paths = plot_dse('kaon', beam, component, scenario, uq_dir, folder,
                                     p2p=MODEL_POINT_TO_POINT_SYSTEMATIC,
                                     e615_file=MODEL_E615_DATA)
                elif model == 'JAM':
                    paths = plot_jam('kaon', beam, component, scenario, uq_dir, folder,
                                     set_name=MODEL_JAM_SET, q2=MODEL_JAM_Q2_GEV2,
                                     p2p=MODEL_POINT_TO_POINT_SYSTEMATIC,
                                     lhapdf_path=MODEL_LHAPDF_PATH)
                else:
                    raise ValueError(f'Unknown model: {model}')
                saved.extend(paths)
    return saved
