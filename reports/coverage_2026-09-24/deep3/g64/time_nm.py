"""Residential PV net-metering installations per utility: EIA-861 2014, 2019 (source files) vs 2024 (warehouse S05).
Denominator: residential customers from each year's Sales_Ult_Cust (Bundled + Delivery rows) for 2014/2019; warehouse S07 for 2024."""
import zipfile, io, pandas as pd, numpy as np, sys
sys.path.insert(0, 'pylib')
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 200)
def num(s): return pd.to_numeric(s.replace('.', np.nan), errors='coerce')
out = {}
z = zipfile.ZipFile('f8612014.zip')
d = pd.read_excel(io.BytesIO(z.read('Net_Metering_2014.xls')), 'Net_Metering_States', header=None, skiprows=3, dtype=str)
d = d[d[0].astype(str).str.fullmatch(r'\d{4}')]
out[2014] = pd.DataFrame({'un': num(d[1]), 'st': d[3], 'res_n': num(d[9]), 'res_mw': num(d[4])})
z = zipfile.ZipFile('f8612019.zip')
d = pd.read_excel(io.BytesIO(z.read('Net_Metering_2019.xlsx')), 'States', header=None, skiprows=3, dtype=str)
d = d[d[0].astype(str).str.fullmatch(r'\d{4}')]
out[2019] = pd.DataFrame({'un': num(d[2]), 'st': d[1], 'res_n': num(d[12]), 'res_mw': num(d[7])})
w = pd.read_csv('out_S05.csv', low_memory=False)
out[2024] = pd.DataFrame({'un': w.UTILITY_NUMBER, 'st': w.STATE, 'res_n': w.RESIDENTIAL_INSTALLATIONS, 'res_mw': w.RESIDENTIAL_CAPACITY_MW})
# sales denominators
def sales(y, f, sheet, hdr):
    z = zipfile.ZipFile(f'f861{y}.zip')
    x = pd.ExcelFile(io.BytesIO(z.read(f)))
    d = pd.read_excel(x, sheet, header=None, skiprows=hdr, dtype=str)
    return d
res = []
for y in (2014, 2019, 2024):
    a = out[y].groupby(['un', 'st'], as_index=False)[['res_n', 'res_mw']].sum()
    a['year'] = y
    res.append(a)
r = pd.concat(res)
# denominators
den = {}
z = zipfile.ZipFile('f8612014.zip'); x = pd.ExcelFile(io.BytesIO(z.read('Sales_Ult_Cust_2014.xls')))
print('2014 sales sheets', x.sheet_names)
d = pd.read_excel(x, x.sheet_names[0], header=None, nrows=4, dtype=str); print(d.iloc[:3, :12].to_string())
z = zipfile.ZipFile('f8612019.zip'); x = pd.ExcelFile(io.BytesIO(z.read('Sales_Ult_Cust_2019.xlsx')))
print('2019 sales sheets', x.sheet_names)
d = pd.read_excel(x, x.sheet_names[0], header=None, nrows=4, dtype=str); print(d.iloc[:3, :14].to_string())
r.to_csv('nm_years.csv', index=False)

def den_from(y, f, rescol):
    z = zipfile.ZipFile(f'f861{y}.zip')
    d = pd.read_excel(io.BytesIO(z.read(f)), 'States', header=None, skiprows=3, dtype=str)
    d = d[d[0].astype(str).str.fullmatch(r'\d{4}')]
    d = d[d[4].isin(['Bundled', 'Delivery'])]
    return pd.DataFrame({'un': num(d[1]), 'st': d[6], 'cust': num(d[rescol])}).groupby(['un', 'st'], as_index=False).cust.sum().assign(year=y)
s24 = pd.read_csv('den_sales.csv').rename(columns={'UTILITY_NUMBER': 'un', 'STATE': 'st', 'RESIDENTIAL_CUSTOMERS': 'cust'})[['un', 'st', 'cust']].assign(year=2024)
D = pd.concat([den_from(2014, 'Sales_Ult_Cust_2014.xls', 11), den_from(2019, 'Sales_Ult_Cust_2019.xlsx', 12), s24])
r = r.merge(D, on=['un', 'st', 'year'], how='right')
r['res_n'] = r.res_n.fillna(0); r['per1k'] = 1000 * r.res_n / r.cust
r.to_csv('nm_years.csv', index=False)
piv = r.pivot_table(index=['un', 'st'], columns='year', values=['per1k', 'res_n', 'cust'])
piv.columns = [f'{a}_{b}' for a, b in piv.columns]
piv = piv.reset_index()
names = pd.read_csv('out_S07.csv', low_memory=False).groupby(['UTILITY_NUMBER', 'STATE']).UTILITY_NAME.first()
piv['name'] = [names.get((u, s), '') for u, s in zip(piv.un, piv.st)]
piv.to_csv('nm_years_wide.csv', index=False)
az = piv[piv.st.isin(['AZ']) & (piv.cust_2024 > 50000)]
print(az[['name', 'cust_2014', 'res_n_2014', 'per1k_2014', 'res_n_2019', 'per1k_2019', 'res_n_2024', 'per1k_2024']].round(1).to_string())
big = piv[(piv.cust_2024 >= 300000) & (piv.cust_2014 > 0)].copy()
big['add_per1k_14_24'] = big.per1k_2024 - big.per1k_2014
print(big.sort_values('per1k_2014', ascending=False)[['st', 'name', 'per1k_2014', 'per1k_2019', 'per1k_2024', 'add_per1k_14_24']].head(25).round(1).to_string())
