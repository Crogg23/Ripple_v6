import json, collections
d=json.load(open('q06.json')); cols=d['cols']
rows=[dict(zip(cols,r)) for r in d['rows']]
def num(v):
    try: return float(v)
    except: return None
# areas: countries vs aggregates
areas={r['AREA_CODE']:r['AREA'] for r in rows}
agg=[a for a in areas if int(a)>=5000]; print('areas',len(areas),'aggregates(code>=5000)',len(agg))
# annual-value areas
ann=sorted(set(r['AREA'] for r in rows if r['ITEM_CODE']=='210400'))
print('annual-series areas', len(ann), ann)
# flags by item
for it in ['210091','210401','210041']:
    c=collections.Counter((r['FLAG'], 'blank' if r['VALUE'] in (None,'') else ('lt' if str(r['VALUE']).startswith('<') else 'num')) for r in rows if r['ITEM_CODE']==it and int(r['AREA_CODE'])<5000)
    print(it, c)
# NOTE values
print('notes', collections.Counter(r['NOTE'] for r in rows).most_common(8))
# FIES blank countries in latest period
it='210091'
last={}
for r in rows:
    if r['ITEM_CODE']==it and int(r['AREA_CODE'])<5000:
        last.setdefault(r['AREA'],{})[r['YEAR_CODE']]=(r['VALUE'],r['FLAG'])
never=[a for a,v in last.items() if all(x[0] in (None,'') for x in v.values())]
print('countries with FIES mod+sev never published', len(never), 'of', len(last))
print(sorted(never))
stopped=[(a,sorted(k for k,x in v.items() if x[0] not in (None,''))) for a,v in last.items() if any(x[0] not in (None,'') for x in v.values()) and v.get('20222024',(None,))[0] in (None,'')]
print('had values but blank in 2022-2024', len(stopped)); [print(s) for s in stopped]
