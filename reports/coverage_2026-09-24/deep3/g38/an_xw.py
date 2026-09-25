import pandas as pd, numpy as np, re
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 40)
t = pd.read_csv('out_S12.csv', dtype={'FRS': str, 'PARENT_CIK': str})
print('TRI facilities', len(t), 'in crosswalk', t.IN_XW.sum(), 'matched', t.MATCHED_LEGAL_NAME.notna().sum())
print(t[t.MATCHED_LEGAL_NAME.notna()].MATCH_METHOD.value_counts())
STOP = {'INC','CORP','CORPORATION','CO','COMPANY','LLC','LP','THE','OF','USA','US','U','S','A','HOLDINGS','HOLDING','INTERNATIONAL','GROUP','LTD','PLC','NORTH','AMERICA','AMERICAN','INDUSTRIES','PRODUCTS','AND','&'}
def toks(s):
    if not isinstance(s, str): return set()
    return {w for w in re.findall(r'[A-Z0-9]+', s.upper()) if w not in STOP and len(w) > 1}
m = t[t.MATCHED_LEGAL_NAME.notna()].copy()
m['has_tri_parent'] = m.PARENT_STD.notna() & (m.PARENT_STD.str.upper() != 'NA')
def agree(r):
    a = toks(r.PARENT_STD) | toks(r.PARENT_RAW)
    b = toks(r.PARENT_LEGAL_NAME) | toks(r.MATCHED_LEGAL_NAME)
    return len(a & b) > 0
m['agree'] = m.apply(agree, axis=1)
g = m[m.has_tri_parent]
print('matched with TRI parent', len(g), 'agree', g.agree.sum(), round(g.agree.mean(),3))
print(g.groupby('MATCH_METHOD').agree.agg(['size','sum','mean']).round(3))
print('matched, no TRI parent named', (~m.has_tri_parent).sum())
print(g[~g.agree][['NAME','ST','PARENT_STD','MATCHED_LEGAL_NAME','PARENT_LEGAL_NAME','MATCH_METHOD']].head(40).to_string())
# recall: TRI facilities whose own parent is a big name but crosswalk has no match
t['has_tri_parent'] = t.PARENT_STD.notna() & (t.PARENT_STD.str.upper() != 'NA')
un = t[t.MATCHED_LEGAL_NAME.isna() & t.has_tri_parent]
print('TRI facilities naming a parent', t.has_tri_parent.sum(), 'with no crosswalk match', len(un))
print(un.PARENT_STD.value_counts().head(25))
