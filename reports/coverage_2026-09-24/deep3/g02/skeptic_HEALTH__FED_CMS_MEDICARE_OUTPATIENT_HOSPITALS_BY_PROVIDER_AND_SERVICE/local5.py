import json, collections, statistics as st
r=json.load(open('../S04.json'))
def n(v):
    try: return float(v)
    except: return None
hc={}
for x in json.load(open('../S06.json')):
    fy=str(x['FISCAL_YEAR_END_DATE'])[:4]
    c=n(x['COST_TO_CHARGE_RATIO'])
    if not c or c<=0: continue
    if fy in ('2023','2024'):
        # prefer FY2024 then FY2023
        prev=hc.get(x['PROVIDER_CCN'])
        if prev is None or fy>prev[0]: hc[x['PROVIDER_CCN']]=(fy,c)
# per-hospital: predicted outlier $ from avg charge x HCRIS CCR (CY2024 formula: 50% of cost above max(1.75xAPC, APC+7750))
P=collections.defaultdict(lambda:[0,0,0,'',0])
for x in r:
    s=n(x['CAPC_SRVCS']); o=n(x['OUTLIER_SRVCS'])
    if s is None or o is None: continue
    k=x['RNDRNG_PRVDR_CCN']
    if k not in hc: continue
    ccr=hc[k][1]; al=n(x['AVG_MDCR_ALOWD_AMT']); chg=n(x['AVG_TOT_SBMTD_CHRGS'])
    cost=chg*ccr; thr=max(1.75*al, al+7750)
    pred=0.5*max(0,cost-1.75*al) if cost>thr else 0
    P[k][0]+=o*n(x['AVG_MDCR_OUTLIER_AMT']); P[k][1]+=s*pred; P[k][2]+=s; P[k][3]=x['RNDRNG_PRVDR_ORG_NAME']; P[k][4]=ccr
tot_o=sum(v[0] for v in P.values()); tot_p=sum(v[1] for v in P.values())
print('hospitals',len(P),'observed $M',round(tot_o/1e6,1),'predicted-from-avg $M',round(tot_p/1e6,1))
# rank correlation observed vs predicted per service
def rank(a):
    idx=sorted(range(len(a)),key=lambda i:a[i]); rk=[0]*len(a)
    for j,i in enumerate(idx): rk[i]=j
    return rk
ks=[k for k,v in P.items() if v[2]>=500]
a=[P[k][0]/P[k][2] for k in ks]; b=[P[k][1]/P[k][2] for k in ks]
ra,rb=rank(a),rank(b); m=len(ks)
mean=(m-1)/2
cov=sum((ra[i]-mean)*(rb[i]-mean) for i in range(m)); var=sum((ra[i]-mean)**2 for i in range(m))
print('spearman obs vs predicted (per service, srv>=500)',round(cov/var,3),'n',m)
for k in ('390256','390339','390336','390004','390096'):
    v=P[k]; print(k,v[3][:35],'ccr',hc[k],'obs $M',round(v[0]/1e6,2),'pred $M',round(v[1]/1e6,2))
# where does Hershey rank on predicted per service?
pp=sorted(ks,key=lambda k:-P[k][1]/P[k][2]); print('Hershey rank on predicted $/service', pp.index('390256')+1,'of',len(pp), '| on observed', sorted(ks,key=lambda k:-P[k][0]/P[k][2]).index('390256')+1)
