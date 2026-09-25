import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',50)
d=pd.read_pickle('out_S04.pkl')
print(d.shape, d.ACCESSION_NUMBER.nunique(), d.CIK.nunique())
d['fd']=pd.to_datetime(d.FILING_DATE,format='%d-%b-%Y',errors='coerce'); d['pr']=pd.to_datetime(d.PERIODOFREPORT,format='%d-%b-%Y',errors='coerce')
print('unparsed fd', d.fd.isna().sum(), 'pr', d.pr.isna().sum(), 'fd range', d.fd.min(), d.fd.max(), 'pr range', d.pr.min(), d.pr.max())
print(d.SUBMISSIONTYPE.value_counts().to_dict())
print('src files', d._SRC_FILE.nunique(), d._SRC_FILE.value_counts().sort_index().head(3).to_dict(), '...', d._SRC_FILE.value_counts().sort_index().tail(3).to_dict())
print('dup accession rows', d.duplicated('ACCESSION_NUMBER').sum(), 'dup full rows', d.duplicated(['ACCESSION_NUMBER','FILING_DATE','SUBMISSIONTYPE','CIK','PERIODOFREPORT']).sum())
dd=d[d.duplicated('ACCESSION_NUMBER',keep=False)].sort_values('ACCESSION_NUMBER'); print(dd.head(6).to_string())
d['q']=d.pr.dt.to_period('Q')
q=d.groupby(['q','SUBMISSIONTYPE']).size().unstack(fill_value=0); print(q.to_string())
d['lag']=(d.fd-d.pr).dt.days
hr=d[d.SUBMISSIONTYPE=='13F-HR']
print('13F-HR lag quantiles', hr.lag.quantile([.01,.5,.9,.95,.99]).to_dict(), 'late >45', (hr.lag>45).mean(), 'neg', (hr.lag<0).sum())
top=d.CIK.value_counts().head(10); print(top.to_string())
for c in top.index[:3]:
    x=d[d.CIK==c]; print(c, x.SUBMISSIONTYPE.value_counts().to_dict(), 'periods', x.pr.nunique(), x.pr.min(), x.pr.max())
    print(x.groupby('pr').size().sort_values(ascending=False).head(5).to_dict())
