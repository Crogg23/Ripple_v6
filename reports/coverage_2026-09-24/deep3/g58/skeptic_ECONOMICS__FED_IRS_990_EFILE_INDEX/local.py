import re, pandas as pd, numpy as np, warnings
warnings.filterwarnings('ignore')
d = pd.read_csv('out_Q1.csv', dtype=str, keep_default_na=False)
d['D'] = pd.to_datetime(d.D); d['SUB'] = pd.to_datetime(d.SUB_DATE); d['k'] = d.K.astype(int)
d['yo'] = d.SUB_DATE_RAW.str.strip().str.fullmatch(r'\d{4}')
d['p'] = pd.to_datetime(d.TAX_PERIOD + '01', format='%Y%m%d'); d['pend'] = d.p + pd.offsets.MonthEnd(0)
d['jul'] = d.DLN.str[5:8].astype(int); d['yd'] = d.DLN.str[13].astype(int)
sy = d.SUB.dt.year; d['dy'] = sy + (((d.yd - sy % 10 + 5) % 10) - 5)
d['rcv'] = pd.to_datetime(d.dy.astype(str) + '-01-01') + pd.to_timedelta(d.jul - 1, unit='D')
d['before_sub'] = (d.SUB.dt.year < d.D.dt.year) | ((~d.yo) & (d.SUB < d.D))
d['before_rcv'] = d.rcv < d.D
d['imp_builder'] = ((~d.yo) & (d.SUB < d.pend)) | (d.yo & (d.SUB.dt.year < d.p.dt.year))
d['imp_rcv'] = d.rcv < d.pend
def norm(s):
    s = re.sub(r'[^A-Z0-9 ]', ' ', s.upper())
    stop = {'INC','THE','OF','AND','CORP','CORPORATION','FOUNDATION','ASSOCIATION','CLUB','CO','LLC','FUND','USA','AMERICA','AMERICAN','INTERNATIONAL','A','FOR','IN','TRUST','ASSN','SOCIETY','CHAPTER','CENTER'}
    return set(w for w in s.split() if w not in stop)
d['name_ok'] = [len(norm(a) & norm(b)) > 0 for a, b in zip(d.LEGAL_NAME, d.TAXPAYER_NAME)]
B = ['990','990EZ','990PF']; ALL = B + ['990O','990EO','990PR']
print('Q1 rows', len(d), 'EINs', d.EIN.nunique(), ' types', d.RETURN_TYPE.value_counts().to_dict())
def hits(forms, before, imp):
    x = d[d.RETURN_TYPE.isin(forms) & d[before] & ~d[imp] & d.name_ok]
    return x.groupby('EIN').agg(D=('D','first'), rd=('RD','first'), ks=('k', lambda s: tuple(sorted(set(s)))))
v = {'builder (labels B, SUB rule, builder impossible)': hits(B,'before_sub','imp_builder'),
     'B, SUB rule, DLN impossible': hits(B,'before_sub','imp_rcv'),
     'ALL labels, SUB rule, DLN impossible': hits(ALL,'before_sub','imp_rcv'),
     'B, DLN receipt rule, DLN impossible': hits(B,'before_rcv','imp_rcv'),
     'ALL labels, DLN receipt rule, DLN impossible': hits(ALL,'before_rcv','imp_rcv')}
den = pd.read_csv('out_Q2.csv').set_index('REV_Y')
for name, h in v.items():
    nr = h[h.rd == '']
    print(f'\n== {name}: {len(h)} EINs, not reinstated {len(nr)}')
    y = h.groupby(h.D.dt.year).size().reindex(den.index, fill_value=0)
    dcol = 'EFILER_ALL_LABELS' if name.startswith('ALL') else 'EFILER_BUILDER_LABELS'
    t = pd.DataFrame({'hits': y, 'den': den[dcol], 'per1000': (y / den[dcol] * 1000).round(2), 'per1000_all_revoked': (y / den.ROWS_ALL * 1000).round(3)})
    print(t.to_string())
    a = y.loc[2019:2021].sum() / den[dcol].loc[2019:2021].sum() * 1000; b = y.loc[2023:2025].sum() / den[dcol].loc[2023:2025].sum() * 1000
    print(f'  2019-21 {a:.2f}  2023-25 {b:.2f}  ratio {b/a:.1f}x')
core = pd.read_csv('../core_strict_recomputed.csv', dtype=str, keep_default_na=False)
hb = v['builder (labels B, SUB rule, builder impossible)']
print('\nbuilder re-derivation vs builder file: mine', len(hb), ' theirs', len(core), ' in both', len(set(hb.index) & set(core.EIN)),
      ' only mine', sorted(set(hb.index) - set(core.EIN)), ' only theirs', sorted(set(core.EIN) - set(hb.index)))
# fair time denominator: EINs with ANY exact-k missed-year return in the index (visible), share received before D
vis = d[d.RETURN_TYPE.isin(ALL) & ~d.imp_rcv & d.name_ok]
g = vis.groupby('EIN').agg(D=('D','first'), anyb=('before_rcv','max'), anyb_sub=('before_sub','max'))
t = g.groupby(g.D.dt.year).agg(visible=('anyb','size'), before_rcv=('anyb','sum'), before_sub=('anyb_sub','sum'))
t['pct_before_rcv'] = (t.before_rcv / t.visible * 100).round(1); t['pct_before_sub'] = (t.before_sub / t.visible * 100).round(1)
print('\nFAIR DENOMINATOR: revoked EINs with an e-filed return for an exact missed year (any time), share received before D')
print(t.to_string())
a = t.loc[2019:2021]; b = t.loc[2023:2025]
print(f'  2019-21 {a.before_rcv.sum()}/{a.visible.sum()} = {a.before_rcv.sum()/a.visible.sum()*100:.1f}%   2023-25 {b.before_rcv.sum()}/{b.visible.sum()} = {b.before_rcv.sum()/b.visible.sum()*100:.1f}%')
v['ALL labels, DLN receipt rule, DLN impossible'].to_csv('hits_all_dln.csv')
d.to_pickle('q1.pkl')
