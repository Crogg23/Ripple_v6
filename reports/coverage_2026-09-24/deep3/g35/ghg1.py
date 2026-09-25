import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',40)
f=pd.read_csv('out_S11.csv',dtype={'FRS':str,'ZIP':str,'COUNTY_FIPS':str,'NAICS_CODE':str})
e=pd.read_csv('out_S12.csv')
print(f.shape, e.shape)
# emission years vs facility rows
em_keys=set(zip(e.FACILITY_ID,e.YR))
f['has_em']=[(a,b) in em_keys for a,b in zip(f.FACILITY_ID,f.YR)]
print(pd.crosstab(f.STATUS.fillna('REPORTED'),f.has_em))
# emission rows with no facility row
fk=set(zip(f.FACILITY_ID,f.YR))
e['has_fac']=[(a,b) in fk for a,b in zip(e.FACILITY_ID,e.YR)]
print('emission facility-years with no facility row:', (~e.has_fac).sum())
print(e[~e.has_fac].YR.value_counts().sort_index().to_dict())
# per year direct totals
print(e.groupby('YR')[['DIRECT_T','SUPPLIER_T','BIOGENIC_T']].sum().div(1e6).round(1))
m=f.merge(e,on=['FACILITY_ID','YR'],how='left')
m['st']=m.STATUS.fillna('REPORTED')
print(m.groupby('st').agg(rows=('YR','size'),direct_pos=('DIRECT_T',lambda s:(s>0).sum()),direct_sum=('DIRECT_T','sum'),sup_pos=('SUPPLIER_T',lambda s:(s>0).sum())))
m.to_pickle('m.pkl')
