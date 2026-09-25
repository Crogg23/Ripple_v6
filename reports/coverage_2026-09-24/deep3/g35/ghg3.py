import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',42)
fac=pd.read_pickle('fac.pkl'); m=pd.read_pickle('m.pkl')
c=pd.read_csv('out_S13.csv',dtype={'REG':str}); ec=pd.read_csv('out_S14.csv',dtype={'FRS':str})
print(c.PGM.value_counts().to_dict()); print(c[c.CO2_NAME.notna()].groupby(['PGM','CO2_NAME','CO2_UNIT']).size())
cur=m[(m.YR==2023)&(m.st!='REPORTED')].set_index('FACILITY_ID').st
fac['status2023']=cur
fac['status2023']=fac.status2023.fillna(pd.Series(np.where(fac.last_rep==2023,'REPORTED_2023','GONE_NO_ROW'),index=fac.index))
print(fac.status2023.value_counts())
x=fac[fac.status2023.str.startswith('STOPPED')].copy()
x['exit_yr']=x.last_rep+1
# transfer: same FRS, other facility id reporting in a year >= exit_yr
rep=m[m.st=='REPORTED'][['FACILITY_ID','YR','FRS']].dropna(subset=['FRS'])
frs_last=rep.groupby(['FRS','FACILITY_ID']).YR.max().reset_index()
def transfer(r):
    if pd.isna(r.frs): return False
    o=frs_last[(frs_last.FRS==r.frs)&(frs_last.FACILITY_ID!=r.name)]
    return bool((o.YR>=r.exit_yr).any())
x['same_frs_other_ghg_id']=x.apply(transfer,axis=1)
# other programs after exit
c2=c[c.PGM.isin(['TRIS','CAMDBS','EIS','E-GGRT'])]
def after(r,p):
    if pd.isna(r.frs): return np.nan
    d=c2[(c2.REG==r.frs)&(c2.PGM==p)]
    return d.YR[d.YR>=r.exit_yr].max() if len(d) else np.nan
for p in ['TRIS','CAMDBS','EIS','E-GGRT']:
    x['after_'+p]=x.apply(lambda r: after(r,p),axis=1)
x['still_other']=x[['after_TRIS','after_CAMDBS','after_EIS']].notna().any(axis=1)
# was the facility in those programs at all (denominator: could it hit?)
regs=c2.groupby('REG').PGM.apply(set)
x['in_any_other']=x.frs.map(lambda r: bool(regs.get(r,set()) & {'TRIS','CAMDBS','EIS'}) if pd.notna(r) else False)
x=x.merge(ec.add_prefix('echo_'),left_on='frs',right_on='echo_FRS',how='left').set_index(x.index)
x['big']=x.last_direct>=25000
x.to_pickle('x.pkl')
grp=x.groupby('status2023')
print(grp.agg(n=('last_rep','size'),frs_filled=('frs',lambda s:s.notna().sum()),big_last=('big','sum'),
   med_last=('last_direct','median'),in_other=('in_any_other','sum'),still_other=('still_other','sum'),
   transfer=('same_frs_other_ghg_id','sum'),echo_land=('echo_FRS',lambda s:s.notna().sum()),echo_active=('echo_IS_ACTIVE','sum')))
for st in x.status2023.unique():
    d=x[(x.status2023==st)&x.in_any_other&(x.exit_yr<=2022)]
    print(st,'exit<=2022 & in other programs:',len(d),'still reporting elsewhere after exit:',d.still_other.sum(), round(d.still_other.mean()*100,1),'%')
    d2=d[d.big]; print('   of those big (>=25k last yr):',len(d2),'still elsewhere:',d2.still_other.sum())
