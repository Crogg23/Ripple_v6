import pandas as pd, numpy as np
b=pd.read_csv('out_S12.csv')
print(b.shape); print(b.REPDTE.value_counts().head())
for c in ['ORDERS_ALL','ORDERS_2020','CD_2020','CMP_2020','CMP_AMT_2020']: b[c]=b[c].fillna(0)
b['dep_per_office']=b.DEPDOM/ b.OFFICES_DOMESTIC.replace(0,np.nan)
b['band']=pd.cut(b.ASSET,[0,1e5,3e5,1e6,1e7,1e8,1e10],labels=['<100M','100-300M','300M-1B','1-10B','10-100B','100B+'])
print(b.band.value_counts().sort_index())
print('any order since 2020:', (b.ORDERS_2020>0).sum(), 'C&D/consent since 2020', (b.CD_2020>0).sum())
print(b.SPECGRP.value_counts().head(12))
# within band: decile of deposits per office
b['dpo_dec']=b.groupby('band',observed=True).dep_per_office.transform(lambda s: pd.qcut(s.rank(method='first'),10,labels=False))
t=b.groupby(['band','dpo_dec'],observed=True).agg(n=('CERT','size'), any_ord=('ORDERS_2020',lambda s:(s>0).mean()), cd=('CD_2020',lambda s:(s>0).mean()), med_dpo=('dep_per_office','median'))
print(t.round(3).to_string())
# small banks under 10B: top decile vs rest
s=b[b.ASSET<1e7]
top=s[s.dpo_dec==9]; rest=s[s.dpo_dec<9]
print('under $10B: top decile dep/office', len(top), 'C&D rate', round((top.CD_2020>0).mean(),3), 'any', round((top.ORDERS_2020>0).mean(),3), '| rest', len(rest), round((rest.CD_2020>0).mean(),3), round((rest.ORDERS_2020>0).mean(),3))
x=top[top.CD_2020>0].sort_values('dep_per_office',ascending=False)
print(x[['CERT','NAME','CITY','STALP','ASSET','OFFICES_DOMESTIC','dep_per_office','SPECGRP','CD_2020','CMP_AMT_2020','LAST_ORDER','TYPES_2020']].head(40).to_string())
# MDI
b['mdi']=b.MDI_STATUS_CODE.notna() & ~b.MDI_STATUS_CODE.astype(str).isin(['0','00','nan'])
print(b.groupby(['band','mdi'],observed=True).agg(n=('CERT','size'), cd=('CD_2020',lambda s:(s>0).mean()), anyo=('ORDERS_2020',lambda s:(s>0).mean()), roa=('NETINC', 'sum')).round(3).to_string())
b.to_pickle('fdic.pkl')
