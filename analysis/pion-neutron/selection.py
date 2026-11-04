"""ePIC pion Sullivan neutron analysis. See README.md for limitations."""
from __future__ import annotations
from collections import Counter
import numpy as np
from tqdm.auto import tqdm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from config import COLORS, CUTS, METRICS
from root_io import writecsv
from plotting import plot_purity, plot_spectrum

def passes(r, cut):
    """Compute passes for the analysis."""
    _, metric, lo, hi = cut
    if lo is None and hi is None:
        return True
    x = r.get(metric, np.nan)
    return bool(np.isfinite(x) and (lo is None or x >= lo) and (hi is None or x < hi))

def summarize(rows, generated):
    """Compute summarize for the analysis."""
    counts = Counter((r['category'] for r in rows))
    s, c, u = (counts[k] for k in ('signal', 'combinatorial', 'unclassified'))
    return {'total': len(rows), 'signal': s, 'combinatorial': c, 'unclassified': u, 'signal_fraction': s / (s + c) if s + c else np.nan, 'signal_fraction_all': s / len(rows) if rows else np.nan, 'candidate_yield_per_generated_neutron': len(rows) / generated if generated else np.nan, 'signal_yield_per_generated_neutron': s / generated if generated else np.nan, 'combinatorial_yield_per_generated_neutron': c / generated if generated else np.nan}

def cut_study(rows, generated, out, sample):
    """Compute cut study for the analysis."""
    folder = out / 'reconstruction' / 'purity'
    folder.mkdir(parents=True, exist_ok=True)
    stages = [('raw', rows)]
    active = [c for c in CUTS if c[2] is not None or c[3] is not None]
    current = rows
    for cut in active:
        current = [r for r in current if passes(r, cut)]
        stages.append((cut[0], current))
    results = [{'stage': name, **summarize(selected, generated)} for name, selected in stages]
    fig, ax = plt.subplots(figsize=(max(6.0, 1.2 * len(stages) + 2), 6.0))
    xx = np.arange(len(stages))
    den = max(1, generated)
    sval = np.asarray([100 * row['signal'] / den for row in results])
    cval = np.asarray([100 * row['combinatorial'] / den for row in results])
    uval = np.asarray([100 * row['unclassified'] / den for row in results])
    ax.bar(xx, sval, color=COLORS['signal'], label='Sullivan-origin candidate', width=0.72)
    ax.bar(xx, cval, bottom=sval, color=COLORS['combinatorial'], label='Background', width=0.72)
    if np.any(uval):
        ax.bar(xx, uval, bottom=sval + cval, color=COLORS['unclassified'], label='Unclassified', width=0.72)
    maximum = max(1.0, float(np.max(sval + cval + uval)))
    for i, row in enumerate(results):
        y = sval[i] + cval[i] + uval[i]
        p = row['signal_fraction']
        ax.text(i, y + max(0.4, maximum * 0.018), f"P = {100 * p:.1f}%\nN = {row['total']}", ha='center', va='bottom', fontsize=10)
    ax.set_xticks(xx, [r['stage'] for r in results], rotation=25, ha='right')
    ax.set_ylabel('Reconstructed neutrons and purity (%)')
    ax.set_ylim(0, maximum * 1.24 + 1)
    ax.legend(fontsize=13)
    ax.minorticks_on()
    fig.tight_layout()
    fig.savefig(folder / f'truth_cutflow_{sample}.png')
    plt.close(fig)
    pass  # No intermediate data export.
    pass  # No intermediate data export.
    return results
