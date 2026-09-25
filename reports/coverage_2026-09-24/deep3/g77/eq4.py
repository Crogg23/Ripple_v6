import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_colwidth',45)
c=pd.read_csv('out_S14.csv')
c['cell']=c.LAT0.astype(str)+','+c.LON0.astype(str)
w=c.pivot_table(index='cell',columns='YR',values='M3_WIN',aggfunc='sum',fill_value=0)
f=c.pivot_table(index='cell',columns='YR',values='M3',aggfunc='sum',fill_value=0)
eg=c.groupby('cell').PLACE_EG.last()
r=pd.DataFrame({'win2026':w[2026],'win2025':w[2025],'win2024':w[2024],'win2021_23_avg':w[[2021,2022,2023]].mean(axis=1).round(1),
  'full2010_20':f[list(range(2010,2021))].sum(axis=1),'full2021_23':f[[2021,2022,2023]].sum(axis=1),'full2024_25':f[[2024,2025]].sum(axis=1),'place':eg})
r['jump']=r.win2026-r.win2021_23_avg
# exclude tectonic west? show top by 2026 window and by jump
print(r.sort_values('win2026',ascending=False).head(25).to_string())
print(r.sort_values('jump',ascending=False).head(15).to_string())
# rank among cells with >=5 in 2026 window where 2010-2020 full had <=3
q=r[(r.win2026>=5)]
print(q.sort_values('full2010_20').to_string())
