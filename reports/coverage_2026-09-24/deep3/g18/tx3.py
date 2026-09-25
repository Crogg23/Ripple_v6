import sys; sys.path.insert(0,'.')
from load import df
import pandas as pd
pd.set_option('display.width',250); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',50)
c=df(10)
for k in ['TOTAL_EXPEND_GIFT','TOTAL_EXPEND_AWARD','TOTAL_EXPEND_EVENT']: c[k]=pd.to_numeric(c[k],errors='coerce').fillna(0)
c=c.sort_values('RECEIVED_DT'); c['key']=c.FILER_IDENT+'|'+c.APPLICABLE_YEAR+'|'+c.REPORT_TYPE_CD+'|'+c.PERIOD_START_DT.fillna('')
cd=c.drop_duplicates('key',keep='last').copy()
# repeated-total trap: same filer, same nonzero gift amount on 3+ reports
cd['rep_amt']=cd.groupby(['FILER_IDENT','TOTAL_EXPEND_GIFT']).REPORT_INFO_IDENT.transform('size')
junk=cd[(cd.TOTAL_EXPEND_GIFT>=1000)&(cd.rep_amt>=3)]
print('repeated $1K+ gift totals (same filer same amount 3+ times):'); print(junk.groupby(['FILER_NAME','TOTAL_EXPEND_GIFT']).size())
g=df(1); items=set(g.REPORT_ID)
x=cd[(cd.TOTAL_EXPEND_GIFT>=1000)&~((cd.rep_amt>=3))].copy(); x['itemized']=x.REPORT_INFO_IDENT.isin(items)
y=x.groupby('APPLICABLE_YEAR').agg(n=('itemized','size'),item=('itemized','sum'),usd=('TOTAL_EXPEND_GIFT','sum'),filers=('FILER_IDENT','nunique'))
y['pct']=(100*y.item/y.n).round(1)
print(y[y.index>='2005'].to_string())
x['yr']=x.APPLICABLE_YEAR.astype(int)
for a,b in [(2005,2011),(2012,2018),(2019,2026)]:
    s=x[(x.yr>=a)&(x.yr<=b)]; print(a,b,'reports',len(s),'itemized',s.itemized.sum(),round(100*s.itemized.mean(),1),'% usd',round(s.TOTAL_EXPEND_GIFT.sum()), 'filers', s.FILER_IDENT.nunique())
# threshold proxy: itemized rows by bracket per era (non-bulk)
g['hi']=pd.to_numeric(g.ACTIVITYAMOUNTRANGEHIGH); g['yr']=g.APPLICABLEYEAR.astype(int)
g['lt100']=g.hi<100
print(g.groupby(pd.cut(g.yr,[2003,2008,2012,2016,2020,2026]),observed=True).agg(rows=('hi','size'),lt100=('lt100','mean'),med=('hi','median')).round(2))
