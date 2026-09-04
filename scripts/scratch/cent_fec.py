"""FEC family, clean: no size cut, exact betweenness, gap, mechanism with a discriminating control.
Also every LEI star sized and named."""
import sys, json, statistics
sys.path.insert(0, '.')
from connect import db
import networkx as nx

c = db.connect()
P = db.rows(c, """select distinct KEY_A, VALUE_A, KEY_B, VALUE_B from LIBRARY_META."CONNECT".ENTITY_XREF
                  where KEY_A in ('FEC_CAND_ID', 'FRS_ID')""")
G = nx.Graph(); L = nx.Graph()
for ka, va, kb, vb in P:
    if (va or '').strip('0 ') == '' or (vb or '').strip('0 ') == '':
        continue
    (G if ka == 'FEC_CAND_ID' else L).add_edge(f"{ka}:{va}", f"{kb}:{vb}")

# LEI stars
stars = sorted(nx.connected_components(L), key=len, reverse=True)
lei_stars = [(next(n for n in s if n.startswith('LEI:')), len(s) - 1) for s in stars[:12]]
multi = sum(1 for n in L if n.startswith('FRS_ID:') and L.degree(n) > 1)
print("LEI graph nodes", L.number_of_nodes(), "components", len(stars), "FRS nodes with >1 LEI:", multi, "top stars:", lei_stars, flush=True)

# FEC, exact
cc = sorted(nx.connected_components(G), key=len, reverse=True)
H = G.subgraph(cc[0]).copy()
print("FEC graph nodes", G.number_of_nodes(), "edges", G.number_of_edges(), "largest", H.number_of_nodes(), flush=True)
bt = nx.betweenness_centrality(H, normalized=True)
dg = dict(H.degree())
rb = {n: i + 1 for i, n in enumerate(sorted(bt, key=bt.get, reverse=True))}
rd = {n: i + 1 for i, n in enumerate(sorted(dg, key=dg.get, reverse=True))}
top = sorted(bt, key=bt.get, reverse=True)[:40]
canddeg = {n: dg[n] for n in H if n.startswith('FEC_CAND_ID:')}

def med(cm): return statistics.median(canddeg[x] for x in H[cm])
def le3(cm): return sum(1 for x in H[cm] if canddeg[x] <= 3)

print("\nTOP 20 exact betweenness:")
for n in top[:20]:
    extra = f" | med cand deg {med(n)} | cands<=3 {le3(n)}" if n.startswith('FEC_CMTE') else ""
    print(f"  {n} | btw {bt[n]:.5f} b#{rb[n]} | deg {dg[n]} d#{rd[n]} | gap {rd[n]-rb[n]}" + extra)

# control: committees in degree band 50-120 NOT in betweenness top 100
band = [n for n in H if n.startswith('FEC_CMTE') and 50 <= dg[n] <= 120]
topset = set(sorted(bt, key=bt.get, reverse=True)[:100])
inn = [n for n in band if n in topset]; out = [n for n in band if n not in topset]
print(f"\ncontrol: committees deg 50-120: {len(band)}; in btw top100: {len(inn)}; not: {len(out)}")
if inn:
    print(f"  median-of-median cand degree: in-top {statistics.median(med(n) for n in inn)} | not-top {statistics.median(med(n) for n in out)}")
    print(f"  mean cands<=3: in-top {statistics.mean(le3(n) for n in inn):.1f} | not-top {statistics.mean(le3(n) for n in out):.1f}")
else:
    print(f"  no band committee in top100. not-top median-of-median {statistics.median(med(n) for n in out)}, mean cands<=3 {statistics.mean(le3(n) for n in out):.1f}")

# names
cm = [n.split(':')[1] for n in top if n.startswith('FEC_CMTE')]
ca = [n.split(':')[1] for n in top if n.startswith('FEC_CAND')]
names = {}
for r in db.rows(c, f"""select CMTE_ID, max(CMTE_NM), max(CMTE_TP), max(IS_AMBIGUOUS::int)
                        from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM
                        where CMTE_ID in ({','.join(repr(x) for x in cm)}) group by 1"""):
    names['FEC_CMTE_ID:' + r[0]] = list(r[1:])
for r in db.rows(c, f"""select C1, max(C2), max(C3), max(C6) from LIBRARY_RAW.LANDING.FED_FEC_CANDIDATES
                        where C1 in ({','.join(repr(x) for x in ca)}) group by 1"""):
    names['FEC_CAND_ID:' + r[0]] = list(r[1:])
leis = [l.split(':')[1] for l, _ in lei_stars]
for r in db.rows(c, f"""select KEY_VALUE, max(CANONICAL_NAME) from LIBRARY_META."CONNECT".ENTITY_GOLDEN
                        where KEY_TYPE='LEI' and KEY_VALUE in ({','.join(repr(x) for x in leis)}) group by 1"""):
    names['LEI:' + r[0]] = r[1]
c.close()
print("\nnamed top 20:")
for n in top[:20]: print(f"  {n} {names.get(n)}")
print("\nLEI stars named:")
for l, k in lei_stars: print(f"  {l} {names.get(l)} facilities {k}")
json.dump({'lei_stars': lei_stars, 'frs_multi': multi, 'fec': [H.number_of_nodes(), H.number_of_edges()],
           'top': [(n, bt[n], dg[n], rd[n], rb[n], med(n) if n.startswith('FEC_CMTE') else None, le3(n) if n.startswith('FEC_CMTE') else None) for n in top],
           'control': {'band': len(band), 'in': len(inn), 'out': len(out), 'in_meds': [med(n) for n in inn], 'out_meds': [med(n) for n in out]},
           'names': names}, open('scripts/scratch/fec_out.json', 'w'))
print("DONE")
