import pandas as pd, numpy as np
pd.set_option('display.width',260)
p=pd.read_csv('coal_plants.csv')
e=pd.read_csv('out_S04.csv',keep_default_na=False,na_values=[''])
US=e.US_SO2_ALL_PLANTS.iloc[0]
p=p.merge(e[['PC','SO2_SRC','CAMD','CHP','SO2_UNADJ','HEAT_UNADJ']],left_on='PLANT_CODE',right_on='PC',how='left')
p['measured']=p.SO2_SRC.fillna('').str.startswith('EPA/CAMD') & (p.SO2_SRC!='EPA/CAMD; EIA')
print(p.SO2_SRC.value_counts(dropna=False))
m=p[p.SO2_SRC=='EPA/CAMD'].copy()
print('coal plants op 2024, CAMD-only source:',len(m),'of',len(p))
m['unscrubbed']=m.lbmm>=0.3
g=m.groupby('unscrubbed').agg(plants=('plant','size'),so2=('so2','sum'),coal_mwh=('coal_mwh','sum'),mw=('mw','sum'),med=('lbmm','median'),ret=('has_ret','sum'))
g['so2_share_US']=g.so2/US; g['coalgen_share']=g.coal_mwh/m.coal_mwh.sum(); g['so2_share_coalset']=g.so2/m.so2.sum()
print(g.to_string())
u=m[m.unscrubbed].sort_values('so2',ascending=False)
u['cum_US']=u.so2.cumsum()/US
print(u[['plant','state','util','mw','so2','lbmm','ret','codes','cum_US','coal_mwh']].to_string())
# peer: subbituminous only, big plants >=500MW
sub=m[m.lbmm.notna()]
print('median rate all measured coal', sub.lbmm.median())
