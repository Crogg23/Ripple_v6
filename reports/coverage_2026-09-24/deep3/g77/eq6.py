import pandas as pd, numpy as np
pd.set_option('display.width',260)
d=pd.read_csv('out_S15.csv'); d['TIME']=pd.to_datetime(d.TIME,format='mixed'); d['yr']=d.TIME.dt.year
def cl(r):
    if 31.8<=r.LAT<=32.5 and -93.55<=r.LON<=-93.25: return 'RED RIVER (Edgefield-Coushatta-Hall Summit)'
    if 32.5<=r.LAT<=32.75 and -94.1<=r.LON<=-93.85: return 'CADDO (Mooringsport-Blanchard)'
    if 31.8<=r.LAT<=32.0 and -94.55<=r.LON<=-94.25: return 'TIMPSON TX'
    return 'other'
d['cl']=d.apply(cl,axis=1)
print(pd.crosstab(d.cl,d.yr).to_string())
print(d[d.MAG>=3].pipe(lambda x: pd.crosstab(x.cl,x.yr)).to_string())
print(d.groupby('cl').agg(n=('MAG','size'),mx=('MAG','max'),first=('TIME','min'),last=('TIME','max'),m4=('MAG',lambda s:(s>=4).sum())).to_string())
rr=d[d.cl.str.startswith('RED')]
print('red river days',rr.TIME.dt.date.nunique(),'depth5',(rr.DEPTH==5).sum(),'of',len(rr),'nets',rr.NET.value_counts().to_dict())
print('same window Jan1-Jun13 red river', rr[(rr.TIME.dt.month<6)|((rr.TIME.dt.month==6)&(rr.TIME.dt.day<=13))].groupby('yr').size().to_dict())
s=pd.read_csv('out_S06.csv'); la=s[s.REGION=='Louisiana']; print(la.groupby('YR').agg(n=('N','sum'),mx=('MAX_MAG','max')).to_dict())
