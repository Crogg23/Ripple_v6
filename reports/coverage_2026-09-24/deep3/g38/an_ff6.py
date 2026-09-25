import pandas as pd, numpy as np
pd.set_option('display.width', 260)
raw = pd.read_csv('out_S18.csv', dtype=str)
raw['js'] = pd.to_datetime(raw.JOBSTARTDATE, format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
raw['je'] = pd.to_datetime(raw.JOBENDDATE, format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
print('raw rows', len(raw), 'blank start', raw.JOBSTARTDATE.isna().sum(), 'unparsed start', (raw.js.isna() & raw.JOBSTARTDATE.notna()).sum(), 'range', raw.js.min(), raw.js.max())
print('start after end', (raw.js > raw.je).sum(), 'start > 2026-09-24', (raw.js > '2026-09-24').sum(), 'before 2008', (raw.js < '2008-01-01').sum())
v = pd.read_csv('out_S15.csv', dtype={'API_NUMBER': str}).merge(raw[['DISCLOSUREID','js']], left_on='DISCLOSURE_ID', right_on='DISCLOSUREID', how='left')
v['yr'] = v.js.dt.year
print(pd.crosstab(v.yr, v.FF_VERSION.astype(str)).tail(12))
print('v4 water reporting by year', v[v.FF_VERSION.astype(str)=='4'].groupby('yr').HAS_WATER.mean().round(2).tail(8).to_dict())
d = pd.read_pickle('ff_disc.pkl').merge(raw[['DISCLOSUREID','js']], left_on='DISCLOSURE_ID', right_on='DISCLOSUREID', how='left')
d['yr'] = d.js.dt.year; d['cty'] = d.state + '|' + d.county.str.upper().str.strip()
v4 = v[v.FF_VERSION.astype(str)=='4'].copy(); v4['cty'] = v4.STATE_NAME + '|' + v4.COUNTY_NAME.str.upper().str.strip()
rep = v4.groupby(['cty','OPERATOR_NAME']).HAS_WATER.mean().rename('rate').reset_index().rename(columns={'OPERATOR_NAME':'op'})
d = d.merge(rep, on=['cty','op'], how='left')
permian = ['Texas|MIDLAND','Texas|MARTIN','Texas|ANDREWS','Texas|HOWARD','Texas|GLASSCOCK','Texas|REEVES','Texas|UPTON','Texas|REAGAN','Texas|LOVING','Texas|WARD','Texas|ECTOR','Texas|CULBERSON','Texas|WINKLER','New Mexico|LEA','New Mexico|EDDY']
P = d[d.cty.isin(permian) & (d.rate >= 0.9)].copy()
P['db'] = P.op == 'Diamondback E&P LLC'
t = P.groupby(['yr','db']).agg(n=('api','size'), gal=('vol','sum'), gw=('gw_gal','sum')).reset_index()
t['gw_share'] = (t.gw/t.gal).round(3); t['gal_B'] = (t.gal/1e9).round(2); t['gw_B'] = (t.gw/1e9).round(2)
print(t.pivot(index='yr', columns='db', values=['n','gw_share','gw_B']))
# Midland county by year
M = P[P.cty == 'Texas|MIDLAND']
print(M.groupby(['yr','db']).apply(lambda g: pd.Series({'n': len(g), 'gw_share': round(g.gw_gal.sum()/g.vol.sum(),3)})).unstack())
d.to_pickle('ff_disc_dated.pkl')
