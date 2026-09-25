import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_rows',300); pd.set_option('display.max_colwidth',40)
e=pd.read_csv('q03.csv',dtype={'FACILITY_ID':str})
f=pd.read_csv('q04.csv',dtype={'FACILITY_ID':str,'FRS':str,'ZIP':str,'COUNTY_FIPS':str,'NAICS_CODE':str})
print(e.shape, f.shape, 'record id unique', e.EMISSION_RECORD_ID.is_unique)
print('dup keys (fac,yr,sector,subsector,gas):', e.duplicated(['FACILITY_ID','REPORTING_YEAR','SECTOR_ID','SUBSECTOR_ID','GAS_ID']).sum(), ' exact dup incl value:', e.duplicated(['FACILITY_ID','REPORTING_YEAR','SECTOR_ID','SUBSECTOR_ID','GAS_ID','CO2E_EMISSION']).sum())
print('years', sorted(e.REPORTING_YEAR.unique()))
# sector identity: most common NAICS-2/3 and subparts among facilities in each sector (2022)
fx=f.drop_duplicates(['FACILITY_ID','REPORTING_YEAR'])
m=e.merge(fx[['FACILITY_ID','REPORTING_YEAR','NAICS_CODE','FACILITY_TYPES','REPORTED_SUBPARTS','FACILITY_NAME','STATE','PARENT_COMPANY','REPORTING_STATUS']],on=['FACILITY_ID','REPORTING_YEAR'],how='left')
print('emission rows with no facility row', m.NAICS_CODE.isna().sum(), m[m.FACILITY_TYPES.isna()].REPORTING_YEAR.value_counts().sort_index().to_dict())
for s,g in m[m.REPORTING_YEAR==2022].groupby('SECTOR_ID'):
    top_n=g.NAICS_CODE.astype(str).str[:4].value_counts().head(3).to_dict()
    sp=g.drop_duplicates('FACILITY_ID').REPORTED_SUBPARTS.fillna('').str.split(',').explode().value_counts().head(5).to_dict()
    print(s, g.FACILITY_ID.nunique(), 'subsectors', sorted(g.SUBSECTOR_ID.unique())[:12], top_n, sp, 'types', g.FACILITY_TYPES.value_counts().head(2).to_dict(), 'co2e Mt', round(g.CO2E_EMISSION.sum()/1e6,1))
# null rows
nul=m[m.CO2E_EMISSION.isna()]
print('null co2e rows', len(nul)); print(pd.crosstab(nul.SECTOR_ID, nul.GAS_ID.fillna(-1)))
m.to_pickle('m.pkl')
