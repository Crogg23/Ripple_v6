import sys; sys.path.insert(0,'.')
from load import df
import pandas as pd
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',55)
e=df(2)
e['who']=(e.RECIPIENTNAMEFIRST.fillna('').str.upper().str.strip()+' '+e.RECIPIENTNAMELAST.fillna('').str.upper().str.strip()).str.strip()
e['ben']=(e.BENEFICIARYNAMEFIRST.fillna('').str.upper().str.strip()+' '+e.BENEFICIARYNAMELAST.fillna('').str.upper().str.strip()).str.strip()
e['d']=pd.to_datetime(e.ACTIVITYDATE)
# regular sessions (convene, sine die) -- general knowledge, not from the warehouse
S={2005:('2005-01-11','2005-05-30'),2007:('2007-01-09','2007-05-28'),2009:('2009-01-13','2009-06-01'),2011:('2011-01-11','2011-05-30'),
   2013:('2013-01-08','2013-05-27'),2015:('2015-01-13','2015-06-01'),2017:('2017-01-10','2017-05-29'),2019:('2019-01-08','2019-05-27'),
   2021:('2021-01-12','2021-05-31'),2023:('2023-01-10','2023-05-29'),2025:('2025-01-14','2025-06-02')}
W=[(pd.Timestamp(a)-pd.Timedelta(days=30),pd.Timestamp(b)+pd.Timedelta(days=20),y) for y,(a,b) in S.items()]
def inwin(d):
    if pd.isna(d): return None
    for a,b,y in W:
        if a<=d<=b: return y
    return 0
e['blackout']=e.d.map(inwin)
f=e[e.LOBBYEVENTKINDCD=='FUNDRAISER']
print('fundraiser rows',len(f),'dated',f.d.notna().sum(),'in blackout',(f.blackout>0).sum())
# share of calendar days in blackout windows between 2005-01 and 2026-06
days=pd.date_range('2005-01-01','2026-06-30')
bl=sum(((days>=a)&(days<=b)).sum() for a,b,y in W)
print('share of days in blackout', round(bl/len(days),3))
fd=f[f.d.notna()]
print('share of dated fundraiser rows in blackout', round((fd.blackout>0).mean(),3))
ch=e[(e.LOBBYEVENTKINDCD=='CHARITY')&e.d.notna()]
print('share of dated charity rows in blackout (control)', round((ch.blackout>0).mean(),3), len(ch))
b=fd[fd.blackout>0]
print(b[['APPLICABLEYEAR','REPORT_ID','FILERNAME','ACTIVITYDATE','ACTIVITYDESCRIPTION','RECIPIENTNAMEPREFIXCD','who','ben']].sort_values('ACTIVITYDATE').to_string())
