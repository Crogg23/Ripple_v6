import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_columns',40); pd.set_option('display.max_rows',300); pd.set_option('display.max_colwidth',40)
h=pd.read_csv('hcris_ltch.csv',dtype={'PROVIDER_CCN':str,'RPT_REC_NUM':str})
l=pd.read_csv('ltch.csv',dtype=str)
h['fy']=pd.to_datetime(h.FISCAL_YEAR_END_DATE).dt.year
h=h.sort_values('FISCAL_YEAR_LENGTH_DAYS').drop_duplicates(['PROVIDER_CCN','fy'],keep='last')
def chain(n):
    n=str(n).upper()
    for k,v in [('SELECT','Select'),('REGENCY','Select'),('KINDRED','Kindred'),('PAM ','PAM'),('VIBRA','Vibra'),('AMG','AMG'),('CORNERSTONE','Cornerstone'),('CONTINUECARE','ContinueCARE'),('NOLAND','Noland'),('LANDMARK','Landmark'),('SAGE','Sage'),('PROMISE','Promise')]:
        if k in n: return v
    return 'independent/other'
l['chain']=l.PROVIDER_NAME.map(chain)
print(pd.crosstab(l.chain,l.OWNERSHIP_TYPE,margins=True))
# matched panel 2015 vs 2023
a=h[h.fy==2015].set_index('PROVIDER_CCN'); b=h[h.fy==2023].set_index('PROVIDER_CCN')
m=a.join(b,lsuffix='_15',rsuffix='_23',how='inner')
m=m[(m.TOTAL_DAYS_ALL_15>0)&(m.TOTAL_DAYS_ALL_23>0)]
m['ms15']=m.TOTAL_DAYS_TITLE_XVIII_15/m.TOTAL_DAYS_ALL_15; m['ms23']=m.TOTAL_DAYS_TITLE_XVIII_23/m.TOTAL_DAYS_ALL_23
print('matched',len(m),'median medicare share 15->23',m.ms15.median().round(3),m.ms23.median().round(3))
print('matched medicare days',m.TOTAL_DAYS_TITLE_XVIII_15.sum(),m.TOTAL_DAYS_TITLE_XVIII_23.sum(),'all days',m.TOTAL_DAYS_ALL_15.sum(),m.TOTAL_DAYS_ALL_23.sum())
print('medicare discharges matched',m.TOTAL_DISCHARGES_TITLE_XVIII_15.sum(),m.TOTAL_DISCHARGES_TITLE_XVIII_23.sum())
print('share of hospitals with medicare share down >10pts', ((m.ms23-m.ms15)<-0.10).mean().round(3))
# FY2023 per-hospital margins
c=h[h.fy==2023].copy()
c=c.merge(l[['CCN','chain','OWNERSHIP_TYPE','STATE']],left_on='PROVIDER_CCN',right_on='CCN',how='left')
c['pm']=c.NET_INCOME_FROM_SERVICE_TO_PATIENTS/c.NET_PATIENT_REVENUE
c['ms']=c.TOTAL_DAYS_TITLE_XVIII/c.TOTAL_DAYS_ALL
print('FY2023 reports',len(c),'median patient margin',c.pm.median().round(3),'share negative',(c.pm<0).mean().round(3))
print(c.groupby(c.OWNERSHIP_TYPE.fillna('not on list')).agg(n=('pm','size'),med_pm=('pm','median'),loss=('NET_INCOME_FROM_SERVICE_TO_PATIENTS','sum'),med_ms=('ms','median'),med_occ=('OCCUPANCY_RATE','median')))
print(c.groupby(c.chain.fillna('not on list')).agg(n=('pm','size'),med_pm=('pm','median'),loss=('NET_INCOME_FROM_SERVICE_TO_PATIENTS','sum'),med_ms=('ms','median'),med_occ=('OCCUPANCY_RATE','median'),oth=('TOTAL_OTHER_INCOME','sum'),ni=('NET_INCOME','sum')))
tot=c.NET_INCOME_FROM_SERVICE_TO_PATIENTS.sum()
s=c.sort_values('NET_INCOME_FROM_SERVICE_TO_PATIENTS')
print('total',tot,'top5 losers sum',s.head(5).NET_INCOME_FROM_SERVICE_TO_PATIENTS.sum(),'top10',s.head(10).NET_INCOME_FROM_SERVICE_TO_PATIENTS.sum())
print(s.head(10)[['PROVIDER_CCN','HOSPITAL_NAME','STATE_CODE','chain','NUMBER_OF_BEDS','NET_PATIENT_REVENUE','NET_INCOME_FROM_SERVICE_TO_PATIENTS','TOTAL_OTHER_INCOME','NET_INCOME','pm']])
print(s.tail(5)[['PROVIDER_CCN','HOSPITAL_NAME','STATE_CODE','chain','NUMBER_OF_BEDS','NET_PATIENT_REVENUE','NET_INCOME_FROM_SERVICE_TO_PATIENTS','NET_INCOME','pm']])
