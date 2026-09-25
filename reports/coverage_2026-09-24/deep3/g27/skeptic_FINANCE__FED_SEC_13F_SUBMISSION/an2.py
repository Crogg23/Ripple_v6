import pandas as pd, numpy as np
d = pd.read_csv('out_K02.csv')
print('rows', len(d), 'n_checked', d.N_CHECKED.iloc[0], 'q1 orig checked', d.N_Q1_ORIG_CHECKED.iloc[0], 'v_all', d.V_ALL.iloc[0])
print('dup joins s_n>1:', (d.S_N>1).sum(), 'f_n>1:', (d.F_N>1).sum(), 'no sub:', d.S_N.isna().sum())
fl = d[d.LOW >= 0.5*d.LINES].copy()
print('flagged', len(fl), 'distinct cik', fl.CIK.nunique())
fl['gap'] = fl.V*999
print('gap total $T', fl.gap.sum()/1e12)
print(fl.groupby(['ST']).agg(n=('A','size'), gapT=('gap', lambda s: s.sum()/1e12)))
fl['q'] = np.where(fl.PER=='31-MAR-2026','Q1-2026','older')
print(fl.groupby(['ST','q','AMT'], dropna=False).agg(n=('A','size'), gapT=('gap', lambda s: s.sum()/1e12)))
# per-period
print(fl.groupby('PER').agg(n=('A','size'), gapT=('gap', lambda s: s.sum()/1e12)).sort_values('n', ascending=False).head(15))
# ciks with >1 flagged filing
c = fl.groupby('CIK').agg(n=('A','size'), gapT=('gap', lambda s: s.sum()/1e12), nm=('NM','first')).sort_values('n', ascending=False)
print('ciks with 2+ flagged filings', (c.n>1).sum(), 'filings', c[c.n>1].n.sum(), 'gap in those ciks $T', c[c.n>1].gapT.sum())
print(c.head(12))
# clean set: Q1 2026 original 13F-HR only
cl = fl[(fl.ST=='13F-HR') & (fl.PER=='31-MAR-2026')]
print('CLEAN Q1-2026 originals flagged', len(cl), 'of', d.N_Q1_ORIG_CHECKED.iloc[0], 'gap $T', cl.gap.sum()/1e12)
# median ratio among flagged
print('median of per-filing MED_R_LOW (flagged):', fl.MED_R_LOW.median(), 'quantiles', fl.MED_R_LOW.quantile([.05,.25,.5,.75,.95]).tolist())
print('share of low lines near 1/1000 (0.0005-0.002):', fl.NEAR_K.sum()/fl.LOW.sum())
fl['vfix'] = fl.V*1000
print('median unit corrected $M', fl.vfix.median()/1e6, 'median lines', fl.LINES.median())
fl = fl.sort_values('gap', ascending=False)
fl['cum'] = fl.gap.cumsum()/fl.gap.sum()
print('top1 share', fl.gap.iloc[0]/fl.gap.sum(), 'top5', fl.gap.iloc[:5].sum()/fl.gap.sum(), 'top20', fl.gap.iloc[:20].sum()/fl.gap.sum(), 'n for 80%', (fl.cum<0.8).sum()+1)
print('gap without T Rowe entities $T', fl[~fl.NM.str.contains('ROWE|Rowe', na=False)].gap.sum()/1e12)
# unflagged filings with low lines
uf = d[(d.LOW < 0.5*d.LINES) & (d.LOW>0)]
print('unflagged filings with some low lines', len(uf), 'low lines', uf.LOW.sum(), 'v_low*999 $T', uf.V_LOW.sum()*999/1e12)
print(uf.sort_values('V_LOW', ascending=False)[['A','LINES','LOW','V_LOW','MED_R_LOW','NM','ST','PER']].head(12).to_string())
hi = d[d.HIGH>0]
print('filings with high lines', len(hi), 'high lines', hi.HIGH.sum(), 'v_high $T', hi.V_HIGH.sum()/1e12)
print(hi.sort_values('V_HIGH', ascending=False)[['A','LINES','HIGH','V_HIGH','NM']].head(8).to_string())
# mixed
mx = d[(d.LOW + d.HIGH >= 50) & (d.LOW < 0.5*d.LINES)]
print('mixed', len(mx)); print(mx[['A','LINES','LOW','HIGH','V','NM']].to_string())
# flagged with lines between 0.5 and 0.9 low
print('flagged low share dist', (fl.LOW/fl.LINES).describe())
print(fl[(fl.LOW/fl.LINES)<0.9][['A','LINES','LOW','V','MED_R','NM','ST']].to_string())
