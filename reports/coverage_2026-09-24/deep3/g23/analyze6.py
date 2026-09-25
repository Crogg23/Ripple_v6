import json, collections as C, statistics as st
def load(q):
    d=json.load(open(q+'.json',encoding='utf-8')); return [dict(zip(d['cols'],r)) for r in d['rows']]
R=load('q10'); A=load('q12'); F=load('q13')
i=lambda x: int(float(x)) if x not in (None,'') else None
ARG={1,6,7}
SRC={21:'1',22:'2',23:'3',24:'4',25:'5',26:'6',27:'7',28:'8',29:'9',30:'10',31:'11',32:'0'}
NAME={'0':'DC','1':'1st','2':'2nd','3':'3rd','4':'4th','5':'5th','6':'6th','7':'7th','8':'8th','9':'9th','10':'10th','11':'11th'}
cases=C.Counter()
for r in R:
    if i(r['DECISION_TYPE_CODE']) in ARG and i(r['CASE_SOURCE_CODE']) in SRC: cases[(SRC[i(r['CASE_SOURCE_CODE'])],i(r['TERM']))]+=r['N_CASES']
app=C.Counter()
for r in A:
    if r['JY'] is not None: app[(str(r['CIRCUIT']),int(r['JY']))]+=r['N_APPEALS']
def blk(c,terms,lag):
    n=sum(cases[(c,t)] for t in terms); d=sum(app[(c,t-lag)] for t in terms); return n,d
print('%-5s %-28s %-28s %s'%('circ','terms 2016-18 (cases/appeals, per1k)','terms 2022-24','ratio'))
rows=[]
for lag in (1,0):
  print('--- lag',lag,'(appeals decided in year term-%d)'%lag)
  for c in NAME:
    n1,d1=blk(c,[2016,2017,2018],lag); n2,d2=blk(c,[2022,2023,2024],lag)
    r1=1000*n1/d1; r2=1000*n2/d2
    print('%-5s %3d/%6d = %.2f            %3d/%6d = %.2f            x%.1f'%(NAME[c],n1,d1,r1,n2,d2,r2,(r2/r1) if r1 else float('inf')))
    if lag==1: rows.append((NAME[c],r1,r2))
  print('   median per-1k, 2022-24:',round(st.median(r[2] for r in rows),2) if lag==1 else '')
# 5th circuit per-term per 1k
print('5th per-term per 1k (lag1):',[(t,cases[('5',t)],app[('5',t-1)],round(1000*cases[('5',t)]/app[('5',t-1)],2)) for t in range(2015,2025)])
# fed petitioner
fp=C.defaultdict(C.Counter)
names=set()
for r in F:
    t=i(r['TERM']); s=i(r['CASE_SOURCE_CODE']); c=SRC.get(s)
    if c is None: continue
    b='2015-20' if 2015<=t<=2020 else ('2021-24' if t>=2021 else None)
    if b is None: continue
    k=(NAME[c],b); fp[k]['n']+=r['N_CASES']
    if r['PET']=='fed':
        fp[k]['fed']+=r['N_CASES']
        if i(r['PARTY_WINNING'])==1: fp[k]['fedwin']+=r['N_CASES']
    if r['NAMES_5TH']: names.update(r['NAMES_5TH'].split(' | ')) if r['PET']=='fed' else None
print('\nfederal petitioner share by circuit:')
for c in NAME.values():
    a=fp[(c,'2015-20')]; b=fp[(c,'2021-24')]
    print('  %-4s 2015-20: fed %2d of %3d   2021-24: fed %2d of %3d (fed won %d)'%(c,a['fed'],a['n'],b['fed'],b['n'],b['fedwin']))
tot=C.Counter();
for (c,b),v in fp.items():
    if c!='5th' and b=='2021-24': tot.update(v)
print('  all other circuits 2021-24: fed',tot['fed'],'of',tot['n'],'fed won',tot['fedwin'])
print('5th fed-petitioner case names 2021-24:',sorted(names))
