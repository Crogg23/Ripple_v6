import pandas as pd, numpy as np, re
pd.set_option('display.width',260); pd.set_option('display.max_colwidth',110); pd.set_option('display.max_rows',300); pd.set_option('display.max_columns',20)
u=pd.read_csv('out_S10.csv',parse_dates=['ACTION_DATE'])
u=u[u.TAG=='IVANTI'].copy()
u['fy']=(u.ACTION_DATE.dt.year+(u.ACTION_DATE.dt.month>=10).astype(int)).astype(int)
P=[('Connect Secure','CONNECT SECURE|PULSE|POLICY SECURE|\bICS\b|\bZTA\b|VPN'),('EPMM/MobileIron','MOBILEIRON|EPMM|MOBILE ?IRON|ENDPOINT MANAGER MOBILE|\bMDM\b'),('Neurons','NEURON'),('EPM/LANDesk','LANDESK|ENDPOINT MANAGER|\bEPM\b'),('ITSM/HEAT/Cherwell','ITSM|\bHEAT\b|CHERWELL|SERVICE MANAGER|\bISM\b'),('Patch/Shavlik','PATCH|SHAVLIK|SECURITY CONTROLS'),('Device/App control','DEVICE CONTROL|APPLICATION CONTROL|LUMENSION'),('UEM/AppSense','APPSENSE|USER WORKSPACE|\bUEM\b|ENVIRONMENT MANAGER')]
def prod(s):
  s=str(s).upper()
  for k,p in P:
    if re.search(p,s): return k
  return 'generic'
u['prod']=u.DESCR.map(prod)
print(u.pivot_table(index='prod',columns='fy',values='FEDERAL_ACTION_OBLIGATION',aggfunc='sum').div(1e3).round(0).to_string())
print(u.pivot_table(index='prod',columns='fy',values='CONTRACT_AWARD_UNIQUE_KEY',aggfunc='nunique').to_string())
x=u[(u.prod=='generic')&u.fy.isin([2024,2025])].sort_values('FEDERAL_ACTION_OBLIGATION',ascending=False)
print(x[['ACTION_DATE','FEDERAL_ACTION_OBLIGATION','AWARDING_SUB_AGENCY_NAME','RECIPIENT_NAME','DESCR']].head(20).to_string())
x=u[(u.prod=='EPMM/MobileIron')&u.fy.isin([2024,2025])].sort_values('FEDERAL_ACTION_OBLIGATION',ascending=False)
print(x[['ACTION_DATE','FEDERAL_ACTION_OBLIGATION','AWARDING_SUB_AGENCY_NAME','RECIPIENT_NAME','DESCR','CONTRACT_AWARD_UNIQUE_KEY']].head(12).to_string())
u.to_pickle('ivanti.pkl')
