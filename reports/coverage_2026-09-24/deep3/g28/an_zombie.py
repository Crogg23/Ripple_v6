import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',40)
d=pd.read_pickle('out_S07.pkl')
for c in ['LAST_YR','REC24','DISB24','INDIV24','COH24','TO_AUTH24','REC26','DISB26','COH26','OTHER_ID_MAX_YR']:
    d[c]=pd.to_numeric(d[c],errors='coerce')
print(len(d), d.FEC_CMTE_ID.nunique(), d.CAND.nunique())
print('last_yr dist', d.LAST_YR.value_counts(dropna=False).sort_index().to_dict())
print('LAST_CYCLE', d.LAST_CYCLE.value_counts(dropna=False).to_dict())
print('has s24', d.DISB24.notna().sum(), 'has s26', d.DISB26.notna().sum())
d['gap']=2024-d.LAST_YR
d['other_run']=d.OTHER_ID_MAX_YR>=2022
# only principal committees, one per candidate to avoid double counting summary (summary is per candidate)
p=d[d.CMTE_DSGN=='P'].drop_duplicates('CAND')
print('principal cands', len(p))
p['grp']=pd.cut(p.LAST_YR,[0,2016,2018,2020,2022,2024,2030],labels=['<=2016','2017-18','2019-20','2021-22','2023-24','2025+'])
g=p.groupby('grp',observed=False).agg(cands=('CAND','size'), with24=('DISB24',lambda x:x.notna().sum()),
    spent_any=('DISB24',lambda x:(x>0).sum()), spent_10k=('DISB24',lambda x:(x>=10000).sum()), spent_100k=('DISB24',lambda x:(x>=100000).sum()),
    disb=('DISB24','sum'), rec=('REC24','sum'), indiv=('INDIV24','sum'), incumb=('IC24',lambda x:(x=='I').sum()), other=('other_run','sum'))
print(g.to_string())
z=p[(p.LAST_YR<=2020)&(p.IC24!='I')&(~p.other_run)&(p.DISB24>0)]
print('zombie-shaped (last ran <=2020, not incumbent 2024, no other id running 2022+, spent in 2024 cycle):', len(z), 'disb', z.DISB24.sum(), 'median', z.DISB24.median(), 'rec', z.REC24.sum(),'indiv',z.INDIV24.sum())
print('by office', z.groupby('OFFICE').agg(n=('CAND','size'),disb=('DISB24','sum'),med=('DISB24','median')).to_string())
cols=['FEC_CMTE_ID','CMTE_NM','CAND','CAND_NAME','OFFICE','OST','LAST_YR','STATUSES','IC24','REC24','INDIV24','DISB24','TO_AUTH24','COH24','DISB26','COH26','CMTE_FILING_FREQ']
print(z.sort_values('DISB24',ascending=False)[cols].head(30).to_string())
z.to_csv('zombie_candidates.csv',index=False)
# concentration: top 5 share
zs=z.sort_values('DISB24',ascending=False)
print('top5 share', zs.DISB24.head(5).sum()/zs.DISB24.sum(), 'top10', zs.DISB24.head(10).sum()/zs.DISB24.sum())
