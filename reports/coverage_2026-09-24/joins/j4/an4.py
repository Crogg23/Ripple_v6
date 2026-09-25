import csv, collections as C
rows = list(csv.DictReader(open('q06_foodcity_reporters.tsv'), delimiter='\t'))
for r in rows: r['DU']=float(r['DU']); r['O30']=float(r['O30'])
fc = [r for r in rows if r['BUYER'].upper().startswith('FOOD CITY')]
knoxarea = {'47093','47009','47155','47105','47001','47145','47089','47173','47057'}
print('Food City buyer names sample', sorted(set(r['BUYER'] for r in fc))[:8], len(set(r['BUYER_DEA_NO'] for r in fc)))
# store level
st = C.defaultdict(lambda: dict(du=0,o30=0))
for r in fc:
    s = st[(r['BUYER_DEA_NO'], r['BUYER'], r['CITY'], r['ST'], r['FIPS'])]; s['du']+=r['DU']; s['o30']+=r['O30']
stores = sorted(st.items(), key=lambda kv: -kv[1]['o30']/kv[1]['du'])
print('\nTop Food City stores by strong share')
for (id_,nm,city,s_,fips),v in stores[:14]: print(id_,nm,city,s_,fips,int(v['du']),int(v['o30']),round(100*v['o30']/v['du'],1))
cluster = [k for k,v in stores if k[3]=='TN' and v['o30']/v['du']>=0.39]
print('cluster', [(k[0],k[1],k[2]) for k in cluster])
cl_ids = {k[0] for k in cluster}
def roll(sel, label):
    agg = C.defaultdict(lambda: [0,0,set(),set()])
    for r in sel:
        a = agg[(r['FAMILY'], r['REPORTER'], r['REPORTER_DEA_NO'], r['RCITY'], r['RST'], r['RACT'])]; a[0]+=r['DU']; a[1]+=r['O30']; a[2].add(r['BUYER_DEA_NO']); a[3].add((r['Y0'],r['Y1']))
    T = sum(v[0] for v in agg.values()); T30 = sum(v[1] for v in agg.values())
    print(f'\n== {label}: pills {int(T):,} strong oxy {int(T30):,} ({100*T30/T:.1f}%) buyers {len(set(r["BUYER_DEA_NO"] for r in sel))}')
    for k,v in sorted(agg.items(), key=lambda kv:-kv[1][1])[:10]:
        print(k, f'pills {int(v[0]):,}', f'oxy30 {int(v[1]):,}', f'{100*v[1]/T30 if T30 else 0:.1f}% of strong', f'{100*v[1]/v[0]:.1f}% own mix', 'stores', len(v[2]), sorted(v[3]))
roll([r for r in fc if r['BUYER_DEA_NO'] in cl_ids], 'six-store Knoxville-area cluster')
for k in cluster:
    roll([r for r in fc if r['BUYER_DEA_NO']==k[0]], f'store {k[1]} {k[2]}')
roll([r for r in fc if r['ST']=='TN' and r['BUYER_DEA_NO'] not in cl_ids], 'other TN Food City stores')
roll([r for r in rows if r['FIPS']=='47093' and not r['BUYER'].upper().startswith('FOOD CITY')], 'other Knox County pharmacies')
