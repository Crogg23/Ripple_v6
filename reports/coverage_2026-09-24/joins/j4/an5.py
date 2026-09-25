import csv, statistics as st
rows = list(csv.DictReader(open('q03_county_panel.tsv'), delimiter='\t'))
dim = {r['COUNTY_FIPS']: float(r['POPULATION_2020']) for r in csv.DictReader(open('q04_dim_county.tsv'), delimiter='\t') if r['POPULATION_2020']}
f = lambda x: float(x) if x not in ('', None) else None
for r in rows:
    for k in ['POP0612','DU_ALL','DU','O30','BASE0612','RATE_AVG','DEATHS','Y_OK','ROWS_ALL','BASE2015','Y0612']: r[k] = f(r[k])
base = [r for r in rows if r['POP0612'] and r['DU'] and r['ROWS_ALL'] == 6 and r['Y0612'] == 7]
for r in base:
    r['ppc'] = r['DU']/7/r['POP0612']; r['p20'] = dim.get(r['FIPS'], r['POP0612']); r['nsup']=6-r['Y_OK']; r['d']=r['DEATHS'] or 0
    r['rate'] = (r['d']+5*r['nsup'])/(6*r['p20'])*1e5
big = sorted([r for r in base if r['POP0612']>=20000], key=lambda r:-r['ppc'])
rk = {r['FIPS']:i+1 for i,r in enumerate(big)}
bigr = sorted(big, key=lambda r:-r['rate']); rkr = {r['FIPS']:i+1 for i,r in enumerate(bigr)}
knox = ['47093','47001','47009','47155','47105','47145','47089','47173','47057','47013','47025','47129']
print('county\tpop0612\tpop2020\tpills_per_person_yr\trank_pills_of',len(big),'\toxy30_pills\tod_rate_1924\tsuppressed_years\tdeaths_known\trank_rate\tbaseline0612\tbaseline2015')
for fp in knox:
    r = next(x for x in base if x['FIPS']==fp)
    print(r['COUNTY'], int(r['POP0612']), int(r['p20']), round(r['ppc'],1), rk.get(fp), int(r['O30']), round(r['rate'],1), int(r['nsup']), int(r['d']), rkr.get(fp), r['BASE0612'], r['BASE2015'], sep='\t')
k = next(x for x in base if x['FIPS']=='47093'); print('Knox DU', int(k['DU']), 'DU_ALL', int(k['DU_ALL']), 'O30', int(k['O30']))
print('US pop>=20k median ppc', round(st.median(r['ppc'] for r in big),1), 'median rate', round(st.median(r['rate'] for r in big),1))
tn = [r for r in big if r['ST']=='TN']; print('TN pop>=20k median ppc', round(st.median(r['ppc'] for r in tn),1), 'median rate', round(st.median(r['rate'] for r in tn),1), len(tn))
print('top 10 pills pop>=20k', [(r['COUNTY'], round(r['ppc'],1), round(r['rate'],1)) for r in big[:10]])
