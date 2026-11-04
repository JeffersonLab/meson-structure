"""Shared orchestration for source cross section, detector response and CSV output."""
from __future__ import annotations
from pathlib import Path
import json
import numpy as np
from .projection import efficiency_and_response, expected_yield, purity_rate_proxy, export_uncertainties
from .projection_generator import sigma_map


def run_projection(channel, beam, generator, signal, background, outdir, methods, luminosities,
                   source_edges, dest_edges, q_edges, make_response, count_background,
                   *, background_mode='none', pt_max=None, min_events=1.0):
    """Build binned yields and export projected uncertainty CSV files."""
    sigma,sigma_err,declared=sigma_map(generator, channel, source_edges,q_edges,pt_max=pt_max)
    outdir=Path(outdir); outdir.mkdir(parents=True,exist_ok=True)
    saved=[]
    for method in methods:
        nt,tag,R,signal_count,nevents=make_response(signal,method,source_edges,dest_edges,q_edges,beam,pt_max)
        efficiency,response=efficiency_and_response(nt,tag,R)
        purity=None
        if background_mode=='rate_proxy':
            if background is None:
                raise ValueError('--background required for rate_proxy')
            mixed_count,nmixed=count_background(background,method,dest_edges,q_edges,beam)
            purity=purity_rate_proxy(signal_count,nevents,mixed_count,nmixed)
        for lum in luminosities:
            signal_yield=expected_yield(sigma,efficiency,response,lum)
            common_meta=dict(generator_declared_events=declared,
                input_generator=str(generator),input_signal=str(signal),
                generator_weight=('PhSpFct*Jacob*xsec_taggedLN_dis' if channel=='pion' else 'PhSpFct*Jacob*xsec_tagged_dis*k_int'),
                efficiency_definition='Event has selected leading reconstructed neutral candidate in truth source bin; NOT decay-ancestry truth matching.',
                background_mode=background_mode, background_input=str(background) if background is not None else None,
                background_proxy_definition='Per-frame ratio of signal-only to mixed candidate yields, clipped to [0,1]' if purity is not None else None)
            saved.extend(map(str,export_uncertainties(outdir,channel,beam,method,lum,dest_edges,q_edges,signal_yield,
                          scenario='signal_only',min_events=min_events,metadata=common_meta)))
            if purity is not None:
                saved.extend(map(str,export_uncertainties(outdir,channel,beam,method,lum,dest_edges,q_edges,signal_yield,
                              purity=purity,scenario='background_rate_proxy',min_events=min_events,metadata=common_meta)))
    return saved
