import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_columns',40); pd.set_option('display.max_rows',200)
t=pd.read_pickle('t2.pkl')
# dedupe: one row per ACTIVITY_ID, prefer a filled flag
t['has']=t.FACILITY_RPT_DEVIATION_FLAG.notna()
t=t.sort_values('has',ascending=False).drop_duplicates('ACTIVITY_ID')
print('deduped', len(t))
t.to_pickle('t3.pkl')
# certs per facility per year: how many
w=t[(t.yr>=2016)&(t.yr<=2025)]
fy=w.groupby(['PGM_SYS_ID','yr']).size()
print('certs per facility-year dist', fy.value_counts().head(8).to_dict())
# Title V universe
p=pd.read_csv('q08.csv',dtype=str)
print(p.PROGRAM_CODE.value_counts().head(15).to_dict())
tv=p[p.PROGRAM_CODE=='CAATVP']
print('CAATVP rows', len(tv), tv.PGM_SYS_ID.nunique(), tv.AIR_OPERATING_STATUS_CODE.value_counts().to_dict())
fac=pd.read_csv('q06.csv',dtype=str)
print('facility class x status (all)'); print(pd.crosstab(fac.AIR_POLLUTANT_CLASS_CODE.fillna('_'), fac.AIR_OPERATING_STATUS_CODE.fillna('_')))
tvo=tv[tv.AIR_OPERATING_STATUS_CODE=='OPR'].PGM_SYS_ID.unique()
print('operating title V', len(tvo))
certfac=set(t.PGM_SYS_ID)
print('title V operating with any cert ever', np.isin(tvo,list(certfac)).mean())
print('cert facilities that are in CAATVP', pd.Series(list(certfac)).isin(tv.PGM_SYS_ID).mean())
