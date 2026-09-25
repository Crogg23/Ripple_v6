import pandas as pd, numpy as np
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 45)
d = pd.read_pickle('out_S02.pkl'); d['FD'] = pd.to_datetime(d.FILING_DATE); d['POR'] = pd.to_datetime(d.PERIOD_OF_REPORT, format='%d-%b-%Y'); d['dt'] = d.DOCUMENT_TYPE.astype(str).str.strip()
f4 = d[d.dt == '4'].copy()
f4['bd'] = np.busday_count(f4.POR.values.astype('datetime64[D]'), f4.FD.values.astype('datetime64[D]'))
print('Form 4 business-day lag distribution:'); print(f4.bd.describe().round(1).to_string())
print('late (>2 bd):', (f4.bd > 2).sum(), round((f4.bd > 2).mean(), 3), ' >30 bd:', (f4.bd > 30).sum(), ' >250 bd:', (f4.bd > 250).sum())
g = f4.groupby(['CIK','ISSUERNAME']).agg(n=('bd','size'), late=('bd', lambda s: (s > 2).sum()), med=('bd','median'))
g['rate'] = g.late / g.n
print('issuers with >=20 Form 4s:', (g.n >= 20).sum(), 'median late rate', g[g.n >= 20].rate.median().round(3))
print(g[g.n >= 20].sort_values('rate', ascending=False).head(12).to_string())
print('\noldest Form 4 periods filed in Q1 2026:'); print(f4.sort_values('POR').head(8)[['ISSUERNAME','POR','FD','bd']].to_string())
print('\nAFF10B5ONE encodings by filing month:'); print(pd.crosstab(d[d.dt=='4'].FD.dt.to_period('M'), d[d.dt=='4'].AFF10B5ONE.fillna('<null>')).to_string())
print('\nplan-flag share (1/true) on Form 4:', round(d[d.dt=='4'].AFF10B5ONE.isin(['1','true']).mean(), 3))
# NO_SECURITIES_OWNED on the 18-Mar FPI wave vs other Form 3s
f3 = d[d.dt == '3']; w = f3.POR == '2026-03-18'
print('\nForm 3 no-securities-owned=1: 18-Mar wave', round((f3[w].NO_SECURITIES_OWNED == '1').mean(), 3), w.sum(), '| other Form 3s', round((f3[~w].NO_SECURITIES_OWNED == '1').mean(), 3), (~w).sum())
