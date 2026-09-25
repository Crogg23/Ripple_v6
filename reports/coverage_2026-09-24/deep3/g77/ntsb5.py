import pandas as pd, numpy as np, math
pd.set_option('display.width',260)
a=pd.read_pickle('p121.pkl')
a['pass_aboard']=a[['PASS_F','PASS_S','PASS_M','PASS_N']].sum(axis=1)
clean=a[~a.yr.isin([2020,2021,2022,2023])]
print('clean pass aboard',clean.pass_aboard.sum(),'pass_s',clean.PASS_S.sum(),'lap aboard',clean[['LAPC_F','LAPC_S','LAPC_M','LAPC_N']].sum().sum())
t=a[a.DAMAGE.isna()|a.DAMAGE.isin(['NONE'])]
print('no-damage aircraft',len(t),'with crew serious',(t.crew_s>0).sum(),'of all crew-serious aircraft',(a.crew_s>0).sum())
g=a.groupby('yr').agg(ac=('EV_ID','size'),ac_crew_s=('crew_s',lambda s:(s>0).sum()),crew_s=('crew_s','sum'),nodmg=('DAMAGE',lambda s:s.isna().sum()),ev_acc=('EV_TYPE',lambda s:(s=='ACC').sum()))
print(g.T.to_string())
b=g.loc[2008:2019]; c=g.loc[2023:2025]
lam=b.ac_crew_s.mean()*3; obs=int(c.ac_crew_s.sum())
p=1-sum(math.exp(-lam)*lam**k/math.factorial(k) for k in range(obs))
print('2008-19 mean',round(b.ac_crew_s.mean(),2),'median',b.ac_crew_s.median(),'2023-25 mean',round(c.ac_crew_s.mean(),2),'obs',obs,'exp',round(lam,1),'p',round(p,4))
lam2=b.crew_s.mean()*3; obs2=int(c.crew_s.sum()); p2=1-sum(math.exp(-lam2)*lam2**k/math.factorial(k) for k in range(obs2)); print('people',round(b.crew_s.mean(),2),obs2,round(lam2,1),round(p2,4))
x=a[(a.crew_s>0)&(a.yr.between(2023,2025))]
print(x.op.value_counts().head(10).to_dict())
y=a[(a.crew_s>0)&(a.yr.between(2008,2019))]
print((y.op.value_counts()/12).head(8).round(2).to_dict())
# drop top-4 carriers: does rise hold?
big=['SOUTHWEST AIRLINES','DELTA AIR','UNITED AIRLINES','AMERICAN AIRLINES','UNITED AIR']
z=a[(a.crew_s>0)&(~a.op.isin(big))].groupby('yr').size()
print('non-big4 crew-serious aircraft by yr', z.to_dict())
w=a[(a.crew_s>0)&(a.op.isin(big))].groupby('yr').size(); print('big4', w.to_dict())
print(x[['EV_DATE','NTSB_NO','OPER_NAME','ACFT_MAKE','ACFT_MODEL','EV_CITY','EV_STATE','CABI_S','FLIG_S','PASS_S','DAMAGE']].head(12).to_string())
