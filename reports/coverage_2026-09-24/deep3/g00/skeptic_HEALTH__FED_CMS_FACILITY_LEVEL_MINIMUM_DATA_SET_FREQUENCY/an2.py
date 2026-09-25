import pandas as pd, numpy as np
from math import comb
def fisher2(a,b,c,d_):
    r1=a+b; r2=c+d_; c1=a+c; n=r1+r2
    pr=lambda x: comb(c1,x)*comb(n-c1,r1-x)/comb(n,r1)
    p0=pr(a); lo=max(0,r1-(n-c1)); hi=min(r1,c1)
    return sum(pr(x) for x in range(lo,hi+1) if pr(x)<=p0*(1+1e-7))
s=pd.read_pickle('mo_joined.pkl')
p=pd.read_csv('K3_pen_mo.csv', dtype=str)
p['PENALTY_DATE']=pd.to_datetime(p.PENALTY_DATE); p['FINE_AMOUNT']=pd.to_numeric(p.FINE_AMOUNT)
print('penalty rows', len(p), 'distinct FINE_ID among fines', p.FINE_ID.nunique(), 'fines', p.PENALTY_TYPE.str.lower().str.startswith('fine').sum(), 'processing', p.PROCESSING_DATE.unique())
p=p.merge(s[['ccn','grp','ctrl','band','rel']], left_on='CMS_CERTIFICATION_NUMBER_CCN', right_on='ccn')
p['y']=p.PENALTY_DATE.dt.year
p['pre']=p.ctrl.notna() & (p.PENALTY_DATE<p.ctrl)
r=p[p.rel]
t=r.groupby('y').agg(pen=('y','size'), pre_reliant=('pre','sum'), homes=('ccn','nunique'), dollars=('FINE_AMOUNT','sum'))
t2=r[~r.pre].groupby('y').agg(pen_post=('y','size'), homes_post=('ccn','nunique'), dollars_post=('FINE_AMOUNT','sum'))
print(t.join(t2).to_string())
lh=r[r.ctrl.isna()]
print('long-held 20 (incl Cassville) by year:', lh.groupby('y').agg(pen=('y','size'),homes=('ccn','nunique'),dollars=('FINE_AMOUNT','sum')).to_dict('index'))
print('min/max penalty date', p.PENALTY_DATE.min().date(), p.PENALTY_DATE.max().date())
# health inspection Fisher in band
b=s[s.band]
for c in ['HEALTH_INSPECTION_RATING','OVERALL_RATING']:
    x=b[b.rel][c]; y=b[~b.rel][c]
    a1=int((x==1).sum()); an=int(x.notna().sum()); o1=int((y==1).sum()); on=int(y.notna().sum())
    print(c, a1, an, o1, on, 'p=%.3f'%fisher2(a1,an-a1,o1,on-o1))
# builder fines: median fines per home
print('fines median band', b.groupby('rel').TOTAL_AMOUNT_OF_FINES_IN_DOLLARS.apply(lambda x: pd.to_numeric(x).median()).to_dict(), 'sum', b.groupby('rel').TOTAL_AMOUNT_OF_FINES_IN_DOLLARS.apply(lambda x: pd.to_numeric(x).sum()).to_dict())
fb=b.copy(); fb['f']=pd.to_numeric(fb.TOTAL_AMOUNT_OF_FINES_IN_DOLLARS)
print('Reliant band top-4 fines share', round(fb[fb.rel].f.nlargest(4).sum()/fb[fb.rel].f.sum(),3), fb[fb.rel].f.nlargest(4).tolist())
# operator clustering in other40
print(s[s.grp=='other40'].CHAIN_NAME.fillna('(none)').value_counts().to_string())
