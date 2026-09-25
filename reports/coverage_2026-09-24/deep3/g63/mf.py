import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_rows',200)
m=pd.read_csv('out_S05.csv',keep_default_na=False,na_values=[''])
print('rows',len(m),'dup keys',(m.KEY_N>1).sum())
for c in ['STATUS','MULTIPLE_FUELS','SWITCH_BETWEEN_OIL_AND_NATURAL_GAS','SWITCH_WHEN_OPERATING','TIME_TO_SWITCH_FROM_GAS_TO_OIL','FACTORS_THAT_LIMIT_SWITCHING','STORAGE_LIMITS','AIR_PERMIT_LIMITS','ENERGY_SOURCE_1','COFIRE_FUELS']:
    print(c, m[c].value_counts(dropna=False).head(12).to_dict())
g=pd.read_csv('out_S06.csv',keep_default_na=False,na_values=[''])
ba_tot=g[g.BA.notna()&g.STATE.isna()].set_index('BA')
st_tot=g.groupby('STATE').WINTER_MW.sum()
ng=m[(m.STATUS=='OP')&(m.ENERGY_SOURCE_1=='NG')&(m.SWITCH_BETWEEN_OIL_AND_NATURAL_GAS=='Y')].copy()
print('OP NG switchers',len(ng),'winter oil MW',ng.NET_WINTER_CAPACITY_WITH_OIL_MW.sum(),'winter gas MW',ng.NET_WINTER_CAPACITY_WITH_NATURAL_GAS_MW.sum())
ng['fast']=ng.TIME_TO_SWITCH_FROM_GAS_TO_OIL.isin(['1H','6H'])
ng['fast_oil_mw']=np.where(ng.fast&(ng.SWITCH_WHEN_OPERATING=='Y'),ng.NET_WINTER_CAPACITY_WITH_OIL_MW,0)
ng['lim_oil_mw']=np.where(ng.STORAGE_LIMITS.eq('Y')|ng.AIR_PERMIT_LIMITS.eq('Y'),ng.NET_WINTER_CAPACITY_WITH_OIL_MW,0)
b=ng.groupby('BA').agg(gens=('PLANT_CODE','size'),plants=('PLANT_CODE','nunique'),oil_w=('NET_WINTER_CAPACITY_WITH_OIL_MW','sum'),fast_oil=('fast_oil_mw','sum'),lim_oil=('lim_oil_mw','sum'))
b=b.join(ba_tot[['WINTER_MW','GENS']].rename(columns={'WINTER_MW':'gas_winter_mw','GENS':'gas_gens'}),how='outer')
b['oil_share']=b.oil_w/b.gas_winter_mw; b['fast_share']=b.fast_oil/b.gas_winter_mw
b=b[b.gas_winter_mw>5000].sort_values('oil_share')
print(b.round(3).to_string())
tot=g[g.BA.isna()&g.STATE.isna()].WINTER_MW.iloc[0]
print('US oil share', ng.NET_WINTER_CAPACITY_WITH_OIL_MW.sum()/tot, 'fast', ng.fast_oil_mw.sum()/tot, 'US gas winter', tot)
ng.to_csv('mf_ng_switch.csv',index=False)
