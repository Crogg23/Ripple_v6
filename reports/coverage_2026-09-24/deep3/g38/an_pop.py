import pandas as pd, numpy as np
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30); pd.set_option('display.max_colwidth', 38)
t = pd.read_pickle('tri_aqs.pkl')
tr = pd.read_csv('out_S13.csv', dtype={'TRACT_GEOID': str, 'COUNTY_FIPS': str})
tr = tr[tr.POP_CENTER_LAT.notna()]
print('tracts', len(tr), 'pop', tr.POPULATION_2020.sum())
R = 3958.8
p2 = np.radians(tr.POP_CENTER_LAT.values)[None, :].astype(np.float64); l2 = np.radians(tr.POP_CENTER_LON.values)[None, :]
pop = tr.POPULATION_2020.values.astype(float)
plat = np.radians(t.LAT.values); plon = np.radians(t.LON.values)
out3 = np.empty(len(t)); cnty = []
for s in range(0, len(t), 400):
    p1 = plat[s:s+400][:, None]; l1 = plon[s:s+400][:, None]
    h = np.sin((p2-p1)/2)**2 + np.cos(p1)*np.cos(p2)*np.sin((l2-l1)/2)**2
    d = 2*R*np.arcsin(np.sqrt(h))
    out3[s:s+400] = (pop[None, :] * (d <= 3)).sum(1)
    cnty.extend(tr.COUNTY_FIPS.values[d.argmin(1)])
t['pop3mi'] = out3; t['county_fips'] = cnty
t.to_pickle('tri_aqs_pop.pkl')
print(t.pop3mi.describe())
