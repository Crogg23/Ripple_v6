import pandas as pd, numpy as np
d = pd.read_csv('out_K03.csv')
d['fl'] = d.LOW >= 0.5*d.LINES
print('no-sub rows', d.S_N.isna().sum(), 'accessions in 2+ windows', (d.N_WINDOWS>1).sum())
f = d[d.fl].copy(); f['gap'] = f.V*999
f['yr'] = f.PER.str[-4:]
g = f.groupby('W').agg(flagged=('A','size'), ciks=('CIK','nunique'), gapT=('gap', lambda s: round(s.sum()/1e12,3)),
    hr=('ST', lambda s: (s=='13F-HR').sum()), chk=('W_CHECKED','first'), hrchk=('W_HR_CHECKED','first'))
# originals only
o = f[f.ST=='13F-HR'].groupby('W').agg(hr_fl=('A','size'), hr_gapT=('gap', lambda s: round(s.sum()/1e12,3)))
g = g.join(o)
g['rate_all'] = (g.flagged/g.chk).round(4); g['rate_hr'] = (g.hr_fl/g.hrchk).round(4)
order = ['01jan2024-29feb2024','01mar2024-31may2024','01jun2024-31aug2024','01sep2024-30nov2024','01dec2024-28feb2025','01mar2025-31may2025','01jun2025-31aug2025','01sep2025-30nov2025','01dec2025-28feb2026','01mar2026-31may2026']
g.index = g.index.str.replace('_form13f.zip','')
print(g.loc[order].to_string())
print('median of per-filing med_r_low, all windows', f.MED_R_LOW.median(), f.MED_R_LOW.quantile([.05,.95]).tolist())
# persistence
wins = f.groupby('CIK').W.nunique()
print('distinct flagged CIKs across 10 windows', len(wins), 'flagged in 8+ windows', (wins>=8).sum(), 'in all 10', (wins==10).sum(), 'in exactly 1', (wins==1).sum())
# T Rowe
t = d[d.CIK==80255].sort_values('W')
print(t[['W','A','LINES','LOW','V','ST','PER','N_WINDOWS']].to_string())
