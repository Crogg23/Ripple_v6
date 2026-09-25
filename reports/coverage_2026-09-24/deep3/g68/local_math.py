"""g68 local math: reproduces every number in g68.md from the S*.pkl pulls. Run clients.py and clients2.py first for OFLC."""
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np
L=lambda f: pd.read_pickle(f).rename(columns=str.lower)
# EOIR
s6=L('S06_eoir_profile_by_custody.pkl'); print('EOIR rows',s6.n.sum(),'odd-field rows',s6.odd_fields.sum(),'lpr null',s6.lpr_null.sum(),'lpr true',s6.lpr_true.sum(),'zip00000',s6.zip0.sum())
s11=L('S11_eoir_fixed_cohort_entered_by_2021_by_nationality.pkl'); t=s11.drop(columns='nationality').sum()
print('fixed cohort pool',t.pool_entered_by_2021,{y:(t['d'+y],t['p'+y]) for y in ['23','24','25','26']},'x',round(t.d26/t.d24,2),'20y',t.d24_20y,t.d26_20y)
b=s11[(s11.pool_entered_by_2021>=15000)&(s11.d24>=30)].assign(x=lambda g:g.d26/g.d24)
print('nationalities',len(b),'median x',round(b.x.median(),2),'min',b.loc[b.x.idxmin(),['nationality','d24','d26']].tolist())
print('VE',s11[s11.nationality=='VE'][['pool_entered_by_2021','d23','d24','d25','d26']].values.tolist())
s12=L('S12_eoir_detained_date_fill_by_case_id_band.pkl'); print((s12.dr_det_filled/s12.dr).round(3).tolist()); print((s12.dr_entry_filled/s12.dr).round(3).tolist())
s7=L('S07_eoir_detained_month_by_residence.pkl'); s7['mon']=pd.to_datetime(s7.mon)
jm=s7[s7.mon.dt.month<=5].pivot_table(index=s7.mon.dt.year,columns='bucket',values='n',aggfunc='sum'); print(jm.loc[2023:].to_string())
# ICE second source
i=L('S13_ice_stints_corroborate_by_month.pkl'); i['mon']=pd.to_datetime(i.mon)
print(i[i.mon.dt.month<=2].groupby(i.mon.dt.year)[['stays','stays_entry_parsed','stays_entered_by_2021','stays_entered_pre2006','by2021_other_violator','by2021_convicted']].sum().to_string())
# OHSS
m=pd.read_pickle('ohss_months.pkl')
g=m[(m.SOURCE_SHEET_NAME=='ICE ERO R&R by Arrest Loc')&(m.thru==202411)&(m.MONTH=='Total')][['FY','TOTAL_n','INTERIOR_n']]
print((g.assign(sh=g.INTERIOR_n/g.TOTAL_n)).round(3).to_string(index=False))
