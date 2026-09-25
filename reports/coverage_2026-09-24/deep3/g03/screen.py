import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',30)
b=pd.read_pickle('inp_big.pkl')
s=pd.read_csv('S23.csv',dtype={'CCN':str})
b=b.merge(s,left_on='RNDRNG_PRVDR_CCN',right_on='CCN',how='left')
b['sep']=b.SEPSIS/b.DIS_LISTED
b['sep_st']=b.sep/b.groupby('st').sep.transform('median')
b['spb_pct']=b.res_rel.rank(pct=True); b['sep_pct']=b.sep_st.rank(pct=True)
print('corr sepsis share vs stays/patient residual, national', round(b.sep.corr(b.res_rel),3), 'n', b.sep.notna().sum())
both=b[(b.spb_pct>=0.9)&(b.sep_pct>=0.9)]
print('top decile on both:', len(both), 'expected by chance about', round(len(b)*0.01))
c=['RNDRNG_PRVDR_CCN','RNDRNG_PRVDR_ORG_NAME','st','HOSPITAL_OWNERSHIP','TOT_BENES','spb','st_med_spb','sep','sep_st','BENE_AVG_RISK_SCRE','COUNT_OF_READM_MEASURES_WORSE']
print(both.sort_values('res_rel',ascending=False)[c].round(3).to_string())
o=b[b.RNDRNG_PRVDR_CCN=='050030'].iloc[0]
print('Oroville pct: spb',round(o.spb_pct,4),'sepsis vs state',round(o.sep_pct,4))
b.to_pickle('inp_screen.pkl')
