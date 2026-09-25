import pandas as pd, numpy as np
pd.set_option('display.width', 260); pd.set_option('display.max_colwidth', 42); pd.set_option('display.max_columns', 20)
d = pd.read_pickle('ff_disc.pkl')
d['cty'] = d.state + '|' + d.county.str.upper().str.strip()
c = d.groupby('cty').agg(n=('api','size'), ops=('op','nunique'), gal=('vol','sum'), fg=('fresh_gal','sum'))
c['fs'] = c.fg / c.gal
print(c.sort_values('gal', ascending=False).head(20).round(3))
# operator within county
oc = d.groupby(['cty','op']).agg(n=('api','size'), gal=('vol','sum'), fg=('fresh_gal','sum'), gwg=('gw_gal','sum')).reset_index()
oc = oc.merge(c[['n','gal','fg']].rename(columns={'n':'cn','gal':'cgal','fg':'cfg'}), left_on='cty', right_index=True)
oc['fs'] = oc.fg/oc.gal
oc['peer_fs'] = (oc.cfg - oc.fg)/(oc.cgal - oc.gal)
oc['peer_n'] = oc.cn - oc.n
oc['excess_fresh_gal'] = oc.fg - oc.peer_fs*oc.gal
big = oc[(oc.n >= 20) & (oc.peer_n >= 50)]
print('operator-county cells', len(big))
print(big.sort_values('excess_fresh_gal', ascending=False).head(25)[['cty','op','n','gal','fs','peer_fs','peer_n','excess_fresh_gal']].assign(gal=lambda x: (x.gal/1e9).round(2), excess_fresh_gal=lambda x:(x.excess_fresh_gal/1e9).round(2)).round(3).to_string())
print('median cell fs - peer_fs', round((big.fs-big.peer_fs).median(),3))
# operator totals
ot = d.groupby('op').agg(n=('api','size'), gal=('vol','sum'), fg=('fresh_gal','sum'), states=('state','nunique')).sort_values('fg', ascending=False)
ot['fs'] = ot.fg/ot.gal
print(ot.head(20).assign(gal=lambda x:(x.gal/1e9).round(2), fg=lambda x:(x.fg/1e9).round(2)).round(3))
oc.to_pickle('ff_opcounty.pkl')
