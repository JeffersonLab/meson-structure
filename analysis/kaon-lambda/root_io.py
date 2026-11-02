"""EDM4eIC ROOT I/O and generator cross-section maps."""
from __future__ import annotations
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tqdm.auto import tqdm
from config import (Q2_EDGES, XB_EDGES)
from plotting import _log_norm_from_positive


from common.io import write_csv_rows

def write_rows_csv(path, rows, columns):
    """Write rows csv analysis output."""
    return write_csv_rows(path, rows, columns)


def _resolve_branch(tree, stem, field):
    """Find a PODIO/EDM4hep scalar or jagged branch despite prefix differences."""
    keys = [str(k).split(';')[0] for k in tree.keys(recursive=True)]
    canonical = [
        f'{stem}.{field}', f'{stem}/{field}', f'{stem}/{stem}.{field}',
        f'{stem}.{stem}.{field}',
        f'{stem}/{stem}/{field}',
        f'{stem}/{stem}.{stem}.{field}',
    ]
    for name in canonical:
        if name in keys:
            return name
    # Fuzzy fallback restricted to the named collection to avoid cross-matches.
    candidates = [name for name in keys
                  if (name.startswith(stem + '.') or name.startswith(stem + '/'))
                  and (name.endswith('.' + field) or name.endswith('/' + field))]
    if len(candidates) == 1:
        return candidates[0]
    return None


def _event_scalar(arr, nmax):
    """Compute event scalar for the analysis."""
    import awkward as ak
    out = np.full(nmax, np.nan)
    try:
        a = ak.firsts(arr) if getattr(arr, 'ndim', 1) > 1 else arr
        a = ak.to_numpy(a, allow_missing=True)
        a = np.asarray(ak.fill_none(a, np.nan), dtype=float).reshape(-1)
        out[:min(nmax, len(a))] = a[:nmax]
    except Exception as e:
        print(f'[WARNING] Could not convert event scalar branch: {e}')
    return out


def read_truth_dis(file, nmax):
    """Read xB and Q2 from event file, allowing PODIO nested branch names."""
    import uproot
    with uproot.open(file) as f:
        t = f['events']
        values = []
        for field in ('x', 'Q2'):
            key = _resolve_branch(t, 'InclusiveKinematicsTruth', field)
            if key is None:
                print(f'[WARNING] InclusiveKinematicsTruth.{field} not found. '
                      'Related maps require a real aligned truth DIS source.')
                values.append(np.full(nmax, np.nan))
            else:
                print(f'[BRANCH] DIS {field}: {key}')
                values.append(_event_scalar(t[key].array(entry_stop=nmax, library='ak'), nmax))
        return values


def generator_cross_section(file,out,nmax=0):
    """Compute generator cross section for the analysis."""
    if not file.exists():
        print(f'[WARNING] Generator ROOT file not found: {file}; skipping sigma maps')
        return
    import uproot
    with uproot.open(file) as f:
        m, ev, proc = f['Meta'],f['Evnts'],f['Process']
        n = min(m.num_entries,ev.num_entries,proc.num_entries)
        ndecl = int(m['MC'].array(entry_stop=1,library='np')['nEvts'][0])
        if nmax: n=min(n,nmax)
        sums=np.zeros((len(XB_EDGES)-1,len(Q2_EDGES)-1))
        sums2=np.zeros_like(sums)
        for first in tqdm(range(0,n,100000), desc="Generator cross-section", unit="chunk", dynamic_ncols=True):
            end=min(n,first+100000)
            mc=m['MC'].array(entry_start=first,entry_stop=end,library='np')
            jac=m['Jacob'].array(entry_start=first,entry_stop=end,library='np')
            inv=ev['invts'].array(entry_start=first,entry_stop=end,library='np')
            xs=proc['xsec_tagged_dis'].array(entry_start=first,entry_stop=end,library='np')
            ki=proc['k_int'].array(entry_start=first,entry_stop=end,library='np')
            w=np.asarray(mc['PhSpFct'],float)*jac*xs*ki
            x=np.asarray(inv['xBj'],float); q=np.asarray(inv['Q2'],float)
            good=np.isfinite(w)&np.isfinite(x)&np.isfinite(q)
            sums+=np.histogram2d(x[good],q[good],bins=(XB_EDGES,Q2_EDGES),weights=w[good])[0]
            sums2+=np.histogram2d(x[good],q[good],bins=(XB_EDGES,Q2_EDGES),weights=w[good]**2)[0]
    sigma=sums/ndecl
    # partial processing uses the declared generator denominator: avoid implying full sample.
    out.mkdir(parents=True,exist_ok=True)
    pass  # No intermediate data export.
    sigma_masked = np.ma.masked_where(~np.isfinite(sigma.T) | (sigma.T <= 0), sigma.T)
    fig,ax=plt.subplots(figsize=(6.2,6.0))
    h=ax.pcolormesh(XB_EDGES,Q2_EDGES,sigma_masked,shading='auto',cmap='viridis',
                    norm=_log_norm_from_positive(sigma))
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel(r'$x_B$'); ax.set_ylabel(r'$Q^2$ [GeV$^2$]')
    ax.set_title(rf'$\sigma_{{\rm int}} = {sigma.sum():.3g}$ nb')
    ax.minorticks_on()
    fig.colorbar(h,ax=ax,label='Cross section [nb/bin]')
    fig.tight_layout();fig.savefig(out/'sigma_xb_q2.png');plt.close(fig)
    print(f'[GENERATOR] integrated sigma within plotted bins: {sigma.sum():.6g} nb (read {n} / {ndecl} events)')

