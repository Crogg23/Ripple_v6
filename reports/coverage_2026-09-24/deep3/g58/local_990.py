"""g58 local math for the 990 lead (no warehouse calls). Reads out_S10, out_S12, out_S14, out_S15.

Recomputes: 470 candidates -> 111 core -> 110 strict core, the per-1,000 time series,
the BMF peer comparison, and the 61 still-revoked-and-off-the-master-list.
Rule used: auto-revocation date D is the due date of the third missed return. For a tax year
ending in month M the due date is the 15th of month M+5, so the three missed tax years end
exactly 5, 17 and 29 months before D. 'Before D' = processed in an earlier calendar year than D
(works for year-only index rows), or a full timestamp earlier than D.
"""
import re
from difflib import SequenceMatcher

import pandas as pd

d = pd.read_csv('out_S12.csv', dtype=str, keep_default_na=False)
d['D'] = pd.to_datetime(d.D)
d['SUB'] = pd.to_datetime(d.SUB_DATE)
d['p'] = pd.to_datetime(d.TAX_PERIOD + '01', format='%Y%m%d')
d['pend'] = d.p + pd.offsets.MonthEnd(0)
d['yo'] = d.SUB_DATE_RAW.str.strip().str.fullmatch(r'\d{4}')
d['k'] = (d.D.dt.year - d.p.dt.year) * 12 + d.D.dt.month - d.p.dt.month
d['before'] = (d.SUB.dt.year < d.D.dt.year) | ((~d.yo) & (d.SUB < d.D))
d['impossible'] = ((~d.yo) & (d.SUB < d.pend)) | (d.yo & (d.SUB.dt.year < d.p.dt.year))
d['hit'] = d.RETURN_TYPE.isin(['990', '990EZ', '990PF']) & d.k.isin([5, 17, 29]) & d.before & ~d.impossible
print('candidate EINs (S10/S12 loose window 5-40 months):', d.EIN.nunique())

h = d[d.hit]
e = h.groupby('EIN').agg(name=('LEGAL_NAME', 'first'), idx=('TAXPAYER_NAME', 'first'), st=('STATE', 'first'),
                         D=('D', 'first'), rd=('RD', 'first'), ks=('k', lambda s: sorted(set(s))))


def norm(s):
    s = re.sub(r'[^A-Z0-9 ]', ' ', s.upper())
    stop = {'INC', 'THE', 'OF', 'AND', 'CORP', 'CORPORATION', 'FOUNDATION', 'ASSOCIATION', 'CLUB', 'CO', 'LLC', 'FUND',
            'USA', 'AMERICA', 'AMERICAN', 'INTERNATIONAL', 'A', 'FOR', 'IN', 'TRUST', 'ASSN', 'SOCIETY', 'CHAPTER', 'CENTER'}
    return set(w for w in s.split() if w not in stop)


e['name_agree'] = [len(norm(a) & norm(b)) > 0 for a, b in zip(e.name, e.idx)]
n2 = lambda x: ' '.join(re.sub(r'\b(INC|THE|CORP|CORPORATION|LTD)\b', '', re.sub(r'[^A-Z0-9 ]', '', x.upper())).split())
e['ratio'] = [SequenceMatcher(None, n2(a), n2(b)).ratio() for a, b in zip(e.name, e.idx)]
core = e[e.name_agree].copy()
b = pd.read_csv('out_S14.csv', dtype=str, keep_default_na=False)
core['in_bmf'] = core.index.isin(set(b[b.ORG_NAME != ''].EIN))
core['reinst'] = core.rd != ''
print('strict core (exact missed year, filed before D, possible period, name agrees):', len(core), ' near-identical names (>=0.85):', (core.ratio >= 0.85).sum())
print('  reinstated on the list:', core.reinst.sum(), ' same-day (retroactive):', (core.rd == core.D.dt.strftime('%Y-%m-%d')).sum())
print('  not reinstated:', (~core.reinst).sum(), ' of those on EO BMF today:', (core.in_bmf & ~core.reinst).sum(),
      ' off BMF:', (~core.in_bmf & ~core.reinst).sum())
print('  filed both checkable missed years (k=17 and k=29):', core.ks.apply(lambda s: {17, 29} <= set(s)).sum())

s15 = pd.read_csv('out_S15.csv')
den = s15.groupby('REV_Y').N.sum()
num = core.groupby(core.D.dt.year).size().reindex(den.index, fill_value=0)
print(pd.DataFrame({'revoked_efilers': den, 'strict_core': num, 'per_1000': (num / den * 1000).round(2)}).to_string())
for a, z in ((2019, 2021), (2019, 2022), (2023, 2025)):
    print(f'  {a}-{z}: {num.loc[a:z].sum()} of {den.loc[a:z].sum()} = {num.loc[a:z].sum() / den.loc[a:z].sum() * 1000:.2f} per 1,000')

nr = s15[~s15.REINSTATED].groupby('GRP')[['N', 'IN_BMF', 'BMF_NEW_RULING']].sum()
nr['pct_on_bmf'] = (nr.IN_BMF / nr.N * 100).round(1)
nr['pct_old_ruling_of_on_bmf'] = ((nr.IN_BMF - nr.BMF_NEW_RULING) / nr.IN_BMF * 100).round(1)
print(nr.to_string())
core.to_csv('core_strict_recomputed.csv')
