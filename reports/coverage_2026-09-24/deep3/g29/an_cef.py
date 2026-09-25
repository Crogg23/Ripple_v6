import pandas as pd, numpy as np, warnings, re
warnings.filterwarnings('ignore')
pd.set_option('display.width',250); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',60)
c=pd.read_pickle('out_S09.pkl')
c['yy']=c.FILING_YR.astype(int); c['year']=np.where(c.yy<=30,2000+c.yy,1900+c.yy)
c['cik']=c.CIK.astype(int)
stale=c[c.year<=2023]
print('stale last-filing types', stale.FILING_TYPE.value_counts().head(12).to_dict())
print('stale with N-8F/RW/N-8F NTC', stale.FILING_TYPE.str.contains(r'N-8F|^RW',regex=True).sum())
# calibration: CIK vs year for funds whose last filing is a first-type filing (N-8A, N-2, N-2/A) filed 2019+
cal=c[c.FILING_TYPE.isin(['N-8A','N-2','N-2/A'])&(c.year>=2014)]
print(cal.groupby('year').cik.agg(['count','min','median','max']).to_string())
# vintage of active registrants (filed 2025-2026)
act=c[c.year>=2025].copy()
bins=[0,1500000,1800000,1900000,1950000,2000000,2050000,2100000,3000000]
act['vint']=pd.cut(act.cik,bins)
act['priv']=act.REGISTRANT_NAME.str.upper().str.contains(r'PRIVATE|CREDIT|INTERVAL|INFRASTRUCTURE|SECONDAR|LENDING|ALTERNATIVE|REAL ASSET|VENTURE|GP STAKES|INCOME FUND',regex=True)
print(act.groupby('vint',observed=True).agg(funds=('cik','size'),private_credit_alt_name=('priv','mean')).round(3).to_string())
print('active', len(act), 'cik>=1.9M', (act.cik>=1900000).sum(), 'cik>=2.0M', (act.cik>=2000000).sum())
print('state top active', act.STATE.value_counts().head(6).to_dict())
new=act[act.cik>=2050000]
print(new.sort_values('cik')[['CIK','REGISTRANT_NAME','CITY','STATE','FILING_TYPE']].to_string(index=False))
