import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_rows',300); pd.set_option('display.max_colwidth',44)
t=pd.read_pickle('t3.pkl'); fac=pd.read_csv('q06.csv',dtype=str); fi=fac.set_index('PGM_SYS_ID')
ids=fac[fac.FACILITY_NAME.str.contains('SUNCOR ENERGY - DENVER REFINERY',case=False,na=False,regex=False)]
print(ids[['PGM_SYS_ID','REGISTRY_ID','FACILITY_NAME','CITY','AIR_POLLUTANT_CLASS_CODE','AIR_OPERATING_STATUS_CODE','CURRENT_HPV']].to_string())
regs=set(ids.REGISTRY_ID)
allp=fac[fac.REGISTRY_ID.isin(regs)].PGM_SYS_ID
x=t[t.PGM_SYS_ID.isin(allp)].sort_values('ACTUAL_END_DATE')
print(x[['PGM_SYS_ID','ACTIVITY_ID','STATE_EPA_FLAG','ACTUAL_END_DATE','FACILITY_RPT_DEVIATION_FLAG']].tail(30).to_string())
v=pd.read_csv('q09.csv',dtype=str); fa=pd.read_csv('q10.csv',dtype={'PGM_SYS_ID':str}); ia=pd.read_csv('q11.csv',dtype=str)
print(v[v.PGM_SYS_ID.isin(allp)][['PGM_SYS_ID','AGENCY_TYPE_DESC','ENF_RESPONSE_POLICY_CODE','PROGRAM_CODES','POLLUTANT_DESCS','EARLIEST_FRV_DETERM_DATE','HPV_DAYZERO_DATE','HPV_RESOLVED_DATE']].sort_values('EARLIEST_FRV_DETERM_DATE').to_string())
print(fa[fa.PGM_SYS_ID.isin(allp)].sort_values('SETTLEMENT_ENTERED_DATE').to_string())
print(ia[ia.PGM_SYS_ID.isin(allp)].sort_values('ACHIEVED_DATE').tail(15).to_string())
# CO pairs: same facility, same date, one N one blank?
co=t[t.STATE_EPA_FLAG.notna()].copy(); co['STATE']=fi.STATE.reindex(co.PGM_SYS_ID).values
co=co[co.STATE=='CO']
pp=co.groupby(['PGM_SYS_ID','ACTUAL_END_DATE']).FACILITY_RPT_DEVIATION_FLAG.apply(lambda s:''.join(sorted(s.fillna('_')))).value_counts().head(8)
print(pp)
