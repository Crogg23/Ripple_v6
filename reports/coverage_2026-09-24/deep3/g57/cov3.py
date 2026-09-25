import pandas as pd, numpy as np
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 200)
for yr in ['2023', '2024']:
    m = pd.read_csv(f'm6_{yr}.csv', dtype={'naics': str})
    nsz = m.groupby('naics').agg(q=('qemp', 'sum'), e=('ESTABS', 'sum'))
    big = nsz[(nsz.q / nsz.e >= 50)].index
    mb = m[m.naics.isin(big)].copy()
    nat = mb.groupby('naics').agg(q=('qemp', 'sum'), os=('EMP20_OK', 'sum'))
    nat['natcov'] = (nat.os / nat.q).clip(upper=1)
    mb['exp'] = mb.qemp * mb.naics.map(nat.natcov)
    st = mb.groupby('st').agg(obs=('EMP20_OK', 'sum'), exp=('exp', 'sum'), qemp=('qemp', 'sum'), cells=('naics', 'count'))
    st['index'] = st.obs / st.exp
    st['size'] = m.groupby('st').qemp.sum() / m.groupby('st').ESTABS.sum()
    st = st.sort_values('index')
    print(yr, 'big-site industries', len(big), 'national cov', round(nat.os.sum() / nat.q.sum(), 3), 'median state index', round(st['index'].median(), 3))
    print(st.head(10).round(3).to_string()); print(st.tail(3).round(3).to_string())
    rural = ['NM', 'WY', 'MT', 'VT', 'ND', 'SD', 'ID', 'NE', 'AK', 'ME', 'WV', 'IA', 'KS', 'NH', 'OK', 'AR', 'MS']
    print('rural peers', st.loc[[s for s in rural if s in st.index], ['index', 'size', 'qemp']].sort_values('index').round(3).T.to_string())
