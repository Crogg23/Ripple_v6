import csv, statistics as st, math
rows = list(csv.DictReader(open('q03_county_panel.tsv'), delimiter='\t'))
f = lambda x: float(x) if x not in ('', None) else None
for r in rows:
    for k in ['POP0612','DU_ALL','DU','O30','BASE0612','RATE_AVG','DEATHS','POPYRS','Y_OK','ROWS_ALL','Y0612','BASE2015']: r[k] = f(r[k])
print('panel rows', len(rows))
print('no NCHS pop', sum(1 for r in rows if r['POP0612'] is None), [ (r['FIPS'],r['DU_ALL']) for r in rows if r['POP0612'] is None][:40])
print('no ARCOS', sum(1 for r in rows if r['DU'] is None and r['POP0612']))
print('no OD rows', sum(1 for r in rows if r['ROWS_ALL'] is None and r['POP0612']))
base = [r for r in rows if r['POP0612'] and r['DU'] is not None and r['ROWS_ALL']]
print('3-way matched', len(base))
comp = [r for r in base if r['Y_OK'] == 6]
print('complete 6yr', len(comp), 'pop share', sum(r['POP0612'] for r in comp)/sum(r['POP0612'] for r in base))
for r in base: r['ppc'] = r['DU']/7/r['POP0612']; r['ppc_all'] = r['DU_ALL']/7/r['POP0612']
top = sorted(base, key=lambda r: -r['ppc_all'])[:8]
print('top ppc_all', [(r['COUNTY'], round(r['ppc_all']), round(r['ppc'])) for r in top])
top = sorted(base, key=lambda r: -r['ppc'])[:12]
print('top ppc clean', [(r['COUNTY'], round(r['ppc']), r['RATE_AVG']) for r in top])
