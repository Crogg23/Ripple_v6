import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_rows',300); pd.set_option('display.max_colwidth',60)
a=pd.read_pickle('S02_adv_all.pkl'); a['usd']=pd.to_numeric(a.SPEND_USD)
keep=set(a[a.PUBLIC_IDS_LIST.fillna('').str.contains('53-6002523')].ADVERTISER_ID)|{'AR10517496269264388097','AR18236540952539824129'}
w=pd.read_pickle('S06_house_weekly.pkl'); w=w[w.ADVERTISER_ID.isin(keep)].copy()
w['usd']=pd.to_numeric(w.SPEND_USD); w['wk']=pd.to_datetime(w.WEEK_START_DATE); w['yr']=w.wk.dt.year
big='AR11776064889791971329'
w['acct']=np.where(w.ADVERTISER_ID==big,'big_US_House','members')
print('accounts in set',len(keep),'with weekly rows',w.ADVERTISER_ID.nunique(),'weekly usd',w.usd.sum(),'stats usd',a[a.ADVERTISER_ID.isin(keep)].usd.sum())
E={2018:'2018-11-06',2020:'2020-11-03',2022:'2022-11-08',2024:'2024-11-05'}
for y,e in E.items():
    e=pd.Timestamp(e)
    inwin=w[(w.wk>=e-pd.Timedelta(days=60))&(w.wk+pd.Timedelta(days=6)<e)&(w.usd>0)]
    prior=w[(w.wk>=e-pd.Timedelta(days=120))&(w.wk<e-pd.Timedelta(days=60))&(w.usd>0)]
    print(y,'last60',inwin.usd.sum(),inwin.ADVERTISER_ID.nunique(),'prior60',prior.usd.sum(),prior.ADVERTISER_ID.nunique())
    if len(inwin): print(inwin.groupby(['ADVERTISER_ID','ADVERTISER_NAME']).agg(usd=('usd','sum'),weeks=('wk','nunique'),first=('wk','min'),last=('wk','max')).to_string())
for y in [2019,2021,2023,2025]:
    e=pd.Timestamp(f'{y}-11-05')
    inwin=w[(w.wk>=e-pd.Timedelta(days=60))&(w.wk+pd.Timedelta(days=6)<e)&(w.usd>0)]
    prior=w[(w.wk>=e-pd.Timedelta(days=120))&(w.wk<e-pd.Timedelta(days=60))&(w.usd>0)]
    print(y,'same window',inwin.usd.sum(),inwin.ADVERTISER_ID.nunique(),'prior60',prior.usd.sum(),prior.ADVERTISER_ID.nunique())
print(w.pivot_table(index='yr',columns='acct',values='usd',aggfunc='sum',margins=True))
for y in range(2019,2027):
    d=w[(w.yr==y)&(w.wk.dt.month<=7)]
    per=d[d.acct=='members'].groupby('ADVERTISER_ID').usd.sum()
    print(y,'Jan-Jul all',d.usd.sum(),'members',d[d.acct=='members'].usd.sum(),'member accts',(per>0).sum(),'median/acct',per[per>0].median(), 'big',d[d.acct=='big_US_House'].usd.sum())
b=w[w.acct=='big_US_House']; print('big first/last',b[b.usd>0].wk.min(),b[b.usd>0].wk.max(),'weeks',(b.usd>0).sum())
print(b.groupby(b.wk.dt.to_period('Q')).usd.sum().to_string())
