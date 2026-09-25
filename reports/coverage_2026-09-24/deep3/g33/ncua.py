import pandas as pd, numpy as np
fs=pd.read_pickle('01_fs220_all.pkl'); cl=pd.read_pickle('03_culist_all.pkl'); fo=pd.read_pickle('02_foicu_all.pkl')
num=lambda s: pd.to_numeric(s,errors='coerce')
d=pd.DataFrame({'cu':fs.CU_NUMBER,'assets':num(fs.ACCT_010),'loans':num(fs.ACCT_025B),'del60':num(fs.ACCT_041B),
  'co':num(fs.ACCT_550),'rec':num(fs.ACCT_551),'members':num(fs.ACCT_083),'b020':num(fs.ACCT_020B)})
d=d.merge(fo[['CU_NUMBER','CU_NAME','CITY','STATE','PEER_GROUP','CU_TYPE','LIMITED_INC','ISMDI','YEAR_OPENED']],left_on='cu',right_on='CU_NUMBER',how='left')
c=cl[['CHARTER_NUMBER','NET_WORTH_RATIO_EXCLUDES_CECL_TRANSITION_PROVISION','RETURN_ON_AVERAGE_ASSETS','LOAN_TO_SHARE_RATIO','TOTAL_LOANS_4_QUARTER_GROWTH','MEMBERS_4_QUARTER_GROWTH','NET_WORTH_4_QUARTER_GROWTH_EXCLUDES_CECL_TRANSITION_PROVISION','LOW_INCOME_DESIGNATION','CREDIT_UNION_TYPE']].copy()
c.columns=['cu','nwr','roa','lts','loan_g','mem_g','nw_g','lowinc','type']
for k in ['nwr','roa','lts','loan_g','mem_g','nw_g']: c[k]=num(c[k])
d=d.merge(c,on='cu',how='left')
d['dq']=d.del60/d.loans
d['nco']=(d.co-d.rec)*4/d.loans
d.to_pickle('ncua_frame.pkl')
