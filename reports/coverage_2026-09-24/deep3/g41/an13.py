import json, re, pandas as pd
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 600); pd.set_option('display.max_colwidth', 70)
d = json.load(open('q13.json')); t = pd.DataFrame(d['rows'], columns=[c.lower() for c in d['cols']])
t['U'] = t.feature_name.str.upper()
T = {
 'SQUAW': r'(?:^|[^A-Z])SQUAW(?!K)', 'NIGGER': r'(?:^|[^A-Z])NIGGER', 'NEGRO': r'(?:^|[^A-Z])NEGRO',
 'JAP': r'(?:^|[^A-Z])JAPS?(?:[^A-Z]|$)', 'CHINAMAN': r'(?:^|[^A-Z])CHINAM[AE]N', 'CHINK': r'(?:^|[^A-Z])CHINKS?(?:[^A-Z]|$)',
 'DAGO': r'(?:^|[^A-Z])DAGOS?(?:[^A-Z]|$)', 'DARKEY': r'(?:^|[^A-Z])DARKE?YS?(?:[^A-Z]|$)', 'HALFBREED': r'(?:^|[^A-Z])HALF[- ]?BREED',
 'REDSKIN': r'(?:^|[^A-Z])REDSKIN', 'SAMBO': r'(?:^|[^A-Z])SAMBOS?(?:[^A-Z]|$)', 'INJUN': r'(?:^|[^A-Z])INJUNS?(?:[^A-Z]|$)',
 'WOP': r'(?:^|[^A-Z])WOPS?(?:[^A-Z]|$)', 'GOOK': r'(?:^|[^A-Z])GOOKS?(?:[^A-Z]|$)', 'PICKANINNY': r'(?:^|[^A-Z])PICKANINN'}
for k, p in T.items():
    t[k] = t.U.str.contains(p, regex=True)
t['is_hist'] = t.U.str.contains('HISTORICAL')
off = t[t.feature_name_official == 'Official'].set_index('feature_id')
var = t[t.feature_name_official == 'Variant']
rows = []
for k in T:
    of = off[off[k]]
    vf = set(var[var[k]].feature_id)
    rows.append(dict(term=k, official_features=len(of), official_historical=int(of.is_hist.sum()),
                     official_first_word=int(of.U.str.match(r'^' + T[k].split(')', 1)[1]).sum()),
                     variant_features=len(vf),
                     variant_feats_renamed=sum(1 for f in vf if f in off.index and not off.loc[f, k])))
print(pd.DataFrame(rows).to_string())
# NEGRO official: position and Spanish use
neg = off[off.NEGRO].copy()
neg['first'] = neg.U.str.match(r'^NEGRO')
nw = set(var[var.NIGGER].feature_id)
neg['nword_var'] = neg.index.isin(nw)
print('NEGRO official', len(neg), 'first word', neg['first'].sum(), 'with nword variant', neg.nword_var.sum())
print(neg[~neg['first']][['feature_name', 'source_originator', 'nword_var']].to_string())
t.to_pickle('q13.pkl')
