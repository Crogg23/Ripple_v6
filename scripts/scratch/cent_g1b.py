import json,collections,networkx as nx
D=json.load(open('scripts/scratch/g1.json')); E=D['edges']; RC=D['rc']
GEO={'NAME@ZIP','GEO_IN','FIPS','ZIP'}
rows=[r for r in E if r['KEY'] not in GEO]
G=nx.Graph()
for r in rows:
    if G.has_edge(r['A'],r['B']): G[r['A']][r['B']]['keys'].add(r['KEY'])
    else: G.add_edge(r['A'],r['B'],keys={r['KEY']})
cc=sorted(nx.connected_components(G),key=len,reverse=True)
print(f"edge rows {len(rows)} nodes {G.number_of_nodes()} pairs {G.number_of_edges()} components {len(cc)} sizes {[len(x) for x in cc[:10]]}")
for i,comp in enumerate(cc[:6]):
    pre=collections.Counter('_'.join(n.split('_')[:2]) for n in comp); print(f"  comp{i} ({len(comp)}): {pre.most_common(4)}")
H=G.subgraph(cc[0]).copy(); bt=nx.betweenness_centrality(H); dg=dict(H.degree())
rb={n:i+1 for i,n in enumerate(sorted(bt,key=bt.get,reverse=True))}; rd={n:i+1 for i,n in enumerate(sorted(dg,key=dg.get,reverse=True))}
comms=list(nx.community.greedy_modularity_communities(H)); cid={n:i for i,cm in enumerate(comms) for n in cm}
def cname(i):
    pre=collections.Counter('_'.join(n.split('_')[:2]) for n in comms[i]); return f"C{i}:{pre.most_common(1)[0][0]}({len(comms[i])})"
print("communities:",[cname(i) for i in range(len(comms))])
print("\nTOP 15 betweenness, entity keys only:")
for n in sorted(bt,key=bt.get,reverse=True)[:15]:
    ks=collections.Counter(k for _,_,d in H.edges(n,data=True) for k in d['keys']); nc=collections.Counter(cname(cid[m]) for m in H[n])
    print(f"{n} | btw {bt[n]:.4f} b#{rb[n]} | deg {dg[n]} d#{rd[n]} | gap {rd[n]-rb[n]} | rows {RC.get(n)} | {dict(ks)} | {dict(nc)}")
ap=list(nx.articulation_points(H)); print(f"\narticulation points ({len(ap)}):")
for n in sorted(ap,key=lambda x:bt[x],reverse=True):
    H2=H.copy(); H2.remove_node(n); cs=sorted((len(x) for x in nx.connected_components(H2)),reverse=True); print(f"  {n} deg {dg[n]} btw {bt[n]:.4f} -> splits off {cs[1:]}")
# who else could bridge health<->corporate if SAM vanished? any table with both NPI-ish and EIN/UEI-ish keys
keys_by_node=collections.defaultdict(set)
for r in rows: keys_by_node[r['A']].add(r['KEY']); keys_by_node[r['B']].add(r['KEY'])
health={'NPI','CCN','CCN~NPI'}; corp={'EIN','UEI','EIN~UEI','CIK','CIK~EIN','LEI','DUNS','DUNS~UEI'}
print("\nnodes carrying BOTH a health key and a corporate key:")
for n,ks in keys_by_node.items():
    if ks&health and ks&corp: print(f"  {n}: {sorted(ks)}")
