import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',45); pd.set_option('display.max_columns',30)
s=pd.read_csv('out_S16.csv')
print(len(s), s.FEATURES.value_counts().sort_index().to_dict())
print('units mix per site:', s.UNITS.value_counts(dropna=False).head(10).to_dict())
print('NPL:', s.NPL.value_counts().to_dict())
s['acres']=s.ACRES_SUM
print('raw battery sum 7.0M mixes units; acres-converted total (excl Miles):', round(s.acres.sum()), ' sites with Miles unit:', s.MILES_SUM.notna().sum())
print(s.sort_values('acres',ascending=False)[['EPA_ID','SITE','ST','NPL','FED','FEATURES','UNITS','acres','FTYPES']].head(15).to_string())
print(s.groupby('FED').acres.describe().round(1))
s['cy']=pd.to_datetime(s.CREATED,errors='coerce').dt.year; s['chy']=pd.to_datetime(s.CHANGED,errors='coerce').dt.year
print('changed year:', s.chy.value_counts().sort_index().to_dict())
print('Miles-unit sites by region:', s[s.MILES_SUM.notna()].REGION.value_counts().to_dict(), s[s.MILES_SUM.notna()].PROGRAMS.value_counts().to_dict())
print('Square-mile sites by region:', s[s.UNITS.fillna('').str.contains('Square')].REGION.value_counts().to_dict())
print('region x units:'); print(pd.crosstab(s.REGION, s.UNITS.fillna('(blank)')))
print('contacts top:', s.CONTACT.value_counts().head(5).to_dict())
