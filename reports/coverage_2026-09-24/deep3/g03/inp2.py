import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',30)
d=pd.read_pickle('inp.pkl')
h=pd.read_csv('S04.csv',dtype=str)
d=d.merge(h,left_on='RNDRNG_PRVDR_CCN',right_on='CCN',how='left')
print('land in hospital general:', d.CCN.notna().sum(), 'of', len(d))
print(d.HOSPITAL_TYPE.value_counts(dropna=False))
big=d[(d.TOT_BENES>=500)].copy()
big['dual']=big.dual.fillna(big.dual.median())
# national OLS: spb ~ risk + dual + alos
X=np.column_stack([np.ones(len(big)),big.BENE_AVG_RISK_SCRE,big.dual])
b,*_=np.linalg.lstsq(X,big.spb,rcond=None)
big['pred']=X@b; big['resid']=big.spb-big.pred
print('coef',b.round(3),'R2',1-((big.resid**2).sum()/((big.spb-big.spb.mean())**2).sum()))
big['st_med_spb']=big.groupby('st').spb.transform('median')
big['st_med_res']=big.groupby('st').resid.transform('median')
big['rel']=big.spb/big.st_med_spb
big['res_rel']=big.resid-big.st_med_res
big['extra_stays']=(big.spb-big.pred-big.st_med_res)*big.TOT_BENES
c=['RNDRNG_PRVDR_CCN','RNDRNG_PRVDR_ORG_NAME','st','HOSPITAL_OWNERSHIP','TOT_BENES','TOT_DSCHRGS','spb','st_med_spb','rel','pred','res_rel','extra_stays','dual','BENE_AVG_RISK_SCRE','COUNT_OF_READM_MEASURES_WORSE','COUNT_OF_FACILITY_READM_MEASURES']
print(len(big),'hospitals >=500 benes; median spb',big.spb.median().round(3))
print(big.sort_values('res_rel',ascending=False)[c].head(25).round(3).to_string())
big.to_pickle('inp_big.pkl')
# readmission worse measures vs residual decile
big['rw']=pd.to_numeric(big.COUNT_OF_READM_MEASURES_WORSE,errors='coerce')
big['dec']=pd.qcut(big.res_rel,10,labels=False)
print(big.groupby('dec').agg(n=('rw','size'),rw_mean=('rw','mean'),any_worse=('rw',lambda s:(s>0).mean()),spb=('spb','median')).round(3))
