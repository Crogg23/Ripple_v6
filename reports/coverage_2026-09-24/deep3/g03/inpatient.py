import pandas as pd, numpy as np
d=pd.read_csv('S03.csv',dtype=str)
for c in d.columns:
    if c.startswith(('TOT_','BENE_')): d[c]=pd.to_numeric(d[c],errors='coerce')
d['st']=d.RNDRNG_PRVDR_STATE_ABRVTN
d['spb']=d.TOT_DSCHRGS/d.TOT_BENES
d['alos']=d.TOT_DAYS/d.TOT_DSCHRGS
d['pps']=d.TOT_MDCR_PYMT_AMT/d.TOT_DSCHRGS
d['nonmc']=1-d.TOT_MDCR_PYMT_AMT/d.TOT_PYMT_AMT
d['dual']=d.BENE_DUAL_CNT/d.TOT_BENES
d['markup']=d.TOT_SUBMTD_CVRD_CHRG/d.TOT_PYMT_AMT
d['cvrd_gap']=1-d.TOT_CVRD_DAYS/d.TOT_DAYS
print(d[['spb','alos','pps','nonmc','dual','markup','cvrd_gap','BENE_AVG_RISK_SCRE']].describe(percentiles=[.01,.1,.5,.9,.99]).T.round(3))
d.to_pickle('inp.pkl')
