import sys; sys.path.insert(0,'.')
from load import df
import pandas as pd
pd.set_option('display.width',250); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',60)
c=df(10)
for k in ['TOTAL_EXPEND_GIFT','TOTAL_EXPEND_AWARD','TOTAL_EXPEND_EVENT']: c[k]=pd.to_numeric(c[k],errors='coerce').fillna(0)
print('cover rows',len(c), 'distinct ids',c.REPORT_INFO_IDENT.nunique())
# dedupe corrections: keep latest received per filer+period+report type
c=c.sort_values('RECEIVED_DT')
c['key']=c.FILER_IDENT+'|'+c.APPLICABLE_YEAR+'|'+c.REPORT_TYPE_CD+'|'+c.PERIOD_START_DT.fillna('')
cd=c.drop_duplicates('key',keep='last')
print('after dedupe',len(cd))
tabs={'GIFT':(1,'TOTAL_EXPEND_GIFT'),'AWARD':(3,'TOTAL_EXPEND_AWARD'),'EVENT':(2,'TOTAL_EXPEND_EVENT')}
ids=set(c.REPORT_INFO_IDENT)
out=[]
for name,(n,col) in tabs.items():
    t=df(n)
    land=t.REPORT_ID.isin(ids).mean()
    print(name,'itemized rows',len(t),'report ids',t.REPORT_ID.nunique(),'land in cover',round(land*100,1),'%')
    # does the itemized report have cover total>0 for that category?
    cc=c.set_index('REPORT_INFO_IDENT')[col]
    tr=t.drop_duplicates('REPORT_ID')
    v=tr.REPORT_ID.map(cc)
    print('   itemized reports whose cover shows >0 in this category', (v>0).sum(),'of',len(tr), '; cover 0', (v==0).sum(), '; not found', v.isna().sum())
    rep_item=set(t.REPORT_ID)
    x=cd[cd[col]>0].copy()
    x['itemized']=x.REPORT_INFO_IDENT.isin(rep_item)
    if 'ACTIVITYAMOUNTRANGEHIGH' in t:
        t['hi']=pd.to_numeric(t.ACTIVITYAMOUNTRANGEHIGH); t['lo']=pd.to_numeric(t.ACTIVITYAMOUNTRANGELOW)
        it=t.groupby('APPLICABLEYEAR').agg(item_lo=('lo','sum'),item_hi=('hi','sum'),item_rows=('ACTIVITY_ID','size'))
    else:
        it=t.groupby('APPLICABLEYEAR').agg(item_rows=('ACTIVITY_ID','size'))
    y=x.groupby('APPLICABLE_YEAR').agg(cover_reports=('REPORT_INFO_IDENT','size'),cover_usd=(col,'sum'),rep_itemized=('itemized','sum'),usd_on_itemized=(col,lambda s:s[x.loc[s.index,'itemized']].sum()))
    y=y.join(it,how='left')
    y['pct_reports_itemized']=(100*y.rep_itemized/y.cover_reports).round(1)
    if 'item_hi' in y: y['item_hi_pct_of_cover']=(100*y.item_hi/y.cover_usd).round(1)
    print(y[y.index>='2004'].round(0).to_string())
