"""ZDC cluster–MC association and Sullivan/background origin classification.

Origin classification is not a particle-level neutron truth match.
"""
from __future__ import annotations
from collections import defaultdict, Counter
import numpy as np
import awkward as ak
import uproot
from tqdm.auto import tqdm
from config import ASSOC_COLLECTION, CHUNK, CLUSTER_COLLECTION, NEUTRAL_COLLECTION, SIGNAL_SOURCE_MIN_FRACTION, SOURCES
from root_io import collection_ids, relation_fields, assoc_fields, getchunk

def matching(path, nmax, reco_rows, sample, out):
    """Fast source-tag classification from persisted ZDC cluster--MC links.

 Weighted contributors are classified immediately if their generatorStatus has
 a source tag 2000..7000. For an untagged contributor, use its MC parent
 chain ONLY if needed, caching results per event. No full MC genealogy walk.
 A source-0 outcome is generator-origin attribution, NOT truth neutron matching.
 """
    default = {'category': 'unclassified', 'source_fraction_signal': np.nan, 'dominant_source': -1, 'truth_neutron_fraction': np.nan, 'association_weight_sum': 0.0, 'n_mc_contributors': 0, 'dominant_mc_index': -1}
    cache = {}
    index_by_event = defaultdict(set)
    for r in reco_rows:
        index_by_event[int(r['event'])].add(int(r['index']))
    if not index_by_event:
        return reco_rows
    with uproot.open(path) as f:
        tree = f['events']
        ids = collection_ids(f)
        for needed in (NEUTRAL_COLLECTION, CLUSTER_COLLECTION, ASSOC_COLLECTION, 'MCParticles'):
            if needed not in ids:
                raise RuntimeError(f'Missing collection metadata: {needed}')
        n = min(int(tree.num_entries), nmax) if nmax else int(tree.num_entries)
        rel = relation_fields(NEUTRAL_COLLECTION, 'clusters')
        assoc = assoc_fields(ASSOC_COLLECTION)
        parents = relation_fields('MCParticles', 'parents')
        essential = {**{'r_' + k: v for k, v in rel.items()}, **{'a_' + k: v for k, v in assoc.items()}, 'pdg': 'MCParticles/MCParticles.PDG', 'status': 'MCParticles/MCParticles.generatorStatus'}
        missing = [k for k, v in essential.items() if v not in tree]
        if missing:
            raise RuntimeError(f'Missing persisted ZDC association branches: {missing}')
        optional = {'energy': f'{CLUSTER_COLLECTION}/{CLUSTER_COLLECTION}.energy'}
        if all((v in tree for v in parents.values())):
            optional.update({'p_' + k: v for k, v in parents.items()})
        else:
            print('[SOURCE WARNING] MC parent relations unavailable; untagged particles may be unclassified', flush=True)
        used = {**essential, **{k: v for k, v in optional.items() if v in tree}}
        selected_chunks = sorted({ev // CHUNK for ev in index_by_event if ev < n})
        stats = Counter()
        for chunk_id in tqdm(selected_chunks, desc=f'ZDC source tags {sample}', unit='chunk', dynamic_ncols=True):
            start = chunk_id * CHUNK
            stop = min(start + CHUNK, n)
            chunk = getchunk(tree, used, start, stop)
            for ev in range(stop - start):
                event = start + ev
                if event not in index_by_event:
                    continue

                def value(k):
                    """Compute value for the analysis."""
                    return ak.to_list(chunk[used[k]][ev])
                pdg = value('pdg')
                status = value('status')
                nmc = len(status)

                def refs(prefix):
                    """Compute refs for the analysis."""
                    begin = value(prefix + 'begin')
                    end = value(prefix + 'end')
                    idx = value(prefix + 'idx')
                    cid = value(prefix + 'cid')
                    return [list(zip(cid[int(i):int(j)], idx[int(i):int(j)])) for i, j in zip(begin, end)]
                daughters = refs('r_')
                contrib = defaultdict(lambda: defaultdict(float))
                energies = value('energy') if 'energy' in used else None
                for w, ri, ci, si, sci in zip(value('a_w'), value('a_ri'), value('a_rc'), value('a_si'), value('a_sc')):
                    ri = int(ri)
                    si = int(si)
                    if int(ci) != ids[CLUSTER_COLLECTION] or int(sci) != ids['MCParticles'] or (not 0 <= si < nmc):
                        continue
                    if not np.isfinite(w) or w <= 0:
                        continue
                    energy = energies[ri] if energies is not None and 0 <= ri < len(energies) else 1.0
                    if np.isfinite(energy) and energy > 0:
                        contrib[ri][si] += float(w * energy)
                mcparents = refs('p_') if 'p_begin' in used else []
                origin_cache = {}

                def classify(j):
                    """Compute classify for the analysis."""
                    if j in origin_cache:
                        return origin_cache[j]
                    if not 0 <= j < nmc:
                        return -1
                    st = int(status[j])
                    block = st // 1000 * 1000 if st >= 0 else -1
                    if block in SOURCES and block != 0:
                        origin_cache[j] = block
                        stats['direct_background'] += 1
                        return block
                    if block != 0:
                        origin_cache[j] = -1
                        return -1
                    if not mcparents or j >= len(mcparents) or (not mcparents[j]):
                        origin_cache[j] = 0
                        stats['direct_signal_root'] += 1
                        return 0
                    seen = set()
                    todo = [j]
                    tags = set()
                    found_root = False
                    while todo:
                        k = todo.pop()
                        if k in seen or not 0 <= k < nmc:
                            continue
                        seen.add(k)
                        sk = int(status[k])
                        bk = sk // 1000 * 1000 if sk >= 0 else -1
                        if bk in SOURCES and bk != 0:
                            tags.add(bk)
                            continue
                        linked = [int(idx) for cid, idx in (mcparents[k] if k < len(mcparents) else []) if int(cid) == ids['MCParticles'] and 0 <= int(idx) < nmc]
                        if not linked and 0 <= sk < 1000:
                            found_root = True
                        todo.extend(linked)
                    result = next(iter(tags)) if len(tags) == 1 else -2 if len(tags) > 1 else 0 if found_root else -1
                    origin_cache[j] = result
                    stats['fallback_parent_search'] += 1
                    return result
                for ni in index_by_event[event]:
                    if ni >= len(daughters):
                        continue
                    energy_by_mc = defaultdict(float)
                    for cid, idx in daughters[ni]:
                        if int(cid) != ids[CLUSTER_COLLECTION]:
                            continue
                        for j, w in contrib.get(int(idx), {}).items():
                            energy_by_mc[j] += w
                    total = sum(energy_by_mc.values())
                    if total <= 0:
                        cache[event, ni] = default.copy()
                        continue
                    src_weights = defaultdict(float)
                    for j, w in energy_by_mc.items():
                        src_weights[classify(j)] += w
                    dominant = max(src_weights, key=src_weights.get)
                    sigfrac = src_weights.get(0, 0.0) / total
                    category = 'signal' if dominant == 0 and sigfrac >= SIGNAL_SOURCE_MIN_FRACTION else 'unclassified' if dominant in (-1, -2) else 'combinatorial'
                    cache[event, ni] = {'category': category, 'source_fraction_signal': sigfrac, 'dominant_source': dominant, 'association_weight_sum': total, 'truth_neutron_fraction': np.nan, 'n_mc_contributors': len(energy_by_mc), 'dominant_mc_index': max(energy_by_mc, key=energy_by_mc.get)}
    for r in reco_rows:
        r.update(cache.get((r['event'], r['index']), default))
    print(f'[SOURCE {sample}]', dict(Counter((r['category'] for r in reco_rows))), 'classification diagnostics:', dict(stats), flush=True)
    return reco_rows
