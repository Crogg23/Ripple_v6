import json, collections, statistics as st
P=json.load(open('S03.json')); I=json.load(open('S08.json'))
K='ESTIMATED_AGE_ADJUSTED_DEATH_RATE_11_CATEGORIES_IN_RANGES'
def mid(b):
    if b.startswith('>'): return 31.0
    a,c=b.split('-'); return (float(a)+float(c))/2
p15={x['FIPS']:x for x in P if x['YEAR']==2015}
p10={x['FIPS']:x for x in P if x['YEAR']==2010}
inj=collections.defaultdict(dict)
for x in I: inj[x['GEOID']][x['PERIOD']]=x
land=set(p15)&set(inj); print('2015 counties', len(p15), 'injury counties', len(inj), 'landed', len(land))
print('in poisoning not injury', [p15[f]['COUNTY'] for f in set(p15)-set(inj)][:10])
def rank(vals):
    s=sorted(range(len(vals)), key=lambda i: vals[i]); rk=[0]*len(vals)
    for r,i in enumerate(s): rk[i]=r
    return rk
def spearman(a,b):
    ra,rb=rank(a),rank(b); n=len(a); ma=sum(ra)/n; mb=sum(rb)/n
    cov=sum((x-ma)*(y-mb) for x,y in zip(ra,rb)); va=sum((x-ma)**2 for x in ra); vb=sum((y-mb)**2 for y in rb)
    return cov/(va*vb)**0.5
big=[f for f in land if (p15[f]['POPULATION'] or 0)>=50000]
for per in ('2019','2021','2023','2024'):
    fs=[f for f in big if per in inj[f] and inj[f][per]['RATE']>=0 and inj[f][per]['RATE_M']==0]
    print(per, 'counties pop>=50k unsuppressed', len(fs), 'spearman(2015 band, actual rate)', round(spearman([mid(p15[f][K]) for f in fs],[inj[f][per]['RATE'] for f in fs]),3))
# rank movers: national percentile 2015 band vs 2023 rate, pop>=50k
per='2023'
fs=[f for f in big if per in inj[f] and inj[f][per]['RATE']>=0 and inj[f][per]['RATE_M']==0]
a=[mid(p15[f][K]) for f in fs]; b=[inj[f][per]['RATE'] for f in fs]
ra=rank(a); rb=rank(b); n=len(fs)
mv=sorted([((rb[i]-ra[i])/n, fs[i]) for i in range(n)], reverse=True)
print('n', n)
print('biggest risers (percentile points), 2015 band -> 2023 actual:')
for d,f in mv[:20]:
    print(' ', round(d*100), p15[f]['COUNTY'], int(p15[f]['POPULATION']), p15[f][K], '->', inj[f]['2023']['RATE'], 'count', inj[f]['2023']['COUNT_SUP'])
print('biggest fallers:')
for d,f in mv[-12:]:
    print(' ', round(d*100), p15[f]['COUNTY'], int(p15[f]['POPULATION']), p15[f][K], '->', inj[f]['2023']['RATE'], 'count', inj[f]['2023']['COUNT_SUP'])
# state-level: pop-weighted 2015 mid vs 2023 rate among pop>=50k, rank states
S=collections.defaultdict(lambda: [0,0,0])
for f in fs:
    s=p15[f]['ST']; w=p15[f]['POPULATION']; S[s][0]+=w; S[s][1]+=w*mid(p15[f][K]); S[s][2]+=w*inj[f]['2023']['RATE']
L=sorted([(round(v[2]/v[0]/(v[1]/v[0]),2), s, round(v[1]/v[0],1), round(v[2]/v[0],1)) for s,v in S.items() if v[0]>1e6], reverse=True)
print('state ratio 2023 actual / 2015 band mid (pop-weighted, counties>=50k):'); print(L[:12]); print(L[-8:])
