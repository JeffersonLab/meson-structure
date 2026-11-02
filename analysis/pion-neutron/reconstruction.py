"""ePIC pion Sullivan neutron analysis. See README.md for limitations."""
from __future__ import annotations
import argparse
import json
import time
from pathlib import Path
import uproot
from tqdm.auto import tqdm
from config import CUTS, DEFAULT_OUT, METRICS, NEUTRAL_COLLECTION
from root_io import select_rows, attach_invariant_masses, optional_truth_dis, resolved
from matching import matching
from plotting import plot_purity, plot_spectrum, plot_xy, efficiency_maps, backgrounds_mc
from selection import cut_study, passes

def main():
    """Parse command-line options and execute the analysis."""
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--signal', type=Path, required=True)
    p.add_argument('--background', type=Path, required=True)
    p.add_argument('--generator', type=Path, default=None, help='Optional standalone generator ROOT. If not an events/MCParticles file, no assumed schema; signal EDM4hep MC truth still plotted.')
    p.add_argument('--outdir', type=Path, default=DEFAULT_OUT)
    p.add_argument('--max-events', type=int, default=0)
    p.add_argument('--skip-generator', action='store_true', help='Skip optional external generator file; keep EDM4hep MC truth plots')
    p.add_argument('--dump-branches', action='store_true')
    args = p.parse_args()
    start = time.perf_counter()
    if not args.signal.is_file():
        p.error(f'Missing signal: {args.signal}')
    if args.background and (not args.background.is_file()):
        p.error(f'Missing mixed file: {args.background}')
    out = args.outdir
    out.mkdir(parents=True, exist_ok=True)
    print('[INPUT]', args.signal, args.background, flush=True)
    print('[CUTS]', CUTS, flush=True)
    if args.dump_branches:
        for path in [args.signal, args.background]:
            with uproot.open(path) as f:
                t = f['events']
                print('\nFILE', path)
                for x in t.keys(recursive=True):
                    if any((token in x.lower() for token in ('hcalfarforwardzdc', 'mcparticle', 'inclusivekinematic'))):
                        print(x)
        return
    truth, ns = select_rows(args.signal, args.max_events, 'MCParticles', truth=True)
    signal, _ = select_rows(args.signal, args.max_events, NEUTRAL_COLLECTION)
    mixed, nm = select_rows(args.background, args.max_events, NEUTRAL_COLLECTION)
    print('[COUNTS] events', ns, nm, 'MC source0 neutrons', len(truth), 'reco signal-only', len(signal), 'reco mixed', len(mixed), flush=True)
    attach_invariant_masses(args.signal, ns, truth, truth=True, label='truth')
    attach_invariant_masses(args.signal, ns, signal, label='signal')
    attach_invariant_masses(args.background, nm, mixed, label='mixed')
    signal = matching(args.signal, ns, signal, 'signal', out)
    mixed = matching(args.background, nm, mixed, 'mixed', out)
    plot_purity(mixed, out / 'reconstruction' / 'purity' / 'purity_mixed.png', 'Signal + background reconstruction')
    for key in tqdm(METRICS, desc='Raw histogram plots', unit='observable', dynamic_ncols=True):
        plot_spectrum([('truth', truth), ('signal_only', signal), ('mixed', mixed)], key, out / 'reconstruction' / 'raw' / f'{key}.png')
        plot_spectrum([('signal', [r for r in mixed if r['category'] == 'signal']), ('combinatorial', [r for r in mixed if r['category'] == 'combinatorial'])], key, out / 'reconstruction' / 'purity' / f'{key}_raw_mixed.png', normalize='common')
        plot_spectrum([('truth', truth)], key, out / 'generator' / f'{key}.png')
    for rows, label in tqdm(((truth, 'generator'), (signal, 'reconstruction/raw'), (mixed, 'reconstruction/raw/mixed')), desc='2D plots', unit='sample', dynamic_ncols=True):
        for x, y in [('E', 'theta_beam_mrad'), ('E', 'xL'), ('xL', 'minus_t'), ('xL', 'pt_beam'), ('W', 'MX'), ('xL', 'MX')]:
            plot_xy(rows, x, y, out / label / f'{x}_vs_{y}.png')
    for sample, rows in tqdm([('mixed', mixed)], desc='Selections and cutflow', unit='sample', dynamic_ncols=True):
        cut_study(rows, len(truth), out, sample)
        keep = [r for r in rows if all((passes(r, c) for c in CUTS))]
        for key in tqdm(METRICS, desc=f'Post-cut plots {sample}', unit='observable', leave=False, dynamic_ncols=True):
            plot_spectrum([('signal', [r for r in keep if r['category'] == 'signal']), ('combinatorial', [r for r in keep if r['category'] == 'combinatorial'])], key, out / 'reconstruction' / 'post-cut' / f'{key}_{sample}.png', normalize='common')
    efficiency_maps(truth, signal, optional_truth_dis(args.signal, ns, out), out, ns)
    backgrounds_mc(args.background, nm, out)
    if not args.skip_generator:
        if args.generator is not None and args.generator.is_file():
            with uproot.open(args.generator) as f:
                if 'events' in f and resolved(f['events'], 'MCParticles', 'PDG'):
                    print('[GENERATOR] external file contains EDM4hep MCParticles; signal file truth is the reference for alignment, no event-by-event correspondence assumed')
                else:
                    print('[GENERATOR] external file format not auto-assumed. MC generator truth from signal EDM4hep used; no cross-section calculation.', flush=True)
        else:
            print('[GENERATOR] optional external ROOT missing; MC truth from signal EDM4hep available', flush=True)
    summary = {'n_signal_events': ns, 'n_mixed_events': nm, 'n_generated_source0_neutrons': len(truth), 'n_signal_reco_candidates': len(signal), 'n_mixed_reco_candidates': len(mixed), 'definition': 'signal means dominant associated ZDC source block 0 (with parent fallback for untagged MC); not truth matched neutron', 'candidate_count_over_generated': 'candidate yield, not exclusive truth-matched efficiency', 'optional_cuts': {c[0]: {'min': c[2], 'max': c[3]} for c in CUTS}, 'reconstructed_invariant_mass_definition': 'W from reconstructed electron/DIS kinematics; MX=(p+q-pn)^2 with electron four-vector; unavailable is NaN, never truth fallback', 'warning': 'MCParticles source0 neutron count may include more than one neutron per generated event. Tagging requires event-level/physics-truth denominator validation.', 'background_event_alignment': 'Not assumed; each file classified independently'}
    pass  # No intermediate data export.
    print('[DONE]', out, summary, 'elapsed_s', round(time.perf_counter() - start, 1), flush=True)
