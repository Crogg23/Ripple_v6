"""Graph 2: entity grain from ENTITY_XREF. GATED - scans 2.67M rows. Run only after 'go'."""
import sys, json, collections, random; sys.path.insert(0,'.')
from connect import db
import networkx as nx
X='LIBRARY_META."CONNECT".ENTITY_XREF'
c=db.connect()
# 1. real per-value fanout (the FANOUT column is a per-source constant, not per value)
fan=db.dicts(c,f"""with p as (select distinct KEY_A,VALUE_A,KEY_B,VALUE_B from {X})
select side,key,val,n from (
 select 'A' side, KEY_A key, VALUE_A val, count(*) n from p group by 1,2,3
 union all select 'B', KEY_B, VALUE_B, count(*) from p group by 1,2,3) where n>=50 order by n desc""")
print("values with real fanout >= 50:"); [print(' ',r) for r in fan[:40]]
junk={(r['KEY'],r['VAL']) for r in fan if r['N']>=500 or (r['VAL'] or '').strip('0 ')=='' or (r['VAL'] or '').upper() in ('N/A','NA','NONE','UNKNOWN','NULL')}
print("dropping as junk hubs:",sorted(junk))
# 2. pull the distinct pair list
P=db.rows(c,f"select distinct KEY_A,VALUE_A,KEY_B,VALUE_B from {X}")
print("distinct pairs:",len(P))
c.close()
G=nx.Graph()
for ka,va,kb,vb in P:
    if (ka,va) in junk or (kb,vb) in junk: continue
    G.add_edge(f"{ka}:{va}",f"{kb}:{vb}")
cc=sorted(nx.connected_components(G),key=len,reverse=True)
print(f"nodes {G.number_of_nodes()} edges {G.number_of_edges()} components {len(cc)} largest {len(cc[0])} sizes {[len(x) for x in cc[:10]]}")
# key-type families per component
fam=collections.Counter(frozenset(n.split(':')[0] for n in comp) for comp in cc); print("component key families:",fam.most_common(10))
out={}
for i,comp in enumerate(cc[:6]):
    H=G.subgraph(comp).copy(); dg=dict(H.degree())
    k=min(300,H.number_of_nodes()); random.seed(7)
    bt=nx.betweenness_centrality(H,k=k if H.number_of_nodes()>3000 else None,normalized=True,seed=7)
    rb={n:j+1 for j,n in enumerate(sorted(bt,key=bt.get,reverse=True))}; rd={n:j+1 for j,n in enumerate(sorted(dg,key=dg.get,reverse=True))}
    print(f"\n== component {i}: {H.number_of_nodes()} nodes {H.number_of_edges()} edges, k={k if H.number_of_nodes()>3000 else 'exact'}")
    print("top 15 betweenness | deg | deg rank | btw rank | gap")
    top=sorted(bt,key=bt.get,reverse=True)[:60]
    for n in top[:15]: print(f"  {n} | {bt[n]:.5f} | {dg[n]} | d#{rd[n]} | b#{rb[n]} | gap {rd[n]-rb[n]}")
    print("quiet: btw top 60, degree <= 5:")
    for n in top:
        if dg[n]<=5: print(f"  {n} | {bt[n]:.5f} b#{rb[n]} | deg {dg[n]} d#{rd[n]}")
    out[i]={'nodes':H.number_of_nodes(),'edges':H.number_of_edges(),'k':k,'top':[(n,bt[n],dg[n],rd[n],rb[n]) for n in top]}
json.dump(out,open('scripts/scratch/g2_out.json','w'))
