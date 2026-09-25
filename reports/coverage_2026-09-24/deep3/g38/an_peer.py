import pandas as pd, numpy as np
pd.set_option('display.width', 260); pd.set_option('display.max_columns', 30); pd.set_option('display.max_colwidth', 36)
t = pd.read_pickle('tri_aqs_pop.pkl')
t['popbin'] = pd.qcut(t.pop3mi.rank(method='first'), 10, labels=False)
carc = t[t.CARC_AIR_LBS > 0].copy()
carc['rank'] = carc.CARC_AIR_LBS.rank(ascending=False)
carc['top100'] = carc['rank'] <= 100
print('pop decile edges', t.groupby('popbin').pop3mi.agg(['min','max']).T.round(0).to_string())
# peer: within population decile, top100 vs rest of carc emitters and vs all TRI
rows = []
for b, g in t.groupby('popbin'):
    c = carc[carc.popbin == b]
    tp = c[c.top100]
    rows.append(dict(bin=b, n_all=len(g), med_all=g.mi_2023.median(), gt10_all=(g.mi_2023>10).mean(), n_top=len(tp), med_top=tp.mi_2023.median() if len(tp) else np.nan, gt10_top=(tp.mi_2023>10).mean() if len(tp) else np.nan))
print(pd.DataFrame(rows).round(2).to_string())
# pooled expected: for each top100 plant, share of same-decile TRI plants farther than 10mi
exp = t.groupby('popbin').apply(lambda g: (g.mi_2023>10).mean())
tp = carc[carc.top100]
print('top100 >10mi actual', (tp.mi_2023>10).sum(), 'expected from pop-decile peers', round(exp.loc[tp.popbin].sum(),1))
print('top100 >20mi actual', (tp.mi_2023>20).sum(), 'expected', round(t.groupby('popbin').apply(lambda g: (g.mi_2023>20).mean()).loc[tp.popbin].sum(),1))
# same-state peers: share of same-state TRI plants > 10mi
st = t.groupby('ST').apply(lambda g: (g.mi_2023>10).mean())
print('top100 expected by state', round(st.loc[tp.ST].sum(),1))
# sector peers
sec = t.groupby('SECTOR').apply(lambda g: (g.mi_2023>10).mean())
print('top100 expected by sector', round(sec.loc[tp.SECTOR].sum(),1))
print(tp.SECTOR.value_counts().head(8))
print(tp.TOP_CARC.value_counts().head(8))
# people near top100 with no monitor within 10mi
far = tp[tp.mi_2023 > 10].sort_values('pop3mi', ascending=False)
print('top100 far plants', len(far), 'people within 3mi total', int(far.pop3mi.sum()), 'median', far.pop3mi.median())
print(far[['NAME','CITY','ST','SECTOR','CARC_AIR_LBS','TOP_CARC','mi_2023','pop3mi','mi_ever','ever_closed']].to_string())
