import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',38); pd.set_option('display.max_rows',200)
x=pd.read_pickle('x.pkl')
x['kind']=np.where(x.types.fillna('').str.contains('Onshore Oil|Gathering|Transmission|LDC'),'oil&gas W',
          np.where(x.subparts.fillna('').str.contains(r'\bHH\b'),'landfill HH',
          np.where(x.subparts.fillna('').str.contains(r'\bD\b'),'power D','other industrial')))
print(pd.crosstab(x.kind,x.status2023,margins=True))
print(x.groupby(['status2023','kind']).agg(n=('big','size'),big=('big','sum'),last_mt=('last_direct',lambda s:round(s.sum()/1e6,2)),med=('last_direct','median')).round(0))
u=x[x.status2023=='STOPPED_REPORTING_UNKNOWN_REASON'].sort_values('last_direct',ascending=False)
print(u.exit_yr.value_counts().sort_index().to_dict())
v=x[x.status2023=='STOPPED_REPORTING_VALID_REASON']
print('valid exit yr', v.exit_yr.value_counts().sort_index().to_dict())
cols=['name','parent','city','state','kind','first_rep','last_rep','last_direct','max_last3','frs','still_other','after_TRIS','after_CAMDBS','after_EIS','same_frs_other_ghg_id','echo_IS_ACTIVE','echo_LAST_INSP','echo_FORMAL']
print(u[cols].head(60).to_string())
u[cols+['subparts','naics']].to_csv('unknown_reason_148.csv')
