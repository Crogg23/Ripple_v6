import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',50); pd.set_option('display.max_colwidth',40)
d=pd.read_csv('out_S12.csv')
d['yr']=pd.to_datetime(d.EV_DATE).dt.year
a=d[(d.FAR_PART=='121')&(d.EV_COUNTRY=='USA')].copy()
print('121 US aircraft',len(a), 'events',a.EV_ID.nunique())
a['crew_s']=a.CABI_S+a.FLIG_S; a['crew_aboard']=a[['CABI_F','CABI_S','CABI_M','CABI_N','FLIG_F','FLIG_S','FLIG_M','FLIG_N']].sum(axis=1)
a['pass_aboard']=a[['PASS_F','PASS_S','PASS_M','PASS_N']].sum(axis=1)
print(a.PHASE_FLT_SPEC.value_counts().head(25).to_dict())
g=a.groupby('yr').agg(ac=('EV_ID','size'),crew_s=('crew_s','sum'),ac_crew_s=('crew_s',lambda x:(x>0).sum()),max_crew_s=('crew_s','max'),pass_s=('PASS_S','sum'),ac_pass_s=('PASS_S',lambda x:(x>0).sum()),
  crew_s_no_pass_s=('crew_s',lambda x: 0))
g['ac_crewonly']=a[(a.crew_s>0)&(a.PASS_S==0)].groupby('yr').size()
g['ac_any_serious']=a[(a.crew_s+a.PASS_S+a.PASS_F+a.CABI_F+a.FLIG_F)>0].groupby('yr').size()
print(g.to_string())
x=a[a.crew_s>0]
print('aircraft with crew serious', len(x), 'crew serious total', x.crew_s.sum(), 'median per aircraft', x.crew_s.median())
print(x.crew_s.value_counts().sort_index().to_dict())
print(x.PHASE_FLT_SPEC.value_counts().to_dict())
x['op']=x.OPER_NAME.fillna('').str.upper().str.replace(r'[^A-Z ]','',regex=True).str.replace(r'\b(INC|LLC|CORP|CORPORATION|CO|COMPANY|DBA|THE)\b','',regex=True).str.split().str[:2].str.join(' ')
a['op']=a.OPER_NAME.fillna('').str.upper().str.replace(r'[^A-Z ]','',regex=True).str.replace(r'\b(INC|LLC|CORP|CORPORATION|CO|COMPANY|DBA|THE)\b','',regex=True).str.split().str[:2].str.join(' ')
o=a.groupby('op').agg(ac=('EV_ID','size'),crew_s=('crew_s','sum'),ac_crew_s=('crew_s',lambda s:(s>0).sum()),pass_s=('PASS_S','sum'),y0=('yr','min'),y1=('yr','max'))
o['share_ac_crew_s']=(o.ac_crew_s/o.ac).round(2)
print(o.sort_values('crew_s',ascending=False).head(25).to_string())
a.to_pickle('p121.pkl'); d.to_pickle('s12.pkl')
