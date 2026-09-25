import pandas as pd, numpy as np, re
o=pd.read_csv('out_S18.csv'); b=pd.read_csv('out_S19.csv')
o['ORDER_DATE']=pd.to_datetime(o.ORDER_DATE)
bankish=re.compile(r'(?i)\b(BANK|TRUST|SAVINGS|FINANCIAL|FSB|SSB|N\.A\.|COMPANY|CORP|BANC|BANCO|FEDERAL|CO\.|INC)\b')
o['resp_bank']=o.RESPONDENTS.fillna('').str.contains(bankish)
o['new_cd']=(o.ORDER_TYPE.fillna('').str.contains('Cease and Desist') & ~o.ORDER_TYPE.fillna('').str.contains('Removal') &
             ~o.ORDER_CATEGORY.fillna('').str.contains('Termination|Modification') & ~o.ORDER_TITLE.fillna('').str.contains('(?i)terminat|modif') & o.resp_bank & (o.CERT_NUMBER>0))
print('new bank C&D/consent orders since 2010:', o.new_cd.sum(), ' by year:'); print(o[o.new_cd].groupby(o.ORDER_DATE.dt.year).size().to_string())
for c in ['ESTYMD','ENDEFYMD']: b[c]=pd.to_datetime(b[c],errors='coerce')
b['mdi']=b.MDI_STATUS_CODE.notna() & ~b.MDI_STATUS_CODE.astype(str).isin(['0','00','nan',''])
b['fdic_sup']=b.BKCLASS.isin(['NM','SB']) | ((b.BKCLASS=='SA') & (b.CHRTAGNT=='STATE'))
b['band']=pd.cut(b.ASSET,[0,1e5,3e5,1e6,1e7,1e10],labels=['<100M','100-300M','300M-1B','1-10B','10B+'])
res=[]
for w0,w1 in [('2010-01-01','2019-12-31'),('2020-01-01','2026-12-31')]:
    alive=b[(b.ESTYMD<=w0)&((b.ENDEFYMD.isna())|(b.ENDEFYMD>w0))].copy()
    hit=set(o[o.new_cd&(o.ORDER_DATE>=w0)&(o.ORDER_DATE<=w1)].CERT_NUMBER)
    alive['hit']=alive.CERT.isin(hit)
    g=alive.groupby(['fdic_sup','band','mdi'],observed=True).agg(n=('CERT','size'),hits=('hit','sum'),rate=('hit','mean')).round(3)
    print('window',w0[:4],w1[:4], 'alive',len(alive)); print(g.to_string())
    s=alive[alive.fdic_sup]
    print(' FDIC-supervised overall MDI', s[s.mdi].hit.mean().round(3), s[s.mdi].hit.sum(), len(s[s.mdi]), ' non-MDI', s[~s.mdi].hit.mean().round(3), s[~s.mdi].hit.sum(), len(s[~s.mdi]))
    if w0.startswith('2020'):
        m=s[s.mdi&s.hit]
        print(m[['CERT','NAME','CITY','STALP','ACTIVE','ASSET','MDI_STATUS_DESC','ENDEFYMD']].to_string())
        # size-standardized expected hits for MDIs using non-MDI band rates
        br=s[~s.mdi].groupby('band',observed=True).hit.mean()
        mm=s[s.mdi]; exp=mm.band.map(br).astype(float).sum()
        print(' MDI observed', mm.hit.sum(), 'expected at non-MDI same-band rates', round(exp,1))
        print(s[s.mdi].MDI_STATUS_DESC.value_counts().to_string())
        print(s[s.mdi].groupby('MDI_STATUS_DESC').hit.agg(['size','sum']).to_string())

# ---- eyeball + stats
from math import comb
def fisher_exact(t):
    (a,b_),(c,d)=t; n1=a+b_; n2=c+d; k=a+c; N=n1+n2
    p=lambda x: comb(n1,x)*comb(n2,k-x)/comb(N,k)
    obs=p(a); return ('one-sided p(>=a)', sum(p(x) for x in range(a,min(n1,k)+1)))
w0='2020-01-01'
alive=b[(b.ESTYMD<=w0)&((b.ENDEFYMD.isna())|(b.ENDEFYMD>w0))&b.fdic_sup].copy()
hit=o[o.new_cd&(o.ORDER_DATE>=w0)]
alive['hit']=alive.CERT.isin(set(hit.CERT_NUMBER))
t=[[alive[alive.mdi].hit.sum(), (~alive[alive.mdi].hit).sum()],[alive[~alive.mdi].hit.sum(), (~alive[~alive.mdi].hit).sum()]]
print('2020-26 fisher', t, fisher_exact(t))
a10=b[(b.ESTYMD<='2010-01-01')&((b.ENDEFYMD.isna())|(b.ENDEFYMD>'2010-01-01'))&b.fdic_sup].copy()
h10=o[o.new_cd&(o.ORDER_DATE>='2010-01-01')&(o.ORDER_DATE<='2019-12-31')]
a10['hit']=a10.CERT.isin(set(h10.CERT_NUMBER))
t=[[a10[a10.mdi].hit.sum(), (~a10[a10.mdi].hit).sum()],[a10[~a10.mdi].hit.sum(), (~a10[~a10.mdi].hit).sum()]]
print('2010-19 fisher', t, fisher_exact(t))
mc=set(alive[alive.mdi&alive.hit].CERT)
print(hit[hit.CERT_NUMBER.isin(mc)][['ORDER_DATE','CERT_NUMBER','BANK_NAME','ORDER_CATEGORY','ORDER_TITLE','RESPONDENTS','CMP_AMOUNT_TOTAL']].sort_values('ORDER_DATE').to_string())
# ROA control among active FDIC-supervised
act=alive[alive.ACTIVE==1].copy(); act['roa']=act.NETINC*4/act.ASSET
act['roa_t']=pd.qcut(act.roa,3,labels=['low','mid','high'])
print(act.groupby(['roa_t','mdi'],observed=True).hit.agg(['size','sum','mean']).round(3).to_string())
# drop BaaS/fintech-partner names? count hits among non-MDI
print('non-MDI hits 2020-26:', alive[~alive.mdi & alive.hit].shape[0])
