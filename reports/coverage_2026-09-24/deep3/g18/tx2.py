import sys; sys.path.insert(0,'.')
from load import df
import pandas as pd
pd.set_option('display.width',250); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',50)
c=df(10)
for k in ['TOTAL_EXPEND_GIFT','TOTAL_EXPEND_AWARD','TOTAL_EXPEND_EVENT']: c[k]=pd.to_numeric(c[k],errors='coerce').fillna(0)
c=c.sort_values('RECEIVED_DT'); c['key']=c.FILER_IDENT+'|'+c.APPLICABLE_YEAR+'|'+c.REPORT_TYPE_CD+'|'+c.PERIOD_START_DT.fillna('')
cd=c.drop_duplicates('key',keep='last')
g=df(1); items=set(g.REPORT_ID)
x=cd[cd.TOTAL_EXPEND_GIFT>0].copy(); x['itemized']=x.REPORT_INFO_IDENT.isin(items)
x['yr']=x.APPLICABLE_YEAR.astype(int)
x['era']=pd.cut(x.yr,[2004,2011,2018,2026],labels=['2005-11','2012-18','2019-26'])
# concentration of gift dollars by filer per era
for era,s in x.groupby('era'):
    f=s.groupby(['FILER_IDENT']).agg(name=('FILER_NAME','last'),usd=('TOTAL_EXPEND_GIFT','sum'),reps=('REPORT_INFO_IDENT','size'),item=('itemized','sum')).sort_values('usd',ascending=False)
    tot=f.usd.sum()
    print(era,'filers',len(f),'total',round(tot),'top5 share',round(100*f.usd.head(5).sum()/tot,1),'median filer',round(f.usd.median()))
    print(f.head(8).to_string())
# distribution of per-report gift amounts, itemized vs not, by era
print(x.groupby(['era','itemized']).TOTAL_EXPEND_GIFT.describe(percentiles=[.5,.9]).round(0).to_string())
# reports with gift >= 1000 : itemized share by era
big=x[x.TOTAL_EXPEND_GIFT>=1000]
print(big.groupby('era').agg(n=('itemized','size'),item=('itemized','sum'),usd=('TOTAL_EXPEND_GIFT','sum')))
