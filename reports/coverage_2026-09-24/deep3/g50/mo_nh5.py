import pandas as pd, numpy as np
from st import binom_sf
pd.set_option('display.width',250)
h = pd.read_pickle('mo_homes2.pkl'); pn = pd.read_pickle('mo_persons.pkl')
nhp = pn[pn.in_nh]
cc = nhp[nhp.comp=='True'].groupby('CMS_CERTIFICATION_NUMBER_CCN').size().rename('reg_c')
h = h.merge(cc, left_on='CMS_CERTIFICATION_NUMBER_CCN', right_index=True, how='left').fillna({'reg_c':0})
print('compliant NH registrants', h.reg_c.sum(), 'homes w/ >=1 compliant', (h.reg_c>0).sum())
rel = h.rel
print('Reliant compliant', h[rel].reg_c.sum(), 'share', h[rel].reg_c.sum()/h.reg_c.sum(), 'res share', h[rel].AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY.sum()/h.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY.sum())
top = h.sort_values('reg_c',ascending=False)[['PROVIDER_NAME','CITY','CHAIN_NAME','AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY','reg','reg_c','SZ_PCT','OVERALL_RATING','ABUSE_ICON','SPECIAL_FOCUS_STATUS','ABUSE_TAGS','HARM_G_PLUS','TOTAL_AMOUNT_OF_FINES_IN_DOLLARS']].head(12)
top['per100_c'] = 100*top.reg_c/top.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY
print(top.to_string())
b = h[h.band=='sz40+']
for lab, d in [('Reliant',b[b.rel]),('other',b[~b.rel])]:
    print('sz40+', lab, 'compliant reg', d.reg_c.sum(), 'res', round(d.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY.sum()), 'per1000', round(1000*d.reg_c.sum()/d.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY.sum(),1))
top4 = ['FOUR SEASONS LIVING CENTER','NORTH VILLAGE PARK','BRIDGEWOOD HEALTH CARE CENTER','BERNARD CARE CENTER']
d = b[b.rel & ~b.PROVIDER_NAME.isin(top4)]
print('sz40+ Reliant minus top4: reg', d.reg.sum(), 'res', d.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY.sum(), 'per1000', 1000*d.reg.sum()/d.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY.sum())
# age & offense of the registrants at the top 4 Reliant homes
t4 = h[h.PROVIDER_NAME.isin(top4)].CMS_CERTIFICATION_NUMBER_CCN
x = nhp[nhp.CMS_CERTIFICATION_NUMBER_CCN.isin(t4)]
print('top4 registrants', len(x), 'median age', x.age.median(), 'under 60', (x.age<60).sum(), 'tier3', (x.tier=='3').sum(), 'noncomp', (x.comp=='False').sum())
r = pd.read_csv('out_S07.csv', dtype=str); r['pid']=r.REGISTRANT_NAME+'|'+r.DATE_OF_BIRTH
child = r[r.OFFENSE.str.upper().str.contains('CHILD|MINOR|UNDER 1|STAT|INCEST|<')].pid.unique()
print('top4 with a child-victim-worded offense', x.pid.isin(child).sum(), '| all NH', nhp.pid.isin(child).sum(), 'of', len(nhp))
print('all NH: median age', round(nhp.age.median(),1), 'IQR', nhp.age.quantile([.25,.75]).round(1).tolist())
h.to_pickle('mo_homes3.pkl')
