import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',44)
m=pd.read_pickle('catchup_accessions.pkl')
names=pd.read_pickle('out_S16.pkl'); hv=pd.read_pickle('out_S17.pkl')
hv['VALUE_USD']=hv.VALUE_USD.astype(float); hv['LINES']=hv.LINES.astype(int)
acc2cik=m.set_index('ACCESSION_NUMBER')[['CIK','fd']]
names=names.join(acc2cik,on='ACCESSION_NUMBER')
nm=names.groupby('CIK').agg(name=('FILINGMANAGER_NAME','last'),city=('FILINGMANAGER_CITY','last'),st=('FILINGMANAGER_STATEORCOUNTRY','last'),crd=('CRDNUMBER','last'))
m=m.merge(hv[['ACCESSION_NUMBER','LINES','VALUE_USD']],on='ACCESSION_NUMBER',how='left')
ev=m.groupby(['CIK','fd']).agg(n=('ACCESSION_NUMBER','size'),hr=('SUBMISSIONTYPE',lambda x:(x=='13F-HR').sum()),p0=('pr','min'),p1=('pr','max'),
    val_latest=('VALUE_USD',lambda x: np.nan),).reset_index()
# value of the most recent quarter in each event (a stock measure, not summed across quarters)
last=m.sort_values('pr').groupby(['CIK','fd']).tail(1)[['CIK','fd','VALUE_USD','LINES','pr']]
ev=ev.drop(columns='val_latest').merge(last,on=['CIK','fd'],how='left').join(nm,on='CIK')
ev['years_back']=((ev.fd-ev.p0).dt.days/365.25).round(1)
e24=ev[ev.fd>='2024-01-01']
print('2024+ events', len(e24), 'managers', e24.CIK.nunique(), 'filings', e24.n.sum(), 'HR', e24.hr.sum())
print('latest-quarter value reported (HR events w/ value):', e24.VALUE_USD.notna().sum(), 'sum $', e24.VALUE_USD.sum(), 'median $', e24.VALUE_USD.median())
print('events reaching back 10+ years:', (e24.years_back>=10).sum())
print(e24.sort_values('n',ascending=False).head(25)[['name','city','st','crd','fd','n','hr','p0','p1','years_back','pr','VALUE_USD','LINES']].to_string())
print('\nbiggest by value:'); print(e24.sort_values('VALUE_USD',ascending=False).head(12)[['name','city','st','fd','n','p0','p1','VALUE_USD']].to_string())
# country mix
print('state/country top', e24.st.value_counts().head(12).to_dict())
# by filing month 2024-2026
print(e24.groupby(e24.fd.dt.to_period('Q')).agg(events=('n','size'),filings=('n','sum')).to_string())
old=ev[ev.fd<'2024-01-01']; print('pre-2024 events', len(old), 'median n', old.n.median(), '2024+ median n', e24.n.median())
ev.to_csv('13f_catchup_events_named.csv',index=False)
