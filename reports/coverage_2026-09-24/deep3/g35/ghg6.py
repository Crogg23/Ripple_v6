import pandas as pd, numpy as np, re
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',40); pd.set_option('display.max_rows',200)
fac=pd.read_pickle('fac2.pkl'); x=pd.read_pickle('x2.pkl'); m=pd.read_pickle('m.pkl')
lf=fac[fac.landfill]
u=pd.read_csv('unknown_landfills.csv',index_col=0,dtype={'frs':str})
print('same FRS other GHG id (landfill unknown):', x.loc[u.index,'same_frs_other_ghg_id'].sum())
big=u[u.last_direct>=25000]
print('unknown landfills >=25k:',len(big),' sum last-year t:',round(big.last_direct.sum()),' median:',big.last_direct.median())
print('exit<=2022 (flag held 2+ yrs):', (big.last_rep<=2021).sum(), round(big[big.last_rep<=2021].last_direct.sum()))
# years on unknown list
u['years_flagged']=u['flags'].str.count('U')
print(u[['name','state','years_flagged']].sort_values('years_flagged',ascending=False).to_string())
# PR peer
print('landfills by state=PR ever:', (lf.state=='PR').sum(), ' reporting 2023:', ((lf.state=='PR')&(lf.s23=='REPORTED')).sum(), ' unknown:',((lf.state=='PR')&(lf.s23.str.contains('UNKNOWN'))).sum(), 'valid:',((lf.state=='PR')&(lf.s23.str.contains('VALID'))).sum())
st=lf.groupby('state').agg(n=('s23','size'),unk=('s23',lambda s:s.str.contains('UNKNOWN').sum()))
print(st[st.unk>0])
# time series eyeball
ids=[1004245,1007198,1007197,1006294,1005166]
ts=m[m.FACILITY_ID.isin(ids)].pivot_table(index='YR',columns='FACILITY_ID',values='DIRECT_T',aggfunc='sum').round(0)
print(ts.to_string())
# coal mines subpart FF
fac['ff']=fac.subparts.fillna('').str.contains(r'(^|,)\s*FF\s*(,|$)')
cm=fac[fac.ff]
print('coal mines FF:',len(cm)); print(cm.groupby('s23').agg(n=('peak','size'),big=('last_direct',lambda s:(s>=25000).sum()),med=('last_direct','median')))
print(cm[cm.s23.str.contains('UNKNOWN')][['name','parent','state','last_rep','last_direct']].sort_values('last_direct',ascending=False).to_string())
