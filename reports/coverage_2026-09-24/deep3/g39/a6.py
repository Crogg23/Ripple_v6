import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_rows',200); pd.set_option('display.max_colwidth',42)
el=pd.read_pickle('el.pkl'); pf=pd.read_pickle('pf.pkl')
fac=pd.read_csv('q06.csv',dtype=str)
fce=pd.read_csv('q12.csv',dtype={'PGM_SYS_ID':str}).set_index('PGM_SYS_ID')
fi=fac.set_index('PGM_SYS_ID')
# registry-level enforcement: sum over all PGM_SYS_IDs sharing a REGISTRY_ID
v=pd.read_csv('q09.csv',dtype=str); v['d']=pd.to_datetime(v.EARLIEST_FRV_DETERM_DATE.fillna(v.HPV_DAYZERO_DATE),errors='coerce')
fa=pd.read_csv('q10.csv',dtype={'PGM_SYS_ID':str}); fa['d']=pd.to_datetime(fa.SETTLEMENT_ENTERED_DATE,errors='coerce')
ia=pd.read_csv('q11.csv',dtype=str); ia['d']=pd.to_datetime(ia.ACHIEVED_DATE,errors='coerce')
reg=fi.REGISTRY_ID
def byreg(df,win=True):
    d=df[(df.d>='2016-01-01')&(df.d<'2026-01-01')] if win else df
    d=d.assign(reg=reg.reindex(d.PGM_SYS_ID).values)
    return d.groupby('reg').size()
vr=byreg(v); far=byreg(fa); iar=byreg(ia)
far_all=byreg(fa,False); iar_all=byreg(ia,False); vr_all=byreg(v,False)
el['reg']=reg.reindex(el.index).values
print('reg null among el', el.reg.isna().sum())
el['enf_reg']=(vr.reindex(el.reg).fillna(0).values+far.reindex(el.reg).fillna(0).values+iar.reindex(el.reg).fillna(0).values)
el['enf_reg_ever']=(vr_all.reindex(el.reg).fillna(0).values+far_all.reindex(el.reg).fillna(0).values+iar_all.reindex(el.reg).fillna(0).values)
el['lastfce']=pd.to_datetime(fce.LAST_FCE.reindex(el.index),errors='coerce')
el['fce_16_25']=fce.N_FCE_16_25.reindex(el.index).fillna(0)
ey=el[el.grp=='every_year_Y']
print('every-year deviators, no enforcement by PGM id:', (~ey.any_enf).sum(), ' by registry id (2016-25):', (ey.enf_reg==0).sum(), ' ever:', (ey.enf_reg_ever==0).sum())
s=ey.groupby('state').agg(n=('yrs','size'),no_enf_pgm=('any_enf',lambda s:(~s).sum()),no_enf_reg=('enf_reg',lambda s:(s==0).sum()),no_enf_ever=('enf_reg_ever',lambda s:(s==0).sum()))
s=s[s.n>=10]; s['pct_reg']=(100*s.no_enf_reg/s.n).round(0)
print(s.sort_values('pct_reg',ascending=False).to_string())
# data-flow check: informal and formal actions and violations per operating major, 2016-2025, TX vs LA vs others
maj=fac[(fac.AIR_POLLUTANT_CLASS_CODE=='MAJ')&(fac.AIR_OPERATING_STATUS_CODE=='OPR')]
cnt=maj.groupby('STATE').size().rename('majors')
w=lambda df: df[(df.d>='2016-01-01')&(df.d<'2026-01-01')].assign(st=lambda x: fi.STATE.reindex(x.PGM_SYS_ID).values).groupby('st').size()
fl=pd.concat([cnt, w(ia).rename('informal'), w(fa).rename('formal'), w(v).rename('viol')],axis=1).fillna(0)
for c in ['informal','formal','viol']: fl[c+'_per_major']=(fl[c]/fl.majors).round(2)
print(fl.loc[['TX','LA','CA','OH','IL','PA','FL','VA','MA','WI','IA','SC','NJ','AL','IN']].to_string())
print('median state per major', fl[fl.majors>=50][['informal_per_major','formal_per_major','viol_per_major']].median().to_dict())
tx=ey[(ey.state=='TX')&(ey.enf_reg==0)]
print(len(tx))
print(tx[['name','city','naics','cls','status','yrs','yyrs','hpv_now','fce_16_25','lastfce','enf_reg_ever']].sort_values('yrs',ascending=False).to_string())
el.to_pickle('el2.pkl')
