import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',40)
p=pd.read_csv('S07.csv',dtype={'BHCMISID':str,'GRANTNUMBER':str})
p['pat']=p.L39A.fillna(0)+p.L39B.fillna(0)
u=pd.read_csv('S05.csv',dtype=str)
u['h']=pd.to_numeric(u.OPERATING_HOURS_PER_WEEK)
svc=u[u.SITE_TYPE_DESCRIPTION!='Administrative']
g=svc.groupby('HEALTH_CENTER_NUMBER').agg(name=('HEALTH_CENTER_NAME','first'),st=('HEALTH_CENTER_STATE','first'),
   sites=('BPHC_ASSIGNED_NUMBER','size'),perm=('LOCATION_TYPE_DESCRIPTION',lambda s:(s=='Permanent').sum()),
   school=('LOCATION_SETTING_DESCRIPTION',lambda s:(s=='School').sum()),mobile=('LOCATION_TYPE_DESCRIPTION',lambda s:(s=='Mobile Van').sum()),
   hours=('h','sum'))
g=g.join(p.set_index('GRANTNUMBER')[['pat','URBANRURALFLAG']],how='inner')
g['pps']=g.pat/g.sites; g['pph']=g.pat/g.hours.replace(0,np.nan)
g['st_med_pps']=g.groupby('st').pps.transform('median'); g['rel']=g.pps/g.st_med_pps
g['st_med_pph']=g.groupby('st').pph.transform('median'); g['relh']=g.pph/g.st_med_pph
print(len(g),'health centers joined; median sites',g.sites.median(),'median patients/site',round(g.pps.median()),'median patients per weekly hour',round(g.pph.median(),1))
c=['name','st','sites','perm','school','mobile','hours','pat','pps','st_med_pps','rel','pph','relh']
print('--- fewest patients per site vs state, 20+ sites')
print(g[g.sites>=20].sort_values('rel')[c].head(15).round(2).to_string())
print('--- most sites')
print(g.sort_values('sites',ascending=False)[c].head(12).round(2).to_string())
print('--- lowest patients per open hour vs state, 10+ sites')
print(g[g.sites>=10].sort_values('relh')[c].head(12).round(2).to_string())
g.to_pickle('uds_hc.pkl')
