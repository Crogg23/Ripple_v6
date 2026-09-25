import json, collections, statistics as st
r=json.load(open('S04.json'))
def n(v):
    try: return float(v)
    except: return None
# national per-APC outlier $ per service, using rows where outlier cells are shown
A=collections.defaultdict(lambda: dict(srv=0,out=0,osrv=0,pay=0,chg=0))
for x in r:
    s=n(x['CAPC_SRVCS']); o=n(x['OUTLIER_SRVCS']); oa=n(x['AVG_MDCR_OUTLIER_AMT'])
    if s is None or o is None: continue
    a=A[x['APC_CD']]; a['srv']+=s; a['out']+=o*oa; a['osrv']+=o; a['pay']+=s*n(x['AVG_MDCR_PYMT_AMT']); a['chg']+=s*n(x['AVG_TOT_SBMTD_CHRGS'])
for k,a in A.items(): a['rate']=a['out']/a['srv']; a['orate']=a['osrv']/a['srv']
H=collections.defaultdict(lambda: dict(srv=0,out=0,osrv=0,exp=0,expo=0,pay=0,chg=0,supout=0,apcs=set()))
for x in r:
    s=n(x['CAPC_SRVCS']); o=n(x['OUTLIER_SRVCS']); oa=n(x['AVG_MDCR_OUTLIER_AMT'])
    h=H[x['RNDRNG_PRVDR_CCN']]; h['name']=x['RNDRNG_PRVDR_ORG_NAME']; h['st']=x['RNDRNG_PRVDR_STATE_ABRVTN']; h['city']=x['RNDRNG_PRVDR_CITY']
    if s is None: continue
    h['pay']+=s*n(x['AVG_MDCR_PYMT_AMT']); h['chg']+=s*n(x['AVG_TOT_SBMTD_CHRGS'])
    if o is None: h['supout']+=s; continue
    a=A[x['APC_CD']]
    h['srv']+=s; h['out']+=o*oa; h['osrv']+=o; h['exp']+=s*a['rate']; h['expo']+=s*a['orate']; h['apcs'].add(x['APC_CD'])
tot=sum(h['out'] for h in H.values())
L=[]
for k,h in H.items():
    if h['exp']>0:
        h['oe']=h['out']/h['exp']; h['ccr_proxy']=h['pay']/h['chg'] if h['chg'] else None
        L.append((k,h))
L.sort(key=lambda kv:-kv[1]['out'])
print('hospitals with outlier-eligible rows', len(L), 'total outlier $', round(tot/1e6,1))
cum=0
for i,(k,h) in enumerate(L):
    cum+=h['out']
    if i+1 in (10,20,50,100,300): print('top',i+1,'share',round(cum/tot,3))
oes=[h['oe'] for k,h in L if h['srv']>=1000]
print('median O/E (srv>=1000)', round(st.median(oes),2), 'n', len(oes))
print('--- top by O/E with srv>=1000 and excess>$1M')
M=[(h['out']-h['exp'],k,h) for k,h in L if h['srv']>=1000]
M.sort(key=lambda t:-t[0])
for ex,k,h in M[:30]:
    print(k, h['name'][:40], h['city'], h['st'], 'O/E', round(h['oe'],2), 'out $M', round(h['out']/1e6,2), 'exp $M', round(h['exp']/1e6,2), 'excess', round(ex/1e6,2), 'osrv/srv', int(h['osrv']), int(h['srv']), 'pay/chg', round(h['ccr_proxy'],3), 'apcs', len(h['apcs']))
json.dump({k:{kk:(list(vv) if isinstance(vv,set) else vv) for kk,vv in h.items()} for k,h in H.items()}, open('oe_hosp.json','w'))
json.dump(A, open('oe_apc.json','w'))
