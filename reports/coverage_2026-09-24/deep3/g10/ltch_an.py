import pandas as pd, numpy as np, re
pd.set_option('display.width',250); pd.set_option('display.max_columns',40); pd.set_option('display.max_rows',300)
h=pd.read_csv('hcris_ltch.csv',dtype={'PROVIDER_CCN':str,'RPT_REC_NUM':str})
l=pd.read_csv('ltch.csv',dtype=str)
p=pd.read_csv('pos_ltch.csv',dtype=str)
h['fy']=pd.to_datetime(h.FISCAL_YEAR_END_DATE).dt.year
def chain(n):
    n=str(n).upper()
    for k,v in [('SELECT','Select'),('REGENCY','Select'),('KINDRED','Kindred'),('PAM ','PAM'),('POST ACUTE MEDICAL','PAM'),('VIBRA','Vibra'),('AMG','AMG'),('CORNERSTONE','Cornerstone'),('CONTINUECARE','ContinueCARE'),('LIFECARE','LifeCare'),('NOLAND','Noland'),('LANDMARK','Landmark'),('SAGE','Sage'),('PROMISE','Promise'),('LTAC','other'),]:
        if k in n: return v
    return 'other'
# one report per ccn-fy: keep longest period
h=h.sort_values('FISCAL_YEAR_LENGTH_DAYS').drop_duplicates(['PROVIDER_CCN','fy'],keep='last')
last=h.groupby('PROVIDER_CCN').fy.max()
first=h.groupby('PROVIDER_CCN').fy.min()
names=h.sort_values('fy').groupby('PROVIDER_CCN').HOSPITAL_NAME.last()
cur=set(l.CCN)
df=pd.DataFrame({'first':first,'last':last,'name':names})
df['on_list']=df.index.isin(cur)
df['chain']=df.name.map(chain)
print('HCRIS LTCH CCNs', len(df), 'on current list', df.on_list.sum())
print(pd.crosstab(df['last'],df.on_list))
gone=df[(~df.on_list)&(df['last']<=2022)]
print('gone (last report <=2022, not on list):',len(gone))
print(gone.chain.value_counts())
# chain in 2013 vs chain now
b=h[h.fy==2013].copy(); b['chain']=b.HOSPITAL_NAME.map(chain)
c=h[h.fy==2023].copy(); c['chain']=c.HOSPITAL_NAME.map(chain)
print(pd.concat([b.chain.value_counts().rename('fy2013'),c.chain.value_counts().rename('fy2023')],axis=1))
# POS termination codes
p['rng']=p.CCN.str[2:6].between('2000','2299')
print(p.PRVDR_CTGRY_CD.value_counts().head(), p.PRVDR_CTGRY_SBTYP_CD.value_counts().head())
print(p.PGM_TRMNTN_CD.value_counts())
p['tyr']=pd.to_datetime(p.TRMNTN_EXPRTN_DT,errors='coerce').dt.year
print(p[p.PGM_TRMNTN_CD!='00'].groupby('tyr').size())
print('current list in POS', len(cur&set(p.CCN)))
print('current-list CCNs with POS term code<>00:', p[p.CCN.isin(cur)&(p.PGM_TRMNTN_CD!='00')][['CCN','FAC_NAME','PGM_TRMNTN_CD','TRMNTN_EXPRTN_DT']])
p['chow']=pd.to_numeric(p.CHOW_CNT,errors='coerce')
q=p[p.CCN.isin(cur)].copy(); q['chain']=q.FAC_NAME.map(chain)
print(q.groupby('chain').chow.agg(['count','mean','sum']))
