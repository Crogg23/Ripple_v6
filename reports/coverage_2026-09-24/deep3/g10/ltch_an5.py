import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_rows',300); pd.set_option('display.max_colwidth',42)
h=pd.read_csv('hcris_ltch.csv',dtype={'PROVIDER_CCN':str,'RPT_REC_NUM':str})
l=pd.read_csv('ltch.csv',dtype=str)
h['fy']=pd.to_datetime(h.FISCAL_YEAR_END_DATE).dt.year
h=h.sort_values('FISCAL_YEAR_LENGTH_DAYS').drop_duplicates(['PROVIDER_CCN','fy'],keep='last')
c=h.merge(l[['CCN','PROVIDER_NAME','OWNERSHIP_TYPE','STATE','CITY_TOWN']],left_on='PROVIDER_CCN',right_on='CCN',how='inner')
c=c[c.OWNERSHIP_TYPE=='For profit'].copy()
c['k']=np.where(c.PROVIDER_NAME.str.upper().str.contains('KINDRED'),'Kindred','otherFP')
c['pm']=c.NET_INCOME_FROM_SERVICE_TO_PATIENTS/c.NET_PATIENT_REVENUE
c['cost_per_day']=c.TOTAL_OPERATING_EXPENSE/c.TOTAL_DAYS_ALL
c['rev_per_day']=c.NET_PATIENT_REVENUE/c.TOTAL_DAYS_ALL
d=c[c.fy==2023].copy()
d['occ_band']=pd.cut(d.OCCUPANCY_RATE,[0,0.6,0.75,2],labels=['<60%','60-75%','75%+'])
print(d.pivot_table(index='occ_band',columns='k',values='pm',aggfunc=['median','count'],observed=False).round(3))
d['bed_band']=pd.cut(d.NUMBER_OF_BEDS,[0,40,70,1000],labels=['<=40','41-70','71+'])
print(d.pivot_table(index='bed_band',columns='k',values='pm',aggfunc=['median','count'],observed=False).round(3))
print(d.groupby('k')[['cost_per_day','rev_per_day']].median().round(0))
kk=d[d.k=='Kindred'].sort_values('NET_INCOME_FROM_SERVICE_TO_PATIENTS')
tot=kk.NET_INCOME_FROM_SERVICE_TO_PATIENTS.sum()
print('Kindred FY23 total',tot,'worst3',kk.head(3).NET_INCOME_FROM_SERVICE_TO_PATIENTS.sum(),'without worst3',tot-kk.head(3).NET_INCOME_FROM_SERVICE_TO_PATIENTS.sum())
print(kk.head(6)[['PROVIDER_CCN','PROVIDER_NAME','STATE','NUMBER_OF_BEDS','NET_PATIENT_REVENUE','NET_INCOME_FROM_SERVICE_TO_PATIENTS','OCCUPANCY_RATE','pm']])
print(c[c.fy.between(2019,2024)].pivot_table(index='fy',columns='k',values='TOTAL_OTHER_INCOME',aggfunc='sum').round(-5))
# kindred cost per day vs other over time
print(c[c.fy.between(2012,2024)].pivot_table(index='fy',columns='k',values=['cost_per_day','rev_per_day'],aggfunc='median').round(0))
