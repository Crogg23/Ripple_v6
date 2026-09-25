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
yrs = ['C_2022','C_2023','C_2024','C_2025','C_2026','C_2027','C_2028','C_2029','C_2030','C_2031','C_2032']
# 2030 spike: who drives it
t = cty[cty.SERIES_CODE == 'DT.TDS.DPPG.CD'].set_index('CC')
t['jump30'] = t.C_2030 - t.C_2029
print('2030 minus 2029, top 5 (B):'); print((t.sort_values('jump30', ascending=False)[['COUNTRY_NAME','C_2028','C_2029','C_2030','C_2031','jump30']].head(5).set_index('COUNTRY_NAME')/1e9).round(2).to_string())
# creditor split for focus countries
parts = {'bilateral':'DT.TDS.BLAT.CD','multilateral':'DT.TDS.MLAT.CD','bonds':'DT.TDS.PBND.CD','comm_banks':'DT.TDS.PCBK.CD','other_private':'DT.TDS.PROP.CD','total_PPG':'DT.TDS.DPPG.CD','IMF':'DT.TDS.DIMF.CD'}
for cc in ['SEN','BTN','PAK','ETH','LBN','MDV','EGY','COM']:
    rows = []
    for k, code in parts.items():
        r = cty[(cty.CC == cc) & (cty.SERIES_CODE == code)]
        if len(r): rows.append(pd.Series(r[yrs].iloc[0].values / 1e9, index=[y[2:] for y in yrs], name=k))
    print('\n==', cc, cty[cty.CC == cc].COUNTRY_NAME.iloc[0], '(US$ B)')
    print(pd.DataFrame(rows).round(2).to_string())
# Senegal and others: debt stock and arrears, rescheduling
for cc in ['SEN','BTN','LBN']:
    r = cty[(cty.CC == cc) & cty.SERIES_CODE.isin(['DT.DOD.DECT.CD','DT.DOD.DPPG.CD','DT.IXA.DLXF.CD','DT.DXR.DPPG.CD','BX.GSR.TOTL.CD','DT.TDS.DECT.EX.ZS'])]
    print('\n', cc); print(r.set_index('SERIES_CODE')[['C_2019','C_2020','C_2021','C_2022','C_2023','C_2024']].to_string(float_format=lambda x: f'{x/1e9:,.2f}B' if abs(x) > 1e6 else f'{x:,.1f}'))
# step-up: scheduled 2026 / actual 2024 among countries with 2024 PPG TDS > $200M, excluding defaulters (actual << scheduled)
s = cty[cty.SERIES_CODE == 'DT.TDS.DPPG.CD'].set_index('CC')
s = s[s.C_2024 > 2e8].copy(); s['step'] = s.C_2026 / s.C_2024
print('\nstep-up 2026 sched / 2024 actual, PPG TDS > $200M in 2024, n=', len(s), 'median', round(s.step.median(), 2))
print(s.sort_values('step', ascending=False)[['COUNTRY_NAME','C_2024','C_2025','C_2026','step']].head(12).to_string(float_format=lambda x: f'{x/1e9:,.2f}B' if abs(x) > 1e6 else f'{x:,.2f}'))
print('share of countries where 2026 sched > 2024 actual:', (s.step > 1).mean().round(3), (s.step > 1).sum())
