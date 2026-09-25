import pandas as pd, itertools, re
d=pd.read_csv('out_S16.csv', dtype={'OWNER_CIK':str})
d['is_dir']=d.RELS.str.contains('Director')
d['is_off']=d.RELS.str.contains('Officer')
ent=re.compile(r'\b(LLC|L\.P\.|LP|FUND|TRUST|CAPITAL|PARTNERS|HOLDINGS|INC|CORP|LTD|MANAGEMENT|GROUP|ADVISORS|INVESTMENT)\b', re.I)
d['owner_entity']=d.OWNER_NAME.fillna('').str.contains(ent)
dd=d[d.is_dir & (d.IS_FUND==0) & ~d.owner_entity]
per=dd.groupby('OWNER_CIK').agg(n=('ICIK','nunique'), name=('OWNER_NAME','first')).sort_values('n',ascending=False)
print('directors (people, non-fund issuers):', len(per), 'median boards', per.n.median(), 'mean', round(per.n.mean(),2))
print(per.n.value_counts().sort_index().to_string())
print('>=6 boards:', (per.n>=6).sum(), ' >=8:', (per.n>=8).sum())
top=per.head(25)
for cik,row in top.iterrows():
    iss=dd[dd.OWNER_CIK==cik]
    spac=iss.ISSUER_NAME.str.contains('ACQUISITION|SPAC|MERGER', case=False).sum()
    print(cik, row['name'], row.n, 'spac-like:',spac, '|', '; '.join(iss.ISSUER_NAME.str[:28].tolist()[:14]))
# fund directors check
fd=d[d.is_dir & (d.IS_FUND==1)].groupby('OWNER_CIK').ICIK.nunique().sort_values(ascending=False)
print('fund-issuer directors top:', fd.head(5).to_dict())
per.to_csv('sec_dir_boards_2024.csv')
