import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_rows',300); pd.set_option('display.max_colwidth',44)
t=pd.read_pickle('t3.pkl')
fac=pd.read_csv('q06.csv',dtype=str); fi=fac.set_index('PGM_SYS_ID')
t['STATE']=fi.STATE.reindex(t.PGM_SYS_ID).values
fl=t[t.FACILITY_RPT_DEVIATION_FLAG.notna()&(t.yr>=2010)&(t.yr<=2025)]
r=fl.groupby(['STATE','yr']).FACILITY_RPT_DEVIATION_FLAG.apply(lambda s:round((s=='Y').mean(),2)).unstack()
n=fl.groupby(['STATE','yr']).size().unstack()
print(r.loc[['TX','CO','LA','CA','OH','PA','IL','NC','SD','WY','NM','UT','KY']].to_string())
print(n.loc[['TX','CO','SD','NC']].to_string())
# Colorado: big facilities
co=fac[(fac.STATE=='CO')&fac.FACILITY_NAME.str.contains('SUNCOR|CHEROKEE|COMANCHE|PAWNEE|CRAIG|HAYDEN|CEMEX|HOLCIM|NUCOR|EVRAZ|PLATTEVILLE|FT ST VRAIN|FORT ST VRAIN',case=False,na=False)]
x=t[t.PGM_SYS_ID.isin(co.PGM_SYS_ID)&(t.yr>=2015)]
x=x.assign(name=fi.FACILITY_NAME.reindex(x.PGM_SYS_ID).values)
print(x.groupby('name').FACILITY_RPT_DEVIATION_FLAG.apply(lambda s:s.fillna('_').value_counts().to_dict()).to_string())
