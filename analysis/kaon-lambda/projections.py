"""Lambda-tagging efficiency and (xB,Q²)->(xK,Q²) migration."""
from __future__ import annotations
import numpy as np
import uproot
from common.projection_root import dis, leading, meson_x, hist2, transitions
from config import PROJECTION_TMAX, PROTON_MASS, PROTON_CROSSING_ANGLE_MRAD


def proton(beam, n):
    """Construct the incident proton four-vector for the configured beam."""
    ep=float(beam.split('x')[-1]); p=np.sqrt(ep**2-PROTON_MASS**2)
    theta=PROTON_CROSSING_ANGLE_MRAD/1000
    return np.tile([ep,p*np.sin(theta),0.,p*np.cos(theta)],(n,1))


def lambda_coordinates(tree, method, beam, qedges=None):
    """Calculate event-level kinematic coordinates for the kaon channel."""
    xb,q=dis(tree,method)
    reco=leading(tree,'ReconstructedLambdas')
    p=proton(beam,len(xb))
    mag=np.linalg.norm(p[:,1:],axis=1)
    xl=(reco[:,0]+np.sum(reco[:,1:]*p[:,1:],axis=1)/mag)/(p[:,0]+mag)
    x=meson_x(xb,xl)
    valid=np.isfinite(x)&np.isfinite(q)&(x>0)&(x<1)&(q>0)&np.isfinite(xl)&(xl>0)&(xl<1)
    if PROJECTION_TMAX is not None:
        d=p-reco
        minus_t=np.sum(d[:,1:]**2,axis=1)-d[:,0]**2
        valid &= np.isfinite(minus_t)&(minus_t>=0)&(minus_t<PROJECTION_TMAX)
    return x,q,valid


def make_response(path, method, src_edges, dst_edges, qedges, beam, pt_max=None):
    """Build truth-to-reconstructed kinematic response counts."""
    with uproot.open(path) as file:
        tree=file['events']; xb,qtruth=dis(tree,'Truth')
        truth=np.isfinite(xb)&np.isfinite(qtruth)&(xb>0)&(xb<1)&(qtruth>0)
        dx,dq,valid=lambda_coordinates(tree,method,beam)
        present=np.isfinite(leading(tree,'ReconstructedLambdas')[:,0])
        tagged=truth&present
        migration_sel=tagged&valid
        source=hist2(xb,qtruth,truth,src_edges,qedges)
        tagged_hist=hist2(xb,qtruth,tagged,src_edges,qedges)
        trans=transitions(xb,qtruth,dx,dq,migration_sel,src_edges,dst_edges,qedges)
        counts=hist2(dx,dq,migration_sel,dst_edges,qedges)
        return source,tagged_hist,trans,counts,len(xb)


def count_background(path,method,dst_edges,qedges,beam):
    """Count reconstructed candidates in the background-overlay sample."""
    with uproot.open(path) as file:
        tree=file['events'];x,q,valid=lambda_coordinates(tree,method,beam)
        return hist2(x,q,valid,dst_edges,qedges),len(x)
