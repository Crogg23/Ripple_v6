import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',38)
d=pd.read_pickle('out_S11.pkl')
num=['N','FILINGS','LATE6','LATE30','NEG_LAG','SELF_LATE','LATE6_SELF','GRANTS','GRANTS_LATE6','GRANTS_LATE30','GRANT_FILINGS_LATE6','GRANT_MAX_LAG']
for c in num: d[c]=pd.to_numeric(d[c])
print('doc types', d.groupby('DOC').N.sum().to_dict())
o=d[(d.DOC=='4')]
print('rows orig 4', o.N.sum(), 'late6', o.LATE6.sum(), o.LATE6.sum()/o.N.sum(), 'late30', o.LATE30.sum(), 'neg', o.NEG_LAG.sum())
print('self-flag L', o.SELF_LATE.sum(), 'late6 & self L', o.LATE6_SELF.sum(), 'share of late6 that admit', o.LATE6_SELF.sum()/o.LATE6.sum())
y=o.groupby('YR')[['N','LATE6','LATE30','GRANTS','GRANTS_LATE6','GRANTS_LATE30']].sum()
y['late_rate']=y.LATE6/y.N; y['grant_late_rate']=y.GRANTS_LATE6/y.GRANTS
print(y.to_string())
# per issuer, all years, orig form 4
g=o.groupby('CIK').agg(issuer=('ISSUER','last'),ticker=('TICKER','last'),n=('N','sum'),filings=('FILINGS','sum'),late6=('LATE6','sum'),late30=('LATE30','sum'),
    grants=('GRANTS','sum'),gl6=('GRANTS_LATE6','sum'),gl30=('GRANTS_LATE30','sum'),glf=('GRANT_FILINGS_LATE6','sum'),gmax=('GRANT_MAX_LAG','max'),years=('YR','nunique'))
g['grate']=g.gl6/g.grants
print('issuers', len(g), 'with 20+ grants', (g.grants>=20).sum())
peer=g[g.grants>=20]
print('peer (20+ option grant lines): median late rate', peer.grate.median(), 'mean', peer.grl if False else peer.gl6.sum()/peer.grants.sum(), 'p90', peer.grate.quantile(.9), 'p99', peer.grate.quantile(.99))
print('issuers >=50% late grants among 20+:', (peer.grate>=0.5).sum())
print(peer.sort_values(['grate','grants'],ascending=False).head(30).to_string())
g.to_pickle('issuer_late.pkl')
