import pandas as pd, re
pd.set_option('display.width',250); pd.set_option('display.max_rows',300); pd.set_option('display.max_columns',40)
exec(open('vote_an.py').read().split("DELEG=")[0])
vm=pd.read_csv('vvmonth.csv'); vm['MON']=vm.MON.str[:7]
# map icpsr -> bioguide per congress
m=v.explode('ICPSR')[['BIOGUIDE','CONGRESS','CHAMBER','STATE','ICPSR','VOTES_ELIGIBLE','VOTES_CAST','MISSED_VOTES']]
m['ICPSR']=m.ICPSR.astype(int)
vm=vm.merge(m[['BIOGUIDE','CONGRESS','ICPSR','STATE']],on=['CONGRESS','ICPSR'],how='left')
print('unmapped member-months', vm.BIOGUIDE.isna().sum(), 'votes', vm[vm.BIOGUIDE.isna()].N.sum())
# consistency check: Voteview sums vs record
agg=vm.groupby(['BIOGUIDE','CONGRESS','CH']).agg(N=('N','sum'),NV=('NV','sum'),P=('PRES','sum')).reset_index()
chk=agg.groupby(['BIOGUIDE','CONGRESS']).agg(N=('N','sum'),NV=('NV','sum'),P=('P','sum')).reset_index().merge(v[['BIOGUIDE','CONGRESS','VOTES_ELIGIBLE','MISSED_VOTES','VOTES_CAST']],on=['BIOGUIDE','CONGRESS'])
chk['elig_eq']=chk.N==chk.VOTES_ELIGIBLE; chk['miss_eq']=chk.NV==chk.MISSED_VOTES; chk['missP_eq']=(chk.NV+chk.P)==chk.MISSED_VOTES
print('record rows checked',len(chk),'eligible matches',chk.elig_eq.sum(),'missed=NV',chk.miss_eq.sum(),'missed=NV+present',chk.missP_eq.sum())
print(chk[~chk.elig_eq|~chk.miss_eq].head(10).to_string())
h=vm[(vm.CH=='HOUSE')&(~vm.STATE.isin(['AS','GU','PR','MP','VI','DC']))].copy()
h['grp']='other'
h.loc[(h.CONGRESS==118)&h.BIOGUIDE.isin(R118),'grp']='run2024'
h.loc[h.BIOGUIDE.isin(R119),'grp']=h.loc[h.BIOGUIDE.isin(R119),'grp'].where(h.CONGRESS==118,'run2026')
h.loc[(h.CONGRESS==118)&h.BIOGUIDE.isin(R119),'grp']='run2026_pre'
t=h.groupby(['MON','grp']).apply(lambda g: round(100*g.NV.sum()/g.N.sum(),2)).unstack()
print(t.to_string())
for who in ['H001095','M001196','P000616','G000574','T000483','P000618','M001195']:
    x=h[h.BIOGUIDE==who].groupby('MON').apply(lambda g: f"{int(g.NV.sum())}/{int(g.N.sum())}")
    print(who, ' '.join(f'{k}:{val}' for k,val in x.items()))
