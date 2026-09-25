"""g58: local analysis of S12, revoked-despite-filing candidates."""
import pandas as pd, re, numpy as np
d = pd.read_csv('out_S12.csv', dtype=str, keep_default_na=False)
d['D'] = pd.to_datetime(d.D); d['SUB'] = pd.to_datetime(d.SUB_DATE)
d['p'] = pd.to_datetime(d.TAX_PERIOD + '01', format='%Y%m%d')
d['yo'] = d.SUB_DATE_RAW.str.strip().str.fullmatch(r'\d{4}')
lo = d.D - pd.DateOffset(months=40); hi = d.D - pd.DateOffset(months=5)
d['inwin'] = d.RETURN_TYPE.isin(['990', '990EZ', '990PF']) & (d.p >= lo) & (d.p <= hi)
d['before'] = (d.SUB.dt.year < d.D.dt.year) | ((~d.yo) & (d.SUB < d.D))
d['hitrow'] = d.inwin & d.before
# expected period-end month for the 3 missed returns: 15th of 5th month after FYE -> FYE month = D month - 5
d['exp_m'] = ((d.D.dt.month - 5 - 1) % 12) + 1
d['same_fye'] = d.p.dt.month == d.exp_m
# the three exact missed periods: D-5m, D-17m, D-29m (month level)
def exact(row):
    for k in (5, 17, 29):
        t = row.D - pd.DateOffset(months=k)
        if row.p.year == t.year and row.p.month == t.month:
            return True
    return False
d['exact3'] = d.apply(exact, axis=1)
h = d[d.hitrow]
e = h.groupby('EIN').agg(name=('LEGAL_NAME', 'first'), idx=('TAXPAYER_NAME', 'first'), st=('STATE', 'first'), D=('D', 'first'),
                         rd=('RD', 'first'), n=('hitrow', 'size'), exact=('exact3', 'any'), same=('same_fye', 'any'),
                         types=('RETURN_TYPE', lambda s: ','.join(sorted(set(s)))), tp=('TAX_PERIOD', lambda s: ','.join(sorted(set(s)))),
                         sub=('SUB_DATE_RAW', lambda s: ' | '.join(sorted(set(s)))))
print('EINs', len(e))
print('exact one of the 3 periods', e.exact.sum(), ' FYE month matches revocation calendar', e.same.sum())
# name agreement: first word overlap (normalize)
def norm(s):
    s = re.sub(r'[^A-Z0-9 ]', ' ', s.upper()); return set(w for w in s.split() if w not in {'INC','THE','OF','AND','CORP','CORPORATION','FOUNDATION','ASSOCIATION','CLUB','CO','LLC','FUND','USA','AMERICA','AMERICAN','INTERNATIONAL','A','FOR','IN','TRUST','ASSN','SOCIETY','CHAPTER','CENTER'})
def agree(r):
    a, b = norm(r['name']), norm(r['idx']); return len(a & b) > 0
e['name_agree'] = e.apply(agree, axis=1)
print('name agrees (a shared non-filler word)', e.name_agree.sum())
e['reinst'] = e.rd != ''
e['retro'] = e.rd == e.D.dt.strftime('%Y-%m-%d')
core = e[e.exact & e.name_agree]
print('core = exact missed period + name agrees:', len(core), ' reinstated', core.reinst.sum(), ' retro', core.retro.sum())
print(core.groupby(core.D.dt.year).size().to_string())
print(core.groupby(core.D.dt.strftime('%Y-%m-%d')).size().sort_values(ascending=False).head(10).to_string())
print(core.types.value_counts().head().to_string())
print(core.st.value_counts().head(8).to_string())
e.to_csv('hits_by_ein.csv')
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 45)
print(core.sample(15, random_state=1)[['name', 'idx', 'st', 'D', 'rd', 'types', 'tp', 'sub']].to_string())
