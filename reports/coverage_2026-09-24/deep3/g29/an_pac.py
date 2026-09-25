import pandas as pd, numpy as np
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',42)
d=pd.read_pickle('out_S04.pkl'); p=pd.read_pickle('out_S06.pkl')
p=p[p.COVERAGE_END_DATE.notna()].copy()
p['yr']=pd.to_datetime(p.COVERAGE_END_DATE).dt.year
p['cycle']=p.yr+(p.yr%2)
# duplicates per committee-cycle?
dup=p.groupby(['CMTE_ID','cycle']).size()
print('cmte-cycle rows', len(dup), 'with >1 row', (dup>1).sum())
p=p.merge(d[['CMTE_ID','CMTE_NM','TRES_NM','CMTE_CITY','CMTE_ST','CMTE_TP','CMTE_DSGN','CONNECTED_ORG_NM','ORG_TP','IS_AMBIGUOUS','SRC']],on='CMTE_ID',how='left')
print('land in dim', p.CMTE_NM.notna().mean())
p['tres']=p.TRES_NM.fillna('').str.upper().str.replace(r'[^A-Z ,]','',regex=True).str.replace(r'\s+',' ',regex=True).str.strip()
p['tres_last_first']=p.tres.str.split(',').str[0].str.strip()+','+p.tres.str.split(',').str[1].fillna('').str.strip().str.split(' ').str[0]
# peer group: nonconnected PACs + super PACs + hybrids, not leadership PACs, not conduits
peer=p[p.COMMITTEE_TYPE.isin(['N','Q','O','V','W']) & (p.COMMITTEE_DESIGNATION!='D') & (p.CONNECTED_ORG_NM.fillna('NONE').str.upper().str.strip().isin(['NONE','','N/A']))].copy()
peer=peer[~peer.CMTE_ID.isin(['C00401224','C00694323'])]
peer['pol']=peer.CONTRIBUTIONS_TO_OTHER_COMMITTEES.fillna(0)+peer.INDEPENDENT_EXPENDITURES.fillna(0)+peer.TRANSFERS_TO_AFFILIATES.fillna(0)
peer['indiv_sh']=peer.INDIVIDUAL_CONTRIBUTIONS/peer.TOTAL_RECEIPTS
big=peer[(peer.TOTAL_RECEIPTS>=250000)&(peer.TOTAL_DISBURSEMENTS>=250000)&(peer.indiv_sh>=0.8)].copy()
big['pol_sh']=big.pol/big.TOTAL_DISBURSEMENTS
print('peer cmte-cycles (>=250K, >=80% indiv):', len(big), 'cmtes', big.CMTE_ID.nunique())
print('median pol share', big.pol_sh.median(), 'by type', big.groupby('COMMITTEE_TYPE').pol_sh.median().round(3).to_dict())
print('share under 10%', (big.pol_sh<0.10).mean(), 'n', (big.pol_sh<0.10).sum())
print('by cycle', big.groupby('cycle').agg(n=('CMTE_ID','size'), med=('pol_sh','median'), low=('pol_sh',lambda x:(x<0.1).mean()), rec=('TOTAL_RECEIPTS','sum')).to_string())
big.to_pickle('pac_big.pkl')
low=big[big.pol_sh<0.10]
print('low-pol $ receipts', low.TOTAL_RECEIPTS.sum()/1e6, 'of all big', big.TOTAL_RECEIPTS.sum()/1e6)
# treasurers
t=big.groupby('tres_last_first').agg(cmtes=('CMTE_ID','nunique'), rows=('CMTE_ID','size'), rec=('TOTAL_RECEIPTS','sum'), disb=('TOTAL_DISBURSEMENTS','sum'), pol=('pol','sum'),
   low_rows=('pol_sh',lambda x:(x<0.1).sum()), med_sh=('pol_sh','median'))
t['pol_sh']=t.pol/t.disb
t=t[t.cmtes>=3]
print(t.sort_values('rec',ascending=False).head(40).round(3).to_string())
print('--- treasurers with >=3 cmtes and pooled pol share <10%, by receipts')
print(t[t.pol_sh<0.10].sort_values('rec',ascending=False).head(30).round(3).to_string())
