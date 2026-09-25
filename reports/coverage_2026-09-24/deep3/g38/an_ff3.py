import pandas as pd, numpy as np
pd.set_option('display.width', 260); pd.set_option('display.max_colwidth', 42); pd.set_option('display.max_columns', 20)
w = pd.read_csv('out_S14.csv', dtype={'API_NUMBER': str})
d = pd.read_pickle('ff_disc.pkl')
ll = w.groupby('DISCLOSURE_ID')[['LATITUDE','LONGITUDE']].first()
d = d.join(ll, on='DISCLOSURE_ID')
d['cty'] = d.state + '|' + d.county.str.upper().str.strip()
v = pd.read_csv('out_S15.csv', dtype={'API_NUMBER': str})
v['cty'] = v.STATE_NAME + '|' + v.COUNTY_NAME.str.upper().str.strip()
v4 = v[v.FF_VERSION.astype(str) == '4']
R = 3958.8
def neigh(sub, others, r=5):
    p1 = np.radians(sub.LATITUDE.values)[:, None]; l1 = np.radians(sub.LONGITUDE.values)[:, None]
    p2 = np.radians(others.LATITUDE.values)[None, :]; l2 = np.radians(others.LONGITUDE.values)[None, :]
    h = np.sin((p2-p1)/2)**2 + np.cos(p1)*np.cos(p2)*np.sin((l2-l1)/2)**2
    dd = 2*R*np.arcsin(np.sqrt(h))
    m = dd <= r
    fg = (m * others.fresh_gal.values[None, :]).sum(); g = (m * others.vol.values[None, :]).sum()
    ops = set(others.op.values[m.any(0)])
    return fg/g if g else np.nan, int(m.any(0).sum()), len(ops)
cases = [('New Mexico|LEA','Permian Resources Operating, LLC'), ('New Mexico|EDDY','Permian Resources Operating, LLC'), ('Texas|REEVES','Permian Resources Operating, LLC'),
         ('Texas|LIVE OAK','ConocoPhillips Company/Burlington Resources'), ('Texas|MIDLAND','Diamondback E&P LLC'), ('Texas|MIDLAND','Apache Corporation'),
         ('Texas|WEBB','SM Energy'), ('Texas|UPTON','Summit Petroleum LLC'), ('Texas|UPTON','TRP Operating LLC'), ('New Mexico|LEA','BTA Oil Producers LLC'), ('Utah|DUCHESNE','FourPoint Resources LLC')]
for cty, op in cases:
    cd = d[d.cty == cty]; me = cd[cd.op == op]; oth = cd[cd.op != op]
    fs = me.fresh_gal.sum()/me.vol.sum(); pf, pn, pops = neigh(me, oth)
    vv = v4[v4.cty == cty]; hw_me = vv[vv.OPERATOR_NAME == op].HAS_WATER.mean(); hw_o = vv[vv.OPERATOR_NAME != op].HAS_WATER.mean()
    comp = me[['gw','fresh','prod','tot']].sum()
    top_peers = oth.groupby('op').agg(n=('api','size'), fs=('fresh_gal','sum'), g=('vol','sum')).assign(fs=lambda x: (x.fs/x.g).round(2)).sort_values('n', ascending=False).head(4)
    print(f'{cty} | {op}: n={len(me)} fresh={fs:.3f} | county peers n={len(oth)} ops={oth.op.nunique()} fresh={oth.fresh_gal.sum()/oth.vol.sum():.3f} | within 5mi peers wells={pn} ops={pops} fresh={pf:.3f} | water-reported me={hw_me:.2f} others={hw_o:.2f}')
    print('    my mix gw/fresh/prod of tot', round(comp['gw']/comp['tot'],3), round(comp['fresh']/comp['tot'],3), round(comp['prod']/comp['tot'],3), '| peers:', top_peers[['n','fs']].to_dict('index'))
# how many operator-county cells over peers by 40+ points with >=20 wells and >=50 peer wells
oc = pd.read_pickle('ff_opcounty.pkl')
big = oc[(oc.n >= 20) & (oc.peer_n >= 50)]
print('cells', len(big), 'fs-peer>0.4:', ((big.fs-big.peer_fs)>0.4).sum(), 'fs-peer<-0.4:', ((big.fs-big.peer_fs)<-0.4).sum())
