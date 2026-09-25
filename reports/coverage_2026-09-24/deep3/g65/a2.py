import pandas as pd, numpy as np
g=pd.read_csv('out_S09.csv',dtype={'SUB':str},keep_default_na=False,na_values=[''])
s=pd.read_csv('out_S10.csv',keep_default_na=False,na_values=[''])
a=g.groupby('ADVERTISER_ID').agg(geo=('USD','sum'),rows=('USD','size'),n100=('USD',lambda v:(v==100).sum()),n0=('USD',lambda v:(v==0).sum()),mx=('USD','max'))
a=a.join(s.set_index('ADVERTISER_ID')[['ADVERTISER_NAME','REGIONS','USD_TOTAL','TOTAL_CREATIVES']],how='left')
print('geo ids',len(a),'in stats',a.USD_TOTAL.notna().sum(), 'regions', a.REGIONS.value_counts(dropna=False).head().to_dict())
a['diff']=a.geo-a.USD_TOTAL
print('geo sum',a.geo.sum(),'stats sum (same ids)',a.USD_TOTAL.sum(), 'stats US total all', s[s.REGIONS=='US'].USD_TOTAL.sum())
print('exact equal', (a['diff']==0).mean(), 'geo>stats', (a['diff']>0).mean(), 'geo<stats',(a['diff']<0).mean())
print(a['diff'].describe().to_string())
# all-100 advertisers
allh=a[(a.n100==a.rows)]
print('\nall rows $100 advertisers', len(allh), 'geo', allh.geo.sum(), 'stats', allh.USD_TOTAL.sum())
print(allh.USD_TOTAL.describe().to_string())
print(allh.sort_values('rows',ascending=False).head(8)[['ADVERTISER_NAME','rows','geo','USD_TOTAL','TOTAL_CREATIVES']].to_string())
# relation: diff vs n100
a['bucket']=pd.cut(a.USD_TOTAL,[-1,0,100,1000,10000,100000,1e6,1e10])
print(a.groupby('bucket').agg(n=('geo','size'),geo=('geo','sum'),stats=('USD_TOTAL','sum'),med_rows=('rows','median'),med_n100=('n100','median'),share_rows100=('n100','sum')).to_string())
# zeros: what are 0 rows? advertisers where total is 0
z=a[a.USD_TOTAL==0]; print('\nstats total 0:',len(z),'their geo sum',z.geo.sum(), 'n0 rows', z.n0.sum())
a.to_pickle('adv.pkl')
