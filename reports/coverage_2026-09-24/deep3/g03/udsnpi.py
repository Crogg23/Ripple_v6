import pandas as pd, re; pd.set_option('display.width',260); pd.set_option('display.max_columns',40)
n=pd.read_csv('S08.csv',dtype=str); u=pd.read_csv('S05.csv',dtype=str)
m=u[u.FQHC_SITE_NPI_NUMBER.notna()].merge(n,left_on='FQHC_SITE_NPI_NUMBER',right_on='NPI',how='left')
stop={'INC','THE','OF','AND','CENTER','CENTERS','HEALTH','COMMUNITY','CLINIC','CLINICS','LLC','CORP','CORPORATION','MEDICAL','CARE','FAMILY','SERVICES','INCORPORATED','CO','COUNTY','HEALTHCARE','A','FOR','ASSOCIATION','D/B/A','DBA'}
def tok(s): return set(w for w in re.findall(r'[A-Z0-9]+',str(s).upper()) if w not in stop and len(w)>2)
m['name_ok']=[bool(tok(a)&(tok(b)|tok(c))) for a,b,c in zip(m.ORG,m.HEALTH_CENTER_NAME,m.SITE_NAME)]
m['st_ok']=m.PST==m.SITE_STATE_ABBREVIATION
m['bad']=m.ENTITY_TYPE_CODE.isna()
dead=m.DEACT.notna()&m.REACT.isna()
print('sites with NPI',len(m),'| invalid or deactivated',int(m.bad.sum()),'| person NPI',int((m.ENTITY_TYPE_CODE=='1').sum()))
ok=m[~m.bad & (m.ENTITY_TYPE_CODE=='2')]
print('org NPIs: name agrees',int(ok.name_ok.sum()),'of',len(ok),'| state agrees',int(ok.st_ok.sum()))
x=ok[~ok.name_ok & ~ok.st_ok]
print('name AND state disagree:',len(x),'sites', x.NPI.nunique(),'NPIs')
print(x[['HEALTH_CENTER_NAME','SITE_NAME','SITE_CITY','SITE_STATE_ABBREVIATION','NPI','ORG','PCITY','PST','TAX1']].head(25).to_string())
print(m[m.ENTITY_TYPE_CODE=='1'][['HEALTH_CENTER_NAME','SITE_NAME','SITE_STATE_ABBREVIATION','NPI','LN','FN','PST']].to_string())
print(m[m.bad][['HEALTH_CENTER_NAME','SITE_NAME','SITE_STATE_ABBREVIATION','NPI','DEACT']].groupby('HEALTH_CENTER_NAME').size().sort_values(ascending=False).head(8))
m.to_pickle('uds_npi.pkl')
