import pandas as pd, numpy as np
pd.set_option('display.width',260)
a=pd.read_pickle('p121.pkl')
print(a.DAMAGE.value_counts(dropna=False).to_dict())
a['crew_aboard']=a[['CABI_F','CABI_S','CABI_M','CABI_N','FLIG_F','FLIG_S','FLIG_M','FLIG_N']].sum(axis=1)
a['pass_aboard']=a[['PASS_F','PASS_S','PASS_M','PASS_N']].sum(axis=1)
a['lap']=a[['LAPC_F','LAPC_S','LAPC_M','LAPC_N']].sum(axis=1)
tot_aboard=a.crew_aboard.sum()+a.pass_aboard.sum()+a.lap.sum()
cabin_aboard=a[['CABI_F','CABI_S','CABI_M','CABI_N']].sum().sum()
print('aboard',tot_aboard,'crew',a.crew_aboard.sum(),'cabin crew coded',cabin_aboard,'pass',a.pass_aboard.sum())
ser=a.crew_s.sum()+a.PASS_S.sum()+a.LAPC_S.sum()
print('serious total',ser,'crew',a.crew_s.sum(),'cabi coded',a.CABI_S.sum(),'flig coded',a.FLIG_S.sum(),'pass',a.PASS_S.sum())
# years with clean split
clean=a[~a.yr.isin([2020,2021,2022,2023])]
print('clean yrs: cabin aboard',clean[['CABI_F','CABI_S','CABI_M','CABI_N']].sum().sum(),'all aboard',clean.crew_aboard.sum()+clean.pass_aboard.sum()+clean.lap.sum(),'cabi_s',clean.CABI_S.sum(),'flig_s',clean.FLIG_S.sum(),'pass_s',clean.PASS_S.sum())
t=a[a.DAMAGE.isin(['NONE','MINR'])]
g=t.groupby('yr').agg(ac=('EV_ID','size'),ac_crew_s=('crew_s',lambda s:(s>0).sum()),crew_s=('crew_s','sum'),ac_pass_s=('PASS_S',lambda s:(s>0).sum()),pass_s=('PASS_S','sum'))
print(g.to_string())
b=g.loc[2008:2019]; c=g.loc[2023:2025]
print('ac_crew_s avg 2008-19',b.ac_crew_s.mean().round(2),'2023-25',c.ac_crew_s.mean().round(2),'crew_s', b.crew_s.mean().round(2), c.crew_s.mean().round(2))
from scipy.stats import poisson
lam=b.ac_crew_s.mean()*3; obs=c.ac_crew_s.sum(); print('obs',obs,'exp',lam,'p',1-poisson.cdf(obs-1,lam))
# operators contributing 2023-25
x=a[(a.crew_s>0)&(a.yr.between(2023,2025))]
print(x.op.value_counts().head(10).to_dict())
y=a[(a.crew_s>0)&(a.yr.between(2008,2019))]
print((y.op.value_counts()/12).head(8).round(2).to_dict())
