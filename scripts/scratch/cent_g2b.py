"""Graph 2 rerun: junk = blanks/sentinels only, or fanout >= 5000. Save fanout table. Print CCN/NPI mix."""
import sys, json, collections; sys.path.insert(0,'.')
from connect import db
import networkx as nx
X='LIBRARY_META."CONNECT".ENTITY_XREF'
c=db.connect()
fan=db.dicts(c,f"""with p as (select distinct KEY_A,VALUE_A,KEY_B,VALUE_B from {X})
select side,key,val,n from (
 select 'A' side, KEY_A key, VALUE_A val, count(*) n from p group by 1,2,3
 union all select 'B', KEY_B, VALUE_B, count(*) from p group by 1,2,3) where n>=20 order by n desc""")
json.dump(fan,open('scripts/scratch/g2_fanout.json','w'),default=str)
def isjunk(k,v,n):
    s=(v or '').strip(); return s=='' or s.strip('0')=='' or s.upper() in ('N/A','NA','NONE','UNKNOWN','NULL','<UNAVAIL>') or n>=5000
junk={(r['KEY'],r['VAL']) for r in fan if isjunk(r['KEY'],r['VAL'],r['N'])}
P=db.rows(c,f"select distinct KEY_A,VALUE_A,KEY_B,VALUE_B from {X}"); c.close()
for ka,va,kb,vb in P:
    for k,v in ((ka,va),(kb,vb)):
        s=(v or '').strip()
        if s=='' or s.strip('0')=='' or s.upper() in ('N/A','NA','NONE','UNKNOWN','NULL','<UNAVAIL>'): junk.add((k,v))
out={'fanout_top':fan[:40],'junk':sorted(junk),'pairs':len(P)}
G=nx.Graph()
for ka,va,kb,vb in P:
    if (ka,va) in junk or (kb,vb) in junk: continue
    G.add_edge(f"{ka}:{va}",f"{kb}:{vb}")
cc=sorted(nx.connected_components(G),key=len,reverse=True)
out['graph']={'nodes':G.number_of_nodes(),'edges':G.number_of_edges(),'components':len(cc),'sizes':[len(x) for x in cc[:12]],
  'families':[sorted({n.split(':')[0] for n in comp}) for comp in cc[:12]]}
H=G.subgraph(cc[0]).copy(); dg=dict(H.degree())
bt=nx.betweenness_centrality(H,k=300,normalized=True,seed=7)
rb={n:j+1 for j,n in enumerate(sorted(bt,key=bt.get,reverse=True))}; rd={n:j+1 for j,n in enumerate(sorted(dg,key=dg.get,reverse=True))}
top=sorted(bt,key=bt.get,reverse=True)[:200]
out['comp0']={'nodes':H.number_of_nodes(),'edges':H.number_of_edges(),'k':300,'top':[(n,bt[n],dg[n],rd[n],rb[n]) for n in top],
  'deg_top':[(n,dg[n]) for n in sorted(dg,key=dg.get,reverse=True)[:20]],
  'top_families':dict(collections.Counter(n.split(':')[0] for n in top))}
# NPI-only view: the physicians with highest betweenness, and their degree
npi=[n for n in sorted(bt,key=bt.get,reverse=True) if n.startswith('NPI:')][:40]
out['comp0']['npi_top']=[(n,bt[n],dg[n],rd[n],rb[n]) for n in npi]
json.dump(out,open('scripts/scratch/g2b_out.json','w'))
print("done",out['graph'])
