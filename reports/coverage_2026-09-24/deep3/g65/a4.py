import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_colwidth',38)
per=pd.read_pickle('camp_adv.pkl')
g=pd.read_csv('out_S09.csv',dtype={'SUB':str},keep_default_na=False,na_values=[''])
g=g[g.SUB.notna()]
tot=g.groupby('ADVERTISER_ID').USD.sum()
top=g.sort_values('USD',ascending=False).groupby('ADVERTISER_ID').head(1).set_index('ADVERTISER_ID')
per['top_st']=top.SUB; per['top_usd']=top.USD; per['top_share']=per.top_usd/tot
m=per[(per.top_st!=per.hs)&(per.top_share>=0.6)&(per.attr>=10000)].sort_values('attr',ascending=False)
print('advertisers attr>=10k:',(per.attr>=10000).sum(),' dominant state != FEC candidate state (>=60%):',len(m), ' $',m.attr.sum())
print(m[['ADVERTISER_NAME','cmte_nm','cand_id','name','hs','years','top_st','top_share','attr']].to_string())
m.to_csv('mismatch.csv')
