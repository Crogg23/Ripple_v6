import pandas as pd, re, warnings
warnings.filterwarnings('ignore')
pd.set_option('display.width',250); pd.set_option('display.max_rows',300)
exec(open('month_an.py').read().split("t=h.groupby")[0].replace("print(","(lambda *a,**k:None)("))
in119=set(v[v.CONGRESS==119].BIOGUIDE)
hv=pd.read_csv('house_flagged.csv')
g=hv[(hv.CONGRESS==118)&hv.full].copy()
g['grp']='stayed'
g.loc[~g.BIOGUIDE.isin(in119),'grp']='left_not_running'
g.loc[g.run,'grp']='ran_2024'
print(g.groupby('grp').MISSED_VOTE_PCT.agg(['count','median','mean']))
print('pooled', g.groupby('grp').apply(lambda x: round(100*x.MISSED_VOTES.sum()/x.VOTES_ELIGIBLE.sum(),2)))
# monthly: departing non-runners
h.loc[(h.CONGRESS==118)&(h.grp=='other')&(~h.BIOGUIDE.isin(in119)),'grp']='left_not_running'
H=h[h.CONGRESS==118]
per=H.groupby(['MON','grp','BIOGUIDE']).agg(N=('N','sum'),NV=('NV','sum')).reset_index()
per['r']=100*per.NV/per.N
t=per.groupby(['MON','grp']).apply(lambda x: f"{100*x.NV.sum()/x.N.sum():.1f}|{x.r.median():.1f}").unstack()
print('118th, pooled|median member, by month'); print(t.to_string())
# 2026 runners minus Hunt, Moulton
H9=h[h.CONGRESS==119].copy()
H9['grp2']=H9.grp
H9.loc[H9.BIOGUIDE.isin(['H001095','M001196']),'grp2']='hunt_moulton'
per9=H9.groupby(['MON','grp2','BIOGUIDE']).agg(N=('N','sum'),NV=('NV','sum')).reset_index(); per9['r']=100*per9.NV/per9.N
t9=per9.groupby(['MON','grp2']).apply(lambda x: f"{100*x.NV.sum()/x.N.sum():.1f}|{x.r.median():.1f}").unstack()
print('119th, pooled|median member'); print(t9.to_string())
# period summary 119: Jan-Nov 2025 vs Dec 2025-Jun 2026
H9['per']=(H9.MON>='2025-12').map({True:'Dec25-Jun26',False:'Jan-Nov25'})
s=H9.groupby(['per','grp2']).apply(lambda x: round(100*x.NV.sum()/x.N.sum(),2)).unstack(); print(s)
pm=H9.groupby(['per','grp2','BIOGUIDE']).agg(N=('N','sum'),NV=('NV','sum')).reset_index(); pm['r']=100*pm.NV/pm.N
print(pm.groupby(['per','grp2']).r.median().unstack())
# how many 2026 runners had their worst stretch in Dec25-Jun26
w=pm[pm.grp2!='other'].pivot_table(index='BIOGUIDE',columns='per',values='r')
w['up']=w['Dec25-Jun26']>w['Jan-Nov25']; w['who']=w.index.map(R119); print(w.sort_values('Dec25-Jun26',ascending=False).round(2).to_string()); print('runners up in campaign stretch', w.up.sum(), 'of', len(w))
o=pm[pm.grp2=='other'].pivot_table(index='BIOGUIDE',columns='per',values='r').dropna(); print('others up', (o['Dec25-Jun26']>o['Jan-Nov25']).sum(), 'of', len(o))
