import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_columns',40)
s=pd.read_csv('K1_star_mo.csv', dtype=str)
m=pd.read_csv('K4_mds_mo.csv', dtype=str)
d=pd.read_csv('K2_def_mo.csv', dtype=str)
d['SURVEY_DATE']=pd.to_datetime(d.SURVEY_DATE)
for c in ['N_ALL','N_ABUSE','N_ABUSE_HJ','N_HARM','N_JKL']: d[c]=d[c].astype(int)
sz=m[(m.Q.str.startswith('I6000'))&(m.R=='Yes')][['CCN','OVERALL_PERCENT']].rename(columns={'CCN':'ccn'})
sz['pct']=pd.to_numeric(sz.OVERALL_PERCENT)
s=s.rename(columns={'CMS_CERTIFICATION_NUMBER_CCN':'ccn'}).merge(sz[['ccn','pct']],on='ccn',how='left')
ctrl={'265735':'2025-08-01','265509':'2025-04-01','265644':'2025-01-25','265649':'2025-01-25','265501':'2025-01-25','265598':'2025-01-25','265668':'2024-10-01','265398':'2024-08-15','265854':'2024-06-01','265856':'2024-06-01','265717':'2024-05-01'}
s['ctrl']=pd.to_datetime(s.ccn.map(ctrl))
s['rel']=s.CHAIN_ID.eq('446')
s['grp']=np.where(s.rel,'Reliant',np.where(s.pct>=40,'other40','rest'))
s['band']=s.pct>=40
agg=d.groupby('CCN').agg(all=('N_ALL','sum'),ab=('N_ABUSE','sum'),abhj=('N_ABUSE_HJ','sum'),jkl=('N_JKL','sum'),surveys=('SURVEY_DATE','nunique')).reset_index().rename(columns={'CCN':'ccn'})
dd=d.merge(s[['ccn','ctrl']],left_on='CCN',right_on='ccn')
post=dd[dd.ctrl.isna() | (dd.SURVEY_DATE>=dd.ctrl)]
aggp=post.groupby('CCN').agg(abhj_post=('N_ABUSE_HJ','sum'),ab_post=('N_ABUSE','sum')).reset_index().rename(columns={'CCN':'ccn'})
s=s.merge(agg,on='ccn',how='left').merge(aggp,on='ccn',how='left').fillna({'all':0,'ab':0,'abhj':0,'jkl':0,'surveys':0,'abhj_post':0,'ab_post':0})
def show(mask,label):
    g=s[mask]
    print(f'{label:32s} homes {len(g):3d} abuse/home {g.ab.mean():.2f} (med {g.ab.median():.0f})  harm-lvl abuse/home {g.abhj.mean():.2f} (med {g.abhj.median():.0f})  homes w/ any {int((g.abhj>0).sum())}  JKL/home {g.jkl.mean():.2f}  survey-dates/home {g.surveys.mean():.1f}')
show(s.rel,'Reliant all 31 (builder S18)')
show(s.rel & s.band,'Reliant in 40%+ band (21)')
show(s.grp.eq('other40'),'other 40%+ (21)')
show(s.grp.eq('rest'),'rest of MO')
g=s[s.rel & s.band]; print('Reliant band harm-lvl abuse/home, post-control only', round(g.abhj_post.mean(),2), 'median', g.abhj_post.median())
g=s[s.rel]; print('Reliant all 31, post-control only', round(g.abhj_post.mean(),2))
print('--- top units, Reliant band harm-level abuse')
g=s[s.rel & s.band].sort_values('abhj',ascending=False)
print(g[['PROVIDER_NAME','abhj','ab','jkl','surveys']].head(6).to_string())
print('Reliant band mean without top 2:', round(g.abhj.iloc[2:].mean(),2), ' without top 4:', round(g.abhj.iloc[4:].mean(),2))
o=s[s.grp.eq('other40')].sort_values('abhj',ascending=False)
print('other top:', o[['PROVIDER_NAME','abhj']].head(4).values.tolist(), 'other without top 2:', round(o.abhj.iloc[2:].mean(),2))
print('harm-lvl abuse per survey-date: Reliant band', round(g.abhj.sum()/g.surveys.sum(),3), 'other40', round(o.abhj.sum()/o.surveys.sum(),3))
print('distribution Reliant band', sorted(g.abhj.astype(int).tolist(), reverse=True))
print('distribution other40   ', sorted(o.abhj.astype(int).tolist(), reverse=True))
for c in ['OVERALL_RATING','HEALTH_INSPECTION_RATING','STAFFING_RATING','QUALITY_MEASURE_RATING']:
    s[c]=pd.to_numeric(s[c])
print('--- star components, 40%+ band (rel=True is Reliant)')
for c in ['OVERALL_RATING','HEALTH_INSPECTION_RATING','STAFFING_RATING','QUALITY_MEASURE_RATING']:
    for r in [True, False]:
        x=s[s.band & (s.rel==r)][c]
        print(f'  {c:26s} rel={r!s:5s} mean {x.mean():.2f}  ones {int((x==1).sum())}/{x.notna().sum()}')
for c in ['REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY','NURSING_CASE_MIX_INDEX','NUMBER_OF_CERTIFIED_BEDS']:
    print(c, s[s.band].groupby('rel')[c].agg(lambda x: round(pd.to_numeric(x).median(),3)).to_dict())
print('PROCESSING_DATE', s.PROCESSING_DATE.unique())
print('--- acquired homes: rating cycle dates vs control date')
a=s[s.ctrl.notna()][['PROVIDER_NAME','ctrl','OVERALL_RATING','HEALTH_INSPECTION_RATING','STAFFING_RATING','RATING_CYCLE_1_STANDARD_SURVEY_HEALTH_DATE','RATING_CYCLE_2_STANDARD_HEALTH_SURVEY_DATE','pct']]
print(a.to_string())
s.to_pickle('mo_joined.pkl')
