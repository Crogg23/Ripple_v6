import pandas as pd, numpy as np
pd.set_option('display.width',240)
c=pd.read_pickle('oflc_cert_keys.pkl')
IT=c.SOC_CODE.str[:5].isin(['15-11','15-12'])
own=c[(c.own_key!='')&IT]; ven=c[(c.cli_key!='')&(c.own_key!=c.cli_key)&IT]
r=pd.read_csv('client_gap.csv')
print('clients',len(r),'negative gap',(r.gap<0).sum(),'gap < -10%',(r.gap<-0.10).sum(),'median',r.gap.median())
# same client, SOC, state AND wage level
k=['cli','SOC_CODE','WORKSITE_STATE_1','PW_WAGE_LEVEL_1']
o=own.assign(cli=own.own_key); v=ven.assign(cli=ven.cli_key)
o=o[o.PW_WAGE_LEVEL_1!='']; v=v[v.PW_WAGE_LEVEL_1!='']
go=o.groupby(k).w_ann.agg(own_med='median',own_n='size'); gv=v.groupby(k).w_ann.agg(ven_med='median',ven_n='size')
j=go.join(gv,how='inner'); j=j[(j.own_n>=5)&(j.ven_n>=5)].reset_index()
j['gap']=j.ven_med/j.own_med-1
print('matched cells',len(j),'clients',j.cli.nunique(),'vendor rows',j.ven_n.sum(),'own rows',j.own_n.sum())
print('cell-level: median gap',round(j.gap.median(),3),'weighted',round(np.average(j.gap,weights=j.ven_n),3),'share of cells vendor lower',round((j.gap<0).mean(),3))
print(j.groupby('PW_WAGE_LEVEL_1').apply(lambda g: pd.Series(dict(cells=len(g),ven_n=g.ven_n.sum(),med_gap=g.gap.median(),w_gap=np.average(g.gap,weights=g.ven_n)))).round(3).to_string())
pc=j.groupby('cli').apply(lambda g: pd.Series(dict(cells=len(g),ven_n=g.ven_n.sum(),w_gap=np.average(g.gap,weights=g.ven_n)))).sort_values('ven_n',ascending=False)
print(pc.round(3).head(25).to_string()); print('clients with lower vendor pay at same level:',(pc.w_gap<0).sum(),'of',len(pc),'median client',round(pc.w_gap.median(),3))
# biggest single cells
print(j.sort_values('ven_n',ascending=False).head(12).round(3).to_string(index=False))
# at-floor share: offered == prevailing wage
c['atfloor']=(c.w==c.pw)&(c.WAGE_UNIT_OF_PAY_1==c.PW_UNIT_OF_PAY_1)
print('offered exactly = prevailing: vendor',round(ven.index.map(c.atfloor).to_series().mean(),3),'own',round(own.index.map(c.atfloor).to_series().mean(),3))
j.to_csv('client_gap_samelevel.csv',index=False)
