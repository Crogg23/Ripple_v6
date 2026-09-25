import pandas as pd, numpy as np
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40); pd.set_option('display.max_rows', 200)
df = pd.read_pickle(r'C:\Code\Ripple_v6\reports\coverage_2026-09-24\deep3\g27\out_S01.pkl')
df = df[df.COUNTRY_CODE.str.strip() != ''].copy()
df['CC'] = df.COUNTRY_CODE.str.strip()
yc = [c for c in df.columns if c.startswith('C_')]
for c in yc:
    df[c] = pd.to_numeric(df[c].replace('', np.nan), errors='coerce')
AGG = {'EAP','ECA','IDA','IDX','LAC','LDC','LIC','LMC','LMY','MIC','MNA','SAS','SSA','UMC'}
cty = df[~df.CC.isin(AGG)]
names = cty.drop_duplicates('CC').set_index('CC').COUNTRY_NAME

def ser(code):
    return cty[cty.SERIES_CODE == code].set_index('CC')[yc]

tds_ppg = ser('DT.TDS.DPPG.CD')
tds_lt = ser('DT.TDS.DLXF.CD')
int_ppg = ser('DT.INT.DPPG.CD')
bond_amt = ser('DT.AMT.PBND.CD')
bond_tds = ser('DT.TDS.PBND.CD')
exp = ser('BX.GSR.TOTL.CD')
res = ser('FI.RES.TOTL.CD')
gni = ser('NY.GNP.MKTP.CD')
tdsx = ser('DT.TDS.DECT.EX.ZS')
imf = ser('DT.TDS.DIMF.CD')
bil = ser('DT.TDS.BLAT.CD'); mlt = ser('DT.TDS.MLAT.CD'); prv = ser('DT.TDS.PRVT.CD')

out = pd.DataFrame({'name': names})
out['exp24'] = exp['C_2024']; out['res24'] = res['C_2024']; out['gni24'] = gni['C_2024']
out['ppg_tds_19'] = tds_ppg['C_2019']; out['ppg_tds_24'] = tds_ppg['C_2024']
out['ppg_tds_26'] = tds_ppg['C_2026']; out['ppg_tds_27'] = tds_ppg['C_2027']; out['ppg_tds_28'] = tds_ppg['C_2028']
out['int_19'] = int_ppg['C_2019']; out['int_24'] = int_ppg['C_2024']
out['bond_prin_26_28'] = bond_amt[['C_2026','C_2027','C_2028']].sum(axis=1)
out['bond_tds_26_28'] = bond_tds[['C_2026','C_2027','C_2028']].sum(axis=1)
out['tdsx_24'] = tdsx['C_2024']
out['sched26_pct_exp'] = 100 * out.ppg_tds_26 / out.exp24
out['act24_pct_exp'] = 100 * out.ppg_tds_24 / out.exp24
out['bond_pct_res'] = 100 * out.bond_prin_26_28 / out.res24
out['int_growth'] = out.int_24 / out.int_19
print('countries', len(out), 'with exports 2024', out.exp24.notna().sum(), 'with reserves 2024', out.res24.notna().sum())
print('\n== PPG debt service: actual 2024 vs scheduled 2026, % of 2024 exports; top 25 by scheduled')
cols = ['name','exp24','ppg_tds_24','ppg_tds_26','act24_pct_exp','sched26_pct_exp','tdsx_24']
o = out[out.exp24 > 0].sort_values('sched26_pct_exp', ascending=False)
print(o[cols].head(25).to_string(float_format=lambda x: f'{x:,.1f}' if abs(x) < 1e6 else f'{x/1e9:,.2f}B'))
print('median sched26 % exp', o.sched26_pct_exp.median(), 'median act24 % exp', o.act24_pct_exp.median())
print('\n== Bond principal due 2026-28 vs 2024 reserves, top 20')
b = out[(out.res24 > 0) & (out.bond_prin_26_28 > 0)].sort_values('bond_pct_res', ascending=False)
print(b[['name','res24','bond_prin_26_28','bond_pct_res','exp24']].head(20).to_string(float_format=lambda x: f'{x:,.1f}' if abs(x) < 1e6 else f'{x/1e9:,.2f}B'))
print('countries with any bond principal due 26-28:', len(b), 'median % res', b.bond_pct_res.median())
print('\n== Interest on PPG debt: 2024 vs 2019, top 20 by growth among int_19 > $100M')
g = out[out.int_19 > 1e8].sort_values('int_growth', ascending=False)
print(g[['name','int_19','int_24','int_growth','exp24']].head(20).to_string(float_format=lambda x: f'{x:,.2f}' if abs(x) < 1e6 else f'{x/1e9:,.2f}B'))
print('median growth', g.int_growth.median(), 'n', len(g))
tot19 = out.int_19.sum(); tot24 = out.int_24.sum()
print(f'all-country PPG interest 2019 {tot19/1e9:.1f}B 2024 {tot24/1e9:.1f}B')
# aggregates check vs LMY
lmy = df[(df.CC=='LMY') & (df.SERIES_CODE=='DT.INT.DPPG.CD')][['C_2019','C_2024']]
print('LMY aggregate', lmy.to_string())
# projection check: scheduled vs later actual (2023 edition not available) - show 2025..2032 for total
tot = tds_ppg[yc[-12:]].sum()
print((tot/1e9).round(1).to_string())
out.to_pickle(r'C:\Code\Ripple_v6\reports\coverage_2026-09-24\deep3\g27\wb_country.pkl')
