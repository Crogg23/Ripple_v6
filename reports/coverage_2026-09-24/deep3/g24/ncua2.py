import pandas as pd
d=pd.read_pickle('ncua.pkl'); nw='NET_WORTH_RATIO_EXCLUDES_CECL_TRANSITION_PROVISION'
d['new']=d.YEAR_OPENED>=2015
print(d.groupby(['band','ISMDI'],observed=True).agg(n=('CHARTER_NUMBER','size'),lt7=(nw,lambda s:(s<7).mean()),roa_neg=('RETURN_ON_AVERAGE_ASSETS',lambda s:(s<0).mean()),med_roa=('RETURN_ON_AVERAGE_ASSETS','median'),mem_g=('MEMBERS_4_QUARTER_GROWTH','median')).round(3).to_string())
print(d.groupby(pd.cut(d.YEAR_OPENED,[0,1960,1990,2010,2019,2026])).agg(n=('CHARTER_NUMBER','size'),mdi=('ISMDI','mean'),lt7=(nw,lambda s:(s<7).mean()),roa_neg=('RETURN_ON_AVERAGE_ASSETS',lambda s:(s<0).mean()),med_assets=('TOTAL_ASSETS','median')).round(3))
print(d[d.YEAR_OPENED>=2019][['CHARTER_NUMBER','CREDIT_UNION_NAME','CITY_MAILING_ADDRESS','STATE_MAILING_ADDRESS','YEAR_OPENED','ISMDI','TOTAL_ASSETS','MEMBERS',nw,'RETURN_ON_AVERAGE_ASSETS']].sort_values('YEAR_OPENED').to_string())
print(d[['TOTAL_ASSETS_4_QUARTER_GROWTH']].describe())
print(d[d.CHARTER_NUMBER.astype(str).isin(['8445','24940','2796','24937'])][['CREDIT_UNION_NAME','TOTAL_ASSETS','TOTAL_ASSETS_4_QUARTER_GROWTH','TOTAL_DEPOSITS','TOTAL_LOANS','TOTAL_DEPOSITS_4_QUARTER_GROWTH','NCUA_REGION','F_INSURED','PEER_GROUP']].to_string())
