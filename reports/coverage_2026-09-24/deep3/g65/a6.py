import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',55)
s=pd.read_pickle('stats_us.pkl')
g=pd.read_csv('out_S09.csv',dtype={'SUB':str},keep_default_na=False,na_values=[''])
off=s[s.PUBLIC_IDS_LIST.fillna('').str.contains('53-6002523')].copy()
print('official House accounts (EIN 53-6002523):',len(off),' stats $',off.USD_TOTAL.sum(), ' ads', pd.to_numeric(off.TOTAL_CREATIVES,errors='coerce').sum())
# also other names looking official but different EIN
oth=s[s.ADVERTISER_NAME.str.upper().str.contains('HOUSE OF REP') & ~s.PUBLIC_IDS_LIST.fillna('').str.contains('53-6002523')]
print('HOUSE OF REP name, other id:',len(oth)); print(oth[['ADVERTISER_NAME','USD_TOTAL','PUBLIC_IDS_LIST']].to_string())
gg=g[g.ADVERTISER_ID.isin(off.ADVERTISER_ID)]
st=gg[gg.SUB.notna()]
tot=st.groupby('ADVERTISER_ID').USD.sum()
top=st.sort_values('USD',ascending=False).groupby('ADVERTISER_ID').head(1).set_index('ADVERTISER_ID')
blank=gg[gg.SUB.isna()].groupby('ADVERTISER_ID').USD.sum()
nrows=st.groupby('ADVERTISER_ID').size()
a=off.set_index('ADVERTISER_ID')[['ADVERTISER_NAME','USD_TOTAL','TOTAL_CREATIVES']].join(pd.DataFrame({'attr':tot,'top_st':top.SUB,'top_usd':top.USD,'blank':blank,'nrows':nrows}))
a['out']=a.attr-a.top_usd
# conservative: each non-top row could be as little as (v-100)
nt=st.merge(top[['SUB']].rename(columns={'SUB':'TOPSUB'}),left_on='ADVERTISER_ID',right_index=True)
nt=nt[nt.SUB!=nt.TOPSUB]
a['out_lb']=nt.assign(lb=np.maximum(nt.USD-100,0)).groupby('ADVERTISER_ID').lb.sum()
a['out_lb']=a.out_lb.fillna(0)
a['top_share']=a.top_usd/a.attr; a['out_share_lb']=a.out_lb/a.attr
a=a.sort_values('attr',ascending=False)
a.to_pickle('official.pkl')
print(a[['ADVERTISER_NAME','USD_TOTAL','attr','blank','top_st','top_share','out','out_lb','out_share_lb','nrows']].head(45).to_string())
b=a[a.attr>=10000]
print('\naccounts attr>=10k',len(b),'median top_share',b.top_share.median(),'n with out_lb share>=10%',(b.out_share_lb>=.10).sum(),'>=25%',(b.out_share_lb>=.25).sum())
print('total attr',a.attr.sum(),'out',a.out.sum(),'out_lb',a.out_lb.sum())
