import pandas as pd, numpy as np
z=pd.read_csv('out_S09.csv', dtype={'ZIP5':str})
print(z.shape, z.RET_ALL.sum(), 'dup zip5', z.ZIP5.duplicated().sum())
print(z[z.ZIP5.duplicated(keep=False)].sort_values('ZIP5').head(10).to_string())
z=z[z.RET_LOW>=1000].copy()
z['rac_sh']=z.RAC_LOW/z.RET_LOW; z['prep_sh']=z.PREP_LOW/z.RET_LOW; z['vita_sh']=z.VITA_LOW/z.RET_LOW; z['eitc_sh']=z.N_EITC/z.RET_ALL
z['agi_per']=z.AGI_K*1000/z.RET_ALL
print('national rac share low', round(z.RAC_LOW.sum()/z.RET_LOW.sum(),3), 'median zip', round(z.rac_sh.median(),3))
st=z.groupby('STATE').apply(lambda g: pd.Series({'zips':len(g),'rac':g.RAC_LOW.sum()/g.RET_LOW.sum(),'med':g.rac_sh.median(),'p90':g.rac_sh.quantile(.9),'max':g.rac_sh.max()})).sort_values('rac',ascending=False)
print(st.round(3).head(12).to_string()); print(st.round(3).tail(5).to_string())
z['st_med']=z.groupby('STATE').rac_sh.transform('median')
z['x_state']=z.rac_sh/z.st_med
print(z.sort_values('rac_sh',ascending=False)[['STATE','ZIP5','RET_LOW','rac_sh','st_med','prep_sh','vita_sh','eitc_sh','agi_per']].head(20).round(3).to_string())
print('corr rac_sh vs eitc_sh', round(z[['rac_sh','eitc_sh']].corr().iloc[0,1],3), 'vs agi', round(np.corrcoef(z.rac_sh, np.log(z.agi_per))[0,1],3))
print('RAL all national:', z.RAL_ALL.sum())
