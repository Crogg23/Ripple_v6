"""Residential customers enrolled in time-varying rates: EIA-861 2014, 2019 source files vs 2024 warehouse (S04).
Share uses each year's Sales_Ult_Cust residential customers (Bundled + Delivery), same as time_nm.py."""
import zipfile, io, pandas as pd, numpy as np, sys
sys.path.insert(0, 'pylib')
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 200)
def num(s): return pd.to_numeric(s.replace('.', np.nan), errors='coerce')
rows = []
for y, f, un, st, res in [(2014, 'Dynamic_Pricing2014.xls', 1, 3, 4), (2019, 'Dynamic_Pricing_2019.xlsx', 1, 4, 6)]:
    z = zipfile.ZipFile(f'f861{y}.zip')
    d = pd.read_excel(io.BytesIO(z.read(f)), 'Dynamic Pricing_States', header=None, skiprows=3, dtype=str)
    d = d[d[0].astype(str).str.fullmatch(r'\d{4}')]
    rows.append(pd.DataFrame({'un': num(d[un]), 'st': d[st], 'enr': num(d[res]), 'year': y}))
w = pd.read_csv('out_S04.csv', low_memory=False)
rows.append(pd.DataFrame({'un': w.UTILITY_NUMBER, 'st': w.STATE, 'enr': w.RESIDENTIAL_CUSTOMERS_ENROLLED, 'year': 2024}))
e = pd.concat(rows).groupby(['un', 'st', 'year'], as_index=False).enr.sum()
D = pd.read_csv('nm_years.csv')[['un', 'st', 'year', 'cust']]
e = D.merge(e, on=['un', 'st', 'year'], how='left')
e['share'] = e.enr / e.cust
p = e.pivot_table(index=['un', 'st'], columns='year', values=['enr', 'share', 'cust'])
p.columns = [f'{a}_{b}' for a, b in p.columns]; p = p.reset_index()
names = pd.read_csv('out_S07.csv', low_memory=False).groupby(['UTILITY_NUMBER', 'STATE']).UTILITY_NAME.first()
p['name'] = [names.get((u, s), '') for u, s in zip(p.un, p.st)]
p.to_csv('dp_years_wide.csv', index=False)
sel = p[(p.cust_2024 >= 250000)].copy()
sel['jump'] = sel.share_2024 - sel.share_2019
cols = ['st', 'name', 'cust_2024', 'enr_2014', 'share_2014', 'enr_2019', 'share_2019', 'enr_2024', 'share_2024']
print(sel[sel.st.isin(['CA', 'OK', 'MO', 'MI', 'MD', 'DE', 'CO', 'AZ'])][cols].round(3).to_string())
print('\nbiggest drops 2019->2024 (share points), big utilities:')
print(sel.sort_values('jump')[cols].head(12).round(3).to_string())
