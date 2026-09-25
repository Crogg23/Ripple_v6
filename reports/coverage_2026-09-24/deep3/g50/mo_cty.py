import pandas as pd, numpy as np
pd.set_option('display.width',250)
r = pd.read_csv('out_S07.csv', dtype=str); r['pid']=r.REGISTRANT_NAME+'|'+r.DATE_OF_BIRTH
p = r.drop_duplicates('pid').copy()
A = p.ADDRESS.fillna('').str.upper()
p['kind'] = np.select([A.str.contains('INCARC'), A.str.contains('MOVED'), A.str.contains('UNKNOWN'), A.eq('')], ['incarcerated','moved out','unknown','blank'], 'street')
print(pd.crosstab(p.kind, p.IS_COMPLIANT, margins=True))
# does any person have mixed compliance/address across rows?
print('persons with >1 compliance value', (r.groupby('pid').IS_COMPLIANT.nunique()>1).sum(), ' >1 address', (r.groupby('pid').ADDRESS.nunique()>1).sum())
s = p[p.kind.isin(['street','unknown','blank'])]
c = s.groupby('COUNTY').agg(n=('pid','size'), nc=('IS_COMPLIANT', lambda x:(x=='False').sum()), unk=('kind', lambda x:(x=='unknown').sum()), blank=('kind', lambda x:(x=='blank').sum()))
c['rate'] = c.nc/c.n
big = c[c.n>=100].sort_values('rate', ascending=False)
print('counties with 100+:', len(big), 'median rate', big.rate.median(), 'statewide', s.IS_COMPLIANT.eq('False').mean())
print(big.head(10).to_string()); print(big.tail(5).to_string())
print('Jackson noncompliant', c.loc['JACKSON'].to_dict() if 'JACKSON' in c.index else None, 'share of state noncompliant', c.loc['JACKSON','nc']/c.nc.sum())
# offense count outliers
r['OFFENSE_COUNT']=pd.to_numeric(r.OFFENSE_COUNT)
print(r.sort_values('OFFENSE_COUNT',ascending=False)[['REGISTRANT_NAME','OFFENSE','OFFENSE_COUNT','TIER','CITY']].head(6).to_string())
print('ages 95+', (pd.to_datetime(p.DATE_OF_BIRTH) < '1931-09-24').sum(), 'under 21', (pd.to_datetime(p.DATE_OF_BIRTH) > '2005-09-24').sum())
print(p[pd.to_datetime(p.DATE_OF_BIRTH) < '1931-09-24'][['REGISTRANT_NAME','DATE_OF_BIRTH','ADDRESS','CITY','IS_COMPLIANT']].to_string())
