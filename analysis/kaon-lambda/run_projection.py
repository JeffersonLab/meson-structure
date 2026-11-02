#!/usr/bin/env python3
"""Export kaon uncertainties and optionally compare model projections."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import argparse
from config import PROJECTION_BEAM, PROJECTION_METHODS, PROJECTION_LUMINOSITIES_FB, PROJECTION_XB_EDGES, PROJECTION_X_EDGES, PROJECTION_Q2_EDGES, PROJECTION_BACKGROUND_MODE, PROJECTION_MIN_EVENTS
from config import MODEL_PLOT_TYPES, MODEL_COMPONENTS, PROJECTION_TMAX

def main():
    """Parse CLI arguments and execute CSV generation or model plotting; return None."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--signal', type=Path)
    parser.add_argument('--plots-only', action='store_true', help='Plot existing uq_csv without ROOT inputs')
    parser.add_argument('--plot-models', action='store_true', help='Render model comparison figures')
    parser.add_argument('--models', nargs='+', choices=('DSE', 'JAM'), default=MODEL_PLOT_TYPES)
    parser.add_argument('--components', nargs='+', choices=('valence', 'glue'), default=MODEL_COMPONENTS)
    parser.add_argument('--uq-scenario', choices=('signal_only', 'background_rate_proxy'), default='signal_only')
    parser.add_argument('--plot-method', choices=('Truth', 'Electron', 'JB'), default='Truth')
    parser.add_argument('--generator', type=Path)
    parser.add_argument('--background', type=Path)
    parser.add_argument('--background-mode', choices=['none', 'rate_proxy'], default=PROJECTION_BACKGROUND_MODE)
    parser.add_argument('--beam', default=PROJECTION_BEAM)
    parser.add_argument('--methods', nargs='+', choices=PROJECTION_METHODS, default=PROJECTION_METHODS)
    parser.add_argument('--luminosities', nargs='+', type=float, default=PROJECTION_LUMINOSITIES_FB)
    parser.add_argument('--outdir', type=Path, default=Path('outputs/projections'))
    args = parser.parse_args()
    if not args.plots_only:
        from common.projection_pipeline import run_projection  # pylint: disable=import-outside-toplevel
        from projections import make_response, count_background  # pylint: disable=import-outside-toplevel
        if args.signal is None or args.generator is None:
            parser.error('--signal and --generator are required unless --plots-only is used')
        for path in (args.signal, args.generator, args.background):
            if path is not None and not path.is_file():
                parser.error(f'File not found: {path}')
        saved = run_projection(
            'kaon', args.beam, args.generator, args.signal, args.background,
            args.outdir, args.methods, args.luminosities, PROJECTION_XB_EDGES,
            PROJECTION_X_EDGES, PROJECTION_Q2_EDGES, make_response,
            count_background, background_mode=args.background_mode,
            pt_max=PROJECTION_TMAX, min_events=PROJECTION_MIN_EVENTS,
        )
        print(f'[DONE] {len(saved)} uncertainty CSV files in {args.outdir}')
    if args.plot_models:
        uq_dir = args.outdir / 'uq_csv' / args.uq_scenario / args.plot_method.lower()
        from common.model_plotting import plot_all_models  # pylint: disable=import-outside-toplevel
        from config import (MODEL_POINT_TO_POINT_SYSTEMATIC, MODEL_JAM_SET,
                            MODEL_JAM_Q2_GEV2, MODEL_LHAPDF_PATH, MODEL_E615_DATA)
        paths = plot_all_models(
            'kaon', args.beam, uq_dir, args.outdir,
            models=args.models, components=args.components,
            p2p=MODEL_POINT_TO_POINT_SYSTEMATIC, jam_set=MODEL_JAM_SET,
            q2=MODEL_JAM_Q2_GEV2, lhapdf_path=MODEL_LHAPDF_PATH,
            e615_file=MODEL_E615_DATA,
        )
        print(f'[DONE] {len(paths)} model figures in {args.outdir / "models"}')
    elif args.plots_only:
        parser.error('--plots-only requires --plot-models')


if __name__ == '__main__':
    main()
