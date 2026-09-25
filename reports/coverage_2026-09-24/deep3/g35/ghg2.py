import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',45)
m=pd.read_pickle('m.pkl')
rep=m[m.st=='REPORTED']; stp=m[m.st!='REPORTED']
g=rep.sort_values('YR').groupby('FACILITY_ID')
fac=pd.DataFrame({'first_rep':g.YR.min(),'last_rep':g.YR.max(),'n_rep':g.YR.size(),
  'name':g.FACILITY_NAME.last(),'parent':g.PARENT_COMPANY.last(),'city':g.CITY.last(),'state':g.STATE.last(),
  'frs':g.FRS.last(),'naics':g.NAICS_CODE.last(),'types':g.FACILITY_TYPES.last(),'subparts':g.REPORTED_SUBPARTS.last()})
last=rep.sort_values('YR').groupby('FACILITY_ID').tail(1).set_index('FACILITY_ID')
fac['last_direct']=last.DIRECT_T
# last 3 and 5 reported years max
def lastk(k):
    return rep.sort_values('YR').groupby('FACILITY_ID').apply(lambda d: d.DIRECT_T.tail(k).max())
fac['max_last3']=lastk(3); fac['max_last5']=lastk(5); fac['peak']=g.DIRECT_T.max()
sg=stp.sort_values('YR').groupby('FACILITY_ID')
s=pd.DataFrame({'first_stop':sg.YR.min(),'latest_stop_yr':sg.YR.max(),'latest_status':sg.st.last(),'ever_unknown':sg.st.apply(lambda x:(x=='STOPPED_REPORTING_UNKNOWN_REASON').any())})
fac=fac.join(s,how='outer')
print('facilities', len(fac), 'with stop rows', fac.first_stop.notna().sum(), 'stop rows w/o any reported year', fac.last_rep.isna().sum())
fac['resumed']=fac.last_rep>fac.first_stop
print('resumed after a stop row:', fac.resumed.sum())
print(fac[fac.first_stop.notna()].groupby(['latest_status','ever_unknown']).size())
# gap between last report and first stop year
fac['gap']=fac.first_stop-fac.last_rep
print(fac.gap.value_counts().sort_index().head(10))
fac.to_pickle('fac.pkl')
