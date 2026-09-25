import pandas as pd, numpy as np, re
pd.set_option('display.width',260); pd.set_option('display.max_colwidth',90); pd.set_option('display.max_rows',300); pd.set_option('display.max_columns',20)
u=pd.read_pickle('ivanti.pkl')
u=u[~u.RECIPIENT_NAME.fillna('').str.upper().str.contains('IVANTIS')].copy()
D=u.DESCR.fillna('').str.upper()
u.loc[D.str.contains('KITEWORKS|CONNECT SECURELY'),'prod']='not Ivanti VPN (Kiteworks / connect securely)'
u.loc[(u['prod']=='generic')&D.str.contains('ACCESS APPLICATIONS AND BUSINESS RESOURCES'),'prod']='EPMM/MobileIron'
u['fy']=u.fy.astype(int)
t=u.pivot_table(index='prod',columns='fy',values='FEDERAL_ACTION_OBLIGATION',aggfunc='sum').div(1e3).round(0)
print(t.to_string())
e=u[u['prod']=='EPMM/MobileIron']
print(e.groupby(['AWARDING_SUB_AGENCY_NAME']).agg(usd=('FEDERAL_ACTION_OBLIGATION','sum'),awards=('CONTRACT_AWARD_UNIQUE_KEY','nunique'),d0=('ACTION_DATE','min'),d1=('ACTION_DATE','max')))
cs=u[u['prod']=='Connect Secure']
keys=sorted(set(e.CONTRACT_AWARD_UNIQUE_KEY)|set(cs[cs.ACTION_DATE>='2023-01-19'].CONTRACT_AWARD_UNIQUE_KEY))
print(len(keys)); open('keys.txt','w').write(','.join(chr(39)+x+chr(39) for x in keys))
u.to_pickle('ivanti2.pkl')
k=pd.read_csv('out_S08.csv')
mdm=k[k.PRODUCT.str.contains('EPMM|MobileIron|Workspace ONE|AirWatch|Intune|MaaS360|BlackBerry|Jamf|SOTI|Endpoint Manager|Mobile Device|MDM|UEM|XenMobile|Citrix Endpoint',case=False,na=False)|k.VULNERABILITY_NAME.str.contains('MobileIron|Workspace ONE|AirWatch|MDM|Mobile Device Manag',case=False,na=False)]
print(mdm[['CVE_ID','VENDOR_PROJECT','PRODUCT','DATE_ADDED','KNOWN_RANSOMWARE_CAMPAIGN_USE']].sort_values('DATE_ADDED').to_string())
k['DATE_ADDED']=pd.to_datetime(k.DATE_ADDED)
r=k[k.DATE_ADDED>='2023-01-01'].groupby(['VENDOR_PROJECT','PRODUCT']).size().sort_values(ascending=False)
print(r.head(15).to_string()); print('products with >=1 since 2023', len(r), 'median', r.median(), 'products with >=8:', (r>=8).sum())
