import pandas as pd, numpy as np, warnings
warnings.filterwarnings('ignore')
pd.set_option('display.width',280); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',45)
b=pd.read_pickle('pac_big.pkl')
pat=r"\b(POLICE|COPS?|SHERIFFS?|TROOPERS?|LAW ENFORCEMENT|OFFICERS|FIRE ?FIGHTERS?|FIRST RESPONDERS?|VETERANS?|VETS|MILITARY|SOLDIERS?|TROOPS|WOUNDED|INJURED|DISABLED|CANCER|BREAST|LEUKEMIA|AUTISM|ALZHEIMERS?|CHILDRENS?|CHILDREN'S|KIDS|WIDOWS|GOLD STAR|HEROES|BLUE LIVES|BACK THE BLUE)\b"
b['sym']=b.CMTE_NM.fillna('').str.upper().str.contains(pat,regex=True)
sp=b[b.COMMITTEE_TYPE.isin(['O','V','W'])].copy()
ie=pd.read_pickle('out_S14.pkl'); ie['cycle']=pd.to_numeric(ie.CYCLE_FILE,errors='coerce'); ie['IE_AMT']=pd.to_numeric(ie.IE_AMT,errors='coerce')
ie=ie.groupby(['SPE_ID','cycle']).IE_AMT.sum().rename('schedE').reset_index()
sp=sp.merge(ie,left_on=['CMTE_ID','cycle'],right_on=['SPE_ID','cycle'],how='left')
sp['schedE']=sp.schedE.fillna(0)
c2=pd.read_pickle('out_S15.pkl'); c2['cycle']=pd.to_numeric(c2.CYCLE,errors='coerce'); c2['AMT']=pd.to_numeric(c2.AMT,errors='coerce')
c2p=c2.pivot_table(index=['CMTE_ID','cycle'],columns='TRANSACTION_TP',values='AMT',aggfunc='sum').fillna(0).reset_index()
c2p['pas2_contrib']=c2p.get('24K',0)+c2p.get('24Z',0)+c2p.get('24C',0)
c2p['pas2_ie']=c2p.get('24E',0)+c2p.get('24A',0)
sp=sp.merge(c2p[['CMTE_ID','cycle','pas2_contrib','pas2_ie']],on=['CMTE_ID','cycle'],how='left').fillna({'pas2_contrib':0,'pas2_ie':0})
sp['alt_pol']=np.maximum(sp.INDEPENDENT_EXPENDITURES.fillna(0),np.maximum(sp.schedE,sp.pas2_ie))+np.maximum(sp.CONTRIBUTIONS_TO_OTHER_COMMITTEES.fillna(0),sp.pas2_contrib)+sp.TRANSFERS_TO_AFFILIATES.fillna(0)
sp['alt_sh']=sp.alt_pol/sp.TOTAL_DISBURSEMENTS
for grp,x in sp.groupby('sym'):
    print('sym' if grp else 'others', 'rows', len(x), 'webk IE $M', round(x.INDEPENDENT_EXPENDITURES.sum()/1e6,2), 'schedE $M', round(x.schedE.sum()/1e6,2), 'pas2 IE $M', round(x.pas2_ie.sum()/1e6,2),
          'webk contrib $M', round(x.CONTRIBUTIONS_TO_OTHER_COMMITTEES.sum()/1e6,2), 'pas2 contrib $M', round(x.pas2_contrib.sum()/1e6,2),
          '| median share webk', round(x.pol_sh.median(),3), 'median share max-of-sources', round(x.alt_sh.median(),3), 'pooled max-of-sources', round(x.alt_pol.sum()/x.TOTAL_DISBURSEMENTS.sum(),3))
s=sp[sp.sym]
cl=s.groupby('CMTE_ID').agg(nm=('CMTE_NM','first'),rec=('TOTAL_RECEIPTS','sum'),disb=('TOTAL_DISBURSEMENTS','sum'),alt=('alt_pol','sum'),webk=('pol','sum'))
cl['alt_sh']=cl.alt/cl.disb
o=sp[~sp.sym].groupby('CMTE_ID').agg(disb=('TOTAL_DISBURSEMENTS','sum'),alt=('alt_pol','sum'))
print('committee-level max-of-sources: sym median', round(cl.alt_sh.median(),3), 'others median', round((o.alt/o.disb).median(),3), '| sym under 10%', (cl.alt_sh<0.1).sum(), 'of', len(cl))
print('sym pooled max-of-sources $M', round(cl.alt.sum()/1e6,2), 'of disb', round(cl.disb.sum()/1e6,2))
# where webk and schedE disagree most for sym
s2=s.assign(diff=s.schedE-s.INDEPENDENT_EXPENDITURES.fillna(0)).sort_values('diff',ascending=False)
print(s2[['CMTE_ID','CMTE_NM','cycle','INDEPENDENT_EXPENDITURES','schedE','pas2_ie','CONTRIBUTIONS_TO_OTHER_COMMITTEES','pas2_contrib']].head(8).round(0).to_string(index=False))
# multi-cycle: does the share rise?
mc=s.sort_values('cycle').groupby('CMTE_ID').filter(lambda x:len(x)>=2).groupby('CMTE_ID').agg(first=('alt_sh','first'),last=('alt_sh','last'))
print('multi-cycle sym PACs', len(mc), 'median first-cycle', round(mc['first'].median(),3), 'median latest-cycle', round(mc['last'].median(),3), 'latest over 30%', (mc['last']>0.3).sum())
sp.to_pickle('sp_verified.pkl')
# donor profile
dn=pd.read_pickle('out_S16.pkl')
for c in ['DONORS','RETIRED_DONORS','GIFTS','AMT','DONORS_10PLUS','AMT_10PLUS','MED_DONOR_TOTAL','AMT_RETIRED']: dn[c]=pd.to_numeric(dn[c],errors='coerce')
dn['cycle']=pd.to_numeric(dn.CYCLE_FILE,errors='coerce')
dn=dn.merge(sp[['CMTE_ID','cycle','sym','TOTAL_RECEIPTS','INDIVIDUAL_CONTRIBUTIONS','CMTE_NM']],on=['CMTE_ID','cycle'],how='inner')
dn['ret_sh']=dn.RETIRED_DONORS/dn.DONORS; dn['item_sh']=dn.AMT/dn.INDIVIDUAL_CONTRIBUTIONS; dn['g_per_donor']=dn.GIFTS/dn.DONORS
print(dn.groupby('sym').agg(rows=('CMTE_ID','size'),donors=('DONORS','sum'),retired=('RETIRED_DONORS','sum'),med_ret_sh=('ret_sh','median'),
    med_item_sh=('item_sh','median'),med_gifts_per_donor=('g_per_donor','median'),med_donor_total=('MED_DONOR_TOTAL','median'),donors10=('DONORS_10PLUS','sum')).round(3).to_string())
print('pooled retired share sym', dn[dn.sym].RETIRED_DONORS.sum()/dn[dn.sym].DONORS.sum(), 'others', dn[~dn.sym].RETIRED_DONORS.sum()/dn[~dn.sym].DONORS.sum())
# same-size peers: others with median donor total under $500 (small-dollar)
sm=dn[(~dn.sym)&(dn.MED_DONOR_TOTAL<=500)]
print('small-dollar other super PACs (median donor total <= $500): rows', len(sm), 'med ret share', round(sm.ret_sh.median(),3), 'pooled', round(sm.RETIRED_DONORS.sum()/sm.DONORS.sum(),3), 'med gifts/donor', round(sm.g_per_donor.median(),2))
dn.to_pickle('donors.pkl')
