import pandas as pd, numpy as np, re, warnings
warnings.filterwarnings('ignore')
pd.set_option('display.width',280); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',42)
e=pd.read_pickle('out_S03.pkl')
e['filed']=pd.to_datetime(e.FILED,format='%Y%m%d',errors='coerce')
e['per']=pd.to_datetime(e.PERIOD,format='%Y%m%d',errors='coerce')
e['lag']=(e.filed-e.per).dt.days
print('period parse fail', e.per.isna().sum(), 'lag<0', (e.lag<0).sum())
k=e[e.FORM.isin(['10-K','10-Q'])].copy()
dl={('10-K','1-LAF'):60,('10-K','2-ACC'):75,('10-K','4-NON'):90,('10-Q','1-LAF'):40,('10-Q','2-ACC'):40,('10-Q','4-NON'):45}
ext={'10-K':15,'10-Q':5}
k['dl']=[dl.get((f,a),np.nan) for f,a in zip(k.FORM,k.AFS)]
k['late']=k.lag>k.dl+k.FORM.map(ext)+3
k['vlate']=k.lag>365
k['cgrp']=np.select([k.COUNTRYBA.eq('US'),k.COUNTRYBA.isin(['CN','HK','MO','TW'])],['US','China/HK/TW'],'Other')
print(k.groupby(['FORM','AFS']).agg(n=('ADSH','size'),late=('late','mean'),vlate=('vlate','sum')).round(3).to_string())
nn=k[(k.AFS=='4-NON')]
print(nn.groupby(['FORM','cgrp']).agg(n=('ADSH','size'),late=('late','mean'),vlate=('vlate','sum')).round(3).to_string())
print('SIC 6770 shells:', nn.groupby(['FORM',nn.SIC.eq('6770')]).agg(n=('ADSH','size'),late=('late','mean'),vlate=('vlate','sum')).round(3).to_string())
# catch-up filers: 10-K filed > 365 days after period end
cu=e[(e.FORM.isin(['10-K','10-Q','10-K/A','10-Q/A']))&(e.lag>365)]
print('catch-up filings', len(cu), 'companies', cu.CIK.nunique())
g=cu.groupby('CIK').agg(name=('NAME','first'),n=('ADSH','size'),first_per=('per','min'),last_filed=('filed','max'),st=('STPRBA','first'),city=('CITYBA','first'),sic=('SIC','first'),ph=('BAPH','first'),bas=('BAS1','first'))
print(g.sort_values('n',ascending=False).head(40).to_string())
cu.to_pickle('catchup.pkl')
