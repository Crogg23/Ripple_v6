import pandas as pd, numpy as np
pd.set_option('display.width', 250)
df = pd.read_pickle('out_S01.pkl'); df = df[df.COUNTRY_CODE.str.strip() != ''].copy(); df['CC'] = df.COUNTRY_CODE.str.strip()
yc = [c for c in df.columns if c.startswith('C_')]
for c in yc: df[c] = pd.to_numeric(df[c].replace('', np.nan), errors='coerce')
AGG = {'EAP','ECA','IDA','IDX','LAC','LDC','LIC','LMC','LMY','MIC','MNA','SAS','SSA','UMC'}
cty = df[~df.CC.isin(AGG)]
def ser(code): return cty[cty.SERIES_CODE == code].set_index('CC')
cb = ser('DT.TDS.PCBK.CD'); ex = ser('BX.GSR.TOTL.CD'); nm = cty.drop_duplicates('CC').set_index('CC').COUNTRY_NAME
o = pd.DataFrame({'name': nm, 'cb22': cb.C_2022, 'cb24': cb.C_2024, 'cb26': cb.C_2026, 'exp24': ex.C_2024})
o['cb26_pct_exp'] = 100 * o.cb26 / o.exp24; o['cb22_pct_exp'] = 100 * o.cb22 / o.exp24
o = o[o.exp24 > 0]
print('commercial-bank PPG debt service scheduled 2026 as % of 2024 exports, top 12; n with exports', len(o), 'median', round(o.cb26_pct_exp.median(), 2))
print(o.sort_values('cb26_pct_exp', ascending=False).head(12).to_string(float_format=lambda x: f'{x/1e9:,.2f}B' if abs(x) > 1e6 else f'{x:,.1f}'))
# Senegal rank on total scheduled 2026 % exports, excluding countries in default/restructuring flagged by arrears > 0 in 2024
arr = ser('DT.IXA.DLXF.CD').C_2024
w = pd.read_pickle('wb_country.pkl')
w['arrears24'] = arr
w2 = w[(w.exp24 > 0)]
print('\nrank of Senegal on sched26 % exp:', int(w2.sched26_pct_exp.rank(ascending=False)['SEN']), 'of', w2.sched26_pct_exp.notna().sum())
print('countries with interest arrears > 0 in 2024 among top 10:')
print(w2.sort_values('sched26_pct_exp', ascending=False).head(10)[['name','sched26_pct_exp','arrears24']].to_string(float_format=lambda x: f'{x/1e9:,.2f}B' if abs(x) > 1e6 else f'{x:,.1f}'))
print('median sched26 % exp among no-arrears countries:', round(w2[w2.arrears24.fillna(0) == 0].sched26_pct_exp.median(), 2), 'n', (w2.arrears24.fillna(0) == 0).sum())
