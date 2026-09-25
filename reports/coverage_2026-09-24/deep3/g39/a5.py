import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_columns',40); pd.set_option('display.max_rows',200)
t=pd.read_pickle('t3.pkl')
fac=pd.read_csv('q06.csv',dtype=str).set_index('PGM_SYS_ID')
w=t[(t.yr>=2016)&(t.yr<=2025)&t.FACILITY_RPT_DEVIATION_FLAG.notna()]
fy=w.groupby(['PGM_SYS_ID','yr']).FACILITY_RPT_DEVIATION_FLAG.apply(lambda s:(s=='Y').any()).rename('y').reset_index()
pf=fy.groupby('PGM_SYS_ID').agg(yrs=('yr','nunique'),yyrs=('y','sum'))
pf['state']=fac.STATE.reindex(pf.index)
pf['name']=fac.FACILITY_NAME.reindex(pf.index); pf['city']=fac.CITY.reindex(pf.index)
pf['naics']=fac.NAICS_CODES.reindex(pf.index); pf['cls']=fac.AIR_POLLUTANT_CLASS_CODE.reindex(pf.index); pf['status']=fac.AIR_OPERATING_STATUS_CODE.reindex(pf.index)
pf['hpv_now']=fac.CURRENT_HPV.reindex(pf.index)
# enforcement 2016-2025
v=pd.read_csv('q09.csv',dtype=str)
v['d']=pd.to_datetime(v.EARLIEST_FRV_DETERM_DATE.fillna(v.HPV_DAYZERO_DATE),errors='coerce')
v=v[(v.d>='2016-01-01')&(v.d<'2026-01-01')]
fa=pd.read_csv('q10.csv',dtype={'PGM_SYS_ID':str})
fa['d']=pd.to_datetime(fa.SETTLEMENT_ENTERED_DATE,errors='coerce')
fa=fa[(fa.d>='2016-01-01')&(fa.d<'2026-01-01')]
ia=pd.read_csv('q11.csv',dtype=str)
ia['d']=pd.to_datetime(ia.ACHIEVED_DATE,errors='coerce')
ia=ia[(ia.d>='2016-01-01')&(ia.d<'2026-01-01')]
pf['viol']=v.groupby('PGM_SYS_ID').size().reindex(pf.index).fillna(0)
pf['hpv']=v[v.ENF_RESPONSE_POLICY_CODE=='HPV'].groupby('PGM_SYS_ID').size().reindex(pf.index).fillna(0)
pf['formal']=fa.groupby('PGM_SYS_ID').size().reindex(pf.index).fillna(0)
pf['pen']=fa.groupby('PGM_SYS_ID').PENALTY_AMOUNT.sum().reindex(pf.index).fillna(0)
pf['informal']=ia.groupby('PGM_SYS_ID').size().reindex(pf.index).fillna(0)
pf['any_enf']=(pf.viol+pf.formal+pf.informal)>0
el=pf[pf.yrs>=8]
el['grp']=np.where(el.yyrs==el.yrs,'every_year_Y',np.where(el.yyrs==0,'never_Y','mixed'))
print('facilities with a flagged cert in 8+ of 10 years:', len(el)); print(el.grp.value_counts())
g=el.groupby('grp').agg(n=('viol','size'),any_viol=('viol',lambda s:(s>0).mean()),any_hpv=('hpv',lambda s:(s>0).mean()),any_formal=('formal',lambda s:(s>0).mean()),any_pen=('pen',lambda s:(s>0).mean()),any_inf=('informal',lambda s:(s>0).mean()),no_enf=('any_enf',lambda s:(~s).mean()),med_pen=('pen','median'))
print(g.round(3))
st=el.groupby(['state','grp']).agg(n=('viol','size'),no_enf=('any_enf',lambda s:(~s).mean()),any_formal=('formal',lambda s:(s>0).mean())).unstack('grp')
st=st[st[('n','every_year_Y')].fillna(0)>=15]
print(st.round(2).to_string())
pf.to_pickle('pf.pkl'); el.to_pickle('el.pkl')
