import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',50)
a=pd.read_pickle('06_icisair_fac_all.pkl'); v=pd.read_pickle('07_icisair_viol_all.pkl'); fa=pd.read_pickle('08_icisair_formal_all.pkl')
om=a[(a.AIR_OPERATING_STATUS_CODE=='OPR')&(a.AIR_POLLUTANT_CLASS_CODE=='MAJ')].copy()
om['sic']=om.SIC_CODES.fillna('').str.split().str[0]
om['hpv_now']=om.CURRENT_HPV.fillna('').str.contains('ddressed')
h=v[v.ENF_RESPONSE_POLICY_CODE=='HPV'].copy()
h['d0']=pd.to_datetime(h.HPV_DAYZERO_DATE,errors='coerce'); h['dr']=pd.to_datetime(h.HPV_RESOLVED_DATE,errors='coerce')
asof=pd.Timestamp('2026-07-31')
g=h.groupby('PGM_SYS_ID').agg(hpv_all=('d0','size'),
  hpv_2020_25=('d0',lambda s:((s>='2020-01-01')&(s<'2026-01-01')).sum()),
  hpv_2015_19=('d0',lambda s:((s>='2015-01-01')&(s<'2020-01-01')).sum()))
op=h[h.dr.isna()&h.d0.notna()].groupby('PGM_SYS_ID').agg(open_n=('d0','size'),open_oldest=('d0','min'))
fa['dt']=pd.to_datetime(fa.SETTLEMENT_ENTERED_DATE,errors='coerce'); fa['pen']=pd.to_numeric(fa.PENALTY_AMOUNT,errors='coerce').fillna(0)
f2=fa[fa.dt>='2020-01-01'].groupby('PGM_SYS_ID').agg(fa_2020=('dt','size'),pen_2020=('pen','sum'),last_fa=('dt','max'))
fall=fa.groupby('PGM_SYS_ID').agg(last_fa_any=('dt','max'))
om=om.merge(g,left_on='PGM_SYS_ID',right_index=True,how='left').merge(op,left_on='PGM_SYS_ID',right_index=True,how='left').merge(f2,left_on='PGM_SYS_ID',right_index=True,how='left').merge(fall,left_on='PGM_SYS_ID',right_index=True,how='left')
for c in ['hpv_all','hpv_2020_25','hpv_2015_19','open_n','fa_2020','pen_2020']: om[c]=om[c].fillna(0)
om['open_yrs']=(asof-om.open_oldest).dt.days/365.25
om['any_2020']=om.hpv_2020_25>0
om['any_1519']=om.hpv_2015_19>0
om['open2y']=om.open_yrs>=2
om.to_pickle('icis_om.pkl')
