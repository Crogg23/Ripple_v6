import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_rows',300); pd.set_option('display.max_colwidth',44)
fy=pd.read_pickle('fy.pkl'); info=pd.read_pickle('info.pkl')
m=pd.read_pickle('m.pkl')
allnames=m.groupby('FACILITY_ID').agg(names=('FACILITY_NAME',lambda s:'|'.join(sorted(set(s.dropna().astype(str))))[:80]), naics=('NAICS_CODE',lambda s:'|'.join(sorted(set(s.dropna().astype(str))))) , subs=('SUBSECTOR_ID',lambda s:','.join(map(str,sorted(set(s))))))
lng=allnames[allnames.names.str.contains('LNG|LIQUEF|Liquef',case=False,regex=True)|allnames.naics.str.contains('488999')]
yrs=list(range(2010,2024))
t=fy.reindex(lng.index)[yrs].div(1e6).round(2)
t=t.join(info[['STATE']]).join(lng)
print(t[t[yrs].max(axis=1)>0.3].sort_values(2023,ascending=False).to_string())
big=t[t[yrs].max(axis=1)>0.3]
print('LNG-named facilities >0.3 Mt some year:', len(big)); print(big[yrs].sum().round(1).to_dict())
# oil and gas systems sector: share of net growth carried by top units
both=fy[(fy[2015]>0)&(fy[2023]>0)]
og=both[both.sector=='Oil & gas systems']; ch=(og[2023]-og[2015]).sort_values(ascending=False)
print('O&G continuing: n',len(og),'net Mt',round(ch.sum()/1e6,2),'top1',round(ch.iloc[0]/1e6,2),'top4',round(ch.iloc[:4].sum()/1e6,2), 'median facility pct', round((og[2023]/og[2015]-1).median(),3))
# all sectors: rank of Sabine Pass
allch=(both[2023]-both[2015]).sort_values(ascending=False)
print('rank 1 of', len(allch), allch.index[0], round(allch.iloc[0]/1e6,2), 'next', round(allch.iloc[1]/1e6,2))
# Sabine pass all subsectors by year
sp=m[m.FACILITY_ID=='1002259'].groupby(['REPORTING_YEAR','SECTOR_ID','SUBSECTOR_ID','GAS_ID']).CO2E_EMISSION.sum().unstack(['SECTOR_ID','SUBSECTOR_ID','GAS_ID']).div(1e6).round(3)
print(sp.to_string())
print(m[m.FACILITY_ID=='1002259'][['REPORTING_YEAR','FACILITY_NAME','PARENT_COMPANY','REPORTED_SUBPARTS']].drop_duplicates().to_string())
