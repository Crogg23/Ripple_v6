import pandas as pd
pd.set_option('display.width',260); pd.set_option('display.max_columns',30)
d=pd.read_csv('out_S03.csv',keep_default_na=False,na_values=[''])
d['st']=d.BOILER_STATUS.str.upper()
coal={'ANT','BIT','LIG','SUB','WC','RC','SGC'}
d['coal']=d.FUELS.fillna('').apply(lambda s: bool(set(s.split(','))&coal))
c=d[(d.st=='OP')&d.coal].copy()
c['codes']=c[['SO2_EX1','SO2_EX2','SO2_EX3']].fillna('').agg(lambda r: set(x for x in r if x),axis=1)
c['fgd']=c.codes.apply(lambda s: 'IF' in s)
c['fgd_or_cfb']=c.codes.apply(lambda s: bool(s & {'IF','CF'}))
p=c.groupby('PLANT_CODE').agg(plant=('PLANT_NAME','first'),state=('STATE','first'),util=('UTILITY_NAME','first'),
   boilers=('BOILER_ID','size'),fgd_boilers=('fgd','sum'),ctl_boilers=('fgd_or_cfb','sum'),mw=('GEN_MW','sum'),
   ret=('RET_YR_MAX','max'),ret_min=('RET_YR_MIN','min'),so2=('SO2_TONS','first'),lbmm=('SO2_LB_MMBTU','first'),
   lbmwh=('SO2_LB_MWH','first'),coal_mwh=('COAL_MWH','first'),net_mwh=('NET_MWH','first'),nerc=('NERC','first'),
   codes=('codes',lambda s: ','.join(sorted(set().union(*s)))),nsr=('NEW_SOURCE_REVIEW',lambda s:''.join(sorted(set(s.fillna('?'))))))
p['group']=p.apply(lambda r: 'all_ctl' if r.ctl_boilers==r.boilers else ('none' if r.ctl_boilers==0 else 'partial'),axis=1)
p['has_ret']=p.ret.notna()
p.to_csv('coal_plants.csv')
print('coal plants OP',len(p), 'with egrid', p.so2.notna().sum())
print(p.groupby('group').agg(plants=('plant','size'),mw=('mw','sum'),so2=('so2','sum'),coal_mwh=('coal_mwh','sum'),med_lbmm=('lbmm','median'),ret_plan=('has_ret','sum')))
tot=p.so2.sum(); print('total so2 these coal plants', tot)
n=p[p.group=='none'].sort_values('so2',ascending=False)
print(n[['plant','state','util','boilers','mw','so2','lbmm','lbmwh','ret','codes','nsr','nerc']].head(40).to_string())
