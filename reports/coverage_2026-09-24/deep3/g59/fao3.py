import json, collections
d=json.load(open('q06.json')); cols=d['cols']
rows=[dict(zip(cols,r)) for r in d['rows']]
ser=collections.defaultdict(dict)
code={}
for r in rows:
    ser[(r['AREA'],r['ITEM_CODE'])][r['YEAR_CODE']]=(r['VALUE'],r['FLAG'])
    code[r['AREA']]=int(r['AREA_CODE'])
Q=sorted(set(r['AREA'] for r in rows if r['ITEM_CODE']=='210091' and r['FLAG']=='Q'))
O=sorted(a for (a,it),v in ser.items() if it=='210091' and code[a]<5000 and all(x[1]=='O' for x in v.values()))
def num(v):
    try: return float(v)
    except: return None
for per in ['20142016','20222024']:
    w=num(ser[('World','210011')][per][0])
    print('period',per,'World undernourished (M)', w, 'PoU', ser[('World','210041')][per])
    tot=0; lt=0
    for a in Q:
        if a in ('China','China, Hong Kong SAR','China, Taiwan Province of'): continue  # avoid double count with China, mainland
        v=ser.get((a,'210011'),{}).get(per,(None,None)); p=ser.get((a,'210041'),{}).get(per,(None,None))
        n=num(v[0]); tot+= n or 0
        print(f"   {a[:30]:30} undernourished={v} PoU={p}")
    print('  Q-country undernourished total', round(tot,1), 'share of world', round(tot/w,3) if w else None)
    to=sum(num(ser.get((a,'210011'),{}).get(per,(None,))[0]) or 0 for a in O); print('  O-country total', round(to,1))
# India alone
print('India 210011', ser[('India','210011')])
# check: is there a World aggregate FIES and does it include Q countries? (FAO says world aggregates include them)
print('World 210091', ser[('World','210091')])
print('World 210081 (M people)', ser[('World','210081')])
