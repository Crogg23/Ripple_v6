import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',50)
d=pd.read_pickle('out_S04.pkl')
d['fd']=pd.to_datetime(d.FILING_DATE,format='%d-%b-%Y'); d['pr']=pd.to_datetime(d.PERIODOFREPORT,format='%d-%b-%Y')
print(sorted(d._SRC_FILE.unique()))
d['lag']=(d.fd-d.pr).dt.days
# filing-window coverage: filings by filing month
fm=d.groupby(d.fd.dt.to_period('Q')).size(); print(fm.to_string())
o=d[d.SUBMISSIONTYPE.isin(['13F-HR','13F-NT'])]
late=o[o.lag>365]
print('original HR/NT filed >365 days after period end:', len(late), 'CIKs', late.CIK.nunique())
# catch-up events: same CIK, same filing date, >=4 late originals
ev=late.groupby(['CIK','fd']).agg(n=('ACCESSION_NUMBER','size'),p0=('pr','min'),p1=('pr','max'),types=('SUBMISSIONTYPE',lambda x:','.join(sorted(set(x))))).reset_index()
big=ev[ev.n>=4].sort_values('n',ascending=False)
print('catch-up events (4+ late originals same day):', len(big), 'CIKs', big.CIK.nunique(), 'filings', big.n.sum())
print(big.head(25).to_string())
print('by filing year', big.groupby(big.fd.dt.year).agg(events=('n','size'),filings=('n','sum')).to_string())
big.to_csv('13f_catchup_events.csv',index=False)
# on-time benchmark: per CIK share of original HR late >47 days, with 20+ HR
hr=d[d.SUBMISSIONTYPE=='13F-HR']
g=hr.groupby('CIK').agg(n=('lag','size'),late47=('lag',lambda x:(x>47).sum()),late365=('lag',lambda x:(x>365).sum()))
g['r']=g.late47/g.n; peer=g[g.n>=20]
print('HR filers 20+', len(peer), 'median late47 share', peer.r.median(), 'p90', peer.r.quantile(.9), 'pooled', peer.late47.sum()/peer.n.sum())
print('HR late47 overall', (hr.lag>47).mean(), 'late47 excl >365', ((hr.lag>47)&(hr.lag<=365)).mean())
