import pandas as pd, numpy as np
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 100)
d = pd.read_pickle('out_S02.pkl')
print(d.dtypes)
print('accession distinct', d.ACCESSION_NUMBER.nunique(), 'rows', len(d))
print(d.DOCUMENT_TYPE.value_counts(dropna=False))
d['POR'] = pd.to_datetime(d.PERIOD_OF_REPORT, format='%d-%b-%Y', errors='coerce')
d['FD'] = pd.to_datetime(d.FILING_DATE)
print('POR unparsed', d.POR.isna().sum(), d.loc[d.POR.isna(), 'PERIOD_OF_REPORT'].value_counts().head())
print('POR range', d.POR.min(), d.POR.max())
print(pd.crosstab(d.POR.dt.to_period('M').astype(str), d.DOCUMENT_TYPE).tail(20))
for c in ['NO_SECURITIES_OWNED','NOT_SUBJECT_SEC16','FORM3_HOLDINGS_REPORTED','FORM4_TRANS_REPORTED','AFF10B5ONE']:
    print(c, pd.crosstab(d[c].fillna('<null>').replace('', '<blank>'), d.DOCUMENT_TYPE).to_string())
m18 = d[d.POR == '2026-03-18']
print('POR 18-Mar-2026:', len(m18), m18.DOCUMENT_TYPE.value_counts().to_dict(), 'issuers', m18.CIK.nunique())
print(m18.ISSUERNAME.value_counts().head(25))
print('filing date of POR=18Mar docs:', m18.FD.value_counts().sort_index().to_string())
print('daily filings by filing date, doc 3:'); print(d[d.DOCUMENT_TYPE.astype(str).str.strip()=='3'].FD.value_counts().sort_index().tail(20).to_string())
