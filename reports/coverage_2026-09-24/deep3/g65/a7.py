import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',80)
w=pd.read_csv('out_S15.csv',parse_dates=['WEEK_START_DATE']).rename(columns={'USD':'usd'})
c=pd.read_csv('out_S16.csv',parse_dates=['DATE_RANGE_START','DATE_RANGE_END'])
a=pd.read_pickle('official.pkl')
print('weekly rows',len(w),'accounts',w.ADVERTISER_ID.nunique(),'sum',w.usd.sum(),'range',w.WEEK_START_DATE.min(),w.WEEK_START_DATE.max())
print('weekly spend==0 rows',(w.usd==0).sum())
w['yr']=w.WEEK_START_DATE.dt.year
print(w.groupby('yr').usd.sum().to_string())
# general election days
E={2018:'2018-11-06',2020:'2020-11-03',2022:'2022-11-08',2024:'2024-11-05',2019:'2019-11-05',2021:'2021-11-02',2023:'2023-11-07',2025:'2025-11-04'}
for days in (60,90):
    rows=[]
    for y,d in E.items():
        d=pd.Timestamp(d); lo=d-pd.Timedelta(days=days)
        # week fully inside window: week start >= lo and week start <= d-6? use week start in [lo, d)
        m=(w.WEEK_START_DATE>=lo)&(w.WEEK_START_DATE<d)
        yr=w[w.yr==y].usd.sum()
        rows.append((y,days,w[m].usd.sum(),yr,w[m].usd.sum()/yr if yr else np.nan,w[m&(w.usd>0)].ADVERTISER_ID.nunique()))
    print(pd.DataFrame(rows,columns=['year','window_days','usd_in_window','usd_year','share','accounts_spending']).to_string())
w.to_pickle('weekly.pkl'); c.to_pickle('creative.pkl')
