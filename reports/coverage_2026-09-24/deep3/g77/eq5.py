import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_colwidth',45)
c=pd.read_csv('out_S14.csv')
c=c[c.LON0>=-105.5]
c['cell']=c.LAT0.astype(str)+','+c.LON0.astype(str)
w=c.pivot_table(index='cell',columns='YR',values='M3_WIN',aggfunc='sum',fill_value=0)
f=c.pivot_table(index='cell',columns='YR',values='M3',aggfunc='sum',fill_value=0)
eg=c.groupby('cell').PLACE_EG.last()
r=pd.DataFrame({'win2026':w[2026],'win2025':w.get(2025),'win2024':w.get(2024),'max_full_2010_20':f[list(range(2010,2021))].max(axis=1),'max_full_2021_25':f[list(range(2021,2026))].max(axis=1),'full2010_25':f[list(range(2010,2026))].sum(axis=1),'place':eg})
print('cells east of 105.5W with any M3+ in 2026 window:', (r.win2026>0).sum(), 'median', r[r.win2026>0].win2026.median())
print(r.sort_values('win2026',ascending=False).head(15).to_string())
