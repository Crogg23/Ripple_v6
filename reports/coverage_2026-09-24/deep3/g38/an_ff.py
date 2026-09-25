import pandas as pd, numpy as np
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 40); pd.set_option('display.max_columns', 20)
w = pd.read_csv('out_S14.csv', dtype={'API_NUMBER': str})
v = pd.read_csv('out_S15.csv', dtype={'API_NUMBER': str})
print('water rows', len(w), 'operator mismatch w vs d', (w.OPERATOR_NAME != w.W_OPERATOR).sum())
print('dup (disclosure, desc) rows', w.duplicated(['DISCLOSURE_ID','DESCRIPTION']).sum())
# coverage by state among FFV4
v4 = v[v.FF_VERSION.astype(str) == '4']
cov = v4.groupby('STATE_NAME').agg(n=('DISCLOSURE_ID','size'), water=('HAS_WATER','mean')).sort_values('n', ascending=False)
print(cov.head(15).round(3))
fresh = {'Groundwater, < 1000TDS', 'Surface Water, < 1000TDS', 'Other, < 1000TDS'}
w['fresh_pct'] = np.where(w.DESCRIPTION.isin(fresh), w.PERCENT, 0)
w['gw_pct'] = np.where(w.DESCRIPTION == 'Groundwater, < 1000TDS', w.PERCENT, 0)
w['prod_pct'] = np.where(w.DESCRIPTION == 'Produced Water', w.PERCENT, 0)
d = w.groupby('DISCLOSURE_ID').agg(state=('STATE_NAME','first'), county=('COUNTY_NAME','first'), op=('OPERATOR_NAME','first'), api=('API_NUMBER','first'),
    vol=('TOTAL_BASE_WATER_VOLUME','first'), fresh=('fresh_pct','sum'), gw=('gw_pct','sum'), prod=('prod_pct','sum'), tot=('PERCENT','sum'), fed=('FEDERAL_WELL','first'), ind=('INDIAN_WELL','first')).reset_index()
d = d[d.tot > 0]
d['fresh_share'] = (d.fresh / d.tot).clip(0, 1)
d['fresh_gal'] = d.fresh_share * d.vol
d['gw_gal'] = (d.gw / d.tot).clip(0,1) * d.vol
print('disclosures', len(d), 'vol describe'); print(d.vol.describe().round(0))
print('vol > 100M gal', (d.vol > 1e8).sum(), 'vol 0', (d.vol == 0).sum())
print('total gal', round(d.vol.sum()/1e9,1), 'B; fresh', round(d.fresh_gal.sum()/1e9,1), 'B; fresh share by gallons', round(d.fresh_gal.sum()/d.vol.sum(),3))
st = d.groupby('state').agg(n=('api','size'), gal_b=('vol', lambda x: x.sum()/1e9), fresh_share=('fresh_gal','sum'))
st['fresh_share'] = st.fresh_share / (st.gal_b*1e9)
print(st.sort_values('n', ascending=False).round(3).head(15))
d.to_pickle('ff_disc.pkl')
