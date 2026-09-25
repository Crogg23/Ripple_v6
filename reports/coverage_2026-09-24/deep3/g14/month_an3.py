import pandas as pd, warnings
warnings.filterwarnings('ignore')
exec(open('month_an.py').read().split("t=h.groupby")[0].replace("print(","(lambda *a,**k:None)("))
hv=pd.read_csv('house_flagged.csv'); full119=set(hv[(hv.CONGRESS==119)&hv.full].BIOGUIDE)
H9=h[(h.CONGRESS==119)&h.BIOGUIDE.isin(full119)].copy()
H9['per']=(H9.MON>='2025-12').map({True:'B Dec25-Jun26',False:'A Jan-Nov25'})
H9['g']=H9.BIOGUIDE.isin(R119).map({True:'runners16',False:'others'})
pm=H9.groupby(['per','g','BIOGUIDE']).agg(N=('N','sum'),NV=('NV','sum')).reset_index(); pm['r']=100*pm.NV/pm.N
print('pooled'); print(pm.groupby(['per','g']).apply(lambda x: round(100*x.NV.sum()/x.N.sum(),2)).unstack())
print('median member'); print(pm.groupby(['per','g']).r.median().unstack().round(2))
print('members', pm.groupby(['per','g']).BIOGUIDE.nunique().unstack())
print('votes in window', H9.groupby('per').apply(lambda x: x[x.g=='others'].groupby('BIOGUIDE').N.sum().median()))
o=pm[pm.g=='others'].pivot_table(index='BIOGUIDE',columns='per',values='r').dropna(); print('others up', (o.iloc[:,1]>o.iloc[:,0]).sum(), 'of', len(o))
for who in ['C001130','L000595','B001282','C001103']:
    x=h[(h.BIOGUIDE==who)&(h.CONGRESS==119)].groupby('MON').apply(lambda g: f"{int(g.NV.sum())}/{int(g.N.sum())}")
    print(R119[who], ' '.join(f'{k[2:]}:{val}' for k,val in x.items()))
