import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_columns',40)
d=pd.read_csv('out_S10.csv')
d['TIME']=pd.to_datetime(d.TIME,format='mixed')
d=d[d.TYPE=='earthquake']
d['yr']=d.TIME.dt.year
p=d[d.ZONE=='PERMIAN'].copy()
p['side']=np.where((p.LAT>=32.0)&(p.LON<=-103.064),'NM','TX')
p['plc']=p.PLACE.str.extract(r',\s*([^,]+)$')[0]
print(pd.crosstab(p.side,p.plc))
w=p[(p.TIME.dt.month<6)|((p.TIME.dt.month==6)&(p.TIME.dt.day<=13))]
for m in [3.0,3.5,4.0]:
  print('same-window Jan1-Jun13 M>=',m); print(pd.crosstab(w[w.MAG>=m].yr, w[w.MAG>=m].side).T.to_string())
for m in [3.0,4.0]:
  print('full-year M>=',m); print(pd.crosstab(p[p.MAG>=m].yr, p[p.MAG>=m].side).T.to_string())
print(pd.crosstab(p.yr,p.MAGTYPE).to_string())
print(p[p.MAG>=4.8].sort_values('TIME')[['TIME','MAG','MAGTYPE','NET','PLACE','DEPTH','LAT','LON']].to_string())
p.to_pickle('permian.pkl')
