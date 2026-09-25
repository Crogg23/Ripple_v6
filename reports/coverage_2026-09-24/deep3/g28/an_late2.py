import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',34)
d=pd.read_pickle('out_S14.pkl')
for c in ['PRE_FIRST_DROPPED','AWARDS','LINES','LATE6','LATE30','LATE365','OWNERS','OWNERS_LATE30','MAX_LAG','MED_LAG']: d[c]=pd.to_numeric(d[c])
print('first filing in table min', d.ISSUER_FIRST_FD.min(), 'pre-first dropped', d.PRE_FIRST_DROPPED.sum())
y=d.groupby('YR')[['AWARDS','LATE6','LATE30','LATE365']].sum(); y['r6']=(y.LATE6/y.AWARDS).round(4); y['r30']=(y.LATE30/y.AWARDS).round(4)
print(y.to_string())
print('total', d.AWARDS.sum(), 'late6', d.LATE6.sum(), round(d.LATE6.sum()/d.AWARDS.sum(),4), 'late30', d.LATE30.sum(), round(d.LATE30.sum()/d.AWARDS.sum(),4), 'late365', d.LATE365.sum())
g=d.groupby('CIK').agg(issuer=('ISSUER','last'),ticker=('TICKER','last'),first=('ISSUER_FIRST_FD','min'),years=('YR','nunique'),awards=('AWARDS','sum'),l6=('LATE6','sum'),l30=('LATE30','sum'),l365=('LATE365','sum'),maxlag=('MAX_LAG','max'),
   yrs_late30=('LATE30',lambda x:(x>0).sum()), own_late30=('OWNERS_LATE30','sum'))
g['r30']=g.l30/g.awards
peer=g[g.awards>=20].copy()
print('peer 20+ awards', len(peer), 'median r30', peer.r30.median(), 'mean', peer.r30.mean(), 'p90', peer.r30.quantile(.9), 'zero-late share', (peer.l30==0).mean())
print('peer r30>=0.5:', (peer.r30>=0.5).sum(), '| & late30 in 3+ separate years:', ((peer.r30>=0.5)&(peer.yrs_late30>=3)).sum())
top=peer[peer.r30>=0.5].sort_values('l30',ascending=False)
print(top.head(25).drop(columns=['first']).to_string())
# persistence: split sample 2017-2020 vs 2021-2024 (out-of-sample test)
e=d[d.YR<=2020].groupby('CIK')[['AWARDS','LATE30']].sum(); l=d[d.YR>=2021].groupby('CIK')[['AWARDS','LATE30']].sum()
m=e.join(l,lsuffix='_e',rsuffix='_l',how='inner'); m=m[(m.AWARDS_e>=10)&(m.AWARDS_l>=10)]
m['bad_e']=m.LATE30_e/m.AWARDS_e>=0.5
grp=m.groupby('bad_e').agg(issuers=('AWARDS_l','size'),awards_l=('AWARDS_l','sum'),late_l=('LATE30_l','sum'),med_rate_l=('LATE30_l',lambda x: np.nan))
grp['pooled_rate_l']=grp.late_l/grp.awards_l
m['r_l']=m.LATE30_l/m.AWARDS_l
grp['median_issuer_rate_l']=m.groupby('bad_e').r_l.median()
print('\nPersistence (10+ awards in both halves):'); print(grp.drop(columns=['med_rate_l']).to_string())
print(m[m.bad_e].join(g[['issuer']]).sort_values('LATE30_l',ascending=False).to_string())
g.to_pickle('issuer_late_v2.pkl'); top.to_csv('late_awards_top_issuers_v2.csv')
