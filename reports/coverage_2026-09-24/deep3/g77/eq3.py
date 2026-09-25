import pandas as pd, numpy as np
pd.set_option('display.width',250)
p=pd.read_pickle('permian.pkl')
nm=p[(p.side=='NM')]
nm['west']=np.where(nm.LON< -104.2,'west of 104.2W (Carlsbad-Hope-Whites City)','east (Malaga-Jal-Eunice)')
print(pd.crosstab(nm[nm.MAG>=3].west, nm[nm.MAG>=3].yr).to_string())
print(pd.crosstab(nm[nm.MAG>=2.5].west, nm[nm.MAG>=2.5].yr).to_string())
print(nm[nm.MAG>=4][['TIME','MAG','MAGTYPE','NET','PLACE','LAT','LON']].to_string())
w=nm[nm.LON< -104.2]
print(w[w.yr<=2024][['TIME','MAG','NET','PLACE','LAT','LON']].to_string())
