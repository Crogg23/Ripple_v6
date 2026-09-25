import pandas as pd, numpy as np, warnings
warnings.filterwarnings('ignore')
pd.set_option('display.width',280); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',40)
e=pd.read_pickle('out_S03.pkl'); s=pd.read_pickle('out_S10.pkl')
s['cik']=s.CIK.astype(int); s['d']=pd.to_datetime(s.D)
s['val']=pd.to_numeric(s.VAL_CALC,errors='coerce').fillna(0)
print('insider sale rows', len(s), 'issuers', s.cik.nunique(), 'range', s.d.min(), s.d.max(), 'val total $B', s.val.sum()/1e9)
print('val_calc vs val_col equal share', (np.isclose(s.val, pd.to_numeric(s.VAL_COL,errors='coerce').fillna(0))).mean(), 'max px', s.MAX_PX.max())
e['cik']=e.CIK.astype(int)
e['filed']=pd.to_datetime(e.FILED,format='%Y%m%d',errors='coerce'); e['per']=pd.to_datetime(e.PERIOD,format='%Y%m%d',errors='coerce')
e['lag']=(e.filed-e.per).dt.days
k=e[e.FORM.isin(['10-K','10-Q'])&e.AFS.isin(['1-LAF','2-ACC','4-NON'])].copy()
dl={('10-K','1-LAF'):60,('10-K','2-ACC'):75,('10-K','4-NON'):90,('10-Q','1-LAF'):40,('10-Q','2-ACC'):40,('10-Q','4-NON'):45}
ext={'10-K':15,'10-Q':5}
k['ext_dl']=k.per+pd.to_timedelta([dl[(f,a)]+ext[f]+3 for f,a in zip(k.FORM,k.AFS)],unit='D')
k['late']=k.filed>k.ext_dl
k=k[(k.filed>='2023-02-01')&(k.filed<='2024-12-31')]
# issuers that appear in insider data at all (so a miss means something)
has=set(s.cik)
k['ins_cov']=k.cik.isin(has)
print('filings', len(k), 'late', k.late.sum(), 'late with any insider sale data at company', (k.late&k.ins_cov).sum())
# sales by cik into a dict of sorted arrays
g={c:(x.d.values, x.val.values) for c,x in s.groupby('cik')}
def win_sum(c, a, b):
    if c not in g: return 0.0, 0
    d,v=g[c]; m=(d>=np.datetime64(a))&(d<=np.datetime64(b)); return v[m].sum(), int(m.sum())
res=[]
for r in k.itertuples():
    pre_v,pre_n=win_sum(r.cik, r.filed-pd.Timedelta(days=30), r.filed-pd.Timedelta(days=1))
    od_v,od_n=(0.0,0)
    if r.late: od_v,od_n=win_sum(r.cik, r.ext_dl+pd.Timedelta(days=1), r.filed-pd.Timedelta(days=1))
    res.append((pre_v,pre_n,od_v,od_n))
k[['pre_v','pre_days','od_v','od_days']]=pd.DataFrame(res,index=k.index)
k.to_pickle('ins_windows.pkl')
cov=k[k.ins_cov]
print('\n30 days before filing, share of filings with any insider open-market sale (companies that show up in insider data at all):')
print(cov.groupby(['AFS','FORM','late']).agg(n=('ADSH','size'),any_sale=('pre_days',lambda x:(x>0).mean()),sale_M=('pre_v',lambda x:x.sum()/1e6)).round(3).to_string())
L=k[k.late]
print('\nlate filings', len(L), 'companies', L.cik.nunique(), 'with sales while overdue', (L.od_days>0).sum(), 'companies', L[L.od_days>0].cik.nunique(), '$M', L.od_v.sum()/1e6)
od=L[L.od_days>0].copy(); od['overdue_days']=(od.filed-od.ext_dl).dt.days
print(od.sort_values('od_v',ascending=False)[['CIK','NAME','FORM','AFS','PERIOD','FILED','overdue_days','od_days','od_v','COUNTRYBA','SIC']].head(30).to_string(index=False))
print('median $ per overdue-sale filing', od.od_v.median(), 'top3 share', od.sort_values('od_v',ascending=False).od_v.head(3).sum()/od.od_v.sum())
