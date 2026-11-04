"""Histograms, candidate-composition plots and background diagnostics."""
from __future__ import annotations
import json
from collections import Counter
import numpy as np
import awkward as ak
import uproot
from tqdm.auto import tqdm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from config import BACKGROUND_SAMPLE_EVENTS, BEAM_DIR, COLORS, METRICS, PLOT_FULL_DATA_RANGE, PLOT_HIST_LOG_Y, PLOT_MAP_LOG_Y, PLOT_Y_HEADROOM, SOURCES
from root_io import writecsv, resolved, getchunk
plt.rcParams.update({'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix', 'font.size': 13, 'axes.labelsize': 13, 'axes.titlesize': 13, 'legend.fontsize': 13, 'legend.frameon': False, 'axes.linewidth': 1.1, 'axes.grid': False, 'xtick.direction': 'in', 'ytick.direction': 'in', 'xtick.top': True, 'ytick.right': True, 'xtick.major.size': 13, 'ytick.major.size': 13, 'xtick.minor.size': 3, 'ytick.minor.size': 3, 'savefig.dpi': 300, 'figure.dpi': 120})
from common.data import finite

def plot_purity(rows, path, label):
    """Readable absolute reconstructed-candidate composition and classified purity."""
    counts = Counter((r['category'] for r in rows))
    n = len(rows)
    s = counts['signal']
    b = counts['combinatorial']
    u = counts['unclassified']
    if not n:
        return
    fig, ax = plt.subplots(figsize=(7.0, 5.7))
    parts = [('Sullivan signal', s, COLORS['signal']), ('Background', b, COLORS['combinatorial']), ('Unclassified', u, COLORS['unclassified'])]
    left = 0.0
    for name, c, color in parts:
        percent = 100.0 * c / n
        if c:
            ax.barh([0], percent, left=left, height=0.42, color=color, label=f'{name}: {percent:.1f}% ({c:,})')
            if percent >= 8:
                ax.text(left + percent / 2, 0, f'{percent:.1f}%', ha='center', va='center', color='white' if color != COLORS['unclassified'] else 'black', fontsize=13, fontweight='bold')
        left += percent
    known = s + b
    purity = 100.0 * s / known if known else float('nan')
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.65, 1.15)
    ax.set_yticks([])
    ax.set_xlabel('Fraction of all reconstructed neutron candidates [%]')
    ax.set_title(label)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0.8), fontsize=13)
    ax.text(0.5, 0.96, f'Classified purity (signal / [signal + background]): {purity:.1f}%' if known else 'Classified purity: unavailable', transform=ax.transAxes, ha='center', va='center', fontsize=13)
    ax.text(0.5, 0.89, f'N = {n:,} reconstructed candidates | classified = {known:,}', transform=ax.transAxes, ha='center', va='center', fontsize=13)
    ax.tick_params(axis='y', left=False, right=False)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)
    pass  # No intermediate data export.

def stairs(ax, values, edges, color, label, den=None):
    """Continuous conventional step histogram, including true zero bins.

 symlog displays zero honestly, while retaining logarithmic scaling above
 the smallest populated bin. No fake floor, masking, or disconnected paths.
 """
    v = finite(values)
    if not len(v):
        return None
    weights = np.full(len(v), 100.0 / den) if den else None
    counts, _ = np.histogram(v, bins=edges, weights=weights)
    if not np.any(counts > 0):
        return counts
    ax.stairs(counts, edges, baseline=0, color=color, lw=1.9, label=f'{label} (N={len(v)})')
    positive = counts[counts > 0]
    ax._hist_smallest = min(float(positive.min()), getattr(ax, '_hist_smallest', float('inf')))
    ax._hist_largest = max(float(positive.max()), getattr(ax, '_hist_largest', 0.0))
    if PLOT_HIST_LOG_Y:
        ax.set_yscale('symlog', linthresh=ax._hist_smallest * 0.5, linscale=0.5)
        ax.set_ylim(0, ax._hist_largest * PLOT_Y_HEADROOM)
    else:
        ax.set_yscale('linear')
        ax.set_ylim(0, ax._hist_largest * 1.15)
    return counts

def plot_spectrum(groups, key, path, normalize='each'):
    """Plot spectrum diagnostic distributions."""
    arrays = [finite((rr.get(key, np.nan) for rr in rows)) for _, rows in groups]
    if not any((len(v) for v in arrays)):
        return
    joint = np.concatenate([v for v in arrays if len(v)])
    if key == 'xL':
        lo, hi = (-0.2, 1.5)
    elif key == 'phi':
        lo, hi = (-np.pi, np.pi)
    elif key == 'delta_phi_pi':
        lo, hi = (0.0, np.pi)
    elif key in ('theta_beam_mrad', 'theta_mrad'):
        lo, hi = (0.0, max(110.0, float(np.max(joint)) * 1.05))
    elif key == 'minus_t':
        lo, hi = (np.min(joint), np.max(joint)) if PLOT_FULL_DATA_RANGE else np.percentile(joint, [0.5, 99.5])
    elif key == 'mass':
        lo, hi = (0.5, 1.4)
    else:
        lo, hi = (np.min(joint), np.max(joint)) if PLOT_FULL_DATA_RANGE else np.percentile(joint, [0.5, 99.5])
        lo = float(lo)
        hi = float(hi)
    if hi <= lo:
        hi = lo + 1
    edges = np.linspace(lo, hi, 64)
    fig, ax = plt.subplots(figsize=(6, 6))
    total = sum((len(v) for v in arrays))
    for (label, rows), v in zip(groups, arrays):
        col = COLORS.get(label, COLORS['truth'])
        stairs(ax, v, edges, col, label, den=total if normalize == 'common' else len(v))
    ax.set(xlabel=METRICS.get(key, key), ylabel='Fraction of candidates [%]')
    ax.legend(loc='best', fontsize=13)
    ax.minorticks_on()
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)

def plot_xy(rows, x, y, path, title=None):
    """Plot xy diagnostic distributions."""
    xy = np.asarray([(r[x], r[y]) for r in rows if np.isfinite(r.get(x, np.nan)) and np.isfinite(r.get(y, np.nan))], float)
    if not len(xy):
        return
    fig, ax = plt.subplots(figsize=(6, 6))
    h, xedge, yedge = np.histogram2d(xy[:, 0], xy[:, 1], bins=25)
    z = np.ma.masked_where(h.T <= 0, h.T)
    img = ax.pcolormesh(xedge, yedge, z, norm=LogNorm(vmin=1, vmax=max(2, h.max())), cmap='viridis')
    fig.colorbar(img, ax=ax, label='Candidates / bin')
    ax.set(xlabel=METRICS.get(x, x), ylabel=METRICS.get(y, y), title=title)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)

def backgrounds_mc(path, nmax, out, sample_events=BACKGROUND_SAMPLE_EVENTS):
    """Background generatorStatus inventory from sampled events, not reco origin."""
    folder = out / 'background_sources'
    folder.mkdir(parents=True, exist_ok=True)
    with uproot.open(path) as f:
        t = f['events']
        n = min(t.num_entries, nmax) if nmax else t.num_entries
        window = min(n, max(1, int(np.ceil(sample_events / 10)))) if n else 0
        window_starts = np.unique(np.linspace(0, max(0, n - window), min(10, max(1, n // window)), dtype=int)) if n else []
        starts = np.unique(np.concatenate([np.arange(k, min(n, k + window)) for k in window_starts])) if n else np.array([], dtype=int)
        fields = {'pdg': 'PDG', 'status': 'generatorStatus', 'px': 'momentum.x', 'py': 'momentum.y', 'pz': 'momentum.z'}
        names = {k: resolved(t, 'MCParticles', v) for k, v in fields.items()}
        if not all(names.values()):
            print('[BACKGROUND] MC source plot skipped: missing MCBranches')
            return
        rows = []
        segments = np.split(starts, np.where(np.diff(starts) > 1)[0] + 1)
        for segment in tqdm(segments, desc='Background MC sample', unit='block', dynamic_ncols=True):
            if not len(segment):
                continue
            sample_chunk = getchunk(t, names, int(segment[0]), int(segment[-1]) + 1)
            for idx in segment:
                try:
                    local = int(idx - segment[0])
                    columns = {k: ak.to_list(sample_chunk[v][local]) for k, v in names.items()}
                    for j, stat in enumerate(columns['status']):
                        stat = int(stat)
                        block = stat // 1000 * 1000 if stat >= 0 else -1
                        if block not in SOURCES or block == 0:
                            continue
                        pp = np.array([columns[k][j] for k in ('px', 'py', 'pz')], float)
                        rows.append(dict(event=int(idx), source=block, pdg=int(columns['pdg'][j]), E=float(np.sqrt(np.dot(pp, pp))), pt=float(np.linalg.norm(pp - np.dot(pp, BEAM_DIR) * BEAM_DIR)), theta_mrad=float(np.arctan2(np.hypot(pp[0], pp[1]), pp[2]) * 1000)))
                except Exception:
                    continue
    pass  # No intermediate data export.
    for key, label in [('E', 'MC momentum [GeV]'), ('pt', 'MC $p_{T,beam}$ [GeV]'), ('theta_mrad', 'MC polar angle [mrad]')]:
        allv = finite((r[key] for r in rows))
        if not len(allv):
            continue
        if key == 'theta_mrad':
            edges = np.linspace(0, max(100, float(np.max(allv)) * 1.01), 66)
        else:
            pos = allv[allv > 0]
            edges = np.geomspace(max(1e-08, float(np.min(pos)) * 0.99) if len(pos) else 1e-08, max(1, float(np.max(pos)) * 1.01) if len(pos) else 1000.0, 66)
        fig, ax = plt.subplots(figsize=(6, 6))
        for j, source in enumerate((k for k in SOURCES if k != 0)):
            subset = [r[key] for r in rows if r['source'] == source]
            if not subset:
                continue
            stairs(ax, subset, edges, plt.get_cmap('tab10')(j), SOURCES[source], den=len(subset))
        if key != 'theta_mrad':
            ax.set_xscale('log')
        ax.set(xlabel=label, ylabel='Fraction within each tagged source [%]')
        ax.legend(fontsize=13)
        ax.minorticks_on()
        fig.tight_layout()
        fig.savefig(folder / f'{key}_by_source.png')
        plt.close(fig)
    report = {'sampled_events': len(starts), 'particle_counts': dict(Counter((r['source'] for r in rows))), 'note': 'MC source plots describe generator-tagged particles, not their rates in reconstructed neutron candidates.'}
    pass  # No intermediate data export.

def efficiency_maps(truth, reco, xq, out, n):
    """Compute efficiency maps for the analysis."""
    if xq is None:
        return
    x, q = xq
    truth_events = {r['event'] for r in truth}
    reco_events = {r['event'] for r in reco}
    xe = np.geomspace(0.0001, 1, 25)
    qe = np.array([4, 10, 20, 40, 80, 160, 320, 640], float)
    base = np.array([i in truth_events for i in range(n)])
    passed = np.array([i in reco_events for i in range(n)])
    good = np.isfinite(x) & np.isfinite(q) & base
    den = np.histogram2d(x[good], q[good], bins=[xe, qe])[0]
    num = np.histogram2d(x[good & passed], q[good & passed], bins=[xe, qe])[0]
    frac = np.divide(num, den, out=np.full_like(num, np.nan), where=den > 0)
    target = out / 'detectors' / 'ZDC_HCal'
    target.mkdir(parents=True, exist_ok=True)
    pass  # No intermediate data export.
    fig, ax = plt.subplots(figsize=(6, 6))
    masked = np.ma.masked_invalid(frac.T)
    im = ax.pcolormesh(xe, qe, masked, cmap='viridis', vmin=0, vmax=1)
    fig.colorbar(im, ax=ax, label='Events with ZDC neutron candidate / tagged MC neutron events')
    ax.set_xscale('log')
    ax.set_yscale('log' if PLOT_MAP_LOG_Y else 'linear')
    ax.set_xlabel('$x_B^{truth}$')
    ax.set_ylabel('$Q^2_{truth}$ [GeV$^2$]')
    fig.tight_layout()
    fig.savefig(target / 'neutron_event_presence_xb_q2.png')
    plt.close(fig)


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
                    paths = plot_dse('pion', beam, component, scenario, uq_dir, folder,
                                     p2p=MODEL_POINT_TO_POINT_SYSTEMATIC,
                                     e615_file=MODEL_E615_DATA)
                elif model == 'JAM':
                    paths = plot_jam('pion', beam, component, scenario, uq_dir, folder,
                                     set_name=MODEL_JAM_SET, q2=MODEL_JAM_Q2_GEV2,
                                     p2p=MODEL_POINT_TO_POINT_SYSTEMATIC,
                                     lhapdf_path=MODEL_LHAPDF_PATH)
                else:
                    raise ValueError(f'Unknown model: {model}')
                saved.extend(paths)
    return saved
