import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_columns',30)
r = pd.read_csv('out_S07.csv', dtype=str)
r['pid'] = r.REGISTRANT_NAME + '|' + r.DATE_OF_BIRTH
r['age'] = (pd.Timestamp('2026-09-24') - pd.to_datetime(r.DATE_OF_BIRTH)).dt.days/365.25
nh = pd.read_csv('out_S08.csv', dtype=str)
d = pd.read_csv('out_S09.csv', dtype=str)
m = pd.read_pickle('mo_nh_match.pkl')
# person-level registry
p = r.groupby('pid').agg(age=('age','first'), tier=('TIER','max'), comp=('IS_COMPLIANT','first'), addr=('ADDRESS','first'), n_off=('OFFENSE','nunique'),
                         offenses=('OFFENSE', lambda s: ' / '.join(sorted(set(s))))).reset_index()
spec = r.ADDRESS.str.upper().fillna('').str.contains('INCARC|MOVED|UNKNOWN') | r.ADDRESS.isna()
street_p = r[~spec].pid.unique()
print('persons', len(p), 'with a street address', len(street_p))
mp = m.drop_duplicates('pid')[['pid','CMS_CERTIFICATION_NUMBER_CCN']]
pn = p.merge(mp, on='pid', how='left')
pn['in_nh'] = pn.CMS_CERTIFICATION_NUMBER_CCN.notna()
print('multi-home persons', m.groupby('pid').CMS_CERTIFICATION_NUMBER_CCN.nunique().max())
ps = pn[pn.pid.isin(street_p)]
print(ps.groupby('in_nh').agg(n=('pid','size'), med_age=('age','median'), p25=('age',lambda s: s.quantile(.25)), under60=('age',lambda s:(s<60).mean()), under50=('age',lambda s:(s<50).mean()),
      tier3=('tier',lambda s:(s=='3').mean()), noncomp=('comp',lambda s:(s=='False').mean())))
# offenses of NH registrants
nhp = pn[pn.in_nh]
off = r[r.pid.isin(nhp.pid)].OFFENSE.str.upper()
print('NH registrants with a child-victim offense word:', r[r.pid.isin(nhp.pid) & off.str.contains('CHILD|MINOR|UNDER 1|<1|STATUTORY|INCEST')].pid.nunique())
print(off.value_counts().head(15))
# homes
for c in ['NUMBER_OF_CERTIFIED_BEDS','AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY','OVERALL_RATING','HEALTH_INSPECTION_RATING','STAFFING_RATING','TOTAL_AMOUNT_OF_FINES_IN_DOLLARS','NUMBER_OF_FINES']:
    nh[c] = pd.to_numeric(nh[c], errors='coerce')
cnt = m.groupby('CMS_CERTIFICATION_NUMBER_CCN').pid.nunique().rename('reg')
h = nh.merge(cnt, left_on='CMS_CERTIFICATION_NUMBER_CCN', right_index=True, how='left').fillna({'reg':0})
d2 = d.rename(columns={'CCN':'CMS_CERTIFICATION_NUMBER_CCN'})
for c in ['N_DEF','ABUSE_TAGS','HARM_G_PLUS','ABUSE_HARM','F600','COMPLAINT_DEF']: d2[c]=pd.to_numeric(d2[c])
h = h.merge(d2, on='CMS_CERTIFICATION_NUMBER_CCN', how='left')
h['per100'] = 100*h.reg/h.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY
print('total MO residents/day', h.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY.sum(), 'registrants in NH', h.reg.sum(), 'homes with >=1', (h.reg>0).sum(), '>=3', (h.reg>=3).sum(), '>=5', (h.reg>=5).sum())
top = h.sort_values('reg', ascending=False)[['CMS_CERTIFICATION_NUMBER_CCN','PROVIDER_NAME','CITY','OWNERSHIP_TYPE','CHAIN_NAME','AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY','reg','per100','OVERALL_RATING','ABUSE_ICON','SPECIAL_FOCUS_STATUS','ABUSE_TAGS','HARM_G_PLUS']].head(25)
print(top.to_string())
h['has'] = np.where(h.reg>=3,'3+',np.where(h.reg>0,'1-2','0'))
print(h.groupby('has').agg(homes=('reg','size'), med_res=('AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY','median'), one_star=('OVERALL_RATING',lambda s:(s==1).mean()), med_star=('OVERALL_RATING','median'),
   abuse_icon=('ABUSE_ICON',lambda s:(s=='Y').mean()), sff=('SPECIAL_FOCUS_STATUS',lambda s:s.notna().mean()), forprofit=('OWNERSHIP_TYPE',lambda s:s.str.startswith('For profit').mean()),
   abuse_tags_per=('ABUSE_TAGS','mean'), harm_per=('HARM_G_PLUS','mean'), fines_med=('TOTAL_AMOUNT_OF_FINES_IN_DOLLARS','median')))
h.to_pickle('mo_homes.pkl'); pn.to_pickle('mo_persons.pkl')
print(h.ABUSE_ICON.value_counts(dropna=False), h.SPECIAL_FOCUS_STATUS.value_counts(dropna=False))
