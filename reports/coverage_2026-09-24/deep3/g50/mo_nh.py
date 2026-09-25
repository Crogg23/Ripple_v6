import pandas as pd, re
r = pd.read_csv('out_S07.csv', dtype=str)
nh = pd.read_csv('out_S08.csv', dtype=str)
print(nh.shape, nh.CMS_CERTIFICATION_NUMBER_CCN.nunique(), nh.PROCESSING_DATE.unique()[:5])
SUF = {'DRIVE':'DR','STREET':'ST','AVENUE':'AVE','ROAD':'RD','HIGHWAY':'HWY','HIGHWAY':'HWY','BOULEVARD':'BLVD','LANE':'LN','COURT':'CT','PLACE':'PL',
       'TERRACE':'TER','PARKWAY':'PKWY','CIRCLE':'CIR','NORTH':'N','SOUTH':'S','EAST':'E','WEST':'W','HWY':'HWY','TRAIL':'TRL','SQUARE':'SQ'}
def norm(a):
    if not isinstance(a,str): return ''
    a = re.sub(r'[^A-Z0-9 ]',' ',a.upper())
    toks = [SUF.get(t,t) for t in a.split()]
    return ' '.join(toks)
def key(a, z):
    n = norm(a); z = (z or '')[:5] if isinstance(z,str) else ''
    toks = n.split()
    if not toks or not toks[0][0].isdigit(): return None
    num = toks[0]
    rest = [t for t in toks[1:] if t not in ('N','S','E','W','NE','NW','SE','SW')]
    word = rest[0] if rest else ''
    return f'{num}|{word}|{z}'
r['key'] = [key(a,z) for a,z in zip(r.ADDRESS, r.ZIP)]
nh['key'] = [key(a,z) for a,z in zip(nh.ADDRESS, nh.ZIP_CODE)]
print('nh keys dup:', nh.key.duplicated().sum(), 'null', nh.key.isna().sum())
r['pid'] = r.REGISTRANT_NAME + '|' + r.DATE_OF_BIRTH
m = r[r.key.notna()].merge(nh[nh.key.notna()][['key','CMS_CERTIFICATION_NUMBER_CCN','PROVIDER_NAME','ADDRESS','CITY']].rename(columns={'ADDRESS':'NH_ADDR','CITY':'NH_CITY'}), on='key', how='inner')
# second field: city agrees
m['city_ok'] = m.CITY.str.upper().str.replace('SAINT','ST').str.strip() == m.NH_CITY.str.upper().str.replace('SAINT','ST').str.strip()
print('matched rows', len(m), 'persons', m.pid.nunique(), 'homes', m.CMS_CERTIFICATION_NUMBER_CCN.nunique(), 'city agrees persons', m[m.city_ok].pid.nunique())
print(m[~m.city_ok][['ADDRESS','CITY','ZIP','NH_ADDR','NH_CITY','PROVIDER_NAME']].drop_duplicates().to_string())
m.to_pickle('mo_nh_match.pkl')
