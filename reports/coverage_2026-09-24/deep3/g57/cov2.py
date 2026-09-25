import pandas as pd, numpy as np
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 200)
exec(open('cov.py').read().split("print('osha totals'")[0])
q6 = q[(q.AGG == '58') & (q.EMP > 0) & q.st.notna()][['st', 'INDUSTRY_CODE', 'EMP', 'ESTABS', 'PAY']].rename(columns={'INDUSTRY_CODE': 'naics', 'EMP': 'qemp'})
for yr in ['2023', '2024']:
    o6 = o[o.YR == yr][['ST', 'NAICS', 'EMP20_OK', 'SITES20_OK', 'DAFW_OK']].rename(columns={'ST': 'st', 'NAICS': 'naics'})
    m = q6.merge(o6, on=['st', 'naics'], how='left').fillna({'EMP20_OK': 0, 'SITES20_OK': 0, 'DAFW_OK': 0})
    nat = m.groupby('naics').agg(q=('qemp', 'sum'), os=('EMP20_OK', 'sum'))
    nat['natcov'] = (nat.os / nat.q).clip(upper=1)
    m['natcov'] = m.naics.map(nat.natcov)
    m['exp'] = m.qemp * m.natcov
    st = m.groupby('st').agg(obs=('EMP20_OK', 'sum'), exp=('exp', 'sum'), qemp=('qemp', 'sum'))
    st['index'] = st.obs / st.exp
    st = st.sort_values('index')
    print(yr, 'states', len(st), 'median index', round(st['index'].median(), 3))
    print(st.head(10).round(3).to_string()); print(st.tail(4).round(3).to_string())
    m.to_csv(f'm6_{yr}.csv', index=False); nat.to_csv(f'nat_{yr}.csv')
