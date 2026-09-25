import pandas as pd, numpy as np
f=pd.read_csv('out_S15.csv', dtype={'FACILITY_UIN':str,'FRS_ID':str})
print(f.shape, 'echo land', f.FRS_ID.notna().mean().round(3))
f['landed']=f.FRS_ID.notna()
print(f.groupby(pd.cut(f.CASES,[0,1,2,4,9,10000])).agg(n=('FACILITY_UIN','size'),land=('landed','mean')).round(3))
e=f[f.landed].copy()
e['nc12']=e.QUARTERS_WITH_NONCOMPLIANCE>=12
e['grp']=pd.cut(e.CASES,[0,1,2,4,10000],labels=['1','2','3-4','5+'])
print(e.groupby(['IS_MAJOR_FACILITY','grp'],observed=True).agg(n=('FACILITY_UIN','size'),nc_any=('QUARTERS_WITH_NONCOMPLIANCE',lambda s:(s>0).mean()),nc12=('nc12','mean'),med_q=('QUARTERS_WITH_NONCOMPLIANCE','median'),act=('IS_ACTIVE','mean')).round(3).to_string())
# repeat facilities with a case in last 5 yrs and full-12-quarter noncompliance
r=e[(e.CASES>=5)&(e.LAST_CASE_YR>=2021)&(e.QUARTERS_WITH_NONCOMPLIANCE>=12)].sort_values('CASES',ascending=False)
print(len(r)); print(r[['FACILITY_UIN','NAME','E_CITY','ST','CASES','FIRST_CASE_YR','LAST_CASE_YR','QUARTERS_WITH_NONCOMPLIANCE','FORMAL_ACTION_COUNT','TOTAL_PENALTIES','IS_MAJOR_FACILITY','COMPLIANCE_STATUS','PCT_MINORITY']].head(40).to_string())
w=f[f.FACILITY_UIN=='110009327022']; print(w.T)
