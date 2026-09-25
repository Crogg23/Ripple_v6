import json, collections, statistics as st
r=json.load(open('S13.json'))
print('rows', len(r), 'distinct NPI', len(set(x['NPI'] for x in r)))
print('NPPES land', sum(1 for x in r if x['ADDR'] is not None), 'PartB land', sum(1 for x in r if x['TOT_MDCR_PYMT_AMT'] is not None))
def yr(x): return int(x['D'][:4])
def win(y): return 'old' if y<=2018 else ('19-21' if y<=2021 else ('22-24' if y<=2024 else '25-26'))
# enrollment counts by state/window
C=collections.defaultdict(collections.Counter)
for x in r: C[x['STATE_CD']][win(yr(x))]+=1
nat=collections.Counter()
for c in C.values(): nat.update(c)
print('national', dict(nat))
for s in ['NY','PR','NJ','TX','CA','FL','PA','GA','OH','IL']:
    print(s, dict(C[s]), 'share 19-21', round(C[s]['19-21']/nat['19-21'],3), 'share 22-24', round(C[s]['22-24']/nat['22-24'],3))
# NY new 2022-2024 suppliers: where, money
ny=[x for x in r if x['STATE_CD']=='NY' and 2022<=yr(x)<=2024]
print('NY 22-24 enrollments', len(ny), 'distinct NPI', len(set(x['NPI'] for x in ny)))
print('  cities', collections.Counter(x['CITY'] for x in ny).most_common(10))
print('  zip', collections.Counter(x['ZIP5'] for x in ny).most_common(8))
print('  officials repeated', [(k,v) for k,v in collections.Counter(x['AO'] for x in ny).most_common(10) if v>1])
print('  addresses repeated', [(k,v) for k,v in collections.Counter(x['ADDR'] for x in ny).most_common(10) if v>1])
paid=[x for x in ny if x['TOT_MDCR_PYMT_AMT']]
print('  with Part B 2024 money', len(paid), 'sum $M', round(sum(x['TOT_MDCR_PYMT_AMT'] for x in paid)/1e6,2))
print('  enum dates', collections.Counter((x['ENUM_DT'] or '')[:4] for x in ny).most_common(8))
print('  multi npi flag', collections.Counter(x['MULTIPLE_NPI_FLAG'] for x in ny))
print('  org name sample', [x['ORG_NAME'] for x in ny][:25])
# per-bene payment: NY new vs NY old vs US new vs US old
def stats(L,lab):
    L=[x for x in L if x['TOT_MDCR_PYMT_AMT'] and x['TOT_BENES']]
    if not L: print(lab,'none'); return
    pb=[x['TOT_MDCR_PYMT_AMT']/x['TOT_BENES'] for x in L]
    print(lab, 'n', len(L), 'sum $M', round(sum(x['TOT_MDCR_PYMT_AMT'] for x in L)/1e6,1), 'median $/bene', round(st.median(pb)), 'median benes', st.median([x['TOT_BENES'] for x in L]), 'median srv/bene', round(st.median([x['TOT_SRVCS']/x['TOT_BENES'] for x in L]),1))
stats([x for x in r if x['STATE_CD']=='NY' and yr(x)<=2021],'NY enrolled <=2021')
stats([x for x in r if x['STATE_CD']=='NY' and 2022<=yr(x)<=2023],'NY enrolled 2022-23')
stats([x for x in r if x['STATE_CD']!='NY' and yr(x)<=2021],'US-ex-NY <=2021')
stats([x for x in r if x['STATE_CD']!='NY' and 2022<=yr(x)<=2023],'US-ex-NY 2022-23')
stats([x for x in r if x['STATE_CD']=='PR'],'PR all')
