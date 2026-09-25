import json, statistics as st, collections as C, re, unicodedata
def load(q):
    d=json.load(open(q+'.json',encoding='utf-8')); return [dict(zip(d['cols'],r)) for r in d['rows']]
def f(x):
    try:
        v=float(x); return v
    except: return None
coa=load('q01'); sc=load('q02'); med=load('q03'); xmed=load('q04'); jus=load('q05'); scdb=load('q06'); scm=load('q07'); coam=load('q08'); fjc=load('q09')

print('=== SCOTUS_JUSTICE vs SCDB')
sj={r['JUSTICE_CODE']:r for r in scdb}
bad=0
for r in jus:
    s=sj.get(r['JUSTICE_CODE'])
    if not s or s['N_ROWS']!=r['N_VOTES'] or s['FIRST_TERM']!=r['FIRST_TERM'] or s['LAST_TERM']!=r['LAST_TERM']: bad+=1; print(' mismatch',r['JUSTICE_NAME'],r['N_VOTES'],s and s['N_ROWS'])
print(' mismatches',bad,' N_VOTES==N_CASES on',sum(r['N_VOTES']==r['N_CASES'] for r in jus),'of',len(jus))
print(' JOIN_NOTE distinct',len({r['JOIN_NOTE'] for r in jus}))
print(' current bench:',[(r['JUSTICE_NAME'],r['FIRST_TERM'],r['LAST_TERM'],r['N_VOTES']) for r in jus if r['IS_CURRENT_BENCH']])
print(' max LAST_TERM',max(r['LAST_TERM'] for r in jus), ' SCDB max term', max(r['LAST_TERM'] for r in scdb))
nv=sorted(r['N_VOTES'] for r in jus); print(' N_VOTES median',st.median(nv),'max',max(jus,key=lambda r:r['N_VOTES'])['JUSTICE_NAME'])
# cases per term implied
print(' SCDB runs per justice', C.Counter(r['N_RUNS'] for r in scdb))

print('\n=== XC_JCS_SCOTUS')
terms=C.Counter(r['TERM'] for r in sc)
print(' terms',min(terms),max(terms),'n terms',len(terms),' justices',len({r['JUSTICENAME'] for r in sc}))
print(' per-term count dist',C.Counter(terms.values()))
print(' terms with !=9', sorted((t,n) for t,n in terms.items() if n!=9)[:40])
# raw vs mart
mk={(r['JUSTICE_NAME'],str(r['TERM'])):r['JCS'] for r in scm}
diff=sum(1 for r in sc if abs(f(r['JCS'])-float(mk.get((r['JUSTICENAME'],str(r['TERM'])),999)))>1e-9)
print(' raw vs mart JCS diffs',diff,' mart rows',len(scm),' mart null FJC_NID',sum(1 for r in scm if not r['FJC_NID']), ' mart null code',sum(1 for r in scm if r['JUSTICE_CODE'] is None))
# names in JCS not in SCOTUS_JUSTICE
jn={r['JUSTICE_NAME'] for r in jus}; xn={r['JUSTICENAME'] for r in sc}
print(' JCS justices not in SCOTUS_JUSTICE',sorted(xn-jn)); print(' SCOTUS_JUSTICE not in JCS',sorted(jn-xn))
# medians by term
byt=C.defaultdict(list)
for r in sc: byt[int(r['TERM'])].append((f(r['JCS']),r['JUSTICENAME']))
cm={}
for t,v in sorted(byt.items()):
    v.sort(); vals=[x[0] for x in v]; cm[t]=st.median(vals)
# compare with SC_MEDIAN in medians
mm={}
for r in med:
    if r['TERM'] not in (None,'NA'): mm[int(r['TERM'])]=r['SC_MEDIAN']
d=[(t,cm[t],mm[t]) for t in mm if t in cm and mm[t] is not None]
print(' medians compare n',len(d),' max absdiff',max(abs(a-b) for _,a,b in d))
bigd=[(t,round(a,3),round(b,3)) for t,a,b in d if abs(a-b)>0.01]; print(' big diffs',bigd[:20])
# median justice identity
print(' median justice by term (9-member terms):')
prev=None
for t,v in sorted(byt.items()):
    if len(v)==9:
        name=v[4][1]
        if name!=prev: print('   ',t,name,round(v[4][0],3)); prev=name
# rank of court median
rk=sorted(cm.items(),key=lambda x:-x[1])
print(' top 8 most conservative court medians (computed):',[(t,round(m,3)) for t,m in rk[:8]])
print(' bottom 5:',[(t,round(m,3)) for t,m in rk[-5:]])
print(' last 12 terms:',[(t,round(cm[t],3)) for t in sorted(cm)[-12:]])
# drift per justice
jt=C.defaultdict(list)
for r in sc: jt[r['JUSTICENAME']].append((int(r['TERM']),f(r['JCS'])))
dr=[]
for j,v in jt.items():
    v.sort()
    if len(v)>=4:
        a=st.mean(x[1] for x in v[:3]); b=st.mean(x[1] for x in v[-3:])
        dr.append((round(b-a,3),j,v[0][0],v[-1][0],round(a,3),round(b,3),len(v)))
dr.sort()
print(' drift (last3 mean - first3 mean), leftmost:',dr[:8]); print(' rightmost:',dr[-6:])
print(' median |drift|',st.median(abs(x[0]) for x in dr))
cur=[r['JUSTICE_NAME'] for r in jus if r['IS_CURRENT_BENCH']]
print(' current bench drift:',[x for x in dr if x[1] in cur], [ (j,jt[j]) for j in cur if j in jt and len(jt[j])<4])
# latest term lineup
lt=max(byt); print(' lineup',lt,sorted([(round(a,3),b) for a,b in byt[lt]]))

print('\n=== MEDIANS typed vs raw')
yc=C.Counter(r['YEAR'] for r in med); print(' years',min(yc),max(yc),' dup years',[y for y,n in yc.items() if n>1])
print(' SC_MEDIAN null years',[r['YEAR'] for r in med if r['SC_MEDIAN'] is None])
print(' term NA',sum(1 for r in med if r['TERM'] in (None,'NA')),' president null',[r['YEAR'] for r in med if r['PRESIDENT_SCORE'] is None])
# raw vs typed per row
xm=sorted(xmed,key=lambda r:int(r['UNNAMED_0'])); md=med
n=0
for a,b in zip(sorted(md,key=lambda r:(r['YEAR'], r['PRESIDENT_SCORE'] or 0)), sorted(xm,key=lambda r:(r['YEAR'], f(r['PRESIDENT']) or 0))):
    for ca,cb in [('HOUSE_MEDIAN','HOUSE_MEDIAN'),('SENATE_MEDIAN','SENATE_MEDIAN'),('SC_MEDIAN','SC_MEDIAN'),('PRESIDENT_SCORE','PRESIDENT')]:
        va=a[ca]; vb=f(b[cb])
        if (va is None)!=(vb is None) or (va is not None and abs(va-vb)>1e-9): n+=1
print(' typed vs raw cell diffs',n)
print(' 1924 rows raw:',[(r['UNNAMED_0'],r['PRESIDENT']) for r in xmed if r['YEAR']==1924])
# circuit series: first/last non-NA year
for i in range(1,14):
    ys=[r['YEAR'] for r in xmed if f(r['CIRCUIT_MEDIAN%d'%i]) is not None]
    print('  circuit',i,'years',min(ys) if ys else None,max(ys) if ys else None,'n',len(ys))
# latest rows
for r in sorted(xmed,key=lambda r:r['YEAR'])[-10:]:
    print('  ',r['YEAR'],r['TERM'],r['CONGRESS'],'P',r['PRESIDENT'][:6],'H',r['HOUSE_MEDIAN'][:6],'S',r['SENATE_MEDIAN'][:6],'SC',r['SC_MEDIAN'][:6],' circ:',[r['CIRCUIT_MEDIAN%d'%i] for i in range(1,14)])
