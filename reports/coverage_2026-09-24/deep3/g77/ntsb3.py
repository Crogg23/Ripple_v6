import pandas as pd, numpy as np
d=pd.read_pickle('s12.pkl')
a=d[d.FAR_PART.isin(['121','129'])].copy()
a['cabi']=a[['CABI_F','CABI_S','CABI_M','CABI_N']].sum(axis=1); a['flig']=a[['FLIG_F','FLIG_S','FLIG_M','FLIG_N']].sum(axis=1)
a['mo']=pd.to_datetime(a.EV_DATE).dt.to_period('Q')
a['lumped']=(a.cabi==0)&(a.flig>=3)
a['split']=(a.cabi>0)
t=a.groupby('mo').agg(n=('EV_ID','size'),lumped=('lumped','sum'),split=('split','sum'))
print(t.loc['2019Q1':'2024Q4'].T.to_string())
l=a[a.lumped]; print('lumped first/last', l.EV_DATE.min(), l.EV_DATE.max(), len(l))
s=a[a.split&(pd.to_datetime(a.EV_DATE)>='2020-07-01')&(pd.to_datetime(a.EV_DATE)<='2024-01-01')]
print(s[['EV_DATE','NTSB_NO','OPER_NAME','cabi','flig','LCHG']].to_string())
# LCHG of lumped vs split
print(a.groupby('lumped').LCHG.agg(['min','max']))
