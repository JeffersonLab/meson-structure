"""Top-level Lambda candidate reconstruction and diagnostic workflow."""
from __future__ import annotations
import csv
import json
from pathlib import Path
from collections import Counter, defaultdict
import numpy as np
import matplotlib
matplotlib.use("Agg")
from tqdm.auto import tqdm
from config import (BACKGROUND_DIAG_EVENTS, DETECTORS, MLSIGMA, MPSIGMA, RUN_FAST_BACKGROUND_DIAG, TMAX, VERTEX_MM_TO_M, XL_MAX)
from plotting import save_1d, save_2d, save_eff2d
from physics import (collect_pi0_pairs, lambda_transfer_and_xl, select_best_pi0)
from physics import _primary_mc_lambda
from root_io import read_truth_dis, write_rows_csv, _resolve_branch
from matching import _association_truth, sampled_background_distributions
from selection import (fit_lambda_mass, fit_pi0_mass, pass_core, pass_lambda_mass, pass_pi0, pass_t, pass_xl, plot_pstar_cutflow, unified_cut_study)


def progress_phase(name):
    """Compute progress phase for the analysis."""
    print(f"\n[PHASE] {name}", flush=True)


def fill(store, data):
    """Compute fill for the analysis."""
    if data is None:
        return
    for key, value in data.items():
        if np.isfinite(value):
            store[key].append(value)


def analyze_reconstruction(file, out, max_events, background_file=None):
    """Read EDM4hep PODIO ROOT branches with uproot, not C++ ROOTFrameReader.

    Kinematics via uproot; persisted PODIO relations for MC origins.
    """
    import uproot
    import awkward as ak

    def branch(tree, stem, field, n):
        """Read an EDM4eIC collection field, accepting common ROOT branch layouts."""
        key = _resolve_branch(tree, stem, field)
        return tree[key].array(entry_stop=n, library='ak') if key else None

    def collection(tree, stems, n):
        """Compute collection for the analysis."""
        for stem in stems:
            fields = {}
            columns = [('E','energy'), ('px','momentum.x'),
                       ('py','momentum.y'), ('pz','momentum.z'),
                       ('mass','mass'), ('pdg','PDG'),
                       ('genstatus','generatorStatus'),
                       ('vx','vertex.x'), ('vy','vertex.y'), ('vz','vertex.z'),
                       ('ex','endpoint.x'), ('ey','endpoint.y'), ('ez','endpoint.z')]
            with tqdm(total=len(columns), desc=f"ROOT {stem[:28]}", unit="branch", leave=False, dynamic_ncols=True) as bar:
                for key, col in columns:
                    bar.set_postfix_str(col, refresh=False)
                    data = branch(tree, stem, col, n)
                    if data is not None: fields[key] = data
                    bar.update(1)
            if all(k in fields for k in ('px','py','pz')) and ('E' in fields or 'mass' in fields):
                print(f'[BRANCH] {stem}: '+', '.join(sorted(fields)))
                return stem, fields
            elif fields:
                print(f'[WARNING] {stem}: incomplete fields {sorted(fields)}')
        return None, {}

    def row_kin(E,px,py,pz,mass=np.nan):
        """Compute row kin for the analysis."""
        if not np.all(np.isfinite([E,px,py,pz])): return None
        pt=np.hypot(px,py); mom=np.hypot(pt,pz)
        theta=np.arctan2(pt,pz)
        mass = mass if np.isfinite(mass) else np.sqrt(max(0,E*E-mom*mom))
        minus_t,xL=lambda_transfer_and_xl(E,px,py,pz)
        return {'E':E,'px':px,'py':py,'pz':pz,'p':mom,'pt':pt,
                'theta_mrad':theta*1000,'phi':np.arctan2(py,px),
                'cos_theta':pz/mom if mom>0 else np.nan,
                'eta':np.arcsinh(pz/pt) if pt>1e-12 else np.nan,
                'mass':mass,'minus_t':minus_t,'xL':xL}

    def signal_mc_only(fields, n):
        """Vectorized source-tag selection BEFORE Python object conversion.

        Keep source-0 Lambda, pi0, neutron and photons used by the existing
        generator plots and event-level diagnostics.  Reject all overlay MC
        objects before calling event_vectors.  Unknown statuses are not signal.
        """
        if not fields or 'pdg' not in fields or 'genstatus' not in fields:
            raise RuntimeError('MCParticles.PDG and generatorStatus required for safe signal filtering')
        pdg, status = fields['pdg'], fields['genstatus']
        mask = ((status >= 0) & (status < 1000) &
                ((pdg == 3122) | (pdg == 111) | (pdg == 2112) | (pdg == 22)))
        selected = {key: arr[mask] for key, arr in fields.items()}
        print('[MC SOURCE FILTER] generatorStatus [0,1000), PDG 3122/111/2112/22; '
              f'kept={int(ak.sum(ak.num(selected["pdg"],axis=1)))} objects / {n} events',flush=True)
        return event_vectors(selected, n)

    def event_vectors(fields,n):
        """Compute event vectors for the analysis."""
        if not fields: return [[] for _ in range(n)]
        # Do not flatten event boundaries. Support both jagged and scalar branches.
        out=[]
        for i in tqdm(range(n), desc="Convert event vectors", unit="evt", leave=False, dynamic_ncols=True):
            e=ak.to_list(fields['E'][i]) if 'E' in fields else None;px=ak.to_list(fields['px'][i]);
            py=ak.to_list(fields['py'][i]);pz=ak.to_list(fields['pz'][i])
            if not isinstance(px,list):px=[px];py=[py];pz=[pz]
            if e is None:e=[np.nan]*len(px)
            elif not isinstance(e,list):e=[e]
            masses=ak.to_list(fields['mass'][i]) if 'mass' in fields else [np.nan]*len(e)
            pdgs=ak.to_list(fields['pdg'][i]) if 'pdg' in fields else [0]*len(e)
            stat=ak.to_list(fields['genstatus'][i]) if 'genstatus' in fields else [-1]*len(e)
            if not isinstance(masses,list):masses=[masses]
            if not isinstance(pdgs,list):pdgs=[pdgs]
            if not isinstance(stat,list):stat=[stat]
            # Optional MC production and endpoint coordinates (mm).
            def optional_list(name, length):
                """Compute optional list for the analysis."""
                if name not in fields:
                    return [np.nan] * length
                v = ak.to_list(fields[name][i])
                return v if isinstance(v, list) else [v]
            optional = {key: optional_list(key,len(e)) for key in
                        ('vx','vy','vz','ex','ey','ez')}
            entries=[]
            for j in range(min(len(e),len(px),len(py),len(pz))):
                mass = float(masses[j]) if j<len(masses) and masses[j] is not None else np.nan
                energy = float(e[j]) if j<len(e) and e[j] is not None else np.nan
                if not np.isfinite(energy) and np.isfinite(mass):
                    energy = np.sqrt(float(px[j])**2+float(py[j])**2+float(pz[j])**2+mass**2)
                k=row_kin(energy,float(px[j]),float(py[j]),float(pz[j]),mass)
                if k is not None:
                    k['_pdg']=int(pdgs[j]) if j<len(pdgs) else 0
                    k['_status']=int(stat[j]) if j<len(stat) and stat[j] is not None else -1
                    for coord, vals in optional.items():
                        v = vals[j] if j < len(vals) else np.nan
                        try: k['_'+coord] = float(v) if v is not None else np.nan
                        except (ValueError,TypeError): k['_'+coord] = np.nan
                    entries.append(k)
            out.append(entries)
        return out

    out.mkdir(parents=True,exist_ok=True)
    progress_phase("Read signal ROOT collections")
    with uproot.open(file) as f:
        tree=f['events']
        n=min(tree.num_entries,max_events) if max_events else tree.num_entries
        print(f'[UPROOT] reading {n}/{tree.num_entries} events; no PODIO reader')
        if max_events and max_events <= 1: print('[TIP] use --dump-branches to inspect ROOT tree schema')
        mc_name,mc_fields=collection(tree,['MCParticles'],n)
        la_name,la_fields=collection(tree,['ReconstructedLambdas','ReconstructedFarForwardLambdas'],n)
        print('[COLLECTIONS] MC:',mc_name,'Lambda:',la_name)
        if not mc_fields: print('[WARNING] MCParticles momentum/mass unavailable: inspect the branch inventory')
        if not la_fields: print('[WARNING] Lambda 4-vector unavailable; inspect ROOT branch names')
        mc=signal_mc_only(mc_fields,n)
        lambdas=event_vectors(la_fields,n)
        det={}
        for d,stem in DETECTORS.items():
            actual,fields=collection(tree,[stem],n)
            det[d]=event_vectors(fields,n)
            print(f'[COLLECTIONS] {d}: {actual}')
        try: xb,q2=read_truth_dis(file,n)
        except Exception as exc:
            print('[WARNING] Cannot read DIS truth:',exc)
            xb=np.full(n,np.nan);q2=np.full(n,np.nan)

    # Optional reconstruction from the file containing overlaid background.
    # Its Lambda collection is read with exactly the same branch logic as signal.
    background_lambdas = [[] for _ in range(n)]
    background_det = {d:[[] for _ in range(n)] for d in DETECTORS}
    if background_file is not None:
        if not Path(background_file).is_file():
            print(f'[WARNING] Background file not found: {background_file}')
        else:
            progress_phase("Read background ROOT collections (large MC branches can be slow)")
            with uproot.open(background_file) as fb:
                tb = fb['events']
                nb = min(int(tb.num_entries), n)
                bg_name, bg_fields = collection(
                    tb, ['ReconstructedLambdas','ReconstructedFarForwardLambdas'], nb)
                bg_tmp = event_vectors(bg_fields, nb)
                # Do NOT load/convert the full background MCParticles collection.
                # Background source distributions use their own sampled ROOT reads.
                # Truth daughter matching (if relations exist) independently reads
                # the needed MC status/PDG and persisted relation branches.
                print('[FAST] Skipping exhaustive background MCParticles conversion', flush=True)
                background_lambdas[:nb] = bg_tmp
                for d, stem in DETECTORS.items():
                    _, fields = collection(tb,[stem],nb)
                    background_det[d][:nb] = event_vectors(fields,nb)
                print(f'[BACKGROUND] Lambda collection: {bg_name}; aligned events={nb}/{n}')

    if background_file is not None and Path(background_file).is_file() and RUN_FAST_BACKGROUND_DIAG:
        progress_phase("Sample background distributions")
        sampled_background_distributions(background_file, out, nb, BACKGROUND_DIAG_EVENTS)

    primary_store=defaultdict(list);reco_store=defaultdict(list);background_store=defaultdict(list)
    # Per-event true Lambda decay vertices; not an experimentally fitted vertex.
    truth_decay_vertices = [None] * n
    reco_event_flags = np.zeros(n, dtype=bool)
    background_event_flags = np.zeros(n, dtype=bool)
    det_store={d:{'neutron':defaultdict(list),'gamma':defaultdict(list)} for d in DETECTORS}
    counters=Counter(events=n); truth_present=[]; truth_n=[];truth_2g=[];reco_present=[]
    counts={d:{'n':[],'g':[]} for d in DETECTORS}
    candidates_rows=[]
    candidate_records=[]
    background_candidate_records=[]
    pi0_truth_store=defaultdict(list)
    pi0_reco_store=defaultdict(list)
    pi0_background_store=defaultdict(list)
    pi0_best_signal=[]
    pi0_best_background=[]
    pi0_pairs_signal=[]
    pi0_pairs_background=[]
    combined_counts={'n':[],'g':[]}
    progress_phase("Process reconstructed events")
    for i in tqdm(range(n), desc="Analyze events", unit="evt", dynamic_ncols=True):
        truth = _primary_mc_lambda(mc[i])
        truth_present.append(truth is not None)
        if truth is not None:
            counters['primary_truth_lambda']+=1
            fill(primary_store,{key:v for key,v in truth.items() if not key.startswith('_')})
            # EDM4hep endpoint is the *end of the MC trajectory*. It can be a
            # decay, a hadronic interaction in material, or a tracking boundary.
            # Do not claim decay truth without parent/daughter process relations.
            endpoint = np.array([truth.get('_ex',np.nan), truth.get('_ey',np.nan),
                                 truth.get('_ez',np.nan)], dtype=float)
            prod = np.array([truth.get('_vx',np.nan), truth.get('_vy',np.nan),
                             truth.get('_vz',np.nan)], dtype=float)
            if np.all(np.isfinite(endpoint)) and np.all(np.isfinite(prod)):
                displacement = (endpoint-prod) * VERTEX_MM_TO_M
                if np.linalg.norm(displacement) > 1.e-8:
                    ep = endpoint * VERTEX_MM_TO_M
                    pv = prod * VERTEX_MM_TO_M
                    truth_decay_vertices[i] = dict(
                        z_m=float(ep[2]),r_m=float(np.hypot(ep[0],ep[1])),
                        production_z_m=float(pv[2]),
                        production_r_m=float(np.hypot(pv[0],pv[1])),
                        flight_length_m=float(np.linalg.norm(displacement)))
        mc_pi0 = [k for k in mc[i] if k['_pdg']==111 and 0<=k['_status']<1000]
        if mc_pi0:
            chosen=max(mc_pi0,key=lambda k:k['E'])
            fill(pi0_truth_store,{key:v for key,v in chosen.items() if not key.startswith('_')})
        # MC particle counts below are event-level diagnostics, NOT daughter matching.
        truth_n.append(any(k['_pdg']==2112 and k['_status']<1000 for k in mc[i]))
        truth_2g.append(sum(k['_pdg']==22 and k['_status']<1000 for k in mc[i])>=2)
        for d in DETECTORS:
            ns=[k for k in det[d][i] if k['_pdg']==2112]
            gs=[k for k in det[d][i] if k['_pdg']==22]
            counts[d]['n'].append(len(ns));counts[d]['g'].append(len(gs))
            for typ,entries in [('neutron',ns),('gamma',gs)]:
                for k in entries:fill(det_store[d][typ],{key:v for key,v in k.items() if not key.startswith('_')})
        # Combined = UNION of ZDC-HCal, B0-ECal, LFHCAL for BOTH n and gamma.
        combined_counts['n'].append(sum(counts[d]['n'][-1] for d in DETECTORS))
        combined_counts['g'].append(sum(counts[d]['g'][-1] for d in DETECTORS))
        pairs = collect_pi0_pairs({d:det[d][i] for d in DETECTORS})
        pairs_bg = collect_pi0_pairs({d:background_det[d][i] for d in DETECTORS})
        best=select_best_pi0(pairs)
        best_bg=select_best_pi0(pairs_bg)
        pi0_best_signal.append(best)
        pi0_best_background.append(best_bg)
        pi0_pairs_signal.append(pairs)
        pi0_pairs_background.append(pairs_bg)
        if best is not None: fill(pi0_reco_store,{k:v for k,v in best.items() if k!='detectors'})
        if best_bg is not None: fill(pi0_background_store,{k:v for k,v in best_bg.items() if k!='detectors'})
        reco_present.append(bool(lambdas[i]))
        reco_event_flags[i] = bool(lambdas[i])
        background_event_flags[i] = bool(background_lambdas[i])
        for k in lambdas[i]:
            counters['lambda_candidates_raw']+=1
            fill(reco_store,{key:v for key,v in k.items() if not key.startswith('_')})
            candidates_rows.append([i,k['E'],k['mass'],k['minus_t'],k['xL'],k['theta_mrad'],k['p'],k['pz'],k['pt']])
            candidate_records.append({'event':i, **{key:val for key,val in k.items() if not key.startswith('_')}})
        for k in background_lambdas[i]:
            fill(background_store,{key:v for key,v in k.items() if not key.startswith('_')})
            background_candidate_records.append(
                {'event':i, **{key:val for key,val in k.items() if not key.startswith('_')}})

    progress_phase("Generate reconstruction, detector, and post-cut plots")
    # Vertex plots: the underlying TRUE MC decay position is shown for
    # (a) all Sullivan Lambdas and (b) events with reconstructed candidates.
    # Mass-constrained photon-pointing z hypothesis is separate from MC endpoint plots.
    vertex_dir = out / 'generator'
    vertex_raw_dir = out / 'reconstruction' / 'raw'
    for key, axis_label in [('z_m',r'$z_{\Lambda,endpoint}^{MC}$ [m]'),
                            ('r_m',r'$r_{\Lambda,endpoint}^{MC}$ [m]'),
                            ('production_z_m',r'$z_{\Lambda,production}^{MC}$ [m]'),
                            ('production_r_m',r'$r_{\Lambda,production}^{MC}$ [m]'),
                            ('flight_length_m',r'$L_{\Lambda,MC}$ [m]')]:
        all_mc = [v[key] for v in truth_decay_vertices if v is not None]
        signal_mc = [v[key] for i,v in enumerate(truth_decay_vertices)
                     if v is not None and reco_event_flags[i]]
        background_mc_vertices = []  # no same-index assumption across ROOT files
        save_1d(all_mc, vertex_dir/f'lambda_mc_endpoint_{key}.png', axis_label)
        save_1d(all_mc, vertex_raw_dir/f'lambda_mc_endpoint_{key}.png',axis_label,
                other=signal_mc,background=background_mc_vertices)
    vxy = [v for v in truth_decay_vertices if v is not None]
    if vxy:
        save_2d([v['z_m'] for v in vxy],[v['r_m'] for v in vxy],
                vertex_dir/'lambda_mc_endpoint_z_vs_r.png',
                r'$z_{\Lambda,decay}^{MC}$ [m]',r'$r_{\Lambda,decay}^{MC}$ [m]')
    else:
        print('[VERTEX WARNING] No valid MCParticles.endpoint for Lambda. '
              'No decay-vertex plot created. Check --dump-branches.')

    # Generator truth: independent 1D and 2D distributions.
    for key, vals in primary_store.items():
        save_1d(vals, out/'generator'/f'{key}.png', key, None)

    # Reconstructed Lambda: ALWAYS overlay the primary truth spectrum on the
    # same axes, using identical bins and original (unscaled) event counts.
    # We intentionally do not normalize the spectra: absolute reconstruction
    # losses remain visible. This is a comparison of inclusive populations,
    # NOT a truth-matched resolution estimate.
    for key in tqdm(sorted(set(reco_store) | set(primary_store) | set(background_store)), desc="Raw Lambda plots", unit="plot", leave=False):
        save_1d(primary_store.get(key, []),
                out/'reconstruction'/'raw'/f'{key}.png', key, None,
                other=reco_store.get(key, []),
                background=background_store.get(key, []),
                denominator=counters['primary_truth_lambda'],
                integral_label=r'$\Lambda$ candidates / truth $\Lambda$')

    # pi0 truth and best reconstructed pair distributions, same event-wise recipe
    # Store pi0 alongside Lambda in the existing reconstruction/raw and post-cut folders.
    pi0_dir=out/'reconstruction'
    for key in sorted(set(pi0_truth_store)|set(pi0_reco_store)|set(pi0_background_store)):
        save_1d(pi0_truth_store.get(key,[]),pi0_dir/'raw'/f'pi0_{key}.png',key,None,
                other=pi0_reco_store.get(key,[]),
                background=pi0_background_store.get(key,[]))
    # Fit the PRE-CUT distribution of exactly ONE best gamma-gamma pair per
    # event, using signal-only reconstruction. The same best-pair observable
    # is used below to apply the pi0 mass cut to signal and background.
    # CAUTION: closest-to-PDG best pairing sculpts the mass distribution;
    # the resulting fitted width is an operational cut parameter, NOT an
    # unbiased detector pi0 mass resolution.
    best_pair_masses=[p['mass'] for p in pi0_best_signal if p is not None]
    pi0_fit=(fit_pi0_mass(best_pair_masses,pi0_dir/'raw')
             if MPSIGMA is not None else None)
    if MPSIGMA is None: print('[CUTS] pi0 mass cut disabled; Gaussian fit not required.',flush=True)
    all_pair_masses=[pair['mass'] for pairs in pi0_pairs_signal for pair in pairs]
    save_1d(all_pair_masses, pi0_dir/'raw'/'pi0_all_gamma_pairs_mass.png',
            r'$m_{\gamma\gamma}$ [GeV]',None,
            other=None,
            background=[pair['mass'] for pairs in pi0_pairs_background for pair in pairs])
    pass  # No intermediate data export.
    pass  # No intermediate data export.

    # Legacy kinematic plots are retained as a comparison; definitive selections
    # and purity are recomputed per candidate after PODIO daughter associations.
    # Post-selection uses Lambda |t| and Lambda mass, plus event-level pi0 mass.

    # Fit the Lambda mass on raw candidates; retain only final selection plots.
    fit = fit_lambda_mass(candidate_records, pi0_dir / 'raw') if MLSIGMA is not None else None

    # Apply association-based ancestry matching to reconstructed Lambda daughters.
    # The old cross-file kinematic-pairing purity proxy is not used.
    lambda_per_event=Counter()
    for r in candidate_records:
        r['_lambda_index']=lambda_per_event[r['event']]
        lambda_per_event[r['event']]+=1
        r['_lambda_fit_pass']=(pass_t(r) and pass_xl(r) and pass_lambda_mass(r,fit))
        r['_all_cuts_pass']=pass_core(r,fit,pi0_fit,pi0_best_signal)
    lambda_bg_per_event=Counter()
    for r in background_candidate_records:
        r['_lambda_index']=lambda_bg_per_event[r['event']]
        lambda_bg_per_event[r['event']]+=1
        r['_lambda_fit_pass']=(pass_t(r) and pass_xl(r) and pass_lambda_mass(r,fit))
        r['_all_cuts_pass']=pass_core(r,fit,pi0_fit,pi0_best_background)
    progress_phase('PODIO association truth matching — signal')
    signal_truth,signal_summary=_association_truth(file,out,n,'signal')
    # Independent pion fit, based on the actual reconstructed Lambda photon daughters.
    # This replaces the event-wise closest-to-PDG pi0 pairing for CUT decisions.
    pi0_daughter_fit=(fit_pi0_mass([r['pi0_daughter_mass_GeV'] for r in signal_truth],
                                  None)
                       if MPSIGMA is not None else None)
    joined_sig,final_sig,_=unified_cut_study(signal_truth,candidate_records,out,'signal',fit,pi0_daughter_fit,counters['primary_truth_lambda'])
    final_bg=[]
    if background_file is not None and Path(background_file).is_file():
        progress_phase('PODIO association truth matching — background mixed')
        bkg_truth,bkg_summary=_association_truth(background_file,out,nb,'mixed')
        joined_bg,final_bg,_=unified_cut_study(bkg_truth,background_candidate_records,out,'mixed',fit,pi0_daughter_fit,counters['primary_truth_lambda'])
        # Correct ONLY the mixed purity bar chart; leave every other output unchanged.
        plot_pstar_cutflow(joined_sig, joined_bg, out, counters['primary_truth_lambda'])
    # Definitive post-cut plots reflect ALL cuts, not the old core-only selections.
    post_dir=out/'reconstruction'/'post-cut'
    final_sig_store=defaultdict(list);final_bg_store=defaultdict(list)
    for r in final_sig: fill(final_sig_store,{k:v for k,v in r.items() if k not in ('event','lambda_index','binary_class','detailed_category','z_lambda_method') and not k.startswith('pass_')})
    for r in final_bg: fill(final_bg_store,{k:v for k,v in r.items() if k not in ('event','lambda_index','binary_class','detailed_category','z_lambda_method') and not k.startswith('pass_')})
    for key in sorted(set(final_sig_store)|set(final_bg_store)|set(primary_store)):
        save_1d(primary_store.get(key,[]),post_dir/f'{key}.png',key,None,
                other=final_sig_store.get(key,[]),background=final_bg_store.get(key,[]),
                denominator=counters['primary_truth_lambda'])
    pass  # No intermediate data export.
    pass  # No intermediate data export.
    pass  # No intermediate data export.


    for store,folder in [(primary_store,'generator'),(reco_store,'reconstruction/raw')]:
        for a,b in [('E','theta_mrad'),('E','eta'),('E','pt'),('E','minus_t'),
                    ('p','pt'),('pz','pt'),('xL','minus_t')]:
            if a in store and b in store and len(store[a])==len(store[b]):
                save_2d(store[a],store[b],out/folder/f'{a}_vs_{b}.png',a,b,None)
    xb=np.asarray(xb,float);q2=np.asarray(q2,float)
    for d in DETECTORS:
        for typ in ('neutron','gamma'):
            store=det_store[d][typ]
            for key,vals in store.items():save_1d(vals,out/'detectors'/d/typ/f'{key}.png',key,None)
            for a,b in [('E','theta_mrad'),('E','pt'),('pz','pt')]:
                if a in store and b in store and len(store[a])==len(store[b]):
                    save_2d(store[a],store[b],out/'detectors'/d/typ/f'{a}_vs_{b}.png',a,b,None)
        for typ in ('n','g'):
            save_1d(counts[d][typ],out/'detectors'/d/f'{typ}_multiplicity.png','multiplicity',None,bins=15)
        for tag,selection,base in [
            ('neutron',np.asarray(counts[d]['n'])>0,truth_n),
            ('one_gamma',np.asarray(counts[d]['g'])>0,truth_2g),
            ('two_gamma',np.asarray(counts[d]['g'])>=2,truth_2g)]:
            save_eff2d(xb,q2,selection,np.asarray(base,bool),out/'detectors'/d/f'presence_{tag}_xb_q2.png',
                       title=f'{d}: candidate presence (not MC-matched)')
    # Combined candidate presence from ALL three calorimeters, irrespective
    # of which calorimeter contains a neutron or a photon.
    nn=np.asarray(combined_counts['n'])
    ng=np.asarray(combined_counts['g'])
    combined_dir=out/'detectors'/'combined'
    base_n=np.asarray(truth_n,bool)
    base_2g=np.asarray(truth_2g,bool)
    for tag,selection,base in [
        ('one_neutron',nn>=1,base_n),
        ('one_gamma',ng>=1,base_2g),
        ('two_gamma',ng>=2,base_2g),
        ('neutron_plus_one_gamma',(nn>=1)&(ng>=1),base_n&base_2g),
        ('neutron_plus_two_gamma',(nn>=1)&(ng>=2),base_n&base_2g),
        ('triple',(nn>=1)&(ng>=2),base_n&base_2g),
        ('pi0_best_pair',np.array([p is not None for p in pi0_best_signal]),base_2g),
        ('pi0_mass_window',np.array([pass_pi0(i, pi0_best_signal, pi0_fit) for i in range(n)]),base_2g),
        ('lambda_candidate',np.asarray(reco_present,bool),np.asarray(truth_present,bool))]:
        save_eff2d(xb,q2,selection,base,combined_dir/f'{tag}_xb_q2.png',
                   title=f'{tag} (event-level, not truth-matched)')
    for typ in ('n','g'):
        save_1d(combined_counts[typ],combined_dir/f'{typ}_multiplicity.png',
                f'{typ} multiplicity',None,bins=15)
    summary_combined={
        'definition':'union of ZDC_HCal, B0_ECal, LFHCAL; event-level candidates',
        'n_events':n,
        'one_neutron':int(np.sum(nn>=1)),
        'one_gamma':int(np.sum(ng>=1)),
        'two_gamma':int(np.sum(ng>=2)),
        'neutron_and_one_gamma':int(np.sum((nn>=1)&(ng>=1))),
        'neutron_and_two_gamma':int(np.sum((nn>=1)&(ng>=2))),
        'fraction_of_all_events_neutron_and_two_gamma_pct':float(100*np.mean((nn>=1)&(ng>=2))) if n else None,
        'warning':'These are not MC-parent-matched daughter detection efficiencies.'}
    combined_dir.mkdir(parents=True,exist_ok=True)
    pass  # No intermediate data export.
    (out/'reconstruction').mkdir(exist_ok=True)
    summary={'input':str(file),'reader':'uproot + awkward','counters':dict(counters),
        'cuts':{'TMAX':TMAX,'XL_MAX':XL_MAX,'MLSIGMA':MLSIGMA,'MPSIGMA':MPSIGMA},
        'warnings':['MC truth associations interpreted with dominant-cluster-contributor ancestry.',
                    'Event-level candidate presence is NOT truth-matched efficiency.',
                    'MC n/g event condition is NOT decay-parent matched.',
                    'Pi0 pair cut still uses closest-mass event-level pair; Lambda-daughter pi0 selection should be validated.',
                    'Truth-matched energy resolution or bias is not estimated here.']}
    pass  # No intermediate data export.
    print('[UPROOT] complete:',dict(counters))
    return counters

