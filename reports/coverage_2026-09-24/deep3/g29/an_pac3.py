import pandas as pd, numpy as np, re, warnings
warnings.filterwarnings('ignore')
pd.set_option('display.width',280); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',48)
b=pd.read_pickle('pac_big.pkl'); d=pd.read_pickle('out_S04.pkl')
pat=r"\b(POLICE|COPS?|SHERIFFS?|TROOPERS?|LAW ENFORCEMENT|OFFICERS|FIRE ?FIGHTERS?|FIRST RESPONDERS?|VETERANS?|VETS|MILITARY|SOLDIERS?|TROOPS|WOUNDED|INJURED|DISABLED|CANCER|BREAST|LEUKEMIA|AUTISM|ALZHEIMERS?|CHILDRENS?|CHILDREN'S|KIDS|WIDOWS|GOLD STAR|HEROES|BLUE LIVES|BACK THE BLUE)\b"
b['sym']=b.CMTE_NM.fillna('').str.upper().str.contains(pat,regex=True)
sp=b[b.COMMITTEE_TYPE.isin(['O','V','W'])]
# committee-level pooled
c=sp.groupby(['CMTE_ID','sym']).agg(nm=('CMTE_NM','first'),tres=('tres_last_first','first'),city=('CMTE_CITY','first'),st=('CMTE_ST','first'),cycles=('cycle','nunique'),
    rec=('TOTAL_RECEIPTS','sum'),disb=('TOTAL_DISBURSEMENTS','sum'),pol=('pol','sum'),ie=('INDEPENDENT_EXPENDITURES','sum'),contrib=('CONTRIBUTIONS_TO_OTHER_COMMITTEES','sum')).reset_index()
c['sh']=c.pol/c.disb
print('committee-level: sym', c[c.sym].shape[0], 'median', c[c.sym].sh.median(), '| others', c[~c.sym].shape[0], 'median', c[~c.sym].sh.median())
print('sym committees under 10%', (c[c.sym].sh<0.1).sum(), 'under 25%', (c[c.sym].sh<0.25).sum(), 'over 50%', (c[c.sym].sh>0.5).sum())
s=c[c.sym].sort_values('rec',ascending=False)
print('sym raised', s.rec.sum()/1e6, 'disb', s.disb.sum()/1e6, 'pol', s.pol.sum()/1e6, 'ie', s.ie.sum()/1e6, 'contrib', s.contrib.sum()/1e6)
print('pooled', s.pol.sum()/s.disb.sum(), 'excluding top 4 raisers', s.iloc[4:].pol.sum()/s.iloc[4:].disb.sum(), 'top4 share of raised', s.head(4).rec.sum()/s.rec.sum())
# treasurer networks inside sym
t=s.groupby('tres').agg(cmtes=('CMTE_ID','size'),names=('nm',lambda x:'; '.join(x)),rec=('rec','sum'),pol=('pol','sum'),disb=('disb','sum'),city=('city',lambda x:'/'.join(sorted(set(x)))))
t['sh']=t.pol/t.disb
print(t.sort_values(['cmtes','rec'],ascending=False).round(3).to_string())
multi=t[t.cmtes>=2]
print('treasurers with 2+ sym PACs:', len(multi), 'covering', multi.cmtes.sum(), 'PACs, raised', multi.rec.sum()/1e6, 'pooled', multi.pol.sum()/multi.disb.sum())
# still registered in 2026 file?
d26=set(d[d.SRC=='bulk_cm26'].CMTE_ID)
s['in_2026']=s.CMTE_ID.isin(d26)
print('sym PACs in the 2026 committee file', s.in_2026.sum(), 'of', len(s), 'raised by those', s[s.in_2026].rec.sum()/1e6)
# treasurer in 2026 file for the multi-PAC treasurers: other committees they serve now
dd=d.copy(); dd['tres']=dd.TRES_NM.fillna('').str.upper().str.replace(r'[^A-Z ,]','',regex=True).str.replace(r'\s+',' ',regex=True).str.strip()
dd['tlf']=dd.tres.str.split(',').str[0].str.strip()+','+dd.tres.str.split(',').str[1].fillna('').str.strip().str.split(' ').str[0]
for tr in multi.index:
    x=dd[(dd.tlf==tr)]
    print(tr, 'all committees in dim:', len(x), '| 2026 file:', (x.SRC=='bulk_cm26').sum(), '|', '; '.join(x.CMTE_NM.fillna('').str[:40].tolist()[:12]))
s.to_csv('sympathy_superpacs_committee_level.csv',index=False)
# ambiguity in these
print('IS_AMBIGUOUS among sym', d[d.CMTE_ID.isin(s.CMTE_ID)].IS_AMBIGUOUS.value_counts().to_dict())
