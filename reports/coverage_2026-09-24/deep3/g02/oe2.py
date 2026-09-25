import json, collections, statistics as st
H=json.load(open('oe_hosp.json'))
g={x['CCN']:x for x in json.load(open('S05.json'))}
hc=collections.defaultdict(dict)
for x in json.load(open('S06.json')):
    fy=str(x['FISCAL_YEAR_END_DATE'])[:4]
    # keep the longest report per ccn-year (some file more than one)
    prev=hc[x['PROVIDER_CCN']].get(fy)
    if prev is None or (x['TOTAL_COSTS'] or 0) > (prev['TOTAL_COSTS'] or 0):
        hc[x['PROVIDER_CCN']][fy]=x
def med(a): return round(st.median(a),3) if a else None
rows=[]
for k,h in H.items():
    if h.get('srv',0) < 1000: continue
    gg=g.get(k,{}); y=hc.get(k,{})
    c23=y.get('2023') or y.get('2022'); c19=y.get('2019')
    ccr=c23['COST_TO_CHARGE_RATIO'] if c23 else None
    gro=None
    if c23 and c19 and c19['OUTPATIENT_TOTAL_CHARGES'] and c19['TOTAL_COSTS'] and c23['OUTPATIENT_TOTAL_CHARGES'] and c23['TOTAL_COSTS']:
        gro=(c23['OUTPATIENT_TOTAL_CHARGES']/c19['OUTPATIENT_TOTAL_CHARGES'])/(c23['TOTAL_COSTS']/c19['TOTAL_COSTS'])
    rows.append(dict(ccn=k,name=h['name'],st=h['st'],oe=h['out']/h['exp'] if h['exp'] else 0,out=h['out'],exp=h['exp'],srv=h['srv'],osrv=h['osrv'],
                     own=gg.get('HOSPITAL_OWNERSHIP'),type=gg.get('HOSPITAL_TYPE'),stars=gg.get('HOSPITAL_OVERALL_RATING'),ccr=ccr,gro=gro,paychg=h['pay']/h['chg'] if h['chg'] else None))
print('hospitals srv>=1000:', len(rows))
zero=sum(1 for r in rows if r['out']==0); print('zero outlier $:', zero, round(zero/len(rows),3))
top=sorted(rows,key=lambda r:-r['oe'])
q=len(rows)//10
for lab,grp in [('top decile O/E',top[:q]),('rest',top[q:])]:
    print(lab, len(grp), 'median ccr', med([r['ccr'] for r in grp if r['ccr']]), 'median charge growth/cost growth 19-23', med([r['gro'] for r in grp if r['gro']]), 'median pay/charge', med([r['paychg'] for r in grp if r['paychg']]))
own=collections.defaultdict(list)
for r in rows: own[r['own']].append(r)
for o,grp in sorted(own.items(), key=lambda kv:-len(kv[1])):
    tot_out=sum(r['out'] for r in grp); tot_exp=sum(r['exp'] for r in grp)
    print(str(o)[:35].ljust(35), len(grp), 'pooled O/E', round(tot_out/tot_exp,2) if tot_exp else None, 'median O/E', med([r['oe'] for r in grp]), 'share >=3x', round(sum(1 for r in grp if r['oe']>=3)/len(grp),3))
# correlation-ish: O/E decile by ccr tercile
cc=sorted([r for r in rows if r['ccr']], key=lambda r:r['ccr'])
t=len(cc)//3
for lab,grp in [('low ccr (high markup)',cc[:t]),('mid ccr',cc[t:2*t]),('high ccr (low markup)',cc[2*t:])]:
    print(lab, len(grp), 'ccr range', round(grp[0]['ccr'],3), round(grp[-1]['ccr'],3), 'pooled O/E', round(sum(r['out'] for r in grp)/sum(r['exp'] for r in grp),2), 'median O/E', med([r['oe'] for r in grp]))
print('--- top 25 by O/E (srv>=1000)')
for r in top[:25]:
    print(r['ccn'], r['name'][:38], r['st'], 'O/E', round(r['oe'],1), 'out $M', round(r['out']/1e6,2), 'osrv', int(r['osrv']), 'srv', int(r['srv']), r['own'], r['type'], 'stars', r['stars'], 'ccr', r['ccr'], 'gro', round(r['gro'],2) if r['gro'] else None)
json.dump(rows, open('oe_rows.json','w'))
