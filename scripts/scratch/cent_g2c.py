"""Hard test on Graph 2 hospital family: articulation points + names. Sampling-free."""
import sys,json,collections; sys.path.insert(0,'.')
from connect import db
import networkx as nx
D=json.load(open('scripts/scratch/g2b_out.json')); c0=D['comp0']
npis=[n for n,*_ in c0['npi_top'][:12]]; ccns=[n for n,*_ in c0['top'][:20]]
quiet_ccn=[n for n,bt,dg,rd,rb in c0['top'] if rd-rb>=40][:12]
dropped=[f"CCN:{v}" for k,v in D['junk']]
c=db.connect()
P=db.rows(c,'select distinct KEY_A,VALUE_A,KEY_B,VALUE_B from LIBRARY_META."CONNECT".ENTITY_XREF where KEY_A=\'CCN\' and KEY_B=\'NPI\'')
G=nx.Graph()
for ka,va,kb,vb in P:
    if (va or '').strip('0 ')=='' or (vb or '').strip('0 ')=='': continue
    G.add_edge(f"CCN:{va}",f"NPI:{vb}")
cc=sorted(nx.connected_components(G),key=len,reverse=True); H=G.subgraph(cc[0]).copy()
print("full CCN-NPI graph (no size cut): nodes",G.number_of_nodes(),"edges",G.number_of_edges(),"largest",H.number_of_nodes())
ap=set(nx.articulation_points(H)); print("articulation points:",len(ap), "of which NPI:",sum(1 for a in ap if a.startswith('NPI:')))
def cut(n):
    if n not in H: return None
    S=set(H); S.discard(n); sz=sorted((len(x) for x in nx.connected_components(H.subgraph(S))),reverse=True); return sum(sz[1:]),sz[1:6]
res={}
for n in npis+quiet_ccn+ccns[:5]+dropped:
    if n in H: res[n]={'deg':H.degree(n),'ap':n in ap,'cut':cut(n) if n in ap else (0,[])}
# biggest cuts among NPI articulation points overall - the true quiet middlemen, sampling-free
npi_ap=[a for a in ap if a.startswith('NPI:')]
best=[]
for a in npi_ap:
    S=set(H); S.discard(a); sz=sorted((len(x) for x in nx.connected_components(H.subgraph(S))),reverse=True); best.append((a,H.degree(a),sum(sz[1:]),sz[1:4]))
best.sort(key=lambda x:-x[2]); print("\nNPI articulation points by nodes cut off (top 15):")
for b in best[:15]: print("  ",b)
ccn_ap=[a for a in ap if a.startswith('CCN:')]; bestc=[]
for a in ccn_ap:
    S=set(H); S.discard(a); sz=sorted((len(x) for x in nx.connected_components(H.subgraph(S))),reverse=True); bestc.append((a,H.degree(a),sum(sz[1:]),sz[1:4]))
bestc.sort(key=lambda x:-x[2]); print("\nCCN articulation points by nodes cut off (top 10):")
for b in bestc[:10]: print("  ",b)
# names
want=set(npis+quiet_ccn+ccns[:8]+dropped+[b[0] for b in best[:15]]+[b[0] for b in bestc[:10]])
for a,_,_,_ in best[:8]: want|=set(H[a])   # hospitals the top NPI bridges connect
vals=collections.defaultdict(list)
for w in want: k,v=w.split(':',1); vals[k].append(v)
names={}
for k,vs in vals.items():
    for r in db.rows(c,f"""select KEY_VALUE, max(CANONICAL_NAME), max(CANONICAL_ADDR) from LIBRARY_META."CONNECT".ENTITY_GOLDEN where KEY_TYPE='{k}' and KEY_VALUE in ({','.join(repr(x) for x in vs)}) group by 1"""):
        names[f"{k}:{r[0]}"]=(r[1],r[2])
c.close()
print("\nTOP NPI bridges, with the hospitals they connect:")
for a,dg,cutn,sz in best[:8]:
    print(f"\n  {a} {names.get(a)} deg {dg} cuts off {cutn} {sz}")
    for h in H[a]: print(f"     - {h} deg {H.degree(h)} {names.get(h)}")
print("\nquiet CCN candidates:")
for n in quiet_ccn: print(f"  {n} {names.get(n)} {res.get(n)}")
print("\ndropped-as-junk CCNs (size cut, owned):")
for n in dropped: print(f"  {n} {names.get(n)} {res.get(n)}")
json.dump({'res':res,'best_npi':best[:30],'best_ccn':bestc[:20],'names':names,'ap_total':len(ap),'graph':[G.number_of_nodes(),G.number_of_edges(),H.number_of_nodes()]},open('scripts/scratch/g2c_out.json','w'))
