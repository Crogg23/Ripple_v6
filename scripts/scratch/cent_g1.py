import sys, json, collections; sys.path.insert(0,'.')
from connect import db
import networkx as nx
c=db.connect()
E=db.dicts(c,'select A,B,KEY,TIER,A_COL,B_COL,MATCHED,A_DISTINCT,B_DISTINCT,MATCH_RATE,CONFIDENCE from LIBRARY_META."CONNECT".CONNECT_EDGES')
# row counts for the landing tables (metadata only)
RC={r['TABLE_NAME']:r['ROW_COUNT'] for r in db.dicts(c,"select table_name,row_count from LIBRARY_RAW.information_schema.tables where table_schema='LANDING'")}
tabs=db.dicts(c,"select table_name,row_count from LIBRARY_META.information_schema.tables where table_schema='CONNECT' order by row_count desc")
c.close()
json.dump({'edges':E,'rc':RC,'connect_tabs':tabs},open('scripts/scratch/g1.json','w'),default=str)
print("CONNECT tables:"); [print(' ',t['TABLE_NAME'],t['ROW_COUNT']) for t in tabs]
def build(rows):
    G=nx.Graph()
    for r in rows:
        if G.has_edge(r['A'],r['B']): G[r['A']][r['B']]['keys'].add(r['KEY'])
        else: G.add_edge(r['A'],r['B'],keys={r['KEY']})
    return G
name_edges=[r for r in E if r['KEY']=='NAME@ZIP']
hard=[r for r in E if r['KEY']!='NAME@ZIP']
for label,rows in [('ALL',E),('HARD (no NAME@ZIP)',hard),('NAME@ZIP only',name_edges)]:
    G=build(rows); cc=sorted(nx.connected_components(G),key=len,reverse=True)
    print(f"\n== {label}: edge rows {len(rows)}  nodes {G.number_of_nodes()}  unique pairs {G.number_of_edges()}  components {len(cc)}  largest {len(cc[0])}  sizes {[len(x) for x in cc[:8]]}")
    # multi-key pairs = corroborated by 2+ keys
    multi=sum(1 for a,b,d in G.edges(data=True) if len(d['keys'])>1); print(f"   pairs with 2+ keys: {multi}")
# node overlap: how many hard nodes are only reachable via names
Ga=build(E); Gh=build(hard)
only_name=set(Ga.nodes)-set(Gh.nodes); print(f"\nnodes that exist ONLY via NAME@ZIP edges: {len(only_name)}")
# centrality on hard graph, largest component
H=Gh.subgraph(max(nx.connected_components(Gh),key=len)).copy()
bt=nx.betweenness_centrality(H,normalized=True); dg=dict(H.degree())
comms=list(nx.community.greedy_modularity_communities(H)); cid={n:i for i,cm in enumerate(comms) for n in cm}
def cname(i):
    pre=collections.Counter('_'.join(n.split('_')[:2]) for n in comms[i]); return f"C{i}:{pre.most_common(1)[0][0]}({len(comms[i])})"
print("\ncommunities:"); [print(' ',cname(i),sorted(comms[i])[:6]) for i in range(len(comms))]
rb={n:i+1 for i,n in enumerate(sorted(bt,key=bt.get,reverse=True))}; rd={n:i+1 for i,n in enumerate(sorted(dg,key=dg.get,reverse=True))}
print(f"\nHARD largest component: nodes {H.number_of_nodes()} edges {H.number_of_edges()}")
print("\nTOP 25 betweenness (hard graph): node | btw | deg | deg_rank | btw_rank | gap | rows | keys | neighbor communities")
for n in sorted(bt,key=bt.get,reverse=True)[:25]:
    ks=collections.Counter(k for _,_,d in H.edges(n,data=True) for k in d['keys'])
    nc=collections.Counter(cname(cid[m]) for m in H[n])
    print(f"{n} | {bt[n]:.4f} | {dg[n]} | d#{rd[n]} | b#{rb[n]} | gap {rd[n]-rb[n]} | rows {RC.get(n)} | {dict(ks)} | {dict(nc)}")
print("\nQUIET MIDDLEMEN: btw rank <= 40 and degree rank - btw rank >= 15")
for n in sorted(bt,key=bt.get,reverse=True)[:40]:
    if rd[n]-rb[n]>=15:
        ks=collections.Counter(k for _,_,d in H.edges(n,data=True) for k in d['keys']); nc=collections.Counter(cname(cid[m]) for m in H[n])
        print(f"{n} | btw {bt[n]:.4f} b#{rb[n]} | deg {dg[n]} d#{rd[n]} | rows {RC.get(n)} | {dict(ks)} | {dict(nc)}")
# articulation points: removing one disconnects the graph - the purest middleman test
ap=list(nx.articulation_points(H)); print(f"\narticulation points ({len(ap)}):")
for n in sorted(ap,key=lambda x:bt[x],reverse=True):
    H2=H.copy(); H2.remove_node(n); cs=sorted((len(x) for x in nx.connected_components(H2)),reverse=True)
    print(f"  {n} deg {dg[n]} btw {bt[n]:.4f} -> splits off {cs[1:]}")
# same on ALL graph for comparison (top 10)
A=Ga.subgraph(max(nx.connected_components(Ga),key=len)).copy(); bta=nx.betweenness_centrality(A); dga=dict(A.degree())
print(f"\nALL graph largest comp {A.number_of_nodes()} nodes; top 10 betweenness:")
for n in sorted(bta,key=bta.get,reverse=True)[:10]: print(f"  {n} btw {bta[n]:.4f} deg {dga[n]}")
json.dump({'bt':bt,'dg':dg,'comm':{n:cid[n] for n in H},'cnames':[cname(i) for i in range(len(comms))],'ap':ap},open('scripts/scratch/g1_out.json','w'))
