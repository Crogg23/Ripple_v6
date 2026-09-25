import pandas as pd, numpy as np, warnings
warnings.filterwarnings('ignore')
pd.set_option('display.width',280); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',45)
sp=pd.read_pickle('sp_verified.pkl'); d=pd.read_pickle('out_S04.pkl')
dn=pd.read_pickle('out_S16.pkl'); dn['cycle']=pd.to_numeric(dn.CYCLE_FILE,errors='coerce')
for c in ['DONORS','RETIRED_DONORS','AMT']: dn[c]=pd.to_numeric(dn[c],errors='coerce')
s=sp[sp.sym]
ids=set(s.CMTE_ID)
d26=dn[(dn.cycle==2026)&dn.CMTE_ID.isin(ids)]
print('sym PACs with itemized 2025-26 gifts', d26.CMTE_ID.nunique(), 'donors', d26.DONORS.sum(), 'amt', d26.AMT.sum())
print(d26.merge(s[['CMTE_ID','CMTE_NM']].drop_duplicates(),on='CMTE_ID')[['CMTE_ID','CMTE_NM','DONORS','RETIRED_DONORS','AMT']].to_string(index=False))
cl=s.groupby('CMTE_ID').agg(name=('CMTE_NM','first'),type=('COMMITTEE_TYPE','first'),treasurer=('tres','first'),city=('CMTE_CITY','first'),st=('CMTE_ST','first'),
   cycles=('cycle',lambda x:','.join(str(int(v)) for v in sorted(x))),raised=('TOTAL_RECEIPTS','sum'),indiv=('INDIVIDUAL_CONTRIBUTIONS','sum'),spent=('TOTAL_DISBURSEMENTS','sum'),
   ie_webk=('INDEPENDENT_EXPENDITURES','sum'),ie_schedE=('schedE','sum'),contrib=('CONTRIBUTIONS_TO_OTHER_COMMITTEES','sum'),to_politics_max=('alt_pol','sum'))
cl['share_max']=cl.to_politics_max/cl.spent
cl['in_2026_file']=cl.index.isin(set(d[d.SRC=='bulk_cm26'].CMTE_ID))
cl['is_ambiguous']=cl.index.map(d.set_index('CMTE_ID').IS_AMBIGUOUS)
cl=cl.sort_values('raised',ascending=False)
cl.to_csv('sympathy_superpacs_41.csv')
print(cl[['name','treasurer','st','cycles','raised','to_politics_max','share_max','in_2026_file']].round(3).to_string())
print('ambiguous', cl.is_ambiguous.sum(), 'overall dim rate', d.IS_AMBIGUOUS.mean())
print('raised', cl.raised.sum(), 'indiv', cl.indiv.sum(), 'spent', cl.spent.sum(), 'max to politics', cl.to_politics_max.sum())
print('cycles', s.cycle.min(), s.cycle.max(), 'coverage end', s.COVERAGE_END_DATE.min(), s.COVERAGE_END_DATE.max())
