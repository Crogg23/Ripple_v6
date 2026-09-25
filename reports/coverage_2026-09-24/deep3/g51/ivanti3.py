import pandas as pd
pd.set_option('display.width',260); pd.set_option('display.max_rows',300)
a=pd.read_csv('out_S11.csv',parse_dates=['ACTION_DATE'])
u=pd.read_pickle('ivanti2.pkl')
tag=u.groupby('CONTRACT_AWARD_UNIQUE_KEY')['prod'].agg(lambda s: s.value_counts().index[0])
a['prod']=a.CONTRACT_AWARD_UNIQUE_KEY.map(tag)
e=a[a['prod']=='EPMM/MobileIron']
print('EPMM named: awards',e.CONTRACT_AWARD_UNIQUE_KEY.nunique(),'usd',round(e.FEDERAL_ACTION_OBLIGATION.sum()))
print(e.groupby('AWARDING_SUB_AGENCY_NAME').agg(usd=('FEDERAL_ACTION_OBLIGATION','sum'),awards=('CONTRACT_AWARD_UNIQUE_KEY','nunique')).round(0))
print(e[e.FEDERAL_ACTION_OBLIGATION.abs()>100000][['AWARD_ID_PIID','ACTION_DATE','FEDERAL_ACTION_OBLIGATION','RECIPIENT_NAME']].sort_values('ACTION_DATE').to_string())
# Connect Secure: award-level, first action = award start
cs=u[u['prod']=='Connect Secure']
first=cs.groupby('CONTRACT_AWARD_UNIQUE_KEY').ACTION_DATE.min()
cuts=pd.to_datetime(['2022-01-19','2023-01-19','2024-01-19','2025-01-19','2026-01-19','2026-09-01'])
lab=['Jan22-Jan23','Jan23-Jan24','Jan24-Jan25 (after ED 24-01)','Jan25-Jan26','Jan26-Aug26']
aw=cs.groupby('CONTRACT_AWARD_UNIQUE_KEY').agg(first=('ACTION_DATE','min'),usd=('FEDERAL_ACTION_OBLIGATION','sum'),agency=('AWARDING_SUB_AGENCY_NAME','first'))
aw['win']=pd.cut(aw['first'],cuts,right=False,labels=lab)
print(aw.groupby('win',observed=False).agg(new_awards=('usd','size'),usd=('usd','sum'),agencies=('agency','nunique')).round(0))
# peers: new awards per window by vendor tag (award first action in window)
s=pd.read_csv('out_S10.csv',parse_dates=['ACTION_DATE'])
d=(s.DESCR.fillna('')+' | '+s.RECIPIENT_NAME.fillna('')+' | '+s.RECIPIENT_PARENT_NAME.fillna('')).str.upper()
s=s[~((s.TAG=='PALOALTO')&~d.str.contains('PALO ?ALTO NETWORKS|GLOBALPROTECT|PAN-OS|PRISMA ACCESS|CORTEX XDR',regex=True))]
s=s[s.TAG!='IVANTI']
f=s.groupby(['TAG','CONTRACT_AWARD_UNIQUE_KEY']).ACTION_DATE.min().reset_index()
f['win']=pd.cut(f.ACTION_DATE,cuts,right=False,labels=lab)
print(pd.crosstab(f.TAG,f.win))
