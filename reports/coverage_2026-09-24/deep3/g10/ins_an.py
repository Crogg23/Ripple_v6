import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_rows',300)
a=pd.read_csv('ins.csv',dtype=str)
a['sd']=pd.to_datetime(a.TIME_PERIOD_START_DATE); a['v']=pd.to_numeric(a.VALUE,errors='coerce')
a['lo']=pd.to_numeric(a.LOWCI,errors='coerce'); a['hi']=pd.to_numeric(a.HIGHCI,errors='coerce')
a=a[a.v.notna()]
W={'pre23':['2023-01-04','2023-02-01','2023-03-01'],'post23':['2023-08-23','2023-09-20','2023-10-18'],
   'pre22':['2022-01-26','2022-03-02','2022-03-30'],'post22':['2022-09-14','2022-10-05','2022-11-02'],
   'pre24':['2024-01-09','2024-02-06','2024-03-05'],'post24':['2024-06-25','2024-07-23','2024-08-20']}
a['w']=None
for k,ds in W.items(): a.loc[a.sd.isin(pd.to_datetime(ds)),'w']=k
s=a[(a.C_GROUP=='By State')&a.w.notna()]
def tab(ind):
    t=s[s.INDICATOR==ind].pivot_table(index='STATE',columns='w',values='v',aggfunc='mean')
    n=s[s.INDICATOR==ind].pivot_table(index='STATE',columns='w',values='v',aggfunc='count')
    t['d23']=t.post23-t.pre23; t['d22']=t.post22-t.pre22; t['d24']=t.post24-t.pre24; t['did']=t.d23-t.d22
    t['nwaves_ok']=(n[['pre23','post23']].min(axis=1)==3)
    return t
u=tab('Uninsured at the Time of Interview'); pb=tab('Public Health Insurance Coverage')
nat=a[(a.C_GROUP=='National Estimate')&a.w.notna()].pivot_table(index='INDICATOR',columns='w',values='v',aggfunc='mean')
print(nat.round(2))
u=u.join(pb[['d23','d22','did']],rsuffix='_pub')
print(u.sort_values('d23',ascending=False).round(2).head(15))
print(u.sort_values('d23').round(2).head(6))
print('states with uninsured up >=2pts Jan-Mar->Aug-Oct 2023:',(u.d23>=2).sum(),' same test 2022 placebo:',(u.d22>=2).sum())
print('median d23',u.d23.median().round(2),'median d22',u.d22.median().round(2),'median d24',u.d24.median().round(2))
print('corr d23 vs public d23', u[['d23','d23_pub']].corr().iloc[0,1].round(2))
u.to_csv('ins_state_windows.csv')
