import pandas as pd, numpy as np
from st import binom_sf, fisher, perm_mean_diff
pd.set_option('display.width',250); pd.set_option('display.max_columns',30)
h = pd.read_pickle('mo_homes.pkl'); pn = pd.read_pickle('mo_persons.pkl')
h['chain'] = h.CHAIN_NAME.fillna('(independent)')
res = h.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY.fillna(0)
tot_res = res.sum(); tot_reg = h.reg.sum()
c = h.groupby('chain').agg(homes=('reg','size'), homes_w=('reg',lambda s:(s>0).sum()), reg=('reg','sum'), residents=('AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY','sum'),
    one_star=('OVERALL_RATING',lambda s:(s==1).sum())).sort_values('reg',ascending=False)
c['res_share']=c.residents/tot_res; c['reg_share']=c.reg/tot_reg; c['per1000']=1000*c.reg/c.residents
print(c.head(12).to_string())
print('median chain-or-indep home registrants among homes with >=1:', h[h.reg>0].reg.median(), ' median home overall:', h.reg.median())
print('top4 homes share', h.reg.nlargest(4).sum()/tot_reg, 'top10', h.reg.nlargest(10).sum()/tot_reg)
# Reliant test: binomial on residents share
rel = c.loc['RELIANT CARE MANAGEMENT']
print('Reliant: reg', rel.reg, 'of', tot_reg, 'expected at resident share', rel.res_share*tot_reg, 'p', binom_sf(int(rel.reg), int(tot_reg), rel.res_share))
# excluding top 4 homes
ex = h[~h.CMS_CERTIFICATION_NUMBER_CCN.isin(h.nlargest(4,'reg').CMS_CERTIFICATION_NUMBER_CCN)]
er = ex[ex.chain=='RELIANT CARE MANAGEMENT']
print('Reliant w/o top4 homes: reg', er.reg.sum(), 'of', ex.reg.sum(), 'res share', er.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY.sum()/ex.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY.sum())
print('Reliant homes list:'); print(h[h.chain=='RELIANT CARE MANAGEMENT'][['PROVIDER_NAME','CITY','AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY','reg','OVERALL_RATING','ABUSE_ICON','ABUSE_TAGS','HARM_G_PLUS']].sort_values('reg',ascending=False).to_string())
# peer: size band
def summ(df,label):
    g = df.groupby(np.where(df.reg>=3,'3+',np.where(df.reg>0,'1-2','0')))
    out = g.agg(homes=('reg','size'), med_res=('AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY','median'), one_star=('OVERALL_RATING',lambda s:(s==1).mean()), 
        abuse_icon=('ABUSE_ICON',lambda s:(s=='Y').mean()), abuse_tags=('ABUSE_TAGS','mean'), abuse_tags_med=('ABUSE_TAGS','median'), harm=('HARM_G_PLUS','mean'), harm_med=('HARM_G_PLUS','median'))
    print('--',label); print(out.to_string())
summ(h[(h.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY>=60)&(h.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY<=240)], 'size 60-240 residents')
summ(h[h.OVERALL_RATING==1], 'one-star homes only')
summ(h[h.chain=='RELIANT CARE MANAGEMENT'], 'Reliant only')
summ(h[(h.chain!='RELIANT CARE MANAGEMENT')&h.OWNERSHIP_TYPE.str.startswith('For profit')], 'for-profit, not Reliant')
# abuse tags per 100 residents
h['abuse_per100'] = 100*h.ABUSE_TAGS/h.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY
print(h.groupby(h.reg>=3).abuse_per100.median())
x = h[(h.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY>=60)&(h.AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY<=240)]
print('perm abuse tags 3+ vs 0 (size band):', perm_mean_diff(x[x.reg>=3].ABUSE_TAGS.fillna(0), x[x.reg==0].ABUSE_TAGS.fillna(0)))
t = pd.crosstab(h.reg>=3, h.ABUSE_ICON=='Y'); print(t, fisher(*t.values.ravel()))
# noncompliant in NH
nc = pn[pn.in_nh & (pn.comp=='False')]
print('noncompliant NH persons', len(nc)); print(nc.merge(h[['CMS_CERTIFICATION_NUMBER_CCN','PROVIDER_NAME']],on='CMS_CERTIFICATION_NUMBER_CCN').PROVIDER_NAME.value_counts().head(8))
# ages at NH: under 50 count; residents younger than 60
nhp = pn[pn.in_nh]
print('NH registrants under 60:', (nhp.age<60).sum(), 'under 50:', (nhp.age<50).sum(), 'tier3:', (nhp.tier=='3').sum())
