import pandas as pd, numpy as np
pd.set_option('display.width', 260); pd.set_option('display.max_colwidth', 44); pd.set_option('display.max_columns', 20)
d = pd.read_pickle('ff_disc.pkl'); d['cty'] = d.state + '|' + d.county.str.upper().str.strip()
v = pd.read_csv('out_S15.csv', dtype={'API_NUMBER': str}); v = v[v.FF_VERSION.astype(str) == '4']
v['cty'] = v.STATE_NAME + '|' + v.COUNTY_NAME.str.upper().str.strip()
rep = v.groupby(['cty','OPERATOR_NAME']).agg(v4=('DISCLOSURE_ID','size'), rate=('HAS_WATER','mean')).reset_index().rename(columns={'OPERATOR_NAME':'op'})
# overall reporting spread among operators with >=20 v4 disclosures
r20 = rep[rep.v4 >= 20]
print('op-county cells >=20 v4 disclosures', len(r20), 'reporting rate quartiles', r20.rate.quantile([.1,.25,.5,.75,.9]).round(2).to_dict())
oc = d.groupby(['cty','op']).agg(n=('api','size'), gal=('vol','sum'), fg=('fresh_gal','sum'), gwg=('gw_gal','sum')).reset_index().merge(rep, on=['cty','op'], how='left')
oc['fs'] = oc.fg/oc.gal; oc['gws'] = oc.gwg/oc.gal
full = oc[(oc.rate >= 0.9) & (oc.n >= 20)]
print('complete reporters (>=90%, >=20 wells) cells', len(full))
for cty, g in full.groupby('cty'):
    if len(g) >= 3:
        print('\n', cty); print(g.sort_values('fs', ascending=False)[['op','n','rate','fs','gws']].assign(gal_b=(g.gal/1e9).round(2)).round(2).to_string(index=False))
# Is fresh share related to reporting rate? all cells >=20
c = oc[oc.n >= 10]
print('\ncorr fresh share vs reporting rate (cells n>=10):', round(c[['fs','rate']].corr().iloc[0,1],3), len(c))
c['rbin'] = pd.cut(c.rate, [0,.5,.9,1.01])
print(c.groupby('rbin').apply(lambda g: pd.Series({'cells':len(g), 'fresh_gal_share': g.fg.sum()/g.gal.sum()})).round(3))
