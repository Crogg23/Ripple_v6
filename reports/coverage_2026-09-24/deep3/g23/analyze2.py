import json, collections as C
d=json.load(open('q10.json',encoding='utf-8')); R=[dict(zip(d['cols'],r)) for r in d['rows']]
def i(x):
    try: return int(float(x))
    except: return None
# code sanity: first/last term per source code, total cases
agg=C.defaultdict(lambda:[9999,0,0])
for r in R:
    c=i(r['CASE_SOURCE_CODE']); t=i(r['TERM']); a=agg[c]; a[0]=min(a[0],t); a[1]=max(a[1],t); a[2]+=r['N_CASES']
for c in [8,21,22,23,24,25,26,27,28,29,30,31,32,None]:
    print('src',c,agg.get(c))
tot=sum(r['N_CASES'] for r in R); print('total cases',tot)
top=sorted(agg.items(),key=lambda x:-x[1][2])[:15]; print('top sources',top)
print('decision types',C.Counter({i(r['DECISION_TYPE_CODE']):0 for r in R}).keys())
dt=C.Counter(); 
for r in R: dt[i(r['DECISION_TYPE_CODE'])]+=r['N_CASES']
print('cases by decision type',dt)
pw=C.Counter()
for r in R: pw[i(r['PARTY_WINNING'])]+=r['N_CASES']
print('party winning',pw)
