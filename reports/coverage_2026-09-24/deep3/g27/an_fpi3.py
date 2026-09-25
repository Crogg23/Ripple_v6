import pandas as pd, numpy as np
from math import comb
def fisher_exact(t):
    (a, b), (c, d) = t
    r1, r2, c1, n = a + b, c + d, a + c, a + b + c + d
    p = lambda x: comb(r1, x) * comb(r2, c1 - x) / comb(n, c1)
    p0 = p(a)
    lo, hi = max(0, c1 - r2), min(r1, c1)
    return (None, sum(p(x) for x in range(lo, hi + 1) if p(x) <= p0 * (1 + 1e-9)))
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 300); pd.set_option('display.max_colwidth', 45)
N = pd.read_pickle('fpi_nonexempt.pkl')
a = pd.read_pickle('out_S07.pkl'); a.columns = [c.upper() for c in a.columns]; a['cikn'] = pd.to_numeric(a.CIKN)
N = N.join(a.set_index('cikn').AFS, on='cikn')
N['AFS'] = N.AFS.fillna('?')
N['grp'] = np.where(N.ba.isin(['CN','HK']), 'China/HK address', 'other non-exempt')
print(pd.crosstab([N.AFS], N.grp, values=N.has3, aggfunc=['size','sum','mean']).round(3).to_string())
for afs in ['1-LAF','2-ACC','4-NON']:
    s = N[N.AFS == afs]
    t = pd.crosstab(s.grp, s.has3)
    if t.shape == (2,2):
        print(afs, 'fisher p', fisher_exact(t.values)[1])
t = pd.crosstab(N.grp, N.has3); print('all sizes fisher p', fisher_exact(t.values)[1], t.to_string())
# within non-accelerated (small) filers, by BA country
s = N[N.AFS == '4-NON']
g = s.groupby('ba').has3.agg(['size','sum','mean']).round(3)
print('\n4-NON by country n>=5'); print(g[g['size'] >= 5].sort_values('size', ascending=False).to_string())
# big China/HK misses: large accelerated or accelerated
print('\nChina/HK misses that are large accelerated or accelerated filers:')
print(N[(N.grp == 'China/HK address') & ~N.has3 & N.AFS.isin(['1-LAF','2-ACC'])][['CIKN','NAME','inc','AFS','TICKERS','EXCHANGES','LAST_FILED']].to_string())
print('\nother non-exempt misses that are LAF/ACC:')
print(N[(N.grp != 'China/HK address') & ~N.has3 & N.AFS.isin(['1-LAF','2-ACC'])][['CIKN','NAME','inc','ba','AFS','TICKERS','EXCHANGES']].to_string())
# lateness: first Form 3 after deadline
h = N[N.has3].copy(); h['late_first'] = h.first3 > '2026-03-18'
print('\nshare of filers whose FIRST Form 3 came after 18 Mar, by group:'); print(h.groupby('grp').late_first.agg(['size','sum','mean']).round(3).to_string())
# name all China/HK misses count by exchange
m = N[(N.grp == 'China/HK address') & ~N.has3]
print('\nChina/HK misses', len(m), 'by exchange', m.EXCHANGES.value_counts().to_dict(), 'by AFS', m.AFS.value_counts().to_dict())
N.to_pickle('fpi_nonexempt_afs.pkl')
