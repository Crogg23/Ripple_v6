import pandas as pd, numpy as np
d=pd.read_csv('out_S10.csv')
print(d.shape, 'foicu land', d.F_CU.notna().sum())
nw='NET_WORTH_RATIO_EXCLUDES_CECL_TRANSITION_PROVISION'
d['band']=pd.cut(d.TOTAL_ASSETS,[0,10e6,50e6,100e6,500e6,1e9,10e9,1e12],labels=['<10M','10-50M','50-100M','100-500M','500M-1B','1-10B','10B+'])
print(d.groupby('band',observed=True).agg(n=('CHARTER_NUMBER','size'),lt7=(nw,lambda s:(s<7).sum()),lt6=(nw,lambda s:(s<6).sum()),med_nw=(nw,'median'),roa_neg=('RETURN_ON_AVERAGE_ASSETS',lambda s:(s<0).mean()), licu=('LOW_INCOME_DESIGNATION',lambda s:(s=='Yes').mean()), assets=('TOTAL_ASSETS','sum')).round(3).to_string())
lic=d[d.LOW_INCOME_DESIGNATION=='Yes']
print('LICU share of assets', round(lic.TOTAL_ASSETS.sum()/d.TOTAL_ASSETS.sum(),3), 'of CUs', round(len(lic)/len(d),3), 'of members', round(lic.MEMBERS.sum()/d.MEMBERS.sum(),3))
print('10B+ LICU:'); print(d[d.TOTAL_ASSETS>=10e9][['CREDIT_UNION_NAME','STATE_MAILING_ADDRESS','TOTAL_ASSETS','MEMBERS','LOW_INCOME_DESIGNATION']].sort_values('TOTAL_ASSETS',ascending=False).to_string())
cols=['CHARTER_NUMBER','CREDIT_UNION_NAME','CITY_MAILING_ADDRESS','STATE_MAILING_ADDRESS','CREDIT_UNION_TYPE','LOW_INCOME_DESIGNATION','TOTAL_ASSETS','MEMBERS',nw,'RETURN_ON_AVERAGE_ASSETS','LOAN_TO_SHARE_RATIO','TOTAL_LOANS_4_QUARTER_GROWTH','MEMBERS_4_QUARTER_GROWTH','NET_WORTH_4_QUARTER_GROWTH_EXCLUDES_CECL_TRANSITION_PROVISION','YEAR_OPENED','ISMDI']
print(d[d[nw]<6].sort_values(nw)[cols].to_string())
print('nw==100:', (d[nw]>=99.9).sum()); print(d[d[nw]>=85][cols].to_string())
# MDI
print(d.groupby('ISMDI').agg(n=('CHARTER_NUMBER','size'),lt7=(nw,lambda s:(s<7).mean()),med_nw=(nw,'median'),roa_neg=('RETURN_ON_AVERAGE_ASSETS',lambda s:(s<0).mean())).round(3))
d.to_pickle('ncua.pkl')
