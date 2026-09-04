"""Block-cut tree: nodes cut off by each articulation point, one pass. Then names."""
import sys,json,collections; sys.path.insert(0,'.')
from connect import db
import networkx as nx
sys.setrecursionlimit(1000000)
c=db.connect()
P=db.rows(c,'select distinct VALUE_A,VALUE_B from LIBRARY_META."CONNECT".ENTITY_XREF where KEY_A=\'CCN\' and KEY_B=\'NPI\'')
G=nx.Graph()
for va,vb in P:
    if (va or '').strip('0 ')=='' or (vb or '').strip('0 ')=='': continue
    G.add_edge(f"CCN:{va}",f"NPI:{vb}")
cc=sorted(nx.connected_components(G),key=len,reverse=True); H=G.subgraph(cc[0]).copy()
print("graph nodes",G.number_of_nodes(),"edges",G.number_of_edges(),"largest",H.number_of_nodes(),flush=True)
blocks=[frozenset(b) for b in nx.biconnected_components(H)]; ap=set(nx.articulation_points(H))
print("blocks",len(blocks),"articulation points",len(ap),"NPI aps",sum(1 for a in ap if a.startswith('NPI:')),flush=True)
# block-cut tree
T=nx.Graph()
for i,b in enumerate(blocks):
    T.add_node(('B',i))
    for v in b:
        if v in ap: T.add_edge(('B',i),('A',v))
root=('B',max(range(len(blocks)),key=lambda i:len(blocks[i])))
# iterative post-order to get subtree node counts: size(B entered from parent AP) = |B|-1 + sum children; size(A) = sum children block sizes
parent={root:None}; order=[root]; stack=[root]
while stack:
    u=stack.pop()
    for w in T[u]:
        if w not in parent: parent[w]=u; order.append(w); stack.append(w)
size={}
for u in reversed(order):
    kids=[w for w in T[u] if parent.get(w)==u]
    if u[0]=='B': size[u]=len(blocks[u[1]])-(1 if parent[u] is not None else 0)+sum(size[w] for w in kids)
    else: size[u]=sum(size[w] for w in kids)
cut={a:size[('A',a)] for a in ap}   # nodes detached when a is removed
best_npi=sorted(((a,H.degree(a),cut[a]) for a in ap if a.startswith('NPI:')),key=lambda x:-x[2])[:25]
best_ccn=sorted(((a,H.degree(a),cut[a]) for a in ap if a.startswith('CCN:')),key=lambda x:-x[2])[:15]
print("\nNPI articulation points by nodes cut off:"); [print("  ",b) for b in best_npi[:15]]
print("\nCCN articulation points by nodes cut off:"); [print("  ",b) for b in best_ccn[:10]]
D=json.load(open('scripts/scratch/g2b_out.json')); c0=D['comp0']
sampled_npi=[n for n,*_ in c0['npi_top'][:12]]
print("\nsampled-betweenness NPIs, are they articulation points?")
for n in sampled_npi: print(f"  {n} deg {H.degree(n) if n in H else None} ap {n in ap} cut {cut.get(n)}")
quiet_ccn=[n for n,bt,dg,rd,rb in c0['top'] if rd-rb>=40][:10]
want=set(sampled_npi+quiet_ccn+[b[0] for b in best_npi[:12]]+[b[0] for b in best_ccn[:10]]+[f"CCN:{v}" for k,v in D['junk']])
for a,_,_ in best_npi[:8]: want|=set(H[a])
vals=collections.defaultdict(list)
for w in want: k,v=w.split(':',1); vals[k].append(v)
names={}
for k,vs in vals.items():
    for r in db.rows(c,f"""select KEY_VALUE, max(CANONICAL_NAME), max(CANONICAL_ADDR) from LIBRARY_META."CONNECT".ENTITY_GOLDEN where KEY_TYPE='{k}' and KEY_VALUE in ({','.join(repr(x) for x in vs)}) group by 1"""):
        names[f"{k}:{r[0]}"]=(r[1],r[2])
c.close()
print("\nTOP NPI bridges with the hospitals they connect:")
for a,dg,cutn in best_npi[:8]:
    print(f"\n  {a} {names.get(a)} deg {dg} cuts off {cutn}")
    for h in H[a]: print(f"     - {h} deg {H.degree(h)} cut {cut.get(h,0)} {names.get(h)}")
print("\nquiet CCNs from sampled run:"); [print(f"  {n} deg {H.degree(n)} ap {n in ap} cut {cut.get(n,0)} {names.get(n)}") for n in quiet_ccn if n in H]
print("\nsize-cut CCNs, owned:"); [print(f"  CCN:{v} deg {H.degree('CCN:'+v)} {names.get('CCN:'+v)}") for k,v in D['junk'] if 'CCN:'+v in H]
json.dump({'graph':[G.number_of_nodes(),G.number_of_edges(),H.number_of_nodes()],'blocks':len(blocks),'ap':len(ap),'best_npi':best_npi,'best_ccn':best_ccn,'names':names,'sampled_npi':[(n,cut.get(n),n in ap) for n in sampled_npi]},open('scripts/scratch/g2d_out.json','w'))
print("DONE")
