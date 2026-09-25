import pandas as pd, re, unicodedata
pd.set_option('display.width',250); pd.set_option('display.max_rows',300)
v=pd.read_csv('vote.csv'); c=pd.read_csv('fcand.csv')
def norm(s):
    s=unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().upper()
    return re.sub(r'[^A-Z ]',' ',s)
c['yr']=pd.to_numeric(c.CAND_ELECTION_YR,errors='coerce')
S=c[(c.OFFICE=='S')&(c.CYCLE==c.yr)].copy()
S['tok']=S.CAND_NAME.map(lambda s:set(norm(s).split()))
h=v[v.CHAMBER=='House'].copy()
h['last']=h.BIONAME.map(lambda s: norm(s.split(',')[0]).split())
h['firsts']=h.BIONAME.map(lambda s: norm(s.split(',',1)[1]).split() if ',' in s else [])
rows=[]
for _,m in h.iterrows():
    cyc=2024 if m.CONGRESS==118 else 2026
    cand=S[(S.CYCLE==cyc)&(S.OFFICE_STATE==m.STATE)]
    for _,k in cand.iterrows():
        if all(t in k.tok for t in m['last']):
            fok=any(any(t.startswith(f[:3]) for t in k.tok) for f in m.firsts if len(f)>=3)
            rows.append(dict(BIOGUIDE=m.BIOGUIDE,CONGRESS=m.CONGRESS,BIONAME=m.BIONAME[:28],STATE=m.STATE,CAND_ID=k.CAND_ID,CAND_NAME=k.CAND_NAME,IC=k.INCUMBENT_CHALLENGER,ST=k.CAND_STATUS,REC=k.TTL_RECEIPTS,fok=fok))
r=pd.DataFrame(rows)
print(r.to_string())
r.to_csv('house_senate_match_raw.csv',index=False)
