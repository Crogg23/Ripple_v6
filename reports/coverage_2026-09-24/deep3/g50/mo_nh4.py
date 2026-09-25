import pandas as pd, numpy as np
from st import binom_sf, fisher
pd.set_option('display.width',250)
h = pd.read_pickle('mo_homes.pkl')
s = pd.read_csv('out_S12.csv', dtype={'CCN':str})
h = h.merge(s[['CCN','SZ_PCT']], left_on='CMS_CERTIFICATION_NUMBER_CCN', right_on='CCN', how='left')
h['rel'] = h.CHAIN_NAME.eq('RELIANT CARE MANAGEMENT')
h['band'] = np.where(h.SZ_PCT>=40,'sz40+', np.where(h.SZ_PCT.notna(),'sz<40','sz suppressed'))
g = h.groupby(['band','rel']).agg(homes=('reg','size'), homes_w=('reg',lambda x:(x>0).sum()), reg=('reg','sum'), res=('AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY','sum'))
g['per1000'] = 1000*g.reg/g.res
print(g.to_string())
# within sz40+ : Reliant vs other
b = h[h.band=='sz40+']
rr = b[b.rel]; oo = b[~b.rel]
print('sz40+ Reliant reg', rr.reg.sum(), 'res', rr.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY.sum(), '| other reg', oo.reg.sum(), 'res', oo.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY.sum())
share = rr.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY.sum()/b.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY.sum()
print('Reliant share of sz40+ residents', share, 'reg share', rr.reg.sum()/b.reg.sum(), 'p', binom_sf(int(rr.reg.sum()), int(b.reg.sum()), share))
print('homes with >=1 registrant: Reliant', (rr.reg>0).sum(), 'of', len(rr), '| other', (oo.reg>0).sum(), 'of', len(oo), 'fisher', fisher((rr.reg>0).sum(), (rr.reg==0).sum(), (oo.reg>0).sum(), (oo.reg==0).sum()))
print(b.sort_values('reg',ascending=False)[['PROVIDER_NAME','CITY','CHAIN_NAME','SZ_PCT','AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY','reg','OVERALL_RATING']].head(25).to_string())
# correlation reg rate vs sz pct overall
x = h[h.SZ_PCT.notna() & (h.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY>0)]
print('spearman-ish: corr of rank(sz) and rank(per1000)', x.SZ_PCT.rank().corr((x.reg/x.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY).rank()))
h.to_pickle('mo_homes2.pkl')
