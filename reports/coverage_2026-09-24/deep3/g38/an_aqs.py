import pandas as pd, numpy as np
a = pd.read_csv('out_S11.csv', dtype=str)
a['est'] = pd.to_datetime(a.SITE_ESTABLISHED_DATE, errors='coerce')
a['clo'] = pd.to_datetime(a.SITE_CLOSED_DATE, errors='coerce')
a['lat'] = a.LATITUDE.astype(float); a['lon'] = a.LONGITUDE.astype(float)
print('rows', len(a), 'open', a.clo.isna().sum())
# open sites at end of each year
for y in [1975,1980,1985,1990,1995,2000,2005,2010,2015,2018,2020,2022,2024,2025]:
    d = pd.Timestamp(f'{y}-12-31')
    op = ((a.est <= d) & (a.clo.isna() | (a.clo > d))).sum()
    print(y, op)
print(a[a.est > pd.Timestamp('2026-06-26')][['AQS_SITE_ID','est','OWNING_AGENCY','LOCAL_SITE_NAME','CITY_NAME']])
# closures 2015-2026 by state
rec = a[(a.clo >= '2015-01-01')]
print(rec.groupby('STATE_NAME').size().sort_values(ascending=False).head(15))
# open sites w/o coords
op = a[a.clo.isna()]
print('open no coords', ((op.lat==0)|op.lat.isna()).sum())
print(op.LOCATION_SETTING.value_counts(dropna=False))
print(op.OWNING_AGENCY.value_counts().head(10))
# sites closed on Dec 31 share
print('closed dec31 share', ((a.clo.dt.month==12)&(a.clo.dt.day==31)).sum(), a.clo.notna().sum())
# states: open sites count
print(op.groupby('STATE_NAME').size().sort_values().head(12))
