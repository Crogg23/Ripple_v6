import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_rows',100)
a=pd.read_csv('out_S08.csv',keep_default_na=False,na_values=[''])
print('rows',len(a),'years',a.DATA_YEAR.value_counts().to_dict(),'dup keys',(a.KEY_N>1).sum(),'runs',a.RUNS.iloc[0])
print(a.OWNERSHIP.value_counts(dropna=False).to_dict()); print(a.SHORT_FORM.value_counts(dropna=False).to_dict())
print('util 99999', (a.UTILITY_NUMBER==99999).sum(), a[a.UTILITY_NAME.str.contains('Adjust',na=False)][['UTILITY_NUMBER','UTILITY_NAME','STATE','TOTAL_TOTAL_METERS']].head())
f=a.fillna({c:0 for c in ['TOTAL_AMR_METERS','TOTAL_AMI_METERS','TOTAL_NON_AMR_AMI_METERS']})
f['sumparts']=f.TOTAL_AMR_METERS+f.TOTAL_AMI_METERS+f.TOTAL_NON_AMR_AMI_METERS
print('total null',a.TOTAL_TOTAL_METERS.isna().sum(),'total==parts',(f.sumparts==f.TOTAL_TOTAL_METERS).sum(),'total>parts',(f.TOTAL_TOTAL_METERS>f.sumparts).sum(),'total<parts',(f.TOTAL_TOTAL_METERS<f.sumparts).sum())
print('nonamr null',a.TOTAL_NON_AMR_AMI_METERS.isna().sum(), 'ami null',a.TOTAL_AMI_METERS.isna().sum(),'amr null',a.TOTAL_AMR_METERS.isna().sum())
f['gap']=f.TOTAL_TOTAL_METERS-f.sumparts
print(f.sort_values('gap',ascending=False)[['UTILITY_NAME','STATE','TOTAL_AMR_METERS','TOTAL_AMI_METERS','TOTAL_NON_AMR_AMI_METERS','TOTAL_TOTAL_METERS','gap']].head(8).to_string())
print(f.sort_values('gap')[['UTILITY_NAME','STATE','TOTAL_AMR_METERS','TOTAL_AMI_METERS','TOTAL_NON_AMR_AMI_METERS','TOTAL_TOTAL_METERS','gap']].head(8).to_string())
US=f[['TOTAL_AMR_METERS','TOTAL_AMI_METERS','TOTAL_NON_AMR_AMI_METERS','TOTAL_TOTAL_METERS']].sum(); print(US)
f.to_pickle('am.pkl')
