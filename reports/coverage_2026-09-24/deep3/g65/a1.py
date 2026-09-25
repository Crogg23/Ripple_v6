import pandas as pd, numpy as np
g=pd.read_csv('out_S09.csv',dtype={'SUB':str},keep_default_na=False,na_values=[''])
s=pd.read_csv('out_S10.csv',keep_default_na=False,na_values=[''])
nm=pd.read_csv('out_S11.csv',keep_default_na=False,na_values=[''])
print('stats rows',len(s),'distinct ids',s.ADVERTISER_ID.nunique()); print(s.REGIONS.value_counts().head(8).to_string())
print(s.PUBLIC_IDS_LIST.dropna().sample(8,random_state=1).to_string())
g=g.merge(nm[['ADVERTISER_ID','NM']],on='ADVERTISER_ID',how='left')
for who in ['MONICA TRANEL FOR MONTANA','NANCY MACE FOR CONGRESS','Inmo Khang']:
    x=g[g.NM==who]
    print('\n==',who,'ids',x.ADVERTISER_ID.nunique(),'rows',len(x),'sum',x.USD.sum())
    print(x.groupby('ADVERTISER_ID').agg(rows=('USD','size'),usd=('USD','sum'),n100=('USD',lambda v:(v==100).sum()),n0=('USD',lambda v:(v==0).sum()),blank=('SUB',lambda v:v.isna().sum())).to_string())
    print(x.sort_values('USD',ascending=False).head(6)[['ADVERTISER_ID','SUB','USD']].to_string())
# blank sub rows
b=g[g.SUB.isna()]
print('\nblank rows',len(b),'usd',b.USD.sum(),'n0',(b.USD==0).sum(),'n100',(b.USD==100).sum(), 'country', b.COUNTRY.value_counts().to_dict())
st=g[g.SUB.notna()].groupby('ADVERTISER_ID').USD.agg(['sum','size'])
bb=b.set_index('ADVERTISER_ID').USD
j=pd.DataFrame({'blank':bb}).join(st)
print(j.describe().to_string())
print((j['blank']==j['sum']).mean())
print(b.sort_values('USD',ascending=False).head(10).to_string())
