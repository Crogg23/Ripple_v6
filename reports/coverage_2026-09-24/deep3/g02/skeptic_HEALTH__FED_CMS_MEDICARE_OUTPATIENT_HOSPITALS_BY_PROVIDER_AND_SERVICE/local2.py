import json, collections, statistics as st
r=json.load(open('../S04.json')); A=json.load(open('apc.json'))['A']
def n(v):
    try: return float(v)
    except: return None
PS=['390004','390096','390256','390336','390339']
for c in ('390256','390339','390336'):
    rows=[x for x in r if x['RNDRNG_PRVDR_CCN']==c and n(x['CAPC_SRVCS'])]
    tot=sum((n(x['OUTLIER_SRVCS']) or 0)*(n(x['AVG_MDCR_OUTLIER_AMT']) or 0) for x in rows)
    rows.sort(key=lambda x:-((n(x['OUTLIER_SRVCS']) or 0)*(n(x['AVG_MDCR_OUTLIER_AMT']) or 0)))
    print(c, 'rows',len(rows),'tot $M',round(tot/1e6,2))
    cum=0
    for x in rows[:8]:
        d=(n(x['OUTLIER_SRVCS']) or 0)*(n(x['AVG_MDCR_OUTLIER_AMT']) or 0); cum+=d
        a=A[x['APC_CD']]
        print('   ',x['APC_CD'],x['APC_DESC'][:40],'srv',x['CAPC_SRVCS'],'out',x['OUTLIER_SRVCS'],'avgout',round(n(x['AVG_MDCR_OUTLIER_AMT']) or 0),'chg',round(n(x['AVG_TOT_SBMTD_CHRGS'])),'alw',round(n(x['AVG_MDCR_ALOWD_AMT'])),'pay',round(n(x['AVG_MDCR_PYMT_AMT'])),'$M',round(d/1e6,2),'cum',round(cum/tot,2),'natrate',round(a['osrv']/a['srv'],3) if a['srv'] else None)
# Does payment include outlier? APC 5115: compare avg pay for 0-outlier rows vs high-share rows
for apc in ('5115','8011','5114'):
    rows=[x for x in r if x['APC_CD']==apc and n(x['OUTLIER_SRVCS']) is not None]
    z=[n(x['AVG_MDCR_PYMT_AMT']) for x in rows if n(x['OUTLIER_SRVCS'])==0]
    zal=[n(x['AVG_MDCR_ALOWD_AMT']) for x in rows if n(x['OUTLIER_SRVCS'])==0]
    hi=[(n(x['AVG_MDCR_PYMT_AMT']),n(x['AVG_MDCR_ALOWD_AMT']),n(x['OUTLIER_SRVCS'])/n(x['CAPC_SRVCS']),n(x['AVG_MDCR_OUTLIER_AMT']),x['RNDRNG_PRVDR_CCN']) for x in rows if n(x['OUTLIER_SRVCS'])/n(x['CAPC_SRVCS'])>=0.5]
    print(apc,'zero-outlier rows',len(z),'median pay',round(st.median(z)),'median allowed',round(st.median(zal)),'| rows >=50% outlier',len(hi))
    for p,al,sh,oa,c in sorted(hi,key=lambda t:-t[2])[:6]: print('     pay',round(p),'allowed',round(al),'share',round(sh,2),'avg outlier',round(oa),'pay-minus-zero-median',round(p-st.median(z)),'expected if included',round(sh*oa),c)
# per-case semantics: ratio outlier/pay by outlier share bucket (pooled)
B=collections.defaultdict(lambda:[0,0,0])
for x in r:
    o=n(x['OUTLIER_SRVCS']); s=n(x['CAPC_SRVCS'])
    if not o: continue
    sh=o/s; b=min(int(sh*10),9)
    B[b][0]+=n(x['AVG_MDCR_OUTLIER_AMT']); B[b][1]+=n(x['AVG_MDCR_PYMT_AMT']); B[b][2]+=1
for b in sorted(B): print('share bucket',b/10,'rows',B[b][2],'mean outlier/mean pay',round(B[b][0]/B[b][1],2))
