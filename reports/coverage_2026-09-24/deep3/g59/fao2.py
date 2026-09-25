import json, collections
d=json.load(open('q06.json')); cols=d['cols']
rows=[dict(zip(cols,r)) for r in d['rows']]
def num(v):
    try: return float(v)
    except: return None
ser=collections.defaultdict(dict)
for r in rows: ser[(r['AREA'],r['ITEM_CODE'])][r['YEAR_CODE']]=(r['VALUE'],r['FLAG'],r['NOTE'])
for it in ['210091','210401']:
    q=sorted(set(r['AREA'] for r in rows if r['ITEM_CODE']==it and r['FLAG']=='Q'))
    print(it,'Q-flag areas',len(q),q)
    qall=[a for a in q if all(v[1]=='Q' for v in ser[(a,it)].values())]
    print('  Q on every period', len(qall))
# O-flag-only countries on 210091
o=sorted(a for (a,it),v in ser.items() if it=='210091' and int(next(r['AREA_CODE'] for r in rows if r['AREA']==a))<5000 and all(x[1]=='O' for x in v.values()))
print('O on every period', len(o), o)
# PoU flag Q?
print('PoU flags', collections.Counter(r['FLAG'] for r in rows if r['ITEM_CODE']=='210041'))
# US & peers
peers=['United States of America','Canada','United Kingdom of Great Britain and Northern Ireland','Germany','France','Italy','Japan','Australia','Spain','Netherlands (Kingdom of the)','Sweden','Republic of Korea','New Zealand','Ireland','Switzerland','Norway','Belgium','Austria','Denmark','Finland','Israel','Portugal']
for it in ['210091','210401']:
    print('== item', it)
    for p in peers:
        s=ser.get((p,it))
        if not s: print(p,'MISSING'); continue
        ks=sorted(s)
        print(f"{p[:28]:28}", ' '.join(f"{s[k][0] or '-'}{s[k][1]}" for k in ks))
