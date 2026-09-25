import json, collections as C, statistics as st
def load(q):
    d=json.load(open(q+'.json',encoding='utf-8')); return [dict(zip(d['cols'],r)) for r in d['rows']]
R=load('q10'); xmed=load('q04'); sc=load('q02'); med=load('q03')
f=lambda x: float(x) if x not in (None,'NA','') else None
i=lambda x: int(float(x)) if x not in (None,'') else None
ARG={1,6,7}
SRC2C={21:1,22:2,23:3,24:4,25:5,26:6,27:7,28:8,29:9,30:10,31:11,32:12,8:13}
# docket share by term
tot=C.Counter(); c5=C.Counter(); c9=C.Counter(); allcirc=C.Counter()
for r in R:
    if i(r['DECISION_TYPE_CODE']) not in ARG: continue
    t=i(r['TERM']); s=i(r['CASE_SOURCE_CODE']); n=r['N_CASES']
    tot[t]+=n
    if s==25: c5[t]+=n
    if s==29: c9[t]+=n
    if s in SRC2C: allcirc[(t,s)]+=n
sh=sorted(((c5[t]/tot[t],t,c5[t],tot[t]) for t in tot),reverse=True)
print('5th circuit share of argued cases, top 8 terms:',[(t,n,T,round(100*s,1)) for s,t,n,T in sh[:8]])
print('5th share last 10 terms:',[(t,c5[t],tot[t],round(100*c5[t]/tot[t],1)) for t in sorted(tot)[-10:]])
print('median term share 5th, all terms:',round(100*st.median(c5[t]/tot[t] for t in tot),1))
# rank of 5th among circuits by term count, last terms
for t in range(2019,2025):
    row=sorted(((allcirc[(t,s)],s) for s in SRC2C),reverse=True)[:3]
    print(' term',t,'top circuits',[(SRC2C[s],n) for n,s in row],'total argued',tot[t])
# highest single-circuit share in any term (any circuit)
best=sorted(((allcirc[(t,s)]/tot[t],t,SRC2C[s],allcirc[(t,s)],tot[t]) for (t,s) in allcirc),reverse=True)[:10]
print('highest single-circuit shares ever:',[(t,c,n,T,round(100*s,1)) for s,t,c,n,T in best])
# circuit medians vs court median -> direction of SCOTUS decision
cm={}; smed={}
for r in xmed:
    if r['TERM'] in (None,'NA'): continue
    t=int(r['TERM']); smed[t]=f(r['SC_MEDIAN'])
    for c in range(1,14): cm[(t,c)]=f(r['CIRCUIT_MEDIAN%d'%c])
grp=C.defaultdict(C.Counter)
for r in R:
    if i(r['DECISION_TYPE_CODE']) not in ARG: continue
    t=i(r['TERM']); s=i(r['CASE_SOURCE_CODE']); c=SRC2C.get(s)
    if c is None or t<1982 or t>2022: continue
    a=cm.get((t,c)); b=smed.get(t)
    if a is None or b is None: continue
    side='circuit right of Court median' if a>b else 'circuit left of Court median'
    g=grp[side]; n=r['N_CASES']; g['n']+=n
    pw=i(r['PARTY_WINNING']); dd=i(r['DECISION_DIRECTION_CODE']); lcd=i(r['LC_DISPOSITION_DIRECTION_CODE'])
    if pw==1: g['rev']+=n
    if pw in (0,1): g['dec']+=n
    if pw==1 and dd==2: g['rev_lib']+=n
    if pw==1 and dd==1: g['rev_con']+=n
    if lcd==1: g['lc_con']+=n
    if lcd in (1,2): g['lc_dir']+=n
for k,g in grp.items():
    print(k,dict(g),' rev%',round(100*g['rev']/g['dec'],1),' lib share of reversals',round(100*g['rev_lib']/(g['rev_lib']+g['rev_con']),1),' lower-court conservative %',round(100*g['lc_con']/g['lc_dir'],1))
# SC median rank
scm=sorted(((v,t) for t,v in smed.items() if v is not None),reverse=True)
rank={t:k+1 for k,(v,t) in enumerate(scm)}
print('SC median rank (1=most conservative) of',len(scm),'terms:',{t:(rank[t],round(smed[t],3)) for t in range(2016,2023)})
# since 1953, 1970
for since in (1937,1953,1970,1990):
    sub=sorted(((v,t) for t,v in smed.items() if v is not None and t>=since),reverse=True)
    print(' since',since,'rank of 2021:',[k+1 for k,(v,t) in enumerate(sub) if t==2021][0],'of',len(sub),' top3',[(t,round(v,3)) for v,t in sub[:3]])
# court vs chambers
right=[];
for r in med:
    if r['SC_MEDIAN'] is None: continue
    if r['SC_MEDIAN']>max(r['HOUSE_MEDIAN'],r['SENATE_MEDIAN']): right.append(r['YEAR'])
print('years Court median right of BOTH chamber medians:',len(right),'of',sum(1 for r in med if r['SC_MEDIAN'] is not None),right)
gap=sorted(((r['SC_MEDIAN']-r['SENATE_MEDIAN'],r['YEAR']) for r in med if r['SC_MEDIAN'] is not None),reverse=True)[:8]
print('largest Court-minus-Senate gaps',[(y,round(g,3)) for g,y in gap])
gapP=sorted(((r['SC_MEDIAN']-r['PRESIDENT_SCORE'],r['YEAR']) for r in med if r['SC_MEDIAN'] is not None and r['PRESIDENT_SCORE'] is not None),reverse=True)[:6]
print('largest Court-minus-President gaps',[(y,round(g,3)) for g,y in gapP])
# circuit series for 5, 9, 11
for c in (2,3,5,9,11):
    print(' circuit',c,[(r['YEAR'],r['CIRCUIT_MEDIAN%d'%c]) for r in sorted(xmed,key=lambda r:r['YEAR']) if r['YEAR']>=2008])
