import pandas as pd, numpy as np
pd.set_option('display.width',250)
h=pd.read_csv('hcris_ltch.csv',dtype={'PROVIDER_CCN':str,'RPT_REC_NUM':str})
l=pd.read_csv('ltch.csv',dtype=str)
h['fy']=pd.to_datetime(h.FISCAL_YEAR_END_DATE).dt.year
h=h.sort_values('FISCAL_YEAR_LENGTH_DAYS').drop_duplicates(['PROVIDER_CCN','fy'],keep='last')
c=h.merge(l[['CCN','PROVIDER_NAME','OWNERSHIP_TYPE','STATE']],left_on='PROVIDER_CCN',right_on='CCN',how='inner')
c=c[c.OWNERSHIP_TYPE=='For profit']
c['k']=np.where(c.PROVIDER_NAME.str.upper().str.contains('KINDRED'),'Kindred',np.where(c.PROVIDER_NAME.str.upper().str.contains('SELECT|REGENCY'),'Select','otherFP'))
c['pm']=c.NET_INCOME_FROM_SERVICE_TO_PATIENTS/c.NET_PATIENT_REVENUE
c['ms']=c.TOTAL_DAYS_TITLE_XVIII/c.TOTAL_DAYS_ALL
t=c[c.fy.between(2012,2024)].pivot_table(index='fy',columns='k',values='pm',aggfunc='median').round(3)
n=c[c.fy.between(2012,2024)].pivot_table(index='fy',columns='k',values='pm',aggfunc='count')
print(t.join(n,rsuffix='_n'))
print(c[c.fy.between(2012,2024)].pivot_table(index='fy',columns='k',values='ms',aggfunc='median').round(3))
print(c[c.fy.between(2012,2024)].pivot_table(index='fy',columns='k',values='OCCUPANCY_RATE',aggfunc='median').round(3))
# Kindred sum of patient income by year
print(c[c.fy.between(2012,2024)].pivot_table(index='fy',columns='k',values='NET_INCOME_FROM_SERVICE_TO_PATIENTS',aggfunc='sum').round(-5))
# kindred hospital-level names in HCRIS 2023 (legal names)
print(c[(c.fy==2023)&(c.k=='Kindred')].HOSPITAL_NAME.str[:30].value_counts().head(5))
