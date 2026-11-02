"""ROOT/EDM4eIC branch reading and reconstructed DIS kinematics.

Reconstructed selection does not use generator truth as a fallback.
"""
from __future__ import annotations
import numpy as np
import awkward as ak
import uproot
from tqdm.auto import tqdm
from config import BEAM_MOM, CHUNK, CUTS, ELECTRON_BEAM_ENERGY_GEV, ELECTRON_COLLECTION_CANDIDATES, ELECTRON_MASS_GEV, NEUTRON_MASS, PROTON_ENERGY, PROTON_MASS, SCATTERED_ELECTRON_COLLECTION
from physics import vec_from_four
from common.io import write_csv_rows

def writecsv(path, rows, fields=None):
    """Compute writecsv for the analysis."""
    columns = fields or (list(rows[0]) if rows else ['event', 'index'])
    return write_csv_rows(path, rows, columns)

def resolved(tree, stem, field):
    """Compute resolved for the analysis."""
    opts = [f'{stem}/{stem}.{field}', f'{stem}.{field}', f'{stem}/{field}']
    for o in opts:
        if o in tree:
            return o
    return None

def wanted(tree, stem, fields):
    """Compute wanted for the analysis."""
    return {k: resolved(tree, stem, k) for k in fields}

def getchunk(tree, names, start, stop):
    """Compute getchunk for the analysis."""
    chosen = list(dict.fromkeys((v for v in names.values() if v)))
    if not chosen:
        return {}
    return tree.arrays(chosen, entry_start=start, entry_stop=stop, library='ak', how=dict)

def rows_from_chunk(arr, names, offset, object_type, only_neutron=False):
    """Compute rows from chunk for the analysis."""
    if not all((names.get(k) for k in ('px', 'py', 'pz'))):
        return []
    n = len(arr[names['px']])
    result = []

    def get(k, i):
        """Compute get for the analysis."""
        name = names.get(k)
        return ak.to_list(arr[name][i]) if name else None
    for i in range(n):
        xx = get('px', i)
        yy = get('py', i)
        zz = get('pz', i)
        if not isinstance(xx, list):
            xx = [xx]
            yy = [yy]
            zz = [zz]
        ee = get('E', i)
        mm = get('mass', i)
        pdg = get('pdg', i)
        status = get('status', i)
        rz = get('rz', i)
        if not isinstance(ee, list):
            ee = [ee] * len(xx)
        if not isinstance(mm, list):
            mm = [mm] * len(xx)
        if not isinstance(pdg, list):
            pdg = [pdg] * len(xx)
        if not isinstance(status, list):
            status = [status] * len(xx)
        if not isinstance(rz, list):
            rz = [rz] * len(xx)
        for j in range(len(xx)):
            try:
                code = int(pdg[j]) if pdg[j] is not None else 0
                stat = int(status[j]) if status[j] is not None else -1
                if only_neutron and code != 2112:
                    continue
                if object_type == 'truth' and (not (code == 2112 and 0 <= stat < 1000)):
                    continue
                e = float(ee[j]) if ee[j] is not None else np.nan
                m = float(mm[j]) if mm[j] is not None else NEUTRON_MASS
                row = vec_from_four(e, float(xx[j]), float(yy[j]), float(zz[j]), m)
                if row is None:
                    continue
                row.update(event=offset + i, index=j, pdg=code, genstatus=stat)
                row['z_reference_m'] = float(rz[j]) * 0.001 if rz[j] is not None else np.nan
                result.append(row)
            except (ValueError, TypeError, IndexError):
                continue
    return result

def select_rows(path, nmax, collection, truth=False):
    """Select rows candidates."""
    fields = {'E': 'energy', 'mass': 'mass', 'px': 'momentum.x', 'py': 'momentum.y', 'pz': 'momentum.z', 'pdg': 'PDG', 'status': 'generatorStatus', 'rz': 'referencePoint.z' if not truth else 'endpoint.z'}
    with uproot.open(path) as f:
        t = f['events']
        n = min(t.num_entries, nmax) if nmax else t.num_entries
        names = {k: resolved(t, collection, v) for k, v in fields.items()}
        if not truth and (not names.get('pdg')):
            raise RuntimeError(f'{collection}: neutron PDG branch missing; cannot reliably select neutron candidates')
        if not all((names.get(k) for k in ('px', 'py', 'pz'))):
            raise RuntimeError(f'{collection}: no momentum branches; use --dump-branches')
        result = []
        for start in tqdm(range(0, n, CHUNK), desc=f'Read {collection}' + (' truth' if truth else ' reco'), unit='chunk', dynamic_ncols=True):
            stop = min(start + CHUNK, n)
            arr = getchunk(t, names, start, stop)
            result.extend(rows_from_chunk(arr, names, start, 'truth' if truth else 'reco', only_neutron=not truth))
    return (result, int(n))

def collection_ids(f):
    """Compute collection ids for the analysis."""
    try:
        p = 'events___CollectionTypeInfo/events___CollectionTypeInfo.'
        m = f['podio_metadata']
        ids = ak.to_list(ak.flatten(m[p + 'collectionID'].array(library='ak'), axis=None))
        names = ak.to_list(ak.flatten(m[p + 'name'].array(library='ak'), axis=None))
        return {str(n): int(k) for k, n in zip(ids, names)}
    except Exception as e:
        raise RuntimeError('Cannot read PODIO metadata for association matching') from e

def relation_fields(parent, rel):
    """Compute relation fields for the analysis."""
    return {'begin': f'{parent}/{parent}.{rel}_begin', 'end': f'{parent}/{parent}.{rel}_end', 'idx': f'_{parent}_{rel}/_{parent}_{rel}.index', 'cid': f'_{parent}_{rel}/_{parent}_{rel}.collectionID'}

def assoc_fields(coll):
    """Compute assoc fields for the analysis."""
    return {'w': f'{coll}/{coll}.weight', 'ri': f'_{coll}_rec/_{coll}_rec.index', 'rc': f'_{coll}_rec/_{coll}_rec.collectionID', 'si': f'_{coll}_sim/_{coll}_sim.index', 'sc': f'_{coll}_sim/_{coll}_sim.collectionID'}

def _event_scalar_values(tree, collection, field, n):
    """One DIS scalar per event (missing/multiple entries -> NaN)."""
    branch = resolved(tree, collection, field)
    if branch is None:
        return None
    a = tree[branch].array(entry_stop=n, library='ak')
    result = np.full(n, np.nan, dtype=float)
    for i, one in enumerate(ak.to_list(a)):
        if isinstance(one, list):
            if len(one) != 1:
                continue
            one = one[0]
        try:
            result[i] = float(one)
        except (TypeError, ValueError):
            pass
    return result

def attach_invariant_masses(path, n, rows, *, truth=False, label='signal'):
    """Compute event W and candidate MX without borrowing MC truth for reco cuts.

 W: Q2/x from appropriate event-level inclusive kinematics, or scattered
 electron four-vector. MX: (p+q-p_n)^2, only when a unique reconstructed
 scattered electron four-vector exists in a dedicated collection.
 """
    if not rows:
        return
    with uproot.open(path) as f:
        tree = f['events']
        n = min(n, int(tree.num_entries))
        coll = 'InclusiveKinematicsTruth' if truth else None
        if not truth:
            for name in ('InclusiveKinematicsElectron', 'InclusiveKinematicsESigma', 'InclusiveKinematicsDA', 'InclusiveKinematicsJB'):
                if resolved(tree, name, 'x') and resolved(tree, name, 'Q2'):
                    coll = name
                    break
        x = _event_scalar_values(tree, coll, 'x', n) if coll else None
        Q2 = _event_scalar_values(tree, coll, 'Q2', n) if coll else None
        event_W = np.full(n, np.nan)
        if x is not None and Q2 is not None:
            W2 = PROTON_MASS ** 2 + Q2 * (1.0 / np.where(x > 0, x, np.nan) - 1.0)
            valid = np.isfinite(W2) & (W2 >= 0) & (Q2 > 0)
            event_W[valid] = np.sqrt(W2[valid])
        event_q = {}
        if not truth:
            options = (SCATTERED_ELECTRON_COLLECTION,) if SCATTERED_ELECTRON_COLLECTION else ELECTRON_COLLECTION_CANDIDATES
            elcoll = None
            branches = None
            for name in options:
                if not name:
                    continue
                required = {k: resolved(tree, name, k) for k in ('momentum.x', 'momentum.y', 'momentum.z')}
                if all(required.values()):
                    elcoll = name
                    branches = required
                    break
            if elcoll:
                ebranch = resolved(tree, elcoll, 'energy')
                read = list(branches.values()) + ([ebranch] if ebranch else [])
                elec_p = np.sqrt(ELECTRON_BEAM_ENERGY_GEV ** 2 - ELECTRON_MASS_GEV ** 2)
                incoming = np.array([ELECTRON_BEAM_ENERGY_GEV, 0.0, 0.0, -elec_p])
                proton = np.array([PROTON_ENERGY, *BEAM_MOM])
                with tqdm(total=n, desc=f'Electron kinematics {label}', unit='event', dynamic_ncols=True, leave=False) as bar:
                    for start in range(0, n, CHUNK):
                        stop = min(start + CHUNK, n)
                        a = tree.arrays(read, entry_start=start, entry_stop=stop, library='ak', how=dict)
                        for k in range(stop - start):
                            vals = [ak.to_list(a[branches[field]][k]) for field in ('momentum.x', 'momentum.y', 'momentum.z')]
                            if any((not isinstance(v, list) or len(v) != 1 for v in vals)):
                                continue
                            px, py, pz = (float(v[0]) for v in vals)
                            if not np.all(np.isfinite([px, py, pz])):
                                continue
                            e = float(ak.to_list(a[ebranch][k])[0]) if ebranch and len(ak.to_list(a[ebranch][k])) == 1 else float(np.sqrt(px * px + py * py + pz * pz + ELECTRON_MASS_GEV ** 2))
                            q = incoming - np.array([e, px, py, pz])
                            event_q[start + k] = q
                            h = proton + q
                            w2 = h[0] ** 2 - np.dot(h[1:], h[1:])
                            event_W[start + k] = np.sqrt(w2) if w2 >= 0 else np.nan
                        bar.update(stop - start)
                print(f'[KINEMATICS {label}] Electron collection: {elcoll}; unambiguous event electrons: {len(event_q)}/{n}', flush=True)
            else:
                print(f'[KINEMATICS {label}] No dedicated scattered-electron four-vector collection found. MX unavailable (no MC-truth substitution). Set SCATTERED_ELECTRON_COLLECTION to your actual branch collection if present.', flush=True)
        proton = np.array([PROTON_ENERGY, *BEAM_MOM])
        w_count = mx_count = 0
        for r in rows:
            ev = int(r['event'])
            r['W'] = float(event_W[ev]) if 0 <= ev < n else np.nan
            w_count += np.isfinite(r['W'])
            q = event_q.get(ev)
            if q is not None:
                n4 = np.array([r['E'], r['px'], r['py'], r['pz']], dtype=float)
                miss = proton + q - n4
                m2 = miss[0] ** 2 - float(np.dot(miss[1:], miss[1:]))
                r['MX'] = float(np.sqrt(m2)) if np.isfinite(m2) and m2 >= 0 else np.nan
            mx_count += np.isfinite(r['MX'])
        print(f'[KINEMATICS {label}] W: {w_count}/{len(rows)} candidates; MX: {mx_count}/{len(rows)} candidates', flush=True)
        if any((c[0] == 'W' and (c[2] is not None or c[3] is not None) for c in CUTS)) and (not w_count) and (not truth):
            raise RuntimeError('W cut requested, but no reconstructed DIS/electron kinematics available; cannot apply a truth-based cut.')
        if any((c[0] == 'MX' and (c[2] is not None or c[3] is not None) for c in CUTS)) and (not mx_count) and (not truth):
            raise RuntimeError('MX cut requested, but no reconstructed scattered-electron four-vector available.')

def optional_truth_dis(path, nmax, out):
    """DIS x and Q2 from signal reco truth branch, event-presence tagging maps."""
    with uproot.open(path) as f:
        t = f['events']
        n = min(t.num_entries, nmax) if nmax else t.num_entries
        xx = resolved(t, 'InclusiveKinematicsTruth', 'x')
        qq = resolved(t, 'InclusiveKinematicsTruth', 'Q2')
        if not xx or not qq:
            return None
        xs = t[xx].array(entry_stop=n, library='ak')
        qs = t[qq].array(entry_stop=n, library='ak')

        def scalar(arr):
            """Compute scalar for the analysis."""
            if arr.ndim > 1:
                arr = ak.firsts(arr)
            return np.asarray(ak.to_numpy(ak.fill_none(arr, np.nan)), float)
        return (scalar(xs), scalar(qs))
