"""PODIO relations, MC ancestry, and background origin diagnostics."""
from __future__ import annotations
import json
from collections import Counter, defaultdict
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tqdm.auto import tqdm
from config import (BACKGROUND_DIAG_EVENTS, BACKGROUND_DIAG_MAX_PARTICLES_PER_SOURCE, BACKGROUND_PDG_LABELS, BACKGROUND_SOURCES, COLOR_NO_BACKGROUND, M_PI0, PLOT_FULL_DATA_RANGE, PROTON_ANGLE_RAD, PURITY_ASSOC, PURITY_CHUNK_EVENTS, PURITY_DEBUG_CANDIDATES, PURITY_SOURCES, Z_VERTEX_GRID_STEPS, Z_VERTEX_SCAN_MAX_M, Z_VERTEX_SCAN_MIN_M)
from plotting import finite, _style_hist_axes, plot_stairs, _square_figure
from root_io import _resolve_branch, write_rows_csv



def _truth_collection_ids(root_file):
    """Map ObjectID collectionIDs using the actual PODIO metadata schema."""
    import awkward as ak
    meta = root_file['podio_metadata']
    prefix = 'events___CollectionTypeInfo/events___CollectionTypeInfo.'
    ids = ak.to_list(ak.flatten(meta[prefix+'collectionID'].array(library='ak'), axis=None))
    names = ak.to_list(ak.flatten(meta[prefix+'name'].array(library='ak'), axis=None))
    result = {int(i): str(n) for i, n in zip(ids, names)}
    if not result:
        raise RuntimeError('Empty PODIO CollectionTypeInfo metadata')
    return result


def _relation_branches(collection, rel):
    """Compute relation branches for the analysis."""
    root = f'{collection}/{collection}.{rel}'
    refs = f'_{collection}_{rel}/_{collection}_{rel}.'
    return [root+'_begin', root+'_end', refs+'index', refs+'collectionID']


def _assoc_branches(name):
    """Compute assoc branches for the analysis."""
    return [f'{name}/{name}.weight',
            f'_{name}_rec/_{name}_rec.index',
            f'_{name}_rec/_{name}_rec.collectionID',
            f'_{name}_sim/_{name}_sim.index',
            f'_{name}_sim/_{name}_sim.collectionID']


def _fast_truth_branches(tree, mapping):
    """Return only branches on the measured Lambda-daughter-to-MC paths."""
    inv = {name: cid for cid, name in mapping.items()}
    daughter_names = [name for name in inv
                      if name.startswith('Reconstructed') and name.endswith('Neutrals')]
    essential = _relation_branches('ReconstructedLambdas', 'particles')
    essential += ['ReconstructedLambdas/ReconstructedLambdas.PDG',
                  'MCParticles/MCParticles.PDG',
                  'MCParticles/MCParticles.generatorStatus']
    essential += _relation_branches('MCParticles', 'parents')
    missing = [b for b in essential if b not in tree]
    if missing:
        raise RuntimeError('Missing required PODIO branches: '+repr(missing))
    branches = set(essential)
    available_daughters = []
    for d in daughter_names:
        b = _relation_branches(d, 'clusters')
        if all(x in tree for x in b):
            branches.update(b)
            for field in ('momentum.x','momentum.y','momentum.z',
                          'energy','referencePoint.x','referencePoint.y','referencePoint.z',
                          'PDG'):
                key = f'{d}/{d}.{field}'
                if key in tree:
                    branches.add(key)
            available_daughters.append(d)
    available_assocs = {}
    for cluster, assoc in PURITY_ASSOC.items():
        b = _assoc_branches(assoc)
        if cluster in inv and all(x in tree for x in b):
            available_assocs[inv[cluster]] = (cluster, assoc)
            branches.update(b)
            energy = f'{cluster}/{cluster}.energy'
            if energy in tree:
                branches.add(energy)
    return sorted(branches), available_daughters, available_assocs


def _association_truth(root_path, out, n_events, sample_label='mixed'):
    """Fast per-candidate origin classification, using only persisted associations.

    Dominant MC identification is separate from contamination measurements. Even
    a signal-origin leading contributor does not establish decay ancestry.
    """
    import uproot
    import awkward as ak
    from collections import defaultdict, Counter

    folder = out/'reconstruction'/'purity'
    folder.mkdir(parents=True, exist_ok=True)
    records = []
    origin_debug = Counter()
    origin_examples = []
    with uproot.open(root_path) as f:
        t = f['events']
        n_events = min(int(n_events), int(t.num_entries))
        ids = _truth_collection_ids(f)
        inv = {v:k for k,v in ids.items()}
        branches, daughters, assocs = _fast_truth_branches(t, ids)
        print(f'[TRUTH {sample_label}] branches={len(branches)}, daughter collections={len(daughters)}, '
              f'associations={len(assocs)}, events={n_events}', flush=True)
        if not assocs:
            raise RuntimeError('No MC cluster association collections available')
        missing_det = [v for v in PURITY_ASSOC if v in inv and inv[v] not in assocs]
        if missing_det:
            print('[TRUTH WARNING] Missing detector associations:', missing_det, flush=True)
        pass  # No intermediate data export.
        lam_id=inv['ReconstructedLambdas']; mc_id=inv['MCParticles']
        for start in tqdm(range(0, n_events, PURITY_CHUNK_EVENTS),
                          desc=f'MC ancestry {sample_label}', unit='chunk', dynamic_ncols=True):
            stop=min(n_events,start+PURITY_CHUNK_EVENTS)
            data=t.arrays(branches,entry_start=start,entry_stop=stop,library='ak',how=dict)
            for ie in range(stop-start):
                def arr(k):
                    """Compute arr for the analysis."""
                    return ak.to_list(data[k][ie])
                def refs(name,relation):
                    """Compute refs for the analysis."""
                    b,e,idx,cid=map(arr,_relation_branches(name,relation))
                    all_refs=list(zip(cid,idx))
                    return [all_refs[int(lo):int(hi)] for lo,hi in zip(b,e)]
                lam_daughters=refs('ReconstructedLambdas','particles')
                lam_pdg=arr('ReconstructedLambdas/ReconstructedLambdas.PDG')
                mc_pdg=arr('MCParticles/MCParticles.PDG')
                mc_status=arr('MCParticles/MCParticles.generatorStatus')
                mc_parents=refs('MCParticles','parents')
                neutrals={inv[d]:refs(d,'clusters') for d in daughters}
                daughter_values = {}
                for d in daughters:
                    keys = ['momentum.x','momentum.y','momentum.z',
                            'energy','referencePoint.x','referencePoint.y',
                            'referencePoint.z','PDG']
                    daughter_values[inv[d]] = {
                        field: arr(f'{d}/{d}.{field}')
                        for field in keys if f'{d}/{d}.{field}' in data
                    }
                cluster_energy={}
                cluster_to_mc=defaultdict(list)
                for cluster_id,(cluster,assoc) in assocs.items():
                    w,r_idx,r_id,s_idx,s_id=map(arr,_assoc_branches(assoc))
                    ek=f'{cluster}/{cluster}.energy'
                    if ek in data:
                        cluster_energy[cluster_id]=arr(ek)
                    for weight,ri,rc,si,sc in zip(w,r_idx,r_id,s_idx,s_id):
                        if int(rc)!=cluster_id or int(sc)!=mc_id or int(si)<0: continue
                        cluster_to_mc[(cluster_id,int(ri))].append((int(si),float(weight)))

                nmc=len(mc_pdg)
                ancestor_cache={}
                def ancestors(j):
                    """Compute ancestors for the analysis."""
                    if j in ancestor_cache: return ancestor_cache[j]
                    found=set();todo=[j]
                    while todo:
                        k=todo.pop()
                        if k in found or not (0<=k<nmc):continue
                        found.add(k)
                        if k<len(mc_parents):
                            todo.extend(int(v) for cid,v in mc_parents[k]
                                        if int(cid)==mc_id and int(v)>=0)
                    ancestor_cache[j]=found
                    return found
                def source(j):
                    # Origin of a secondary is determined from generator-tagged
                    # parents, not from its Geant4 status alone.
                    """Compute source for the analysis."""
                    aa=ancestors(j)
                    roots=[]
                    for k in aa:
                        st=int(mc_status[k])
                        block=(st//1000)*1000 if st>=0 else -1
                        if block in PURITY_SOURCES and block!=0:
                            roots.append((k,block))
                    if roots:
                        distinct={b for _,b in roots}
                        return next(iter(distinct)) if len(distinct)==1 else -2
                    # A source-zero label requires a reached generator-level
                    # root, but cannot prove Sullivan decay without parents.
                    return 0 if any(0<=int(mc_status[k])<1000 for k in aa) else -1

                for il, pdg_l in enumerate(lam_pdg):
                    if int(pdg_l)!=3122:continue
                    kid_refs=lam_daughters[il] if il<len(lam_daughters) else []
                    record=dict(event=start+ie,lambda_index=il,sample=sample_label,
                                category='unclassified',binary_class='unclassified',reason='',
                                n_daughters=len(kid_refs),n_associated_daughters=0,
                                n_signal_daughters=0,n_background_daughters=0,
                                lambda_mc_index=-1,pi0_mc_index=-1,
                                common_lambda_fraction=np.nan,
                                common_lambda_is_dominant=False,
                                pi0_daughter_mass_GeV=np.nan,
                                theta_gg_mrad=np.nan,
                                z_lambda_reco_m=np.nan,
                                z_lambda_method='unavailable')
                    for label in ('n','g1','g2'):
                        record[f'{label}_mc_index']=-1
                        record[f'{label}_source']=-1
                        record[f'{label}_source_fraction']=np.nan
                        record[f'{label}_dominant_fraction']=np.nan
                        record[f'{label}_association_count']=0
                    if len(kid_refs)!=3:
                        record['reason']='lambda has not exactly 3 daughter references'
                        records.append(record);continue
                    # Geometric observables from exactly the three Lambda daughters.
                    # Photon directions are reconstructed 3-momenta in the ROOT file.
                    if len(kid_refs) == 3:
                        def daughter_four(i):
                            """Compute daughter four for the analysis."""
                            cid, idx = map(int,kid_refs[i])
                            values = daughter_values.get(cid,{})
                            if idx < 0 or any(k not in values or idx >= len(values[k])
                                              for k in ('momentum.x','momentum.y','momentum.z','energy')):
                                return None
                            p = np.array([values[f'momentum.{q}'][idx] for q in 'xyz'],dtype=float)
                            en = float(values['energy'][idx])
                            if not np.all(np.isfinite(p)) or not np.isfinite(en): return None
                            point = None
                            if all(f'referencePoint.{q}' in values and idx < len(values[f'referencePoint.{q}']) for q in 'xyz'):
                                point = np.array([values[f'referencePoint.{q}'][idx] for q in 'xyz'],float)*1e-3
                            return p,en,point
                        g1,g2=daughter_four(1),daughter_four(2)
                        if g1 is not None and g2 is not None:
                            p1,e1,pos1=g1; p2,e2,pos2=g2
                            n1=np.linalg.norm(p1); n2=np.linalg.norm(p2)
                            if n1>0 and n2>0:
                                record['theta_gg_mrad']=float(1e3*np.arctan2(np.linalg.norm(np.cross(p1,p2)),np.dot(p1,p2)))
                            pgg=p1+p2
                            m2=(e1+e2)**2-float(np.dot(pgg,pgg))
                            if np.isfinite(m2) and m2 >= -1e-6:
                                record['pi0_daughter_mass_GeV']=float(np.sqrt(max(0.,m2)))
                            # Vertex hypothesis via pi0 PDG mass constraint, not the reconstructed pi0 mass.
                            # Detector reference points need to represent actual impact points.
                            if (pos1 is not None and pos2 is not None and
                                np.all(np.isfinite(pos1)) and np.all(np.isfinite(pos2)) and
                                min(pos1[2],pos2[2]) > 10. and e1>0 and e2>0 and
                                np.linalg.norm(pos1[:2]-pos2[:2])>1e-4):
                                from scipy.optimize import brentq
                                def eqz(z):
                                    """Compute eqz for the analysis."""
                                    origin=np.array([np.tan(PROTON_ANGLE_RAD)*z,0.,z])
                                    v1=pos1-origin;v2=pos2-origin
                                    a=np.linalg.norm(v1);b=np.linalg.norm(v2)
                                    if min(a,b)<1e-9:return np.nan
                                    cos=np.clip(np.dot(v1,v2)/(a*b),-1.,1.)
                                    return 2*e1*e2*(1-cos)-M_PI0**2
                                zmin=Z_VERTEX_SCAN_MIN_M
                                zmax=min(Z_VERTEX_SCAN_MAX_M,float(pos1[2]),float(pos2[2]))-1.e-3
                                if zmax>zmin:
                                    zgrid=np.linspace(zmin,zmax,Z_VERTEX_GRID_STEPS)
                                    fgrid=[eqz(z) for z in zgrid]
                                    roots=[]
                                    for k in range(len(zgrid)-1):
                                        if np.isfinite(fgrid[k]) and np.isfinite(fgrid[k+1]) and fgrid[k]*fgrid[k+1]<0:
                                            roots.append(float(brentq(eqz,zgrid[k],zgrid[k+1])))
                                    if len(roots)==1:
                                        record['z_lambda_reco_m']=roots[0]
                                        record['z_lambda_method']='pi0_mass_constrained_photon_pointing'
                                    elif len(roots)>1:
                                        record['z_lambda_method']='ambiguous_multiple_roots'
                                    else:
                                        record['z_lambda_method']='no_physical_root'
                    chosen=[];valid=True;all_sourced=[];daughter_weights=[]
                    trace = {'event': start+ie, 'lambda_index': il, 'daughters': {}}
                    for j,(dcid,dindex) in enumerate(kid_refs):
                        label=('n','g1','g2')[j]
                        dcid,dindex=int(dcid),int(dindex)
                        dt={'reco_collection_id':dcid, 'reco_collection':ids.get(dcid, 'UNKNOWN'),
                            'reco_index':dindex, 'clusters':[], 'mc_contributors':[]}
                        trace['daughters'][label]=dt
                        weighted=defaultdict(float)
                        associations=0
                        if dcid not in neutrals:
                            dt['failure']='daughter_collection_relation_missing'
                            origin_debug[f'{label}:daughter_collection_relation_missing']+=1
                            valid=False;chosen.append(-1);daughter_weights.append({});continue
                        if not 0<=dindex<len(neutrals[dcid]):
                            dt['failure']='daughter_index_out_of_range'
                            origin_debug[f'{label}:daughter_index_out_of_range']+=1
                            valid=False;chosen.append(-1);daughter_weights.append({});continue
                        daughter_clusters=neutrals[dcid][dindex]
                        if not daughter_clusters:
                            dt['failure']='no_cluster_references'
                            origin_debug[f'{label}:no_cluster_references']+=1
                        any_supported=False
                        any_association=False
                        any_valid_association=False
                        for ccid,cindex in daughter_clusters:
                            ccid,cindex=int(ccid),int(cindex)
                            cl={'collection_id':ccid,'collection':ids.get(ccid,'UNKNOWN'),
                                'index':cindex, 'association_collection':None, 'association_count':0}
                            dt['clusters'].append(cl)
                            if ccid not in assocs:
                                cl['failure']='cluster_collection_has_no_loaded_MC_association'
                                continue
                            any_supported=True
                            cl['association_collection']=assocs[ccid][1]
                            ass=cluster_to_mc.get((ccid,cindex),[])
                            cl['association_count']=len(ass)
                            if not ass:
                                cl['failure']='no_MC_association_for_cluster'
                                continue
                            any_association=True
                            energies=cluster_energy.get(ccid,[])
                            ce=max(0.,float(energies[cindex])) if 0<=cindex<len(energies) else 1.
                            for mc_idx,weight in ass:
                                if not 0<=mc_idx<nmc or not np.isfinite(weight) or weight<=0:
                                    continue
                                weighted[mc_idx]+=weight*ce
                                associations+=1
                                any_valid_association=True
                        record[f'{label}_association_count']=associations
                        if not weighted or sum(weighted.values())<=0:
                            if not dt.get('failure'):
                                dt['failure']=('cluster_collection_has_no_loaded_MC_association' if not any_supported
                                               else 'no_MC_association_for_cluster' if not any_association
                                               else 'invalid_MC_indices_or_nonpositive_weights' if not any_valid_association
                                               else 'nonpositive_weighted_sum')
                            origin_debug[f'{label}:{dt["failure"]}']+=1
                            valid=False;chosen.append(-1);daughter_weights.append({});continue
                        dt['failure']=None
                        origin_debug[f'{label}:associated']+=1
                        if len(origin_examples)<PURITY_DEBUG_CANDIDATES:
                            for mc_idx, contribution in sorted(weighted.items(),key=lambda v:-v[1])[:6]:
                                aa=ancestors(mc_idx)
                                dt['mc_contributors'].append({
                                    'mc_index':int(mc_idx),'pdg':int(mc_pdg[mc_idx]),
                                    'generator_status':int(mc_status[mc_idx]),
                                    'inferred_source':int(source(mc_idx)),
                                    'weighted_contribution':float(contribution),
                                    'ancestors':[{'index':int(k),'pdg':int(mc_pdg[k]),
                                                  'generator_status':int(mc_status[k])}
                                                 for k in sorted(aa)[:40]],
                                    'ancestors_truncated':len(aa)>40})
                        daughter_weights.append(dict(weighted))
                        record['n_associated_daughters']+=1
                        leader=max(weighted,key=weighted.get)
                        chosen.append(leader)
                        total=sum(weighted.values())
                        leadfraction=weighted[leader]/total
                        sourceweights=defaultdict(float)
                        for mc_idx, wgt in weighted.items():
                            sourceweights[source(mc_idx)]+=wgt
                        source_lead=max(sourceweights,key=sourceweights.get)
                        source_fraction=sourceweights[source_lead]/total
                        record[f'{label}_mc_index']=int(leader)
                        record[f'{label}_source']=int(source_lead)
                        record[f'{label}_source_fraction']=float(source_fraction)
                        record[f'{label}_dominant_fraction']=float(leadfraction)
                        all_sourced.append(sourceweights)
                        if source_lead==0:record['n_signal_daughters']+=1
                        elif source_lead in PURITY_SOURCES:record['n_background_daughters']+=1

                    # Fast operational source classification.  The candidate is
                    # Sullivan-origin if ANY of its three neutral daughters has
                    # an identified dominant source-0 MC contribution. It is
                    # combinatorial only if ALL THREE have explicit background
                    # source tags. Missing associations must NOT veto an already
                    # identified Sullivan daughter.
                    daughter_sources = [record[f'{name}_source'] for name in ('n', 'g1', 'g2')]
                    if any(src == 0 for src in daughter_sources):
                        record['binary_class'] = 'signal'
                        record['category'] = 'sullivan_origin_candidate'
                        record['reason'] = 'at least one neutral has dominant Sullivan MC source'
                    elif all(src in PURITY_SOURCES and src != 0 for src in daughter_sources):
                        record['binary_class'] = 'combinatorial'
                        record['category'] = 'background_only'
                        record['reason'] = 'all three neutrals have explicit background MC sources'
                    else:
                        record['binary_class'] = 'unclassified'
                        record['category'] = 'unclassified'
                        record['reason'] = 'no identified Sullivan daughter; at least one neutral source unresolved'
                    trace['binary_class']=record['binary_class']
                    trace['category']=record['category']
                    if len(origin_examples)<PURITY_DEBUG_CANDIDATES:
                        origin_examples.append(trace)
                    records.append(record)
            print(f'[TRUTH {sample_label}] {stop}/{n_events} events',flush=True)

    # Classes are assigned per candidate above, immediately after the neutral
    # MC source lookup. No common-Lambda ancestry is required for this metric.
    # Retain a small diagnostic breakdown to distinguish missing associations
    # from real background-only candidates.
    diagnostic = Counter()
    for record in records:
        ss = [record.get(f'{d}_source', -1) for d in ('n', 'g1', 'g2')]
        diagnostic[f'associated_daughters_{record["n_associated_daughters"]}'] += 1
        diagnostic['any_source_0'] += int(0 in ss)
        diagnostic['all_explicit_background'] += int(all(k in PURITY_SOURCES and k != 0 for k in ss))
        diagnostic['unresolved_without_signal'] += int(0 not in ss and any(k not in PURITY_SOURCES for k in ss))
    print(f'[SOURCE CLASSIFICATION {sample_label}]', dict(diagnostic), flush=True)
    debug_report={'sample':sample_label,'input':str(root_path),'n_candidates':len(records),
                  'trace_limit':PURITY_DEBUG_CANDIDATES,
                  'daughter_outcomes':dict(origin_debug),
                  'interpretation':'Missing associations are UNKNOWN, never proof of background. '
                    'Only positive valid cluster-to-MC associations support source tags.',
                  'example_candidates':origin_examples}
    pass  # No intermediate data export.
    print(f'[ORIGIN DEBUG {sample_label}]',dict(origin_debug),flush=True)
    print('[ORIGIN DEBUG] Detailed traces:',folder/f'origin_debug_{sample_label}.json',flush=True)

    # Numerator and denominator are always reported, including unknowns.
    counts=Counter(r['category'] for r in records)
    n=len(records); true=counts['true_signal_lambda']; common=counts['common_sullivan_lambda']; unknown=counts['unclassified']
    summary=dict(sample=sample_label,n_candidates=n,category_counts=dict(counts),
                 strict_verified_fraction=None,
                 common_sullivan_lambda_fraction=None,
                 common_or_partial_lambda_fraction=None,
                 unresolved_fraction=unknown/n if n else None,
                 strict_truth_definition='requires explicit neutron/pi0/two-photon decay ancestry; not established by common calorimeter origin',
                 common_lambda_definition='all three dominant MC contributors share one Sullivan Lambda (PDG 3122, generatorStatus < 1000); NOT strict decay truth',
                 strict_fraction_is_lower_bound_when_unresolved=False,
                 note='Combinatorial and mixed categories use dominant MC origin; contamination weights are in per-daughter columns.',
                 numerical_caveat='MC association weights and HEXPLIT splitting require validation before publication.')
    binary_counts = Counter(r['binary_class'] for r in records)
    classified = binary_counts['signal'] + binary_counts['combinatorial']
    summary['binary_class_counts'] = dict(binary_counts)
    summary['classification_diagnostics'] = dict(diagnostic)
    summary['strict_matching_not_run'] = True
    summary['binary_signal_fraction_classified'] = (
        binary_counts['signal']/classified if classified else None)
    summary['binary_signal_fraction_all'] = binary_counts['signal']/n if n else None
    summary['binary_definition'] = ('signal if at least one reconstructed Lambda daughter has identified dominant Sullivan MC source; '
        'combinatorial if all three have identified nonzero source blocks; otherwise unclassified. '
        'No common Lambda ancestor required; this is origin-tag purity, not exclusive truth matching.')
    pass  # No intermediate data export.
    pass  # No intermediate data export.
    print(f'[TRUTH {sample_label}] {summary}',flush=True)
    return records,summary


def sampled_background_distributions(root_path, out, max_events, n_sample=BACKGROUND_DIAG_EVENTS):
    """Fast, light-weight diagnostic. Sample complete events, not individual rare types.

    No full MC inventory; all labels explicitly refer to the sampled events.
    """
    import uproot
    import awkward as ak
    folder = out / 'background_sources'
    folder.mkdir(parents=True, exist_ok=True)
    with uproot.open(root_path) as f:
        tree = f['events']
        n = min(int(tree.num_entries), max_events)
        # Ten short contiguous windows spread through the file: low read/decompression cost.
        per_window = max(1, min(n, n_sample)//10) if n else 0
        starts = np.linspace(0, max(0,n-per_window), min(10,max(1,n//per_window)), dtype=np.int64) if n else []
        indices = np.unique(np.concatenate([np.arange(k,min(n,k+per_window)) for k in starts])) if n else np.array([],dtype=np.int64)
        required = ['PDG', 'generatorStatus', 'momentum.x', 'momentum.y', 'momentum.z']
        optional = ['mass', 'vertex.x', 'vertex.y', 'vertex.z']
        names = {k: _resolve_branch(tree, 'MCParticles', k) for k in required + optional}
        missing = [k for k in required if not names[k]]
        if missing:
            raise RuntimeError('Fast MC diagnostics: missing branches '+str(missing))
        needed = [v for v in names.values() if v]
        all_rows = []
        # Group near-by sampled events into contiguous blocks to avoid many tiny reads.
        segments = np.split(indices, np.flatnonzero(np.diff(indices)>1)+1) if len(indices) else []
        for local in tqdm(segments, desc="Sample background", unit="window", dynamic_ncols=True):
            if not len(local):continue
            block_start=int(local[0])
            data = tree.arrays(needed, entry_start=int(local[0]),
                               entry_stop=int(local[-1])+1, library='ak')
            evsel = local - local[0]
            def flat(field, default=0.):
                """Compute flat for the analysis."""
                if names[field] is None:
                    return None
                return ak.to_numpy(ak.flatten(data[names[field]][evsel], axis=None))
            pdg = flat('PDG').astype(np.int32)
            stat = flat('generatorStatus').astype(np.int32)
            px,py,pz = [flat('momentum.' + x) for x in 'xyz']
            mass = flat('mass')
            if mass is None: mass = np.zeros_like(px)
            vx,vy,vz = (flat('vertex.'+x) for x in 'xyz')
            mom = np.sqrt(px**2+py**2+pz**2)
            pt = np.hypot(px,py)
            fields = dict(E=np.sqrt(mom**2+mass**2), pt=pt,
                          theta_mrad=np.arctan2(pt,pz)*1e3,
                          eta=np.arcsinh(pz/np.maximum(pt,1e-12)),
                          phi=np.arctan2(py,px),
                          vz=vz if vz is not None else np.full(len(px),np.nan),
                          r=np.hypot(vx,vy) if vx is not None and vy is not None else np.full(len(px),np.nan))
            block = np.where(stat >= 0, (stat//1000)*1000, -1)
            for source in BACKGROUND_SOURCES:
                if source == 0: continue
                idx = np.flatnonzero(block == source)
                if not len(idx): continue
                # Uniformly sample the selected particles, retain PDG/kinematics.
                remaining = max(0, BACKGROUND_DIAG_MAX_PARTICLES_PER_SOURCE -
                                sum(len(row['pdg']) for row in all_rows if row['source']==source))
                if not remaining: continue
                if len(idx) > remaining:
                    idx = np.random.default_rng(12345+block_start+source).choice(idx,remaining,replace=False)
                all_rows.append(dict(source=source,pdg=pdg[idx],
                                     **{k:v[idx] for k,v in fields.items()}))
    joined = {}
    for source in BACKGROUND_SOURCES:
        if source == 0:continue
        rows = [r for r in all_rows if r['source']==source]
        if rows:joined[source] = {key:np.concatenate([r[key] for r in rows])
                                 for key in ['pdg','E','pt','theta_mrad','eta','phi','vz','r']}
    # Publication-style square, separate figures, one observable per figure.
    # Common binning for comparison; each source is normalized independently.
    source_colors = ['#1F4E79','#C55A11','#2E8B57','#865A9E','#BE4550','#667788']
    plot_specs = [
        ('E', r'MC energy [GeV]', 'energy_by_source.png', True),
        ('pt', r'MC transverse momentum [GeV]', 'pt_by_source.png', True),
        ('theta_mrad', r'MC polar angle [mrad]', 'theta_by_source.png', False),
        ('eta', r'MC pseudorapidity', 'eta_by_source.png', False),
        ('phi', r'MC azimuth [rad]', 'phi_by_source.png', False),
        ('vz', r'MC production $z$ [mm]', 'vz_by_source.png', False),
        ('r', r'MC production $r$ [mm]', 'r_by_source.png', False),
    ]
    for metric, xlabel, filename, logx in tqdm(plot_specs, desc='Background plots', unit='plot', leave=False):
        combined = np.concatenate([cols[metric][np.isfinite(cols[metric])]
                                   for cols in joined.values() if len(cols[metric])]) if joined else np.array([])
        if not combined.size:
            continue
        if logx:
            positives = combined[combined > 0]
            if not len(positives): continue
            lo=max(float(np.min(positives)) if PLOT_FULL_DATA_RANGE else float(np.percentile(positives,.25)),1e-8)
            hi=float(np.max(positives)) if PLOT_FULL_DATA_RANGE else float(np.percentile(positives,99.75))
            if hi<=lo: hi=lo*10
            bins=np.geomspace(lo,hi,71)
        else:
            lo,hi=(np.min(combined),np.max(combined)) if PLOT_FULL_DATA_RANGE else np.percentile(combined,[.25,99.75])
            if hi<=lo:lo-=.5;hi+=.5
            bins=np.linspace(lo,hi,71)
        fig,ax=_square_figure()
        for (source, cols),color in zip(sorted(joined.items()),source_colors):
            v=finite(cols[metric]);v=v[v>0] if logx else v
            if not len(v):continue
            plot_stairs(ax,v,bins,linewidth=1.9,color=color,
                    weights=np.full(len(v),100.0/len(v)),
                    label=f'{BACKGROUND_SOURCES[source]} (N={len(v):,})')
        if logx:ax.set_xscale('log')
        _style_hist_axes(ax, values=combined, xlabel=xlabel)
        ax.set_xlabel(xlabel);ax.set_ylabel('Fraction of each source [%]')
        if ax.has_data():ax.legend(fontsize=13,loc='best')
        fig.tight_layout();fig.savefig(folder/filename);plt.close(fig)
    # Six separate, square PDG plots replace the cramped 3x2 montage.
    for source,cols in sorted(joined.items()):
        counts=Counter(map(int,cols['pdg']))
        top=counts.most_common(12)
        if not top:continue
        fig,ax=_square_figure()
        labels=[BACKGROUND_PDG_LABELS.get(p,str(p)) for p,_ in reversed(top)]
        vals=[c for _,c in reversed(top)]
        ax.barh(labels, vals, color=COLOR_NO_BACKGROUND, height=.7)
        ax.set_xscale('log');ax.set_xlim(left=.8)
        ax.set_xlabel('Sampled MC particles [count]')
        ax.set_title(BACKGROUND_SOURCES[source]);ax.tick_params(direction='in')
        fig.tight_layout();fig.savefig(folder/f'pdg_composition_{source}.png');plt.close(fig)
    # Same square figure convention for background Lambda-only kinematics.
    for metric, xlabel, logx, filename in [
        ('E', r'Background $\Lambda$ energy [GeV]',True,'lambda_mc_energy_by_source.png'),
        ('theta_mrad',r'Background $\Lambda$ polar angle [mrad]',False,'lambda_mc_theta_by_source.png')]:
        bysource={source:finite(cols[metric][np.abs(cols['pdg'])==3122]) for source,cols in joined.items()}
        data=[v[v>0] if logx else v for v in bysource.values() if len(v)]
        if not data:continue
        both=np.concatenate(data)
        if not len(both):continue
        lo,hi=np.percentile(both,[0,100]);hi=max(hi,lo*10) if logx else max(hi,lo+1)
        edges=np.geomspace(max(lo,1e-6),hi,61) if logx else np.linspace(lo,hi,61)
        fig,ax=_square_figure()
        for (source, v),color in zip(sorted(bysource.items()),source_colors):
            v=v[v>0] if logx else v
            if len(v):plot_stairs(ax,v,edges,linewidth=1.9,color=color,
                               weights=np.full(len(v),100./len(v)),label=BACKGROUND_SOURCES[source])
        if logx:ax.set_xscale('log')
        _style_hist_axes(ax, values=both, xlabel=xlabel)
        ax.set(xlabel=xlabel,ylabel='Fraction of each source [%]')
        if ax.has_data():ax.legend(fontsize=13)
        fig.tight_layout();fig.savefig(folder/filename);plt.close(fig)
    report = dict(n_sampled_events=int(len(indices)), n_available_events=int(n),
                  sampled_particle_counts={str(k):len(v['pdg']) for k,v in joined.items()},
                  caveat='Sampled MC shapes only. Counts not full-frame counts. Not reco purity.')
    pass  # No intermediate data export.
    print('[BACKGROUND SAMPLE]',report,flush=True)

