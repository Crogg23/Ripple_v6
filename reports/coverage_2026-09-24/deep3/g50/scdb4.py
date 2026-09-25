import pandas as pd, numpy as np
from st import fisher
pd.set_option('display.width',250); pd.set_option('display.max_rows',200); pd.set_option('display.max_colwidth',60)
c = pd.read_csv('out_S10.csv', dtype={'CASE_ID':str}); c.columns=[x.lower() for x in c.columns]
arg = c[c.decision_type.isin([1,6,7])].copy()
arg['st'] = arg.source.between(300,302)
t = arg.groupby('term').agg(cases=('case_id','size'), st=('st','sum'))
t['share']=t.st/t.cases
r5 = (t.st.rolling(5).sum()/t.cases.rolling(5).sum())
print('lowest 5-term windows (end term):'); print(r5.sort_values().head(5).round(3).to_string())
print('2020-24 terms rank among 79 (1=lowest):', t.share.rank(method='min').loc[2020:2024].to_dict(), 'n terms', len(t))
for a,b in [(2010,2014),(2015,2019),(2020,2024)]:
    x=t.loc[a:b]; print(a,b,'argued',x.cases.sum(),'state',x.st.sum(), round(x.st.sum()/x.cases.sum(),3))
# petitions (CourtListener), lag one year
d=pd.read_csv('out_S13.csv'); d.columns=[q.lower() for q in d.columns]
pv=d.pivot_table(index='y',columns='kind',values='n',aggfunc='sum').fillna(0)
for (a,b),(pa,pb) in [((2015,2019),(2014,2018)),((2020,2024),(2019,2023))]:
    sp=pv.loc[pa:pb,'state'].sum(); fp=pv.loc[pa:pb,'federal'].sum()
    x=t.loc[a:b]; sa=x.st.sum(); fa=x.cases.sum()-sa
    print(f'terms {a}-{b}: petitions filed {pa}-{pb} state {sp:.0f} federal {fp:.0f} state share {sp/(sp+fp):.3f} | argued state {sa} per1000 petitions {1000*sa/sp:.2f} | argued non-state {fa} per1000 fed petitions {1000*fa/fp:.2f}')
# issue areas
arg['win']=np.where(arg.term.between(2015,2019),'15-19',np.where(arg.term.between(2020,2024),'20-24',None))
s = arg[arg.st & arg.win.notna()]
print(pd.crosstab(s.issue_area, s.win))
print('criminal procedure(1) share of all argued:', arg[arg.win.notna()].groupby('win').apply(lambda x:(x.issue_area==1).mean()).round(3).to_dict())
print('state-court crim-pro argued:', s[s.issue_area==1].groupby('win').size().to_dict(), ' all crim-pro argued:', arg[arg.win.notna() & (arg.issue_area==1)].groupby('win').size().to_dict())
print(s[s.win=='20-24'][['term','case_name','source','source_state','issue_area','party_winning','dec_dir','maj_votes','min_votes']].to_string())
print('fisher state share 15-19 vs 20-24:', fisher(52, 314-52, 19, 295-19))
