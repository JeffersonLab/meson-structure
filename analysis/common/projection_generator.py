"""Weighted Sullivan-generator cross sections on a specified source grid."""
from __future__ import annotations
import numpy as np
import uproot


def sigma_map(filename, channel, xedges, qedges, *, pt_max=None, chunk=100000):
    """Return nb/bin and generator-MC error; always normalize to declared nEvts."""
    if channel not in ('pion', 'kaon'):
        raise ValueError(channel)
    sumw = np.zeros((len(xedges)-1, len(qedges)-1))
    sumw2 = np.zeros_like(sumw)
    with uproot.open(filename) as file:
        meta, events, process = (file[k] for k in ('Meta','Evnts','Process'))
        mcname = 'MC' if 'MC' in meta else 'Monte Carlo'
        declared = int(meta[mcname].array(entry_stop=1,library='np')['nEvts'][0])
        available = min(meta.num_entries,events.num_entries,process.num_entries)
        if declared < 2 or available <= 0:
            raise ValueError('Insufficient generator events')
        # No silent partial-event normalization: partial input invalidates sigma estimates.
        if available != declared:
            raise ValueError(f'Generator contains {available} entries, but declares {declared}; provide complete generator sample')
        for start in range(0,available,chunk):
            end=min(available,start+chunk)
            mc=meta[mcname].array(entry_start=start,entry_stop=end,library='np')
            jac=np.asarray(meta['Jacob'].array(entry_start=start,entry_stop=end,library='np'),float)
            inv=events['invts'].array(entry_start=start,entry_stop=end,library='np')
            xs_name='xsec_taggedLN_dis' if channel=='pion' else 'xsec_tagged_dis'
            xs=np.asarray(process[xs_name].array(entry_start=start,entry_stop=end,library='np'),float)
            weights=np.asarray(mc['PhSpFct'],float)*jac*xs
            if channel=='kaon':
                weights*=np.asarray(process['k_int'].array(entry_start=start,entry_stop=end,library='np'),float)
            x=np.asarray(process['xpi'].array(entry_start=start,entry_stop=end,library='np'),float) if channel=='pion' else np.asarray(inv['xBj'],float)
            q=np.asarray(inv['Q2'],float)
            valid=np.isfinite(weights)&np.isfinite(x)&np.isfinite(q)&(x>0)&(x<1)&(q>0)
            if channel=='pion':
                xl=np.asarray(process['xL'].array(entry_start=start,entry_stop=end,library='np'),float)
                valid &= np.isfinite(xl)&(xl>0)&(xl<1)
                if pt_max is not None:
                    part=np.stack([np.asarray(process[f'n_mom{a}_lab'].array(entry_start=start,entry_stop=end,library='np'),float) for a in 'xyz'],axis=1)
                    beam=np.stack([np.asarray(process[f'p_mom{a}_incident'].array(entry_start=start,entry_stop=end,library='np'),float) for a in 'xyz'],axis=1)
                    norms=np.linalg.norm(beam,axis=1)
                    axis=np.divide(beam,norms[:,None],out=np.full_like(beam,np.nan),where=norms[:,None]>0)
                    pt=np.linalg.norm(part-np.sum(part*axis,axis=1)[:,None]*axis,axis=1)
                    valid &= np.isfinite(pt)&(pt<pt_max)
            sumw += np.histogram2d(x[valid],q[valid],bins=(xedges,qedges),weights=weights[valid])[0]
            sumw2 += np.histogram2d(x[valid],q[valid],bins=(xedges,qedges),weights=weights[valid]**2)[0]
    err=np.sqrt(np.maximum(sumw2-sumw**2/declared,0)/(declared*(declared-1)))
    return sumw/declared,err,declared
