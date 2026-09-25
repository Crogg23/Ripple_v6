import pandas as pd, re, unicodedata
pd.set_option('display.width',250); pd.set_option('display.max_rows',300)
v=pd.read_csv('vote.csv'); f=pd.read_csv('fecid.csv'); c=pd.read_csv('fcand.csv')
def norm(s):
    s=unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().upper()
    return re.sub(r'[^A-Z ]',' ',s)
# candidacies of interest
c['yr']=pd.to_numeric(c.CAND_ELECTION_YR,errors='coerce')
want=c[((c.OFFICE=='S')&(c.CYCLE==c.yr))|((c.OFFICE=='P')&(c.yr.isin([2024,2028])))].copy()
# route 1: bridge
b=f.merge(want,left_on='FEC_ID',right_on='CAND_ID')
b['route']='bridge'
# route 2: last name + state (senate) ; last name only for P
v['last']=v.BIONAME.map(lambda s: norm(s.split(',')[0]).strip())
v['first']=v.BIONAME.map(lambda s: norm(s.split(',')[1]).split()[0] if ',' in s else '')
want['last']=want.CAND_NAME.map(lambda s: norm(str(s).split(',')[0]).strip())
want['first']=want.CAND_NAME.map(lambda s: norm(str(s).split(',')[1]).split()[0] if ',' in str(s) and norm(str(s).split(',')[1]).split() else '')
mem=v[['BIOGUIDE','STATE','last','first']].drop_duplicates()
n=mem.merge(want,on='last')
n=n[((n.OFFICE=='S')&(n.STATE==n.OFFICE_STATE))|(n.OFFICE=='P')]
n['first_ok']=[a[:3]==b_[:3] for a,b_ in zip(n.first_x,n.first_y)]
print('name matches', len(n), 'first-name agree', n.first_ok.sum())
print(n[['BIOGUIDE','STATE','first_x','CAND_NAME','CAND_ID','CYCLE','OFFICE','yr','CAND_STATUS','TTL_RECEIPTS','first_ok']].sort_values(['CYCLE','OFFICE']).to_string())
bb=set(zip(b.BIOGUIDE,b.CAND_ID)); nn=set(zip(n[n.first_ok].BIOGUIDE,n[n.first_ok].CAND_ID))
print('bridge only', bb-nn); print('name only', nn-bb)
n[n.first_ok].to_csv('runner_cands.csv',index=False)
b.to_csv('runner_bridge.csv',index=False)
