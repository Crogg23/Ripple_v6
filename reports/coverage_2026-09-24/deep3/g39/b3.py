import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_rows',300); pd.set_option('display.max_colwidth',38)
m=pd.read_pickle('m.pkl')
SECT={2:'Waste',3:'Power plants',4:'Refineries',5:'Chemicals',6:'Metals',7:'Pulp & paper',8:'Minerals',14:'Other',15:'Oil & gas systems'}
d=m[m.SECTOR_ID.isin(SECT.keys())&(m.GAS_ID!=8)&m.CO2E_EMISSION.notna()]
# facility main sector = sector with most direct CO2e across all years
fs=d.groupby(['FACILITY_ID','SECTOR_ID']).CO2E_EMISSION.sum().reset_index().sort_values('CO2E_EMISSION').drop_duplicates('FACILITY_ID',keep='last').set_index('FACILITY_ID').SECTOR_ID
fy=d.groupby(['FACILITY_ID','REPORTING_YEAR']).CO2E_EMISSION.sum().unstack()
fy['sector']=fs.reindex(fy.index).map(SECT)
info=m.sort_values('REPORTING_YEAR').drop_duplicates('FACILITY_ID',keep='last').set_index('FACILITY_ID')[['FACILITY_NAME','STATE','PARENT_COMPANY','NAICS_CODE']]
a,b=2015,2023
both=fy[(fy[a]>0)&(fy[b]>0)].copy()
both['chg']=both[b]-both[a]; both['pct']=both[b]/both[a]-1
print('facilities with direct emissions in both %d and %d: %d'%(a,b,len(both)))
s=both.groupby('sector').agg(n=('chg','size'),sum_a=(a,'sum'),sum_b=(b,'sum'),med_pct=('pct','median'),grew=('pct',lambda x:(x>0).mean()))
s['sector_pct']=s.sum_b/s.sum_a-1
print(s.assign(sum_a=lambda x:(x.sum_a/1e6).round(1),sum_b=lambda x:(x.sum_b/1e6).round(1)).round(3).to_string())
top=both.sort_values('chg',ascending=False).head(25).join(info)
top[a]=(top[a]/1e6).round(2); top[b]=(top[b]/1e6).round(2); top['chg']=(top.chg/1e6).round(2)
print(top[['sector','FACILITY_NAME','STATE','NAICS_CODE',a,b,'chg','pct']].round(2).to_string())
fy.to_pickle('fy.pkl'); info.to_pickle('info.pkl')
