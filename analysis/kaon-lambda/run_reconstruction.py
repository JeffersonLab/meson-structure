"""Command-line entry point for kaon–Lambda reconstruction."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import argparse
import time
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
from config import MLSIGMA, MPSIGMA, PROTON_CROSSING_ANGLE_MRAD, PROTON_PX, PROTON_PY, PROTON_PZ, THETA_GG_MAX_MRAD, THETA_GG_MIN_MRAD, THETA_LAMBDA_MAX_MRAD, THETA_LAMBDA_MIN_MRAD, TMAX, XL_MAX, Z_LAMBDA_MAX_M, Z_LAMBDA_MIN_M
from root_io import generator_cross_section
from reconstruction import analyze_reconstruction

def validate_cuts():
    """Validate configured reconstruction selection boundaries."""
    for name, value in [('TMAX', TMAX), ('XL_MAX', XL_MAX), ('MLSIGMA', MLSIGMA), ('MPSIGMA', MPSIGMA)]:
        if value is not None and (not np.isfinite(value) or value <= 0):
            raise ValueError(f'{name} must be None or finite and positive, got {value}')
    for name, lo, hi in [('THETA_GG', THETA_GG_MIN_MRAD, THETA_GG_MAX_MRAD), ('THETA_LAMBDA', THETA_LAMBDA_MIN_MRAD, THETA_LAMBDA_MAX_MRAD), ('Z_LAMBDA', Z_LAMBDA_MIN_M, Z_LAMBDA_MAX_M)]:
        if lo is not None and hi is not None and (lo > hi):
            raise ValueError(f'{name}: min > max')

def main():
    """Parse command-line options and execute the analysis."""
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--signal', type=Path, required=True, help='Signal-only reconstructed ROOT file')
    p.add_argument('--background', type=Path, default=None, help='Reconstructed ROOT file with background overlaid')
    p.add_argument('--generator', type=Path, default=None)
    p.add_argument('--outdir', type=Path, default=Path('outputs/lambda/18x275'))
    p.add_argument('--max-events', type=int, default=0)
    p.add_argument('--skip-generator', action='store_true')
    p.add_argument('--dump-branches', action='store_true', help='List relevant ROOT event branches and exit')
    args = p.parse_args()
    validate_cuts()
    started = time.perf_counter()
    if not args.signal.is_file():
        p.error(f'No such ROOT input: {args.signal}')
    print(f'[CUTS] TMAX={TMAX}, XL_MAX={XL_MAX}, MLSIGMA={MLSIGMA}, MPSIGMA={MPSIGMA}, THETA_GG=({THETA_GG_MIN_MRAD},{THETA_GG_MAX_MRAD}), THETA_LAMBDA=({THETA_LAMBDA_MIN_MRAD},{THETA_LAMBDA_MAX_MRAD}), Z_LAMBDA=({Z_LAMBDA_MIN_M},{Z_LAMBDA_MAX_M})')
    print('[INPUT] signal only:', args.signal)
    print('[INPUT] reco + background:', args.background if args.background else 'disabled')
    print('[OUTPUT]', args.outdir)
    print(f'[BEAM] proton crossing angle = {PROTON_CROSSING_ANGLE_MRAD:+.3f} mrad in xz; p=({PROTON_PX:.6f}, {PROTON_PY:.6f}, {PROTON_PZ:.6f}) GeV')
    args.outdir.mkdir(parents=True, exist_ok=True)
    if args.dump_branches:
        import uproot
        with uproot.open(args.signal) as f:
            t = f['events']
            print(f'[BRANCH INVENTORY] {len(t.keys(recursive=True))} branches')
            for key in t.keys(recursive=True):
                if any((token in key.lower() for token in ('mcparticle', 'inclusivekinematics', 'reconstructedlambda', 'neutrals', 'associat', 'cluster', 'simcalo', 'podio'))):
                    print(key)
        return
    if not args.skip_generator and args.generator is not None:
        generator_cross_section(args.generator, args.outdir / 'generator', 0)
    analyze_reconstruction(args.signal, args.outdir, args.max_events, args.background)
    print('[DONE] plots:', args.outdir)
    print(f'[TIMING] Total elapsed: {time.perf_counter() - started:.1f} s', flush=True)
if __name__ == '__main__':
    main()
