import sys,json,collections; sys.path.insert(0,'.')
from connect import db
import networkx as nx
c=db.connect()
INC=db.dicts(c,'select A,B,KEY,TIER,MATCHED,CONFIDENCE from LIBRARY_META."CONNECT".CONNECT_EDGES_INC'); c.close()
E=json.load(open('scripts/scratch/g1.json'))['edges']
print("INC keys:",collections.Counter(r['KEY'] for r in INC).most_common(12))
print("INC tiers:",collections.Counter(r['TIER'] for r in INC))
GEO={'NAME@ZIP','GEO_IN','FIPS','ZIP'}
def run(label,rows):
    G=nx.Graph()
    for r in rows:
        if r['KEY'] in GEO: continue
        G.add_edge(r['A'],r['B'])
    cc=sorted(nx.connected_components(G),key=len,reverse=True); H=G.subgraph(cc[0]).copy()
    bt=nx.betweenness_centrality(H); dg=dict(H.degree())
    rb={n:i+1 for i,n in enumerate(sorted(bt,key=bt.get,reverse=True))}; rd={n:i+1 for i,n in enumerate(sorted(dg,key=dg.get,reverse=True))}
    print(f"\n== {label}: nodes {G.number_of_nodes()} pairs {G.number_of_edges()} comps {len(cc)} sizes {[len(x) for x in cc[:6]]}; largest comp {H.number_of_nodes()} nodes")
    for n in sorted(bt,key=bt.get,reverse=True)[:8]: print(f"  {n} | btw {bt[n]:.4f} b#{rb[n]} | deg {dg[n]} d#{rd[n]} | gap {rd[n]-rb[n]}")
    ap=[(n,sorted((len(x) for x in nx.connected_components(H.subgraph(set(H)-{n}))),reverse=True)[1:]) for n in nx.articulation_points(H)]
    print("  articulation:",sorted(ap,key=lambda x:-sum(x[1]))[:5])
run("EDGES_INC alone, entity keys",INC)
run("UNION EDGES + EDGES_INC, entity keys",E+INC)
new=[r for r in INC if (r['A']=='FED_SAM_EXCLUSIONS_FULL_R2' or r['B']=='FED_SAM_EXCLUSIONS_FULL_R2')]
print("\nSAM edges in INC:",len(new),collections.Counter(r['KEY'] for r in new))
