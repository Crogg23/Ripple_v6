import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_rows',200)
c = pd.read_csv('out_S10.csv', dtype={'CASE_ID':str}); c.columns=[x.lower() for x in c.columns]
arg = c[c.decision_type.isin([1,6,7])].copy()
# coding check: state-source code vs state column
arg['src_statecode'] = arg.source.between(300,303)
print(pd.crosstab(arg.src_statecode, arg.source_state.notna()))
print('source codes when source_state present:', arg[arg.source_state.notna()].source.value_counts().head(8).to_dict())
print('source codes 300+ w/o state:', arg[arg.src_statecode & arg.source_state.isna()][['term','case_name','source']].head(10).to_string())
arg['state_src'] = arg.source_state.notna() | arg.src_statecode
arg['state_origin'] = arg.origin_state.notna() | arg.origin.between(300,303)
t = arg.groupby('term').agg(cases=('case_id','size'), st=('state_src','sum'), st_orig=('state_origin','sum'), orig_miss=('origin', lambda s: s.isna().sum()))
t['share']=t.st/t.cases; t['orig_share']=t.st_orig/t.cases
print('rank of 2020-24 shares among all terms (1=lowest):'); t['rank']=t.share.rank(method='min')
print(t.sort_values('share').head(12).to_string())
print(t.loc[2010:].to_string())
w = lambda a,b: t.loc[a:b]
for a,b in [(1946,1968),(1969,1985),(1986,2004),(2005,2014),(2015,2019),(2020,2024)]:
    x=w(a,b); print(a,b,'cases',x.cases.sum(),'state src',x.st.sum(), round(x.st.sum()/x.cases.sum(),3), '| state origin', x.st_orig.sum(), round(x.st_orig.sum()/x.cases.sum(),3))
arg.to_pickle('scdb_arg2.pkl')
