import pandas as pd, numpy as np, re
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',50)
m=pd.read_pickle('m.pkl'); fac=pd.read_pickle('fac2.pkl')
u=pd.read_csv('unknown_landfills.csv',dtype={'frs':str})
rep=m[m.st=='REPORTED']
keys={1004245:['BLACK WARRIOR','COKER'],1006294:['CENTRAL WASTE'],1007198:['FOOTHILL'],1006191:['JACKSONVILLE N','NORTH SANITARY'],1007197:['NORTH COUNTY'],
1005166:['TOA BAJA'],1003592:['RICHFIELD'],1007194:['TOA ALTA'],1003723:['EAST DUVAL','GREENFIELD'],1011381:['KEARNY','1-D'],1011713:['YAUCO'],
1013978:['HAYWIRE'],1006470:['NABORS'],1008253:['SIMCO'],1004823:['AL TURI'],1007083:['CABO ROJO'],1000331:['BEULAH']}
for fid,ks in keys.items():
    ex=int(u.loc[u.FACILITY_ID==fid,'last_rep'].iloc[0])+1
    hits=rep[(rep.FACILITY_ID!=fid)&(rep.YR>=ex)&rep.FACILITY_NAME.str.upper().str.contains('|'.join(re.escape(k) for k in ks))]
    hits=hits.groupby(['FACILITY_ID','FACILITY_NAME','STATE']).YR.max().reset_index()
    print(fid, ks, 'exit',ex,'->', hits.to_dict('records') if len(hits) else 'no other GHGRP facility by that name after exit')
# parent peers: San Joaquin county, Jacksonville, PR municipalities
for p in ['SAN JOAQUIN','JACKSONVILLE','BLACK WARRIOR','OZARK MOUNTAIN']:
    d=fac[fac.parent.fillna('').str.upper().str.contains(p)]
    print(p, d[['name','state','last_rep','s23']].to_dict('records'))
# large-landfill denominators
lf=fac[fac.landfill]
big=lf[lf.last_direct>=25000]
print('landfills whose last report >=25k:', len(big), big.s23.value_counts().to_dict())
