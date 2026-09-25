import pandas as pd, numpy as np
pd.set_option('display.width', 260); pd.set_option('display.max_colwidth', 44)
w = pd.read_csv('out_S14.csv', dtype={'API_NUMBER': str})
d = pd.read_pickle('ff_disc.pkl').join(w.groupby('DISCLOSURE_ID')[['LATITUDE','LONGITUDE','WELL_NAME']].first(), on='DISCLOSURE_ID')
d['cty'] = d.state + '|' + d.county.str.upper().str.strip()
v = pd.read_csv('out_S15.csv', dtype={'API_NUMBER': str}); v = v[v.FF_VERSION.astype(str) == '4']
v['cty'] = v.STATE_NAME + '|' + v.COUNTY_NAME.str.upper().str.strip()
rep = v.groupby(['cty','OPERATOR_NAME']).HAS_WATER.mean().rename('rate').reset_index().rename(columns={'OPERATOR_NAME':'op'})
d = d.merge(rep, on=['cty','op'], how='left')
d['gws'] = (d.gw/d.tot).clip(0,1)
db = d[d.op == 'Diamondback E&P LLC']
print('Diamondback wells', len(db), 'gal B', round(db.vol.sum()/1e9,2), 'fresh B', round(db.fresh_gal.sum()/1e9,2), 'fresh gw B', round(db.gw_gal.sum()/1e9,2))
print(db.groupby('cty').agg(n=('api','size'), gwB=('gw_gal', lambda x: round(x.sum()/1e9,2)), gws_gal=('gw_gal','sum'), gal=('vol','sum'), med_well_gws=('gws','median'), share_wells_any_gw=('gws', lambda x: (x>0).mean()), share_wells_all_gw=('gws', lambda x: (x>=0.99).mean())).assign(gws_gal=lambda x: (x.gws_gal/x.gal).round(3)).drop(columns='gal').sort_values('n', ascending=False))
# 5-mile complete-reporter peers for Diamondback Midland and Martin
R = 3958.8
def peer5(me, oth):
    p1 = np.radians(me.LATITUDE.values)[:, None]; l1 = np.radians(me.LONGITUDE.values)[:, None]
    p2 = np.radians(oth.LATITUDE.values)[None, :]; l2 = np.radians(oth.LONGITUDE.values)[None, :]
    dd = 2*R*np.arcsin(np.sqrt(np.sin((p2-p1)/2)**2 + np.cos(p1)*np.cos(p2)*np.sin((l2-l1)/2)**2))
    m = (dd <= 5).any(0)
    o = oth[m]
    return len(o), o.op.nunique(), round(o.gw_gal.sum()/o.vol.sum(), 3), o.groupby('op').size().sort_values(ascending=False).head(5).to_dict()
permian = ['Texas|MIDLAND','Texas|MARTIN','Texas|ANDREWS','Texas|HOWARD','Texas|GLASSCOCK','Texas|REEVES','Texas|UPTON','Texas|REAGAN','Texas|LOVING','Texas|WARD','Texas|ECTOR','Texas|CULBERSON','Texas|WINKLER','New Mexico|LEA','New Mexico|EDDY']
P = d[d.cty.isin(permian)]
comp = P[(P.rate >= 0.9)]
me = comp[comp.op == 'Diamondback E&P LLC']; oth = comp[comp.op != 'Diamondback E&P LLC']
print('Diamondback Permian complete-reporter wells', len(me), 'gw share', round(me.gw_gal.sum()/me.vol.sum(),3), '| 5mi complete-reporter peers', peer5(me, oth))
for c in ['Texas|MIDLAND','Texas|MARTIN']:
    m1 = me[me.cty == c]; print(c, len(m1), round(m1.gw_gal.sum()/m1.vol.sum(),3), peer5(m1, oth))
# Permian operators ranked by fresh groundwater gallons, complete reporters only
r = comp.groupby('op').agg(n=('api','size'), gal=('vol','sum'), gw=('gw_gal','sum'), fr=('fresh_gal','sum'))
r['gw_share'] = r.gw/r.gal; r['fresh_share'] = r.fr/r.gal
print('Permian complete reporters total gal B', round(r.gal.sum()/1e9,1), 'gw B', round(r.gw.sum()/1e9,2), 'gw share', round(r.gw.sum()/r.gal.sum(),3))
print(r[r.n >= 50].sort_values('gw', ascending=False).assign(gal=lambda x:(x.gal/1e9).round(2), gw=lambda x:(x.gw/1e9).round(2), fr=lambda x:(x.fr/1e9).round(2)).round(3).head(15).to_string())
print('median op gw_share (n>=50)', round(r[r.n>=50].gw_share.median(),3), 'ops', (r.n>=50).sum())
# without Martin: does Diamondback stay above?
nm = me[me.cty != 'Texas|MARTIN']; print('Diamondback ex-Martin gw share', round(nm.gw_gal.sum()/nm.vol.sum(),3), len(nm))
print('--- per county, Diamondback vs complete-reporter wells within 5 miles')
for c in me.cty.value_counts().index:
    m1 = me[me.cty == c]
    n, k, s, _ = peer5(m1, oth)
    print(c, len(m1), round(m1.gw_gal.sum()/m1.vol.sum(),3), 'peers', n, k, s)
# placebo: same test for every other complete-reporter operator with >=100 Permian wells
print('--- same 5-mile test for other big operators')
for op, g in comp.groupby('op'):
    if len(g) >= 100 and op != 'Diamondback E&P LLC':
        o2 = comp[comp.op != op]
        n, k, s, _ = peer5(g, o2)
        print(op, len(g), round(g.gw_gal.sum()/g.vol.sum(),3), 'peers', n, k, s)
