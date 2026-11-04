#!/usr/bin/env python3
"""Haystack-style event display for ePIC npsim EDM4hep ROOT files.

Goal: reproduce plots like Dmitry Romanov's slides, i.e. one event shown as
z(t) and r(t), with points coloured by generator/background source and G4
ancestry.

This script should be run on the *npsim* EDM4hep file, not on the EICrecon
output, because we want the original hit/contribution timing information.

It supports two kinds of input collections:
  1. direct hit collections with fields time, position.{x,y,z} and a relation
     to MCParticles (e.g. tracker/vertex/mpgd hits),
  2. CalorimeterHitContribution collections with fields time, energy and a
     relation to MCParticles. In that case hit positions are recovered from the
     parent SimCalorimeterHit collection using contributions_begin/end.

Typical use:

python plot_haystack.py --file npsim_4 --event 2231 --mode tracker \
    --outdir outputs/haystack

python plot_haystack.py --file npsim_4 --event 0 --mode calo \
    --outdir outputs/haystack_calo

Inspect available collections first if needed:
python plot_haystack.py --file npsim_4 --inspect
"""
from __future__ import annotations
import argparse
from functools import lru_cache
from pathlib import Path
import json
import re
import sys

import awkward as ak
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import uproot

# -----------------------------------------------------------------------------
# Local defaults for your ifarm layout
# -----------------------------------------------------------------------------
BASE = Path('/volatile/eic/fraisse/sullivan_background_test')
STEM = 'k_lambda_18x275_bkg_{}_4000evt_specialstatuses_epic26080'
FILES = {
    'npsim_0': BASE / 'npsim_chunks' / (STEM.format(0) + '.edm4hep.root'),
    'npsim_4': BASE / 'npsim_chunks' / (STEM.format(4) + '.edm4hep.root'),
}

CATEGORY_ORDER = [
    'signal_generator',
    #'g4_signal',
    #'g4_background',
    'synrad',
    'electron_beamgas',
    'coulomb',
    'touschek',
    'proton_beamgas',
    'DIS_NC',
    'unknown',
]

LABELS = {
    'signal_generator': 'signal (generator)',
    # 'g4_signal': 'G4 sec. of signal',
    # 'g4_background': 'G4 sec. of background',
    'synrad': 'bkg 2000 (synrad)',
    'electron_beamgas': 'bkg 3000 (e-gas brems)',
    'coulomb': 'bkg 4000 (e-gas Coulomb)',
    'touschek': 'bkg 5000 (e-gas Touschek)',
    'proton_beamgas': 'bkg 6000 (p-gas / pythia)',
    'DIS_NC': 'bkg 7000 (DIS NC)',
    'unknown': 'other',
}

COLORS = {
    'signal_generator': '#1f9d55',
    # 'g4_signal': '#9be6b4',
    # 'g4_background': '#e53e3e',
    'synrad': '#f2b632',
    'electron_beamgas': '#4299e1',
    'coulomb': '#9f7aea',
    'touschek': '#d53f8c',
    'proton_beamgas': '#8b5a2b',
    'DIS_NC': '#805ad5',
    'unknown': '#718096',
}

PRESET_PATTERNS = {
    'tracker': [
        r'.*Vertex.*Hits$',
        r'.*Tracker.*Hits$',
        r'.*MPGD.*Hits$',
        r'.*B0(?!.*(?:ECal|Ecal|ECAL)).*Hits$',
        r'.*RomanPot.*Hits$',
        r'.*OffMomentum.*Hits$',
        r'.*TOF.*Hits$',
    ],

    'calo': [
        # LFHCAL (actual collection names may use HcalFarForward)
        r'.*(?:LFHCAL|HcalFarForward).*Hits(?:Contributions)?$',
        # B0 electromagnetic calorimeter
        r'.*(?:B0ECal|B0Ecal|EcalB0).*Hits(?:Contributions)?$',
        # ZDC electromagnetic / hadronic calorimeters
        r'.*EcalFarForwardZDC.*Hits(?:Contributions)?$',
        r'.*HcalFarForwardZDC.*Hits(?:Contributions)?$',
    ],
}

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def tree_for(path: Path):
    f = uproot.open(path)
    if 'events' not in f:
        f.close()
        raise ValueError(f'No events tree in {path}')
    return f, f['events']


def all_branches(tree):
    return [k.split(';')[0] for k in tree.keys(recursive=True)]

def field_branch(branches, coll, field):
    """
    Find a PODIO branch corresponding to a field of collection `coll`.

    Handles e.g.
      Collection/Collection.time
      Collection/Collection.position.x
      Collection.time
      Collection.position.x
    """
    wanted_suffixes = (
        f'{coll}/{coll}.{field}',
        f'{coll}.{field}',
    )

    # exact suffix match first
    for b in branches:
        if b in wanted_suffixes:
            return b

    # More tolerant PODIO matching
    candidates = []

    for b in branches:
        if not (b.startswith(coll + '/') or b.startswith(coll + '.')):
            continue

        # Remove "Collection/" if present
        rest = b[len(coll):]
        if rest.startswith('/'):
            rest = rest[1:]

        # Remove repeated collection name
        if rest.startswith(coll + '.'):
            rest = rest[len(coll) + 1:]
        elif rest.startswith('.'):
            rest = rest[1:]

        if rest.lower() == field.lower():
            candidates.append(b)

    if not candidates:
        return None

    candidates.sort(key=len)
    return candidates[0]

def relation_index_candidates(branches, coll, relationship=None):
    cands = []
    rel_tokens = []
    if relationship is not None:
        rel_tokens.extend([
            f'_{coll}_{relationship}',
            f'{coll}_{relationship}',
            f'{coll}#{0}',
        ])
    else:
        rel_tokens.extend([f'_{coll}_MCParticle', f'_{coll}_particle', f'{coll}#{0}'])

    for b in branches:
        if b.rsplit('.', 1)[-1] != 'index':
            continue
        prefix = b.split('/')[0]
        if any(tok in prefix for tok in rel_tokens):
            cands.append(b)
    cands.sort(key=lambda s: (0 if relationship and relationship in s else 1, len(s)))
    return cands


def event_array(tree, bname, event):
    if bname is None:
        return None
    arr = tree.arrays([bname], entry_start=event, entry_stop=event + 1,
                      library='ak', how=dict)[bname]
    return np.asarray(ak.to_numpy(ak.flatten(arr, axis=None)))


def status_source(status: int) -> str:
    s = int(status)
    if 1 <= s <= 4:
        return 'signal'
    if 2000 <= s < 3000:
        return 'synrad'
    if 3000 <= s < 4000:
        return 'electron_beamgas'
    if 4000 <= s < 5000:
        return 'coulomb'
    if 5000 <= s < 6000:
        return 'touschek'
    if 6000 <= s < 7000:
        return 'proton_beamgas'
    if 7000 <= s < 8000:
        return 'DIS_NC'
    return 'unknown'


def build_mc_resolver(tree, branches, event):
    statuses = event_array(tree, field_branch(branches, 'MCParticles', 'generatorStatus'), event)
    times = event_array(tree, field_branch(branches, 'MCParticles', 'time'), event)
    p_begin = event_array(tree, field_branch(branches, 'MCParticles', 'parents_begin'), event)
    p_end = event_array(tree, field_branch(branches, 'MCParticles', 'parents_end'), event)

    if statuses is None:
        raise RuntimeError('MCParticles.generatorStatus branch not found')
    statuses = np.asarray(statuses, dtype=int)
    times = None if times is None else np.asarray(times, dtype=float)

    parent_indices = None
    if p_begin is not None and p_end is not None:
        for cand in relation_index_candidates(branches, 'MCParticles', 'parents'):
            vals = event_array(tree, cand, event)
            if vals is not None and len(vals) >= int(np.max(p_end, initial=0)):
                parent_indices = np.asarray(vals, dtype=int)
                break

    @lru_cache(None)
    def ancestor_source(idx: int) -> str:
        if idx < 0 or idx >= len(statuses):
            return 'unknown'
        direct = status_source(statuses[idx])
        if direct != 'unknown':
            return direct
        if parent_indices is None or p_begin is None or p_end is None:
            return 'unknown'
        seen = {idx}
        frontier = [idx]
        for _ in range(100):
            nxt = []
            for cur in frontier:
                lo, hi = int(p_begin[cur]), int(p_end[cur])
                if not (0 <= lo <= hi <= len(parent_indices)):
                    continue
                for pidx in parent_indices[lo:hi]:
                    pidx = int(pidx)
                    if pidx in seen or pidx < 0 or pidx >= len(statuses):
                        continue
                    seen.add(pidx)
                    src = status_source(statuses[pidx])
                    if src != 'unknown':
                        return src
                    nxt.append(pidx)
            if not nxt:
                break
            frontier = nxt
        return 'unknown'

    def classify_particle(idx: int) -> str:
        """Return the haystack category for one referenced MCParticle.

        Direct generator particles keep their explicit source category except for
        signal, which is named 'signal_generator'.
        Geant4 secondaries whose ancestry traces to the signal become
        'g4_signal'. Secondaries from any background become 'g4_background'.
        """
        if idx < 0 or idx >= len(statuses):
            return 'unknown'
        direct_src = status_source(statuses[idx])
        if direct_src == 'signal':
            return 'signal_generator'
        if direct_src in ('synrad', 'electron_beamgas', 'coulomb', 'touschek', 'proton_beamgas', 'DIS_NC'):
            return direct_src
        # anc = ancestor_source(idx)
        # if anc == 'signal':
        #     return 'g4_signal'
        # if anc in ('synrad', 'electron_beamgas', 'coulomb', 'touschek', 'proton_beamgas', 'DIS_NC'):
        #     return 'g4_background'
        return 'unknown'

    # useful for title / reference region
    signal_times = np.asarray([], dtype=float)
    if times is not None:
        mask = np.isin(statuses, [1, 2, 3, 4]) & np.isfinite(times)
        signal_times = times[mask]
    return statuses, times, classify_particle, signal_times


def collection_names_from_patterns(branches, patterns):
    """Discover collection names matching regexes.

    We infer collection names from branch prefixes before the first '/' or from
    the prefix before the first '.'.
    """
    names = set()
    regexes = [re.compile(p) for p in patterns]
    for b in branches:
        prefix = b.split('/')[0]
        prefix = prefix.split('.')[0]
        if any(r.search(prefix) for r in regexes):
            names.add(prefix)
    return sorted(names)


def discover_collection(tree, branches, coll):
    """Return metadata for a direct-hit or contribution collection."""
    time_b = field_branch(branches, coll, 'time')
    if time_b is None:
        return None

    # Direct hit style: collection itself has position.{x,y,z}
    px = field_branch(branches, coll, 'position.x')
    py = field_branch(branches, coll, 'position.y')
    pz = field_branch(branches, coll, 'position.z')
    if px and py and pz:
        return {
            'kind': 'direct',
            'time': time_b,
            'x': px,
            'y': py,
            'z': pz,
            'energy': field_branch(branches, coll, 'energy'),
            'mc_rel_candidates': relation_index_candidates(branches, coll, 'MCParticle') + relation_index_candidates(branches, coll, 'particle'),
        }

    # Contribution style: positions come from parent hit collection.
    if coll.endswith('Contributions'):
        hitcoll = coll[:-len('Contributions')]
        bb = field_branch(branches, hitcoll, 'contributions_begin')
        ee = field_branch(branches, hitcoll, 'contributions_end')
        hx = field_branch(branches, hitcoll, 'position.x')
        hy = field_branch(branches, hitcoll, 'position.y')
        hz = field_branch(branches, hitcoll, 'position.z')
        if bb and ee and hx and hy and hz:
            return {
                'kind': 'contribution',
                'time': time_b,
                'energy': field_branch(branches, coll, 'energy'),
                'hitcoll': hitcoll,
                'contrib_begin': bb,
                'contrib_end': ee,
                'x': hx,
                'y': hy,
                'z': hz,
                'mc_rel_candidates': relation_index_candidates(branches, coll, 'particle') + relation_index_candidates(branches, coll, 'MCParticle'),
            }
    return None


def choose_relation(tree, event, candidates, expected_len):
    for b in candidates:
        arr = event_array(tree, b, event)
        if arr is not None and len(arr) == expected_len:
            return np.asarray(arr, dtype=int), b
    return None, None


def load_direct_hits(tree, event, meta):
    t = event_array(tree, meta['time'], event)
    x = event_array(tree, meta['x'], event)
    y = event_array(tree, meta['y'], event)
    z = event_array(tree, meta['z'], event)
    if t is None or x is None or y is None or z is None:
        return None
    n = len(t)
    refs, ref_branch = choose_relation(tree, event, meta['mc_rel_candidates'], n)
    r = np.hypot(x, y)
    e = event_array(tree, meta['energy'], event) if meta['energy'] else None
    return {
        'time': np.asarray(t, dtype=float),
        'z': np.asarray(z, dtype=float),
        'r': np.asarray(r, dtype=float),
        'energy': None if e is None else np.asarray(e, dtype=float),
        'mc_refs': refs,
        'mc_ref_branch': ref_branch,
    }


def load_contributions(tree, event, meta):
    t = event_array(tree, meta['time'], event)
    if t is None:
        return None
    t = np.asarray(t, dtype=float)
    n = len(t)
    starts = event_array(tree, meta['contrib_begin'], event)
    ends = event_array(tree, meta['contrib_end'], event)
    xs = event_array(tree, meta['x'], event)
    ys = event_array(tree, meta['y'], event)
    zs = event_array(tree, meta['z'], event)
    if starts is None or ends is None or xs is None or ys is None or zs is None:
        return None
    starts = np.asarray(starts, dtype=int)
    ends = np.asarray(ends, dtype=int)
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    zs = np.asarray(zs, dtype=float)

    hit_index = np.full(n, -1, dtype=int)
    for ihit, (a, b) in enumerate(zip(starts, ends)):
        if 0 <= a <= b <= n:
            hit_index[a:b] = ihit

    z = np.full(n, np.nan)
    r = np.full(n, np.nan)
    valid = hit_index >= 0
    z[valid] = zs[hit_index[valid]]
    r[valid] = np.hypot(xs[hit_index[valid]], ys[hit_index[valid]])

    refs, ref_branch = choose_relation(tree, event, meta['mc_rel_candidates'], n)
    e = event_array(tree, meta['energy'], event) if meta['energy'] else None
    return {
        'time': t,
        'z': z,
        'r': r,
        'energy': None if e is None else np.asarray(e, dtype=float),
        'mc_refs': refs,
        'mc_ref_branch': ref_branch,
    }


def gather_points(tree, branches, event, collections):
    pieces = []
    used = []
    for coll in collections:
        meta = discover_collection(tree, branches, coll)
        if meta is None:
            continue
        if meta['kind'] == 'direct':
            data = load_direct_hits(tree, event, meta)
        else:
            data = load_contributions(tree, event, meta)
        if data is None or len(data['time']) == 0:
            continue
        pieces.append(data)
        used.append((coll, meta['kind'], data['mc_ref_branch'], len(data['time'])))

    if not pieces:
        return None, used

    time = np.concatenate([p['time'] for p in pieces])
    z = np.concatenate([p['z'] for p in pieces])
    r = np.concatenate([p['r'] for p in pieces])
    energy = None
    if any(p['energy'] is not None for p in pieces):
        energy = np.concatenate([
            p['energy'] if p['energy'] is not None else np.full(len(p['time']), np.nan)
            for p in pieces
        ])
    refs = np.concatenate([
        p['mc_refs'] if p['mc_refs'] is not None else np.full(len(p['time']), -1, dtype=int)
        for p in pieces
    ]).astype(int)
    return {'time': time, 'z': z, 'r': r, 'energy': energy, 'mc_refs': refs}, used


def build_categories(mc_refs, classify_particle):
    if mc_refs is None:
        return np.array(['unknown'] * 0, dtype=object)
    return np.array([classify_particle(int(i)) for i in mc_refs], dtype=object)


def signal_span_from_points(time, cats):
    mask = np.isin(cats, ['signal_generator', 'g4_signal']) & np.isfinite(time)
    if not np.any(mask):
        return None, None
    return float(np.min(time[mask])), float(np.max(time[mask]))


def configure_publication_style():
    """Matplotlib's STIX gives LaTeX-like text without requiring TeX installed."""
    plt.rcParams.update({
        'font.family': 'STIXGeneral',
        'mathtext.fontset': 'stix',
        'font.size': 12,
        'axes.labelsize': 15,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 10,
        'axes.linewidth': 0.9,
        'xtick.direction': 'in',
        'ytick.direction': 'in',
        'xtick.top': True,
        'ytick.right': True,
        'xtick.major.size': 5,
        'ytick.major.size': 5,
        'xtick.minor.size': 2.5,
        'ytick.minor.size': 2.5,
        'xtick.major.width': 0.8,
        'ytick.major.width': 0.8,
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
        'savefig.facecolor': 'white',
    })


def plot_haystack(event, time, z, r, cats, outpath: Path, point_size=8.0,
                  tmin=0.0, tmax=2000.0, max_points_per_cat=120000,
                  show_signal_window=False, seed=1234,
                  point_alpha=0.55, legend_outside=True, export_pdf=True):
    """Plot transparent, ordered scatter layers so rare signal remains visible.

    Background categories are drawn before the signal categories. All plotted
    counts in the legend refer to the full selected time range, *not* the
    downsampled display. Scatter is rasterized in vector PDF exports to avoid
    enormous files while keeping text/axes as vector artwork.
    """
    configure_publication_style()
    rng = np.random.default_rng(seed + event)
    fig, axes = plt.subplots(2, 1, figsize=(11.6, 6.9), sharex=True,
                             gridspec_kw={'hspace': 0.075})

    # Draw backgrounds first. Signal and its G4 secondaries remain on top.
    draw_order = [c for c in CATEGORY_ORDER
                  if c not in ('signal_generator', 'g4_signal')] + [
                  'g4_signal', 'signal_generator']
    handles = {}
    counts = {}
    span_lo, span_hi = signal_span_from_points(time, cats)
    signal_cats = {'signal_generator', 'g4_signal'}

    for ax, yy, ylabel in ((axes[0], z, r'$z$ (mm)'),
                            (axes[1], r, r'$r$ (mm)')):
        for cat in draw_order:
            mask = ((cats == cat) & np.isfinite(time) & np.isfinite(yy)
                    & (time >= tmin) & (time <= tmax))
            idx = np.flatnonzero(mask)
            if len(idx) == 0:
                continue
            counts[cat] = max(counts.get(cat, 0), len(idx))
            if max_points_per_cat > 0 and len(idx) > max_points_per_cat:
                idx = rng.choice(idx, size=max_points_per_cat, replace=False)
            is_signal = cat in signal_cats
            # A small transparent background, a somewhat larger signal layer.
            size = point_size * (1.35 if is_signal else 0.65)
            alpha = min(0.98, point_alpha + 0.22) if is_signal else point_alpha
            artist = ax.scatter(time[idx], yy[idx], s=size,
                                c=COLORS[cat], alpha=alpha,
                                edgecolors='none', linewidths=0,
                                marker='o', rasterized=True,
                                zorder=5 if is_signal else 2)
            handles.setdefault(cat, artist)
        if show_signal_window and span_lo is not None and span_hi is not None:
            # Deliberately subtle: optional, disabled by default.
            ax.axvline(span_lo, color='0.5', lw=0.8, alpha=0.6, zorder=1)
            ax.axvline(span_hi, color='0.5', lw=0.8, alpha=0.6, zorder=1)
        ax.set_ylabel(ylabel)
        ax.grid(False)
        ax.minorticks_on()
        ax.tick_params(which='both', direction='in', top=True, right=True)
        ax.margins(y=0.06)

    axes[1].set_xlabel(r'Hit time $t$ (ns)')
    axes[1].set_xlim(tmin, tmax)

    # Legend keeps the conceptual order, independent of painting order.
    ordered = [cat for cat in CATEGORY_ORDER if cat in handles]
    legend_handles = [handles[cat] for cat in ordered]
    legend_labels = [f'{LABELS[cat]} ({counts[cat]:,})' for cat in ordered]
    if legend_handles:
        if legend_outside:
            fig.legend(legend_handles, legend_labels,
                       loc='center left', bbox_to_anchor=(0.775, 0.53),
                       frameon=False, markerscale=2.0,
                       labelspacing=0.45, handletextpad=0.45)
            fig.subplots_adjust(left=0.105, right=0.75, bottom=0.12, top=0.975)
        else:
            axes[0].legend(legend_handles, legend_labels,
                           loc='upper right', frameon=False,
                           markerscale=2.0, labelspacing=0.35)
            fig.subplots_adjust(left=0.105, right=0.975,
                                bottom=0.12, top=0.975)
    else:
        fig.subplots_adjust(left=0.105, right=0.975,
                            bottom=0.12, top=0.975)

    fig.savefig(outpath, dpi=300)
    if export_pdf:
        fig.savefig(outpath.with_suffix('.pdf'), dpi=300)
    plt.close(fig)


def diagnose_calo_statuses(tree, branches, event, mc_refs):
    """Inspect MCParticle generator statuses referenced by ZDC contributions."""

    statuses = event_array(
        tree,
        field_branch(branches, 'MCParticles', 'generatorStatus'),
        event
    )

    if statuses is None:
        print("[DIAG] No MCParticles.generatorStatus found")
        return

    statuses = np.asarray(statuses, dtype=int)
    refs = np.asarray(mc_refs, dtype=int)

    valid = (refs >= 0) & (refs < len(statuses))
    valid_refs = refs[valid]

    print("\n========== CALO MC STATUS DIAGNOSTIC ==========")
    print(f"Total MCParticles: {len(statuses)}")
    print(f"Total calo contributions: {len(refs)}")
    print(f"Valid MC references: {len(valid_refs)}")
    print(f"Invalid MC references: {np.sum(~valid)}")
    print(f"Unique MCParticles contributing: {len(np.unique(valid_refs))}")

    if not len(valid_refs):
        return

    print("\nGenerator statuses of calo contributing particles:")

    unique, counts = np.unique(
        statuses[valid_refs],
        return_counts=True
    )

    for status, count in zip(unique, counts):
        print(
            f"  generatorStatus={status:5d} : "
            f"{count:8d} contributions "
            f"({100 * count / len(valid_refs):5.1f}%)"
        )

    print("\nGenerator statuses among ALL MCParticles:")

    unique, counts = np.unique(statuses, return_counts=True)

    for status, count in zip(unique, counts):
        print(f"  generatorStatus={status:5d}: {count:8d} particles")

    print("==============================================\n")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument('--file', choices=list(FILES), default='npsim_4')
    ap.add_argument('--event', type=int, required=False, default=0)
    ap.add_argument('--events', nargs='+', type=int, default=None,
                    help='Optional list of events. If given, overrides --event.')
    ap.add_argument('--mode', choices=['tracker', 'calo', 'custom'], default='tracker',
                    help='Predefined collection set. Use custom with --collections.')
    ap.add_argument('--collections', nargs='+', default=None,
                    help='Explicit collection names when using --mode custom, or to override discovery.')
    ap.add_argument('--outdir', type=Path, default=Path('outputs/haystack'))
    ap.add_argument('--tmin', type=float, default=0.0)
    ap.add_argument('--tmax', type=float, default=2000.0)
    ap.add_argument('--max-points-per-cat', type=int, default=120000)
    ap.add_argument('--point-size', '--point_size', dest='point_size', type=float, default=8.0, help='Base scatter area in pt^2')
    ap.add_argument('--point-alpha', type=float, default=0.55, help='Background marker opacity (0..1)')
    ap.add_argument('--legend-inside', action='store_true', help='Put frameless legend inside upper panel')
    ap.add_argument('--no-pdf', action='store_true', help='Disable PDF export')
    ap.add_argument('--show-signal-window', action='store_true', help='Show vertical signal timing lines (off by default)')
    ap.add_argument('--inspect', action='store_true', help='Print matching collection names and relevant branches, then exit')
    args = ap.parse_args()
    if not (0.0 <= args.point_alpha <= 1.0):
        ap.error('--point-alpha must be between 0 and 1')

    path = FILES[args.file]
    if not path.exists():
        ap.error(f'No such file: {path}')

    handle, tree = tree_for(path)
    branches = all_branches(tree)

    if args.collections:
        collections = args.collections
    else:
        if args.mode == 'custom':
            ap.error('--mode custom requires --collections')
        patterns = PRESET_PATTERNS[args.mode]
        collections = collection_names_from_patterns(branches, patterns)
        if args.mode == 'calo':
            # Do not use both SimCalorimeterHits and their Contributions.
            # Contributions carry individual timings and MCParticle references.
            available = set(collections)
            collections = [c for c in collections if not (
                c + 'Contributions' in available and
                discover_collection(tree, branches, c + 'Contributions') is not None
            )]

    if args.inspect:
        print(f'File: {path}')
        print(f'Mode: {args.mode}')
        print('Collections:')
        for coll in collections:
            meta = discover_collection(tree, branches, coll)
            if meta is None:
                print(f'  {coll}: unusable (missing time/position/relation info)')
                continue
            print(f'  {coll}:')
            print(json.dumps(meta, indent=2))
        print('\nRelevant MC branches:')
        for tok in ['MCParticles', 'parents', 'generatorStatus']:
            for b in branches:
                if tok in b:
                    print(' ', b)
        handle.close()
        return

    if not collections:
        print('No collections found for this mode. Try --inspect or --mode custom --collections ...', file=sys.stderr)
        handle.close()
        sys.exit(1)

    args.outdir.mkdir(parents=True, exist_ok=True)
    event_list = args.events if args.events is not None else [args.event]

    for event in event_list:
        if not (0 <= event < tree.num_entries):
            print(f'Skip event {event}: file has {tree.num_entries} entries')
            continue

        print(f'\n=== event {event} ===')
        try:
            _, _, classify_particle, signal_particle_times = build_mc_resolver(tree, branches, event)
        except Exception as exc:
            print(f'ERROR while building MC ancestry for event {event}: {exc}')
            continue

        gathered, used = gather_points(tree, branches, event, collections)
        if gathered is None:
            print('  No usable hits/contributions found in requested collections')
            continue

        for coll, kind, relb, nh in used:
            print(f'  {coll:40s} kind={kind:12s} n={nh:7d} relation={relb}')

        time = np.asarray(gathered['time'], dtype=float)
        z = np.asarray(gathered['z'], dtype=float)
        r = np.asarray(gathered['r'], dtype=float)
        mc_refs = gathered['mc_refs']
        if args.mode == 'calo' and mc_refs is not None:
            diagnose_calo_statuses(tree, branches, event, mc_refs)
        if mc_refs is None:
            cats = np.array(['unknown'] * len(time), dtype=object)
        else:
            cats = build_categories(mc_refs, classify_particle)

        # simple report
        unique, counts = np.unique(cats, return_counts=True)
        report = ', '.join(f'{u}={c}' for u, c in zip(unique, counts))
        print('  Categories:', report)
        if signal_particle_times is not None and len(signal_particle_times):
            print(f'  Signal MC particle production-time span: {np.min(signal_particle_times):.1f} .. {np.max(signal_particle_times):.1f} ns')

        outname = args.outdir / f'{args.file}_event_{event:05d}_{args.mode}_haystack.png'
        plot_haystack(
            event=event,
            time=time,
            z=z,
            r=r,
            cats=cats,
            outpath=outname,
            tmin=args.tmin,
            tmax=args.tmax,
            max_points_per_cat=args.max_points_per_cat,
            point_size=args.point_size,
            point_alpha=args.point_alpha,
            legend_outside=not args.legend_inside,
            export_pdf=not args.no_pdf,
            show_signal_window=args.show_signal_window,
        )
        print(f'  Wrote: {outname}')
        if not args.no_pdf:
            print(f'  Wrote: {outname.with_suffix(".pdf")}')

    handle.close()


if __name__ == '__main__':

    main()