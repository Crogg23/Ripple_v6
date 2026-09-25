import pandas as pd, numpy as np
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 200); pd.set_option('display.max_colwidth', 50)
u = pd.read_pickle('out_S06.pkl'); u.columns = [c.upper() for c in u.columns]; u['cikn'] = pd.to_numeric(u.CIKN, errors='coerce'); d = pd.read_pickle('out_S02.pkl')
d['cikn'] = pd.to_numeric(d.CIK, errors='coerce')
d['FD'] = pd.to_datetime(d.FILING_DATE); d['POR'] = pd.to_datetime(d.PERIOD_OF_REPORT, format='%d-%b-%Y')
d['dt'] = d.DOCUMENT_TYPE.astype(str).str.strip()
u['listed'] = u.EXCHANGES.fillna('').str.contains('NYSE|Nasdaq', case=False)
u['fpi'] = u.FORMS.str.contains('20-F|40-F') & ~u.FORMS.str.contains('10-K')
u['dom'] = u.FORMS.str.contains('10-K') & ~u.FORMS.str.contains('20-F|40-F')
print(u.EXCHANGES.value_counts().head(10))
print('universe', len(u), 'fpi', u.fpi.sum(), 'fpi listed', (u.fpi & u.listed).sum(), 'dom listed', (u.dom & u.listed).sum())
anyf = d.groupby('cikn').agg(n=('dt','size'), n3=('dt', lambda s: (s.isin(['3','3/A'])).sum()), n4=('dt', lambda s: (s.isin(['4','4/A'])).sum()),
                             first=('FD','min'), n3_m18=('POR', lambda s: 0))
f3 = d[d.dt.isin(['3','3/A'])].groupby('cikn').FD.min().rename('first3')
anyf = anyf.join(f3)
u = u.join(anyf, on='cikn')
u['hit'] = u.n.fillna(0) > 0
u['hit3_after_mar'] = u.first3 >= '2026-03-01'
L = u[u.listed]
print('\nland rate, listed, any insider filing Jan-Mar 2026:')
print(L.groupby(np.where(L.fpi, 'FPI (20-F/40-F)', np.where(L.dom, 'domestic 10-K', 'mixed'))).hit.agg(['size','sum','mean']).to_string())
F = L[L.fpi].copy()
F['cty'] = F.COUNTRYBA.fillna('?')
g = F.groupby('cty').agg(listed_fpis=('hit','size'), with_filing=('hit','sum')).assign(rate=lambda x: (x.with_filing / x.listed_fpis).round(3))
print('\nFPIs by country of business address (n >= 8):'); print(g[g.listed_fpis >= 8].sort_values('listed_fpis', ascending=False).to_string())
print('\nall FPIs rate', round(F.hit.mean(), 3), 'n', len(F), 'median country rate (n>=8)', g[g.listed_fpis >= 8].rate.median())
F.to_pickle('fpi_listed.pkl')
# what share of the 18-Mar Form 3 wave issuers are in the FPI universe
m = d[(d.POR == '2026-03-18') & d.dt.isin(['3','3/A'])]
ci = m.cikn.unique()
print('\n18-Mar form-3 issuers', len(ci), 'in FPI universe', u[u.fpi].cikn.isin(ci).sum(), 'in domestic', u[u.dom].cikn.isin(ci).sum(), 'not in DERA universe', len(set(ci) - set(u.cikn)))
