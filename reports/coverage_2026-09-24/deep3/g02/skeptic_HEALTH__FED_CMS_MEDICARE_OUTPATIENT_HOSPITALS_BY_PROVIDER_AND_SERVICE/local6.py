import json, collections, statistics as st
r=json.load(open('../S04.json'))
def n(v):
    try: return float(v)
    except: return None
A=collections.defaultdict(lambda: dict(srv=0,out=0,osrv=0))
for x in r:
    s=n(x['CAPC_SRVCS']); o=n(x['OUTLIER_SRVCS'])
    if s is None or o is None: continue
    a=A[x['APC_CD']]; a['srv']+=s; a['out']+=o*n(x['AVG_MDCR_OUTLIER_AMT']); a['osrv']+=o
# per-APC 25th pct of row-level avg outlier per case, as a conservative hidden per-case
Q=collections.defaultdict(list)
for x in r:
    o=n(x['OUTLIER_SRVCS'])
    if o: Q[x['APC_CD']].append(n(x['AVG_MDCR_OUTLIER_AMT']))
q25={k:sorted(v)[len(v)//4] for k,v in Q.items()}
for label,k_h,percase in [('1 case @ APC p25',1,'p25'),('1 case @ APC mean',1,'mean'),('3 cases @ mean',3,'mean'),('5.5 @ mean',5.5,'mean'),('10 @ mean',10,'mean')]:
    H=collections.defaultdict(float)
    for x in r:
        s=n(x['CAPC_SRVCS']); o=n(x['OUTLIER_SRVCS'])
        if s is None: continue
        if o is not None: H[x['RNDRNG_PRVDR_CCN']]+=o*n(x['AVG_MDCR_OUTLIER_AMT'])
        else:
            a=A[x['APC_CD']]
            pc=(q25.get(x['APC_CD'],0) if percase=='p25' else (a['out']/a['osrv'] if a['osrv'] else 0))
            H[x['RNDRNG_PRVDR_CCN']]+=k_h*pc
    v=sorted(H.values(),reverse=True); T=sum(v)
    print(label.ljust(20),'total $M',round(T/1e6,1),'top10',round(sum(v[:10])/T,3),'top50',round(sum(v[:50])/T,3),'top100',round(sum(v[:100])/T,3),'hosp with $0',sum(1 for x in v if x==0),'of',len(v))
# PA 5115 share
rows=[x for x in r if x['APC_CD']=='5115' and x['RNDRNG_PRVDR_STATE_ABRVTN']=='PA' and n(x['CAPC_SRVCS'])]
sh=[x for x in rows if n(x['OUTLIER_SRVCS']) is not None]
PS={'390004','390096','390256','390336','390339'}
tot=sum(n(x['OUTLIER_SRVCS'])*n(x['AVG_MDCR_OUTLIER_AMT']) for x in sh); ps=sum(n(x['OUTLIER_SRVCS'])*n(x['AVG_MDCR_OUTLIER_AMT']) for x in sh if x['RNDRNG_PRVDR_CCN'] in PS)
srv=sum(n(x['CAPC_SRVCS']) for x in sh); pss=sum(n(x['CAPC_SRVCS']) for x in sh if x['RNDRNG_PRVDR_CCN'] in PS)
hid=[x for x in rows if n(x['OUTLIER_SRVCS']) is None]
print('PA 5115 shown: PSH share $',round(ps/tot,3),'cases',int(pss),'of',int(srv),round(pss/srv,3),'| PA hidden 5115 rows',len(hid),'services',int(sum(n(x['CAPC_SRVCS']) for x in hid)))
# Lancaster rank at srv>=500
