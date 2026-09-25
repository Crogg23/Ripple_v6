import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_columns',40)
p=pd.read_pickle('permian.pkl')
p['basin']=np.select([p.LON<=-103.0, p.LON>=-101.2],[ 'DELAWARE(west of 103W)','EAST(east of 101.2W, Scurry etc)'],'MIDLAND(103W-101.2W)')
for m in [3.0,4.0]:
  x=p[p.MAG>=m]
  print('M>=',m); print(pd.crosstab([x.basin],x.yr).to_string())
nm=p[p.side=='NM']
print(pd.crosstab(nm.yr,nm.NET)); print(pd.crosstab(nm.yr,nm.MAGTYPE))
nm3=nm[(nm.MAG>=3)&(nm.yr>=2021)].copy()
nm3['cell']=(nm3.LAT.round(1)).astype(str)+','+(nm3.LON.round(1)).astype(str)
nm3['town']=nm3.PLACE.str.replace(r'^[\d\.]+ km [NSEW]+ of ','',regex=True)
print(nm3.groupby('town').agg(n=('MAG','size'),mx=('MAG','max'),first=('TIME','min'),last=('TIME','max')).sort_values('n',ascending=False).to_string())
print(nm3.groupby('cell').size().sort_values(ascending=False).head(10))
print(nm3[nm3.yr==2026][['TIME','MAG','MAGTYPE','NET','PLACE','DEPTH','LAT','LON']].to_string())
# ratio small to big on NM side as detection check
for s in ['NM','TX']:
  x=p[(p.side==s)&(p.yr>=2019)]
  t=pd.crosstab(x.yr, pd.cut(x.MAG,[0,2.99,3.49,9]))
  print(s); print(t.to_string())
