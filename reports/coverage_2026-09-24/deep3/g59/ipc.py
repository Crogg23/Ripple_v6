import json, collections
d=json.load(open('q03.json'))
cols=d['cols']; rows=[dict(zip(cols,r)) for r in d['rows']]
an=collections.defaultdict(dict)
for r in rows: an[r['COUNTRY']].setdefault(r['VALIDITY_PERIOD'],{})[r['PHASE']]=r
out=[]
def f(x):
    try: return float(x)
    except: return None
for c,vs in an.items():
    per='current' if 'current' in vs else 'first projection'
    a0=vs[per]['all']
    pop=f(a0['TOTAL_COUNTRY_POPULATION']); date=a0['DATE_OF_ANALYSIS']
    g=lambda v,p: f(vs.get(v,{}).get(p,{}).get('NUMBER')) if vs.get(v,{}).get(p) else None
    a=g(per,'all'); p3=g(per,'3+'); p4=g(per,'4'); p5=g(per,'5')
    fp3=g('first projection','3+') if per=='current' else None
    fp5=g('first projection','5') if per=='current' else None
    cov=(a/pop) if pop and a else None
    out.append(dict(c=c,date=date,per=per,pop=pop,a=a,cov=cov,p3=p3,sh=(p3/a if a else None),p4=p4,p5=p5,fp3=fp3,fp5=fp5,frm=a0['C_FROM'],to=a0['C_TO'],vs=sorted(vs)))
out.sort(key=lambda x:-(x['p3'] or 0))
for o in out:
    print(f"{o['c']:4} {o['date']:9} {o['per'][:5]:5} pop={int(o['pop'] or 0):>11,} an={int(o['a'] or 0):>11,} cov={o['cov'] and round(o['cov'],2)} p3={int(o['p3'] or 0):>10,} sh={o['sh'] and round(o['sh'],3)} p4={int(o['p4'] or 0):>9,} p5={int(o['p5'] or 0):>8,} fp3={o['fp3'] and int(o['fp3'])} fp5={o['fp5'] and int(o['fp5'])} {o['frm']}..{o['to']} {len(o['vs'])}")
print('countries',len(out),'total p3', int(sum(o['p3'] or 0 for o in out)), 'p5', int(sum(o['p5'] or 0 for o in out)))
json.dump(out, open('ipc_summary.json','w'), indent=0)
