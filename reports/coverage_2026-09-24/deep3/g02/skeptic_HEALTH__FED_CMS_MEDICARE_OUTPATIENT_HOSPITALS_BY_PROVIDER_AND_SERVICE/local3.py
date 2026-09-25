import json, collections, statistics as st
r=json.load(open('../S04.json'))
def n(v):
    try: return float(v)
    except: return None
PS=['390004','390096','390256','390336','390339']
# per-APC per-case outlier $ on shown rows
A=collections.defaultdict(lambda: dict(srv=0,out=0,osrv=0))
for x in r:
    s=n(x['CAPC_SRVCS']); o=n(x['OUTLIER_SRVCS'])
    if s is None or o is None: continue
    a=A[x['APC_CD']]; a['srv']+=s; a['out']+=o*n(x['AVG_MDCR_OUTLIER_AMT']); a['osrv']+=o
for k_hidden in (0,1,5.5,10):
    N=collections.defaultdict(lambda:[0,0])
    for x in r:
        s=n(x['CAPC_SRVCS']); o=n(x['OUTLIER_SRVCS'])
        if s is None: continue
        a=A[x['APC_CD']]; per=a['out']/a['osrv'] if a['osrv'] else 0
        d=o*n(x['AVG_MDCR_OUTLIER_AMT']) if o is not None else k_hidden*per
        N[x['APC_CD']][0]+=d; N[x['APC_CD']][1]+=s
    O=E=0
    for x in r:
        if x['RNDRNG_PRVDR_CCN'] not in PS: continue
        s=n(x['CAPC_SRVCS']); o=n(x['OUTLIER_SRVCS'])
        if s is None: continue
        if k_hidden==0 and o is None: continue
        a=A[x['APC_CD']]; per=a['out']/a['osrv'] if a['osrv'] else 0
        O+= o*n(x['AVG_MDCR_OUTLIER_AMT']) if o is not None else k_hidden*per
        E+= s*N[x['APC_CD']][0]/N[x['APC_CD']][1]
    tot=sum(v[0] for v in N.values())
    print('hidden per row',k_hidden,'national $M',round(tot/1e6,1),'PSH obs $M',round(O/1e6,2),'exp $M',round(E/1e6,2),'O/E',round(O/E,1),'share',round(O/tot,3))
# 5115 in PA: charges, implied CCR, outlier share
print('--- APC 5115 PA rows (shown outlier)')
rows=[x for x in r if x['APC_CD']=='5115' and x['RNDRNG_PRVDR_STATE_ABRVTN']=='PA' and n(x['CAPC_SRVCS'])]
nat=[x for x in r if x['APC_CD']=='5115' and n(x['CAPC_SRVCS'])]
print('national 5115 median avg charge',round(st.median([n(x['AVG_TOT_SBMTD_CHRGS']) for x in nat])),'PA median',round(st.median([n(x['AVG_TOT_SBMTD_CHRGS']) for x in rows])), 'PA rows',len(rows))
rows.sort(key=lambda x:-n(x['AVG_TOT_SBMTD_CHRGS']))
for x in rows[:15]:
    o=n(x['OUTLIER_SRVCS']); s=n(x['CAPC_SRVCS']); al=n(x['AVG_MDCR_ALOWD_AMT']); oa=n(x['AVG_MDCR_OUTLIER_AMT'])
    imp=(2*oa+1.75*al)/n(x['AVG_TOT_SBMTD_CHRGS']) if o else None
    print('  ',x['RNDRNG_PRVDR_CCN'],x['RNDRNG_PRVDR_ORG_NAME'][:40],'srv',int(s),'out',x['OUTLIER_SRVCS'],'chg',round(n(x['AVG_TOT_SBMTD_CHRGS'])),'alw',round(al),'chg/alw',round(n(x['AVG_TOT_SBMTD_CHRGS'])/al,1),'impliedCCR<=',round(imp,3) if imp else None)
for c in ('390004','390096'):
    for x in r:
        if x['RNDRNG_PRVDR_CCN']==c and x['APC_CD'] in ('5115','5114','5116') and n(x['CAPC_SRVCS']): print('  acquired',c,x['APC_CD'],'srv',x['CAPC_SRVCS'],'out',x['OUTLIER_SRVCS'],'chg',round(n(x['AVG_TOT_SBMTD_CHRGS'])),'alw',round(n(x['AVG_MDCR_ALOWD_AMT'])))
# HCRIS CCRs for PS
h=json.load(open('../S06.json'))
for x in sorted([x for x in h if x['PROVIDER_CCN'] in PS], key=lambda x:(x['PROVIDER_CCN'],str(x['FISCAL_YEAR_END_DATE']))):
    if str(x['FISCAL_YEAR_END_DATE'])[:4]>='2021': print('  hcris',x['PROVIDER_CCN'],x['FISCAL_YEAR_BEGIN_DATE'],x['FISCAL_YEAR_END_DATE'],'ccr',x['COST_TO_CHARGE_RATIO'],'op chg',x['OUTPATIENT_TOTAL_CHARGES'],'cost',x['TOTAL_COSTS'],'beds',x['NUMBER_OF_BEDS'])
