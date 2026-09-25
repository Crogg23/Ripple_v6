import pandas as pd, re
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 600); pd.set_option('display.max_colwidth', 80)
t = pd.read_pickle('q13.pkl')
off = t[t.feature_name_official == 'Official'].set_index('feature_id')
var = t[t.feature_name_official == 'Variant']
print('features in extract', t.feature_id.nunique(), 'with official row', off.index.nunique())
# SQUAW official list
print(off[off.SQUAW][['feature_name', 'source_originator', 'publication_date', 'date_created']].to_string())
# classify NEGRO official
SP = r'\b(CERRO|CERRITO|CERRIOT|CERROS|OJO|ARROYO|CA.ON|MONTE|RINCON|LAGUNA|CUCHILLO|EL|LOS|LAS|MAR|TORO|OSO|PUERTO|CABO|QUEBRADA|R.O|BARRIO|COMUNIDAD|RESIDENCIAL)\b|NEGRON'
neg = off[off.NEGRO].copy()
neg['spanish'] = neg.U.str.contains(SP, regex=True)
nw = set(var[var.NIGGER].feature_id)
neg['nword_var'] = neg.index.isin(nw)
neg['yr'] = pd.to_datetime(neg.publication_date).dt.year
print('NEGRO official', len(neg), '| spanish-use', neg.spanish.sum(), '| english-use', (~neg.spanish).sum(),
      '| english historical', (~neg.spanish & neg.is_hist).sum(), '| english current (not historical)', (~neg.spanish & ~neg.is_hist).sum(),
      '| with nword variant', neg.nword_var.sum(), '| spanish with nword', (neg.spanish & neg.nword_var).sum())
print('first-word spanish check:', neg[neg.spanish & neg.U.str.match('^NEGRO')].feature_name.tolist())
eng = neg[~neg.spanish]
print('english official by originator:'); print(eng.source_originator.fillna('(blank)').value_counts().head(8))
print('english official pub year bucket:'); print(pd.cut(eng.yr, [0, 1963, 1981, 1999, 2009, 2019, 2030]).value_counts(dropna=False).sort_index())
print('english: date_created range', eng.date_created.min(), eng.date_created.max(), '| created after 2000:', (pd.to_datetime(eng.date_created) >= '2000-01-01').sum())
# renamed away timelines
def renamed(term_cols):
    vf = set(var[var[term_cols].any(axis=1)].feature_id)
    o = off.loc[[f for f in vf if f in off.index]]
    o = o[~o[term_cols].any(axis=1)] if isinstance(term_cols, list) else o
    return o
for label, cols in [('SQUAW', ['SQUAW']), ('NEGRO or n-word', ['NEGRO', 'NIGGER'])]:
    o = renamed(cols)
    o = o[~o[cols].any(axis=1)]
    yr = pd.to_datetime(o.publication_date).dt.year
    print(label, 'renamed-away features', len(o))
    print(yr.fillna(0).astype(int).value_counts().sort_index().to_string())
# n-word variants: what official now
o = off.loc[[f for f in set(var[var.NIGGER].feature_id) if f in off.index]]
print('nword features', len(o), 'official now NEGRO', o.NEGRO.sum(), 'other', (~o.NEGRO).sum())
neg.to_pickle('neg.pkl')
