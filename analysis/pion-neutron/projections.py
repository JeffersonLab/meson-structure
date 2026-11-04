"""Neutron-tagging efficiency and (xπ,Q²) response from ePIC reconstructed files."""
from __future__ import annotations
import numpy as np
import uproot
from common.projection_root import dis, leading, beam_xl, meson_x, hist2, transitions
from config import (NEUTRAL_COLLECTION, PROJECTION_TRUTH_NEUTRON_STATUS,
                    PROJECTION_INCOMING_PROTON_STATUS, NEUTRON_MASS)


def coordinates(tree, method):
    """Calculate event-level kinematic coordinates for the pion channel."""
    proton=leading(tree,'MCParticles',pdg=2212,status=PROJECTION_INCOMING_PROTON_STATUS)
    neutron=leading(tree,NEUTRAL_COLLECTION,pdg=2112)
    xb,q=dis(tree,method)
    xl,_=beam_xl(neutron,proton)
    x=meson_x(xb,xl)
    valid=np.isfinite(x)&np.isfinite(q)&(x>0)&(x<1)&(q>0)&np.isfinite(xl)&(xl>0)&(xl<1)
    return x,q,valid


def make_response(path,method,src_edges,dst_edges,qedges,beam,pt_max=None):
    """Build truth-to-reconstructed kinematic response counts."""
    with uproot.open(path) as file:
        tree=file['events'];xb,qtruth=dis(tree,'Truth')
        proton=leading(tree,'MCParticles',pdg=2212,status=PROJECTION_INCOMING_PROTON_STATUS)
        neutron=leading(tree,'MCParticles',pdg=2112,status=PROJECTION_TRUTH_NEUTRON_STATUS,energy_from_mass=NEUTRON_MASS)
        xl,pt=beam_xl(neutron,proton)
        xtruth=meson_x(xb,xl)
        truth=np.isfinite(xtruth)&np.isfinite(qtruth)&np.isfinite(pt)&(xtruth>0)&(xtruth<1)&(qtruth>0)&(xl>0)&(xl<1)
        if pt_max is not None:
            truth &= pt<pt_max
        xreco,qreco,valid=coordinates(tree,method)
        present=np.isfinite(leading(tree,NEUTRAL_COLLECTION,pdg=2112)[:,0])
        tagged=truth&present
        migration_sel=tagged&valid
        source=hist2(xtruth,qtruth,truth,src_edges,qedges)
        taghist=hist2(xtruth,qtruth,tagged,src_edges,qedges)
        trans=transitions(xtruth,qtruth,xreco,qreco,migration_sel,src_edges,dst_edges,qedges)
        counts=hist2(xreco,qreco,migration_sel,dst_edges,qedges)
        return source,taghist,trans,counts,len(xtruth)


def count_background(path,method,dst_edges,qedges,beam):
    """Count reconstructed candidates in the background-overlay sample."""
    with uproot.open(path) as file:
        tree=file['events'];x,q,valid=coordinates(tree,method)
        return hist2(x,q,valid,dst_edges,qedges),len(x)
