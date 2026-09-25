import pandas as pd, numpy as np, re
pd.set_option('display.width',280); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',48)
b=pd.read_pickle('pac_big.pkl')
pat=r"\b(POLICE|COPS?|SHERIFFS?|TROOPERS?|LAW ENFORCEMENT|OFFICERS|FIRE ?FIGHTERS?|FIRST RESPONDERS?|VETERANS?|VETS|MILITARY|SOLDIERS?|TROOPS|WOUNDED|INJURED|DISABLED|CANCER|BREAST|LEUKEMIA|AUTISM|ALZHEIMERS?|CHILDRENS?|CHILDREN'S|KIDS|WIDOWS|GOLD STAR|HEROES|BLUE LIVES|BACK THE BLUE)\b"
b['nm']=b.CMTE_NM.fillna('').str.upper()
b['sym']=b.nm.str.contains(pat,regex=True)
b['grp']=np.where(b.COMMITTEE_TYPE.isin(['O','V','W']),'superPAC/hybrid','PAC N/Q')
def summ(x):
    return pd.Series({'cmte_cycles':len(x),'cmtes':x.CMTE_ID.nunique(),'raised_M':x.TOTAL_RECEIPTS.sum()/1e6,'pol_M':x.pol.sum()/1e6,
        'pooled_pol_sh':x.pol.sum()/x.TOTAL_DISBURSEMENTS.sum(),'median_pol_sh':x.pol_sh.median(),'share_under10':(x.pol_sh<0.10).mean(),'n_under10':(x.pol_sh<0.10).sum()})
print(b.groupby(['grp','sym']).apply(summ).round(3).to_string())
# size band peer: same size band
b['band']=pd.cut(b.TOTAL_RECEIPTS,[0,1e6,5e6,1e12],labels=['0.25-1M','1-5M','5M+'])
print(b[b.grp=='superPAC/hybrid'].groupby(['band','sym'],observed=True).apply(summ).round(3).to_string())
print(b.groupby(['cycle','grp','sym']).apply(summ)[['cmtes','raised_M','median_pol_sh','share_under10']].round(3).to_string())
s=b[b.sym]
cols=['CMTE_ID','CMTE_NM','COMMITTEE_TYPE','cycle','tres','CMTE_CITY','CMTE_ST','TOTAL_RECEIPTS','pol','pol_sh','CASH_CLOSE_OF_PERIOD']
print(s.sort_values('TOTAL_RECEIPTS',ascending=False)[cols].round(3).to_string(index=False))
s.to_csv('sympathy_pacs.csv',index=False)
