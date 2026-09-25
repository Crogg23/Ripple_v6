import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_columns',40); pd.set_option('display.max_rows',300); pd.set_option('display.max_colwidth',40)
h=pd.read_csv('hcris_ltch.csv',dtype={'PROVIDER_CCN':str,'RPT_REC_NUM':str})
l=pd.read_csv('ltch.csv',dtype=str); p=pd.read_csv('pos_ltch.csv',dtype=str)
h['fy']=pd.to_datetime(h.FISCAL_YEAR_END_DATE).dt.year
h=h.sort_values('FISCAL_YEAR_LENGTH_DAYS').drop_duplicates(['PROVIDER_CCN','fy'],keep='last')
exec(open('chain.py').read()) if False else None
def chain(n):
    n=str(n).upper()
    for k,v in [('SELECT','Select'),('REGENCY','Select'),('KINDRED','Kindred'),('PAM ','PAM'),('VIBRA','Vibra'),('AMG','AMG'),('CORNERSTONE','Cornerstone'),('CONTINUECARE','ContinueCARE'),('NOLAND','Noland'),('LANDMARK','Landmark'),('SAGE','Sage'),('PROMISE','Promise'),('LIFECARE','LifeCare')]:
        if k in n: return v
    return 'other'
p['chain']=p.FAC_NAME.map(chain); p['td']=pd.to_datetime(p.TRMNTN_EXPRTN_DT,errors='coerce')
act=p[p.PGM_TRMNTN_CD=='00']
term=p[(p.PGM_TRMNTN_CD!='00')&(p.td>='2016-01-01')]
t=pd.concat([act.chain.value_counts().rename('active_now'),term.chain.value_counts().rename('closed_2016_2025'),p[(p.PGM_TRMNTN_CD!='00')&(p.td>='2024-01-01')].chain.value_counts().rename('closed_2024_25')],axis=1).fillna(0)
t['closed_share']=(t.closed_2016_2025/(t.active_now+t.closed_2016_2025)).round(3)
print(t.sort_values('active_now',ascending=False))
print('07 conversions since 2016', (term.PGM_TRMNTN_CD=='07').sum(), ' 01', (term.PGM_TRMNTN_CD=='01').sum())
# FY2023 Kindred vs other for-profit, same state
c=h[h.fy==2023].merge(l[['CCN','PROVIDER_NAME','OWNERSHIP_TYPE','STATE']],left_on='PROVIDER_CCN',right_on='CCN',how='inner')
c['chain']=c.PROVIDER_NAME.map(chain)
c['pm']=c.NET_INCOME_FROM_SERVICE_TO_PATIENTS/c.NET_PATIENT_REVENUE
fp=c[c.OWNERSHIP_TYPE=='For profit']
rows=[]
for st,g in fp.groupby('STATE'):
    k=g[g.chain=='Kindred']; o=g[g.chain!='Kindred']
    if len(k) and len(o): rows.append((st,len(k),round(k.pm.median(),3),len(o),round(o.pm.median(),3)))
r=pd.DataFrame(rows,columns=['state','n_kindred','kindred_med_pm','n_otherFP','other_med_pm'])
print(r); print('states where kindred median below peers:',(r.kindred_med_pm<r.other_med_pm).sum(),'of',len(r))
k=fp[fp.chain=='Kindred']; print('kindred FY23 n',len(k),'median pm',k.pm.median().round(3),'neg share',(k.pm<0).mean().round(3),'sum pat income',k.NET_INCOME_FROM_SERVICE_TO_PATIENTS.sum())
o=fp[fp.chain!='Kindred']; print('other FP n',len(o),'median pm',o.pm.median().round(3),'neg share',(o.pm<0).mean().round(3))
# Kindred medicare share + occupancy vs others
print(fp.groupby(fp.chain=='Kindred').apply(lambda g: pd.Series({'n':len(g),'med_ms':(g.TOTAL_DAYS_TITLE_XVIII/g.TOTAL_DAYS_ALL).median(),'med_occ':g.OCCUPANCY_RATE.median(),'med_beds':g.NUMBER_OF_BEDS.median()})))
# the 5 FY2023 gov loss check
g=c[c.OWNERSHIP_TYPE=='Government'][['PROVIDER_CCN','HOSPITAL_NAME','STATE','NUMBER_OF_BEDS','NET_INCOME_FROM_SERVICE_TO_PATIENTS','TOTAL_DAYS_TITLE_XVIII','TOTAL_DAYS_ALL']]
print(g)
