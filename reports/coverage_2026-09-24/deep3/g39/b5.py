import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_rows',300); pd.set_option('display.max_colwidth',40)
fy=pd.read_pickle('fy.pkl'); info=pd.read_pickle('info.pkl')
yrs=list(range(2010,2024))
g=fy.copy(); g[yrs]=g[yrs].fillna(0)
g['chg']=g[2023]-g[2015]
top=g.sort_values('chg',ascending=False).head(15).join(info)
tp=top[['sector','FACILITY_NAME','STATE','NAICS_CODE',2015,2019,2023,'chg']].copy()
for c in [2015,2019,2023,'chg']: tp[c]=(tp[c]/1e6).round(2)
print(tp.to_string())
tot=g[yrs].sum()/1e6
print('all direct (sector 2-8,14,15, excl biogenic) Mt by year', tot.round(0).to_dict())
print('facilities that grew by >1 Mt 2015-2023:', (g.chg>1e6).sum())
# FRS for LNG facilities -> ICIS-Air
f=pd.read_csv('q04.csv',dtype={'FACILITY_ID':str,'FRS':str})
lng_ids=['1002259','1013179','1014135','1013553','1005420','1013753']
frs=f[f.FACILITY_ID.isin(lng_ids)].groupby('FACILITY_ID').FRS.apply(lambda s:sorted(set(s.dropna()))).to_dict()
print(frs)
fac=pd.read_csv('q06.csv',dtype=str)
t=pd.read_pickle('t3.pkl'); v=pd.read_csv('q09.csv',dtype=str); fa=pd.read_csv('q10.csv',dtype={'PGM_SYS_ID':str}); ia=pd.read_csv('q11.csv',dtype=str)
for fid,fl in frs.items():
    ps=fac[fac.REGISTRY_ID.isin([x.split('.')[0] for x in fl])]
    for _,p in ps.iterrows():
        tt=t[t.PGM_SYS_ID==p.PGM_SYS_ID]; tt=tt[tt.yr>=2016]
        vv=v[v.PGM_SYS_ID==p.PGM_SYS_ID]; ff=fa[fa.PGM_SYS_ID==p.PGM_SYS_ID]; ii=ia[ia.PGM_SYS_ID==p.PGM_SYS_ID]
        ff16=ff[ff.SETTLEMENT_ENTERED_DATE.fillna('')>='2016']
        print(fid, info.loc[fid,'FACILITY_NAME'], '|', p.PGM_SYS_ID, p.FACILITY_NAME, p.AIR_POLLUTANT_CLASS_CODE, p.CURRENT_HPV,
              '| certs16+', len(tt), 'Y', (tt.FACILITY_RPT_DEVIATION_FLAG=='Y').sum(), 'N', (tt.FACILITY_RPT_DEVIATION_FLAG=='N').sum(),
              '| viol', len(vv), 'HPV', (vv.ENF_RESPONSE_POLICY_CODE=='HPV').sum(), '| formal16+', len(ff16), 'pen', ff16.PENALTY_AMOUNT.sum(), '| NOV', len(ii))
