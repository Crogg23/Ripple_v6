import json, collections as C, statistics as st, unicodedata, re
def load(q):
    d=json.load(open(q+'.json',encoding='utf-8')); return [dict(zip(d['cols'],r)) for r in d['rows']]
coa=[r for r in load('q01') if r['JCS'] not in (None,'NA','')]; coam=load('q08'); fjc=load('q09'); xmed=load('q04'); med=load('q03')
f=lambda x: float(x) if x not in (None,'NA','') else None
print('rows',len(coa),'distinct names',len({r['NAME'] for r in coa}))
dn=C.Counter(r['NAME'] for r in coa)
dups=[n for n,c in dn.items() if c>1]
print('dup names',len(dups),[(n,[(r['CIRCUIT'],round(f(r['JCS']),3)) for r in coa if r['NAME']==n]) for n in dups])
# raw vs mart
rk=C.Counter((r['NAME'],int(r['CIRCUIT'])) for r in coa); mk=C.Counter((r['JCS_JUDGE_NAME'],int(r['CIRCUIT'])) for r in coam)
print('raw not in mart',list((rk-mk).items())); print('mart not in raw',list((mk-rk).items()))
print('circuits',sorted(C.Counter(r['CIRCUIT'] for r in coa).items(),key=lambda x:int(x[0])))
vals=C.Counter(round(f(r['JCS']),6) for r in coa)
print('distinct JCS values',len(vals),' judges sharing a value with >=1 other:',sum(c for v,c in vals.items() if c>1))
print('top shared',vals.most_common(12))
# presidential scores by year
pres=C.defaultdict(set)
for r in xmed:
    if f(r['PRESIDENT']) is not None: pres[round(f(r['PRESIDENT']),6)].add(r['YEAR'])
ps={v:(min(y),max(y)) for v,y in pres.items()}
print('president scores',sorted(ps.items(),key=lambda x:x[1]))
eq=sum(1 for r in coa if round(f(r['JCS']),6) in ps)
print('judges whose JCS equals a president score exactly:',eq,'of',len(coa))
# circuit medians equal to a president score: count circuit-year cells
cells=0;eqc=0
for r in xmed:
    for i in range(1,14):
        v=f(r['CIRCUIT_MEDIAN%d'%i])
        if v is None: continue
        cells+=1
        if any(abs(v-p)<0.0006 for p in ps): eqc+=1
print('circuit-year median cells equal (3dp) to a president score:',eqc,'of',cells)
for i in (12,13):
    vs=[f(r['CIRCUIT_MEDIAN%d'%i]) for r in xmed if f(r['CIRCUIT_MEDIAN%d'%i]) is not None]
    print(' circuit',i,'cells',len(vs),'equal pres',sum(1 for v in vs if any(abs(v-p)<0.0006 for p in ps)))
# FJC match
def norm(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    s=re.sub(r'[^a-z, ]',' ',s); return s
def key(name):
    n=norm(name); last,_,rest=n.partition(','); first=(rest.split() or [''])[0]
    return last.strip(), first
CN={'First':1,'Second':2,'Third':3,'Fourth':4,'Fifth':5,'Sixth':6,'Seventh':7,'Eighth':8,'Ninth':9,'Tenth':10,'Eleventh':11,'District of Columbia':12,'Federal':13}
fj=C.defaultdict(list)
for r in fjc:
    m=re.search(r'for the (.+?) Circuit',r['COURT_NAME'] or '')
    c=CN.get(m.group(1)) if m else None
    fj[key(r['JUDGE_NAME'])+(c,)].append(r)
print('FJC appeals rows',len(fjc),' courts',C.Counter(re.sub(r'U.S. Court of Appeals for the ','',r['COURT_NAME']) for r in fjc).most_common(20))
hit=[];miss=[]
for r in coa:
    k=key(r['NAME'])+(int(r['CIRCUIT']),)
    if fj.get(k): hit.append((r,fj[k][0]))
    else: miss.append(r)
print('matched on last+first+circuit',len(hit),'of',len(coa)); print(' sample misses',[(m['NAME'],m['CIRCUIT']) for m in miss[:25]])
# party split
byp=C.defaultdict(list)
for r,fr in hit: byp[fr['PARTY_OF_APPOINTING_PRESIDENT']].append(f(r['JCS']))
for p,v in byp.items(): print(' party',p,'n',len(v),'median',round(st.median(v),3),'min',round(min(v),3),'max',round(max(v),3),' share on "wrong" side of 0:',round(sum(1 for x in v if (x>0 if p=='Democratic' else x<0))/len(v),3))
# commission year coverage
yrs=C.Counter()
for r,fr in hit: yrs[(fr['COMMISSION_DATE'] or '')[:3]+'0s']+=1
allf=C.Counter()
for r in fjc:
    if 'assignment' in (r['APPOINTING_PRESIDENT'] or '').lower(): continue
    allf[(r['COMMISSION_DATE'] or '')[:3]+'0s']+=1
print(' coverage by commission decade (JCS matched / FJC appointments):',[(d,yrs[d],allf[d]) for d in sorted(allf)])
newest=sorted(hit,key=lambda x:x[1]['COMMISSION_DATE'] or '')[-6:]
print(' newest in JCS:',[(r['NAME'],fr['COMMISSION_DATE'],fr['APPOINTING_PRESIDENT']) for r,fr in newest])
missing_recent=[(r['JUDGE_NAME'],r['COMMISSION_DATE'],r['APPOINTING_PRESIDENT']) for r in fjc if (r['COMMISSION_DATE'] or '')>='2023-06-01' and 'assignment' not in (r['APPOINTING_PRESIDENT'] or '').lower()]
hitn={fr['NID'] for _,fr in hit}
print(' FJC appeals commissions since 2023-06:',len(missing_recent),' in JCS:',sum(1 for r in fjc if (r['COMMISSION_DATE'] or '')>='2023-06-01' and r['NID'] in hitn))
print('  ',missing_recent[:30])
# Trump-appointee scores
tr=[f(r['JCS']) for r,fr in hit if 'Trump' in (fr['APPOINTING_PRESIDENT'] or '')]
print(' Trump appointees n',len(tr),'distinct scores',len(set(round(x,4) for x in tr)),C.Counter(round(x,3) for x in tr).most_common(8))
bd=[f(r['JCS']) for r,fr in hit if 'Biden' in (fr['APPOINTING_PRESIDENT'] or '')]
print(' Biden appointees n',len(bd),C.Counter(round(x,3) for x in bd).most_common(8))
json.dump([[r['NAME'],r['CIRCUIT'],r['JCS'],fr['NID'],fr['APPOINTING_PRESIDENT'],fr['PARTY_OF_APPOINTING_PRESIDENT'],fr['COMMISSION_DATE'],fr['TERMINATION_DATE']] for r,fr in hit],open('coa_fjc_match.json','w'))
