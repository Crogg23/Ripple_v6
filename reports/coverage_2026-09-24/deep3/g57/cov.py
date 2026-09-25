import pandas as pd
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 200)
q = pd.read_csv('out_S08.csv', dtype={'AREA_FIPS': str, 'AGG': str, 'INDUSTRY_CODE': str, 'DISCLOSURE_CODE': str})
o = pd.read_csv('out_S12.csv', dtype={'YR': str, 'ST': str, 'NAICS': str})
fips = {'01':'AL','02':'AK','04':'AZ','05':'AR','06':'CA','08':'CO','09':'CT','10':'DE','11':'DC','12':'FL','13':'GA','15':'HI','16':'ID','17':'IL','18':'IN','19':'IA','20':'KS','21':'KY','22':'LA','23':'ME','24':'MD','25':'MA','26':'MI','27':'MN','28':'MS','29':'MO','30':'MT','31':'NE','32':'NV','33':'NH','34':'NJ','35':'NM','36':'NY','37':'NC','38':'ND','39':'OH','40':'OK','41':'OR','42':'PA','44':'RI','45':'SC','46':'SD','47':'TN','48':'TX','49':'UT','50':'VT','51':'VA','53':'WA','54':'WV','55':'WI','56':'WY','72':'PR','78':'VI'}
q['st'] = q.AREA_FIPS.str[:2].map(fips)
print('osha totals', o.groupby('YR')[['SITES_ALL','SITES_OK','EMP_OK','EMP20_OK']].sum().to_string())
tot = q[q.AGG == '51'].set_index('st').EMP
# state coverage, all private industries
os_ = o.groupby(['YR', 'ST'])[['EMP_OK', 'EMP20_OK', 'SITES_OK']].sum().reset_index()
os_['qcew'] = os_.ST.map(tot)
os_['cov'] = os_.EMP20_OK / os_.qcew
s23 = os_[os_.YR == '2023'].dropna().sort_values('cov')
print('national cov 2023', s23.EMP20_OK.sum() / s23.qcew.sum(), 'median state', s23['cov'].median())
print(s23.head(12).to_string()); print(s23.tail(5).to_string())
s24 = os_[os_.YR == '2024'].dropna().set_index('ST')['cov']
s23i = s23.set_index('ST')['cov']
print('corr 23 vs 24', s23i.corr(s24))
os_.to_csv('state_cov.csv', index=False)
