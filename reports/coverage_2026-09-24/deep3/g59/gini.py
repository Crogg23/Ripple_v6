import json, collections
d=json.load(open('q04.json')); cols=d['cols']
rows=[dict(zip(cols,r)) for r in d['rows']]
print(len(rows), 'entities', len(set(r['ENTITY'] for r in rows)))
dup=collections.Counter((r['ENTITY'],r['YEAR']) for r in rows); print('dup entity-year', sum(1 for v in dup.values() if v>1))
nocode=collections.Counter(r['ENTITY'] for r in rows if not r['CODE']); print('no code', len(nocode), list(nocode.items())[:40])
vals=collections.Counter(r['GINI_COEFFICIENT'] for r in rows)
top=vals.most_common(5); print(top)
for v,_ in top[:3]:
    print(v, sorted(set((r['ENTITY'],r['YEAR']) for r in rows if r['GINI_COEFFICIENT']==v))[:25])
yrs=[int(r['YEAR']) for r in rows]; print('years', min(yrs), max(yrs))
g=[float(r['GINI_COEFFICIENT']) for r in rows]; print('gini range', min(g), max(g))
print('regions', collections.Counter(r['WORLD_REGION_ACCORDING_TO_OWID'] for r in rows))
# latest per country with code
latest={}
for r in rows:
    if r['CODE'] and (r['ENTITY'] not in latest or int(r['YEAR'])>int(latest[r['ENTITY']]['YEAR'])): latest[r['ENTITY']]=r
ly=collections.Counter(int(r['YEAR'])//5*5 for r in latest.values()); print('latest-year buckets', sorted(ly.items()))
us=[(r['YEAR'],round(float(r['GINI_COEFFICIENT']),3)) for r in rows if r['CODE']=='USA']; print('USA', sorted(us)[-12:], len(us))
