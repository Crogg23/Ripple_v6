import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_rows',300); pd.set_option('display.max_colwidth',40)
m=pd.read_pickle('m.pkl')
m['nullgas']=m.GAS_ID.isna()
m['status']=m.REPORTING_STATUS.fillna('(reported)')
print(pd.crosstab(m.status, m.nullgas))
print(pd.crosstab(m.FACILITY_TYPES.isna(), m.nullgas))
y=m[m.REPORTING_YEAR==2023]
fs=y.groupby('FACILITY_ID').agg(n=('CO2E_EMISSION','size'),nn=('CO2E_EMISSION',lambda s:s.notna().sum()),status=('status','first'))
print('2023 facilities', len(fs), 'all-null', (fs.nn==0).sum(), round((fs.nn==0).mean(),3))
print(fs[fs.nn==0].status.value_counts())
print('2023 rows', len(y), 'null', y.CO2E_EMISSION.isna().sum(), round(y.CO2E_EMISSION.isna().mean(),3))
# biggest nulls? facilities with null gas-1 rows in supplier sectors: what do they report otherwise
g1=m[(m.GAS_ID==1)&m.CO2E_EMISSION.isna()]
print(g1.groupby(['SECTOR_ID','SUBSECTOR_ID']).size())
print(g1[['FACILITY_NAME','STATE','REPORTING_YEAR','SECTOR_ID','SUBSECTOR_ID','FACILITY_TYPES']].drop_duplicates('FACILITY_NAME').head(12).to_string())
# supplier vs direct
SUP=[9,10,11,12,13,16,17]
m['kind']=np.where(m.SECTOR_ID.isin([10,11,12,13,16]),'supplier',np.where(m.SECTOR_ID.isin([9,17]),'injection',np.where(m.GAS_ID==8,'biogenic','direct')))
k=m.pivot_table(index='REPORTING_YEAR',columns='kind',values='CO2E_EMISSION',aggfunc='sum').div(1e6).round(0)
k['total']=k.sum(axis=1); print(k)
print('all-years sum Bt', round(m.CO2E_EMISSION.sum()/1e9,2), 'direct share', round(m[m.kind=='direct'].CO2E_EMISSION.sum()/m.CO2E_EMISSION.sum(),3))
top=m.sort_values('CO2E_EMISSION',ascending=False).head(8)
print(top[['FACILITY_ID','FACILITY_NAME','STATE','REPORTING_YEAR','SECTOR_ID','SUBSECTOR_ID','GAS_ID','CO2E_EMISSION','FACILITY_TYPES']].to_string())
