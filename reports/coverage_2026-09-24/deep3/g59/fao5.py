import json, re
d=json.load(open('q06.json')); cols=d['cols']
rows=[dict(zip(cols,r)) for r in d['rows']]
def num(v):
    try: return float(v)
    except: return None
areas=sorted(set((int(r['AREA_CODE']),r['AREA']) for r in rows if int(r['AREA_CODE'])<5000))
sus=[a for a in areas if re.search(r'Africa|Asia|America|Europe|World|excluding|including|countries|Countries|Union|former|Oceania|Caribbean|^China$', a[1])]
print('suspect aggregates under 5000:', sus)
AGG={351,420,429}
print('excluding', AGG)
Q=set(r['AREA'] for r in rows if r['ITEM_CODE']=='210091' and r['FLAG']=='Q')
for it,lab in [('210081','mod+sev people (M)'),('210071','severe people (M)'),('210011','undernourished (M)')]:
    for per in ['20142016','20222024']:
        w=[num(r['VALUE']) for r in rows if r['ITEM_CODE']==it and r['AREA']=='World' and r['YEAR_CODE']==per][0]
        pub=0;n=0
        for r in rows:
            if r['ITEM_CODE']==it and r['YEAR_CODE']==per and int(r['AREA_CODE'])<5000 and int(r['AREA_CODE']) not in AGG:
                v=num(r['VALUE'])
                if v is not None: pub+=v; n+=1
        print(f'{lab:22} {per} world={w} published-country-sum={round(pub,1)} n={n} unpublished={round(w-pub,1)} ({round((w-pub)/w*100,1)}%)')
# Q countries' undernourished (excluding China sub-areas) 2022-24, and PoU-based
