import pandas as pd, numpy as np
pd.set_option('display.width',250)
e=pd.read_pickle('ad_district2.pkl'); v=pd.read_csv('out_S17.csv',keep_default_na=False,na_values=['']); m=pd.read_csv('out_S19.csv')
# official ads 2023-01-03 onward (118th/119th), district-targeted; credit the district holder (named accounts only when name matches, generic always)
x=e[(e.DATE_RANGE_START>='2023-01-03')&(e.name_ok|e.generic)].copy()
x['dn']=x.dn.astype(int); v['dn']=v.DISTRICT_CODE.astype(int)
x=x.merge(v[['CONGRESS','STATE_ABBREV','dn','BIOGUIDE_ID']],left_on=['cong','st','dn'],right_on=['CONGRESS','STATE_ABBREV','dn'],how='left')
# split an ad's midpoint across the districts it targeted
x['share']=x.mid/x.groupby('AD_ID').AD_ID.transform('size')
per=x.groupby('BIOGUIDE_ID').agg(off_mid=('share','sum'),ads=('AD_ID','nunique'),generic_ads=('generic','sum'))
# House members serving in 118th (2023-24): denominator
h=v[v.CONGRESS==118].drop_duplicates('BIOGUIDE_ID')[['BIOGUIDE_ID','BIONAME','STATE_ABBREV','dn','PARTY_CODE']]
m24=m[m.CYCLE==2024].set_index('BIOGUIDE')
h=h.join(m24[['OUTSIDE_AGAINST','OUTSIDE_FOR']],on='BIOGUIDE_ID')
h=h.join(per,on='BIOGUIDE_ID')
h['off_mid']=h.off_mid.fillna(0); h['buys']=h.off_mid>0
print('118th House members',len(h),'with 2024 outside-money row',h.OUTSIDE_AGAINST.notna().sum(),' buying official Google ads 2023-26 (district-targeted):',h.buys.sum())
h['oa']=h.OUTSIDE_AGAINST.fillna(0)
h['tier']=pd.cut(h.oa,[-1,0,100000,1000000,5000000,1e12],labels=['$0','<$100K','$100K-1M','$1M-5M','$5M+'])
t=h.groupby('tier',observed=False).agg(members=('BIOGUIDE_ID','size'),buy=('buys','sum'),mid=('off_mid','sum'),median_mid_buyers=('off_mid',lambda s:s[s>0].median()))
t['buy_rate']=t.buy/t.members
print(t.to_string())
print('party split'); print(h.groupby('PARTY_CODE').agg(members=('buys','size'),buy=('buys','sum'),mid=('off_mid','sum')).to_string())
top=h.sort_values('off_mid',ascending=False).head(15)
print(top[['BIONAME','STATE_ABBREV','dn','PARTY_CODE','off_mid','ads','generic_ads','oa']].to_string())
# concentration
b=h[h.buys].sort_values('off_mid',ascending=False)
print('buyers',len(b),'total mid',b.off_mid.sum(),'top5 share',b.off_mid.head(5).sum()/b.off_mid.sum(),'median buyer mid',b.off_mid.median())
h.to_pickle('members118.pkl')
