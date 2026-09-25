import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_rows',300); pd.set_option('display.max_colwidth',44)
t=pd.read_pickle('t3.pkl'); fac=pd.read_csv('q06.csv',dtype=str); fi=fac.set_index('PGM_SYS_ID')
t['STATE']=fi.STATE.reindex(t.PGM_SYS_ID).values
c=t[t.FACILITY_RPT_DEVIATION_FLAG.notna()&(t.yr>=2016)&(t.yr<=2025)].copy()
rate=c.groupby('STATE').FACILITY_RPT_DEVIATION_FLAG.apply(lambda s:(s=='Y').mean())
good=rate[rate>=0.25].index
c=c[c.STATE.isin(good)]
v=pd.read_csv('q09.csv',dtype=str)
h=v[v.ENF_RESPONSE_POLICY_CODE=='HPV'].copy()
h['d0']=pd.to_datetime(h.HPV_DAYZERO_DATE,errors='coerce'); h['d1']=pd.to_datetime(h.HPV_RESOLVED_DATE,errors='coerce')
h=h[h.d0.notna()]
mm=c[['PGM_SYS_ID','ACTIVITY_ID','d','FACILITY_RPT_DEVIATION_FLAG','STATE']].merge(h[['PGM_SYS_ID','d0','d1','POLLUTANT_DESCS']],on='PGM_SYS_ID',how='inner')
mm['open']=(mm.d0<=mm.d-pd.Timedelta(days=365))&(mm.d1.isna()|(mm.d1>mm.d))
op=mm[mm.open].drop_duplicates('ACTIVITY_ID')
print('states with Y rate >=25%:', len(good))
print('flagged certs 2016-25 in those states', len(c), 'N share', round((c.FACILITY_RPT_DEVIATION_FLAG=='N').mean(),3))
print('certs filed while an HPV (day zero 1+ yr earlier) was unresolved:', len(op), 'N share', round((op.FACILITY_RPT_DEVIATION_FLAG=='N').mean(),3), 'facilities', op.PGM_SYS_ID.nunique())
x=op[op.FACILITY_RPT_DEVIATION_FLAG=='N']
print('N certs under open HPV', len(x), 'facilities', x.PGM_SYS_ID.nunique())
print(x.groupby('STATE').size().sort_values(ascending=False).head(10).to_dict())
# unresolved-HPV age sanity: how many open HPVs have null resolved date and very old day zero
print('HPV rows with null resolved date', h.d1.isna().sum(), 'of', len(h), '; null-resolved with day zero before 2015:', (h.d1.isna()&(h.d0<'2015-01-01')).sum())
