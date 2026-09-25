"""g20 local analysis: recomputes every headline number from the r*.json pulls. No warehouse calls."""
import sys; sys.path.insert(0, '.')
from load import df
import pandas as pd, numpy as np

# ---------- FJC_APPOINTMENT (r01) + Voteview meta (r04) + party votes (r10)
a = df(1)
for c in ['NOMINATION_DATE', 'CONFIRMATION_DATE']: a[c + '_d'] = pd.to_datetime(a[c], errors='coerce')
m = a.AYES_NAYS.str.extract(r'^\s*(\d+)\s*/+\s*(\d+)\s*$')
a['ayes'] = pd.to_numeric(m[0]); a['nays'] = pd.to_numeric(m[1])
a['pres'] = a.APPOINTING_PRESIDENT
t = a.pres == 'Donald J. Trump'
a.loc[t & (a.NOMINATION_DATE_d >= '2025-01-20'), 'pres'] = 'Trump (2nd)'
a.loc[t & (a.NOMINATION_DATE_d < '2025-01-20'), 'pres'] = 'Trump (1st)'
a['days'] = (a.CONFIRMATION_DATE_d - a.NOMINATION_DATE_d).dt.days
art3 = a[a.COURT_TYPE.isin(['U.S. District Court', 'U.S. Court of Appeals', 'Supreme Court'])]
print(art3.groupby('pres').agg(n=('NID', 'size'), recorded=('ayes', lambda s: s.notna().mean()),
      med_nays=('nays', 'median'), med_days=('days', 'median')).loc[
      ['William J. Clinton', 'George W. Bush', 'Barack Obama', 'Trump (1st)', 'Joseph R. Biden', 'Trump (2nd)']].round(3))

v = df(4)
v['d'] = pd.to_datetime(v.DATE); v['CONGRESS'] = v.CONGRESS.astype(int)
for c in ['YEA_COUNT', 'NAY_COUNT', 'ROLLNUMBER']: v[c] = pd.to_numeric(v[c])
s = v[(v.CHAMBER == 'Senate') & (v.VOTE_QUESTION.fillna('') == 'On the Nomination')]
r = a[a.ayes.notna() & (a.CONFIRMATION_DATE_d >= '1989-01-03')]
j = r.merge(s, left_on='CONFIRMATION_DATE_d', right_on='d')
j = j[(j.YEA_COUNT == j.ayes) & (j.NAY_COUNT == j.nays)]
print('FJC recorded votes since 1989 with exact same-day Voteview tally:', j[['NID', 'SEQUENCE']].drop_duplicates().shape[0], 'of', len(r))

pv = df(10)
for c in ['CONGRESS', 'ROLLNUMBER', 'YEA', 'NAY']: pv[c] = pd.to_numeric(pv[c])
w = pv.pivot_table(index=['CONGRESS', 'ROLLNUMBER'], columns=pv.PARTY_CODE.fillna('NA'), values=['YEA', 'NAY'], aggfunc='sum', fill_value=0)
w.columns = [f'{x}_{y}' for x, y in w.columns]; w = w.reset_index()
j = j[j.CONFIRMATION_DATE_d >= '2023-01-03'].copy()
j['last'] = j.JUDGE_NAME.str.split(',').str[0].str.upper()
j = j[[l in str(d).upper() for l, d in zip(j['last'], j.VOTE_DESC)]].drop_duplicates(['NID', 'SEQUENCE']).merge(w, on=['CONGRESS', 'ROLLNUMBER'])
tr = j.pres.str.startswith('Trump')
j['opp_yea'] = np.where(tr, j.YEA_100 + j.YEA_328, j.YEA_200)
print(j.groupby('pres').agg(n=('NID', 'size'), zero_opp=('opp_yea', lambda s: (s == 0).sum()), med_opp=('opp_yea', 'median')))

# ---------- Voteview time comparisons
v['yr'] = v.d.dt.year
sen = v[v.CHAMBER == 'Senate']; hou = v[v.CHAMBER == 'House']
print('Senate top years:', sen.groupby('yr').size().sort_values(ascending=False).head(3).to_dict())
pn = sen[sen.BILL_NUMBER.fillna('').str.startswith('PN')].groupby('yr').size()
print('Senate PN roll calls top years:', pn.sort_values(ascending=False).head(3).to_dict())
h = hou.groupby('yr').size(); print('House odd years since 1973, lowest:', h[(h.index % 2 == 1) & (h.index >= 1973)].sort_values().head(3).to_dict())

# ---------- IRS527 related (r05)
rel = df(5)
nw = rel.ORG_NAME.str.upper().str.contains('NATIONWIDE')
print('Nationwide rows:', nw.sum(), 'of', len(rel))

# ---------- Freedom House (r02)
f = df(2); f['TOTAL'] = pd.to_numeric(f.TOTAL); f['ED'] = f.EDITION.astype(int)
p = f.pivot_table(index=['COUNTRY_TERRITORY', 'C_T'], columns='ED', values='TOTAL').reset_index()
peer = p[(p[2013] >= 85) & (p.C_T == 'c')].copy(); peer['d'] = peer[2025] - peer[2013]
print('85+ peers:', len(peer), 'median change', peer.d.median(), '| worst 5:', peer.sort_values('d').head(5)[['COUNTRY_TERRITORY', 'd']].values.tolist())

# ---------- Blue-slip test (r20): crossover by home-state Senate delegation, district judges only
sd = df(20); sd['CONGRESS'] = sd.CONGRESS.astype(int)
deleg = sd.groupby(['CONGRESS', 'STATE_ABBREV']).PARTY_CODE.agg(
    lambda s: 'RR' if set(s) == {'200'} else ('DD' if '200' not in set(s) else 'split')).rename('deleg').reset_index()
ST = {'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY','Puerto Rico':'PR','Columbia':'DC','Guam':'GU','Virgin Islands':'VI','Northern Mariana Islands':'MP'}
dj = j[j.COURT_TYPE == 'U.S. District Court'].copy()
dj['st'] = dj.COURT_NAME.map(lambda c: next((v for k, v in ST.items() if c.endswith(k)), None))
dj = dj.merge(deleg, left_on=['CONGRESS', 'st'], right_on=['CONGRESS', 'STATE_ABBREV'], how='left')
print(dj.groupby(['pres', 'deleg']).agg(n=('NID', 'size'), zero_opp=('opp_yea', lambda s: (s == 0).sum()), med_opp=('opp_yea', 'median')))
