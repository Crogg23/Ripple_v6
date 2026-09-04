"""Detached-subtree per top physician (child side only), name checks, Blank hospital composition."""
import sys, json
sys.path.insert(0, '.')
from connect import db
import networkx as nx

c = db.connect()
P = db.rows(c, """select distinct VALUE_A, VALUE_B from LIBRARY_META."CONNECT".ENTITY_XREF
                  where KEY_A='CCN' and KEY_B='NPI'""")
G = nx.Graph()
for va, vb in P:
    if (va or '').strip('0 ') == '' or (vb or '').strip('0 ') == '':
        continue
    G.add_edge(f"CCN:{va}", f"NPI:{vb}")
H = G.subgraph(max(nx.connected_components(G), key=len)).copy()
blocks = [frozenset(b) for b in nx.biconnected_components(H)]
ap = set(nx.articulation_points(H))
T = nx.Graph()
for i, b in enumerate(blocks):
    T.add_node(('B', i))
    for v in b:
        if v in ap:
            T.add_edge(('B', i), ('A', v))
root = ('B', max(range(len(blocks)), key=lambda i: len(blocks[i])))
parent = {root: None}; order = [root]; stack = [root]
while stack:
    u = stack.pop()
    for w in T[u]:
        if w not in parent:
            parent[w] = u; order.append(w); stack.append(w)

def detached(a):
    """Nodes on the child side of articulation point a in the block-cut tree rooted at the giant block."""
    out = set(); st = [w for w in T[('A', a)] if parent.get(w) == ('A', a)]
    while st:
        u = st.pop()
        if u[0] == 'B':
            out |= set(blocks[u[1]]) - {a}
        st += [w for w in T[u] if parent.get(w) == u]
    return out

top = json.load(open('scripts/scratch/g2d_out.json'))['best_npi'][:8]
res = {}
for a, dgr, cutn in top:
    d = detached(a)
    fac = sorted(x for x in d if x.startswith('CCN:'))
    docs = sum(1 for x in d if x.startswith('NPI:'))
    res[a] = {'deg': dgr, 'cut': cutn, 'detached_total': len(d), 'detached_facilities': fac,
              'detached_physicians': docs, 'parent_side': sorted(set(H[a]) - set(fac))}
    print(f"\n{a} deg {dgr} cut {cutn} detached {len(d)} = {len(fac)} facilities + {docs} physicians; parent side: {res[a]['parent_side']}")
    for f in fac:
        print(f"   child {f} deg {H.degree(f)}")

blank = 'CCN:113300'
nb = set(H[blank]); multi = [n for n in nb if H.degree(n) > 1]
print(f"\nBlank neighbors {len(nb)}; with >1 affiliation: {len(multi)} -> {[(n, sorted(H[n])) for n in multi]}")

ids = [a.split(':')[1] for a, _, _ in top]
q = f"""select KEY_VALUE, count(distinct CANONICAL_NAME), count(distinct CANONICAL_ADDR),
               min(CANONICAL_NAME), max(CANONICAL_NAME), min(CANONICAL_ADDR), max(CANONICAL_ADDR), max(NAME_SOURCE)
        from LIBRARY_META."CONNECT".ENTITY_GOLDEN where KEY_TYPE='NPI' and KEY_VALUE in ({','.join(repr(x) for x in ids)}) group by 1"""
print("\nname uniqueness per NPI:")
rows = db.rows(c, q)
for r in rows: print("  ", r)
q2 = """select NPI, PROVIDER_LAST_NAME_LEGAL_NAME, PROVIDER_FIRST_NAME, PROVIDER_CREDENTIAL_TEXT,
               PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME,
               HEALTHCARE_PROVIDER_TAXONOMY_CODE_1
        from LIBRARY_RAW.LANDING.FED_CMS_NPPES where NPI in ('1417615519','1871090175')"""
print("\nNPPES rows for the two degree-2 bridges:")
try:
    for r in db.rows(c, q2): print("  ", r)
except Exception as e:
    print("NPPES lookup failed:", str(e)[:200])
c.close()
json.dump({'res': res, 'blank': {'neighbors': len(nb), 'multi': [(n, sorted(H[n])) for n in multi]},
           'names': [list(map(str, r)) for r in rows]}, open('scripts/scratch/g2e_out.json', 'w'))
print("DONE")
