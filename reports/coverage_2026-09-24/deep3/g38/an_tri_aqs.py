import pandas as pd, numpy as np
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30); pd.set_option('display.max_colwidth', 40)
a = pd.read_csv('out_S11.csv', dtype=str)
a['est'] = pd.to_datetime(a.SITE_ESTABLISHED_DATE, errors='coerce'); a['clo'] = pd.to_datetime(a.SITE_CLOSED_DATE, errors='coerce')
a['lat'] = a.LATITUDE.astype(float); a['lon'] = a.LONGITUDE.astype(float)
a = a[(a.lat != 0) & a.lat.notna()]
t = pd.read_csv('out_S12.csv', dtype={'FRS': str})
print('tri rows', len(t), 'distinct frs', t.FRS.nunique(), 'null frs', t.FRS.isna().sum())
t = t[t.LAT.notna() & (t.LAT != 0)].copy()
R = 3958.8
def nearest(plat, plon, slat, slon):
    p1 = np.radians(plat)[:, None]; l1 = np.radians(plon)[:, None]
    p2 = np.radians(slat)[None, :]; l2 = np.radians(slon)[None, :]
    out_d = np.empty(len(plat)); out_i = np.empty(len(plat), dtype=int)
    for s in range(0, len(plat), 500):
        dp = p2 - p1[s:s+500]; dl = l2 - l1[s:s+500]
        h = np.sin(dp/2)**2 + np.cos(p1[s:s+500])*np.cos(p2)*np.sin(dl/2)**2
        d = 2*R*np.arcsin(np.sqrt(h))
        out_i[s:s+500] = d.argmin(1); out_d[s:s+500] = d.min(1)
    return out_d, out_i
open23 = a[(a.est <= '2023-12-31') & (a.clo.isna() | (a.clo >= '2023-01-01'))].reset_index(drop=True)
opennow = a[a.clo.isna()].reset_index(drop=True)
ever = a.reset_index(drop=True)
print('sites open in 2023', len(open23), 'open now', len(opennow))
d, i = nearest(t.LAT.values, t.LON.values, open23.lat.values, open23.lon.values)
t['mi_2023'] = d; t['near_site'] = open23.AQS_SITE_ID.values[i]; t['near_setting'] = open23.LOCATION_SETTING.values[i]
d2, i2 = nearest(t.LAT.values, t.LON.values, ever.lat.values, ever.lon.values)
t['mi_ever'] = d2; t['ever_site'] = ever.AQS_SITE_ID.values[i2]; t['ever_closed'] = ever.clo.values[i2]; t['ever_est'] = ever.est.values[i2]
t.to_pickle('tri_aqs.pkl')
print(t.mi_2023.describe())
carc = t[t.CARC_AIR_LBS > 0].sort_values('CARC_AIR_LBS', ascending=False)
print('facilities with carcinogen air', len(carc), 'total lbs', carc.CARC_AIR_LBS.sum())
top = carc.head(100)
print('top100 share of carc air', top.CARC_AIR_LBS.sum()/carc.CARC_AIR_LBS.sum())
for lab, g in [('all TRI', t), ('carc>0', carc), ('top100 carc', top), ('top25 carc', carc.head(25))]:
    print(lab, len(g), 'median mi', round(g.mi_2023.median(),1), '>10mi', (g.mi_2023>10).mean().round(3), '>20mi', (g.mi_2023>20).mean().round(3))
print(top[['NAME','CITY','ST','SECTOR','CARC_AIR_LBS','TOP_CARC','mi_2023','near_site','mi_ever','ever_closed']].head(40).to_string())
