"""g61 local analysis. Re-derives every headline number in ../g61.md from the qNN.json pulls. No warehouse calls."""
import statistics as st
from collections import Counter, defaultdict
from load import load, num

H = 8784  # hours in 2024
ops, sf, cs, dr, suc = load('q07'), load('q08'), load('q09'), load('q10'), load('q11')
fac = {r['FACILITY_NUMBER']: r for r in load('q12')}
am = load('q14')

print('=== OPERATIONAL: Holly Springs ===')
hs = [r for r in ops if r['UTILITY_NUMBER'] == 8748][0]
src, ret, loss = num(hs['TOTAL_SOURCES_MWH']), num(hs['SALES_TO_ULTIMATE_CUSTOMERS_MWH']), num(hs['TOTAL_ENERGY_LOSSES_MWH'])
rev = num(hs['REVENUE_FROM_RETAIL_SALES_THOUSAND_DOLLARS'])
pk = max(num(hs['SUMMER_PEAK_DEMAND_MW']), num(hs['WINTER_PEAK_DEMAND_MW']))
print('bought', src, 'billed', ret, 'lost', loss, 'loss%', round(100 * loss / src, 1))
print('price c/kWh', round(rev / ret * 100, 2), 'value of lost MWh $M', round(loss * rev / ret / 1000, 2), 'retail revenue $M', rev / 1000)
print('purchase load factor', round(100 * src / (pk * H), 1), 'billed load factor', round(100 * ret / (pk * H), 1))
mun = [(100 * num(r['TOTAL_ENERGY_LOSSES_MWH']) / num(r['TOTAL_SOURCES_MWH']), r['UTILITY_NAME'], r['STATE'])
       for r in ops if r['OWNERSHIP_TYPE'] == 'Municipal' and num(r['TOTAL_ENERGY_LOSSES_MWH']) and num(r['TOTAL_SOURCES_MWH'])]
mun.sort(reverse=True)
print('munis with losses', len(mun), 'median', round(st.median(x[0] for x in mun), 2), 'top3', [(round(a, 1), b, c) for a, b, c in mun[:3]])


def lf(r, col):
    p = max(num(r['SUMMER_PEAK_DEMAND_MW']) or 0, num(r['WINTER_PEAK_DEMAND_MW']) or 0)
    return 100 * (num(r[col]) or 0) / (p * H) if p > 0 else None


for states in (('MS',), ('MS', 'TN', 'AL', 'KY', 'GA')):
    L = [r for r in ops if r['STATE'] in states and r['OWNERSHIP_TYPE'] == 'Municipal' and (num(r['SALES_TO_ULTIMATE_CUSTOMERS_MWH']) or 0) > 0]
    b = sorted((lf(r, 'SALES_TO_ULTIMATE_CUSTOMERS_MWH'), r['UTILITY_NAME']) for r in L if lf(r, 'SALES_TO_ULTIMATE_CUSTOMERS_MWH'))
    s = [lf(r, 'TOTAL_SOURCES_MWH') for r in L if lf(r, 'TOTAL_SOURCES_MWH')]
    ls = [100 * (num(r['TOTAL_ENERGY_LOSSES_MWH']) or 0) / num(r['TOTAL_SOURCES_MWH']) for r in L if num(r['TOTAL_SOURCES_MWH'])]
    print(states, 'n', len(L), 'median purchase LF', round(st.median(s), 1), 'median billed LF', round(st.median(x[0] for x in b), 1),
          'lowest billed', b[0][1], 'median loss%', round(st.median(ls), 2))


def per(r, a, c):
    x, y = num(r[a]), num(r[c])
    return x / y if x and y else None


ms = [r for r in suc if r['STATE'] == 'MS' and r['OWNERSHIP'] == 'Municipal' and r['SERVICE_TYPE'] == 'Bundled']
res = sorted((per(r, 'RESIDENTIAL_SALES_MWH', 'RESIDENTIAL_CUSTOMERS'), r['UTILITY_NAME']) for r in ms if per(r, 'RESIDENTIAL_SALES_MWH', 'RESIDENTIAL_CUSTOMERS'))
com = sorted((per(r, 'COMMERCIAL_SALES_MWH', 'COMMERCIAL_CUSTOMERS'), r['UTILITY_NAME']) for r in ms if per(r, 'COMMERCIAL_SALES_MWH', 'COMMERCIAL_CUSTOMERS'))
print('MS munis residential MWh/customer: n', len(res), 'median', round(st.median(x[0] for x in res), 2), 'lowest', res[0])
print('MS munis commercial MWh/customer: n', len(com), 'median', round(st.median(x[0] for x in com), 1), 'lowest', com[0])
s3 = [r for r in suc if r['STATE'] in ('MS', 'TN', 'AL') and r['OWNERSHIP'] == 'Municipal' and r['SERVICE_TYPE'] == 'Bundled']
v = sorted((per(r, 'RESIDENTIAL_SALES_MWH', 'RESIDENTIAL_CUSTOMERS'), r['UTILITY_NAME']) for r in s3 if per(r, 'RESIDENTIAL_SALES_MWH', 'RESIDENTIAL_CUSTOMERS'))
print('MS/TN/AL munis residential MWh/customer: n', len(v), 'median', round(st.median(x[0] for x in v), 2), 'lowest', v[0])
hsm = [r for r in am if r['UTILITY_NUMBER'] == 8748][0]
print('HS meters', hsm['TOTAL_TOTAL_METERS'], 'AMI', hsm['TOTAL_AMI_METERS'], 'AMI-recorded MWh', hsm['TOTAL_ENERGY_SERVED_AMI_MWH'])
msco = [100 * (num(r['TOTAL_ENERGY_LOSSES_MWH']) or 0) / num(r['TOTAL_SOURCES_MWH']) for r in ops
        if r['STATE'] == 'MS' and r['OWNERSHIP_TYPE'] == 'Cooperative' and num(r['TOTAL_SOURCES_MWH']) and (num(r['SALES_TO_ULTIMATE_CUSTOMERS_MWH']) or 0) > 0]
print('MS co-ops loss%: n', len(msco), 'median', round(st.median(msco), 2))

print('=== OPERATIONAL: free power line ===')
g = defaultdict(list)
for r in ops:
    rt = num(r['SALES_TO_ULTIMATE_CUSTOMERS_MWH']) or 0
    fr = num(r['FURNISHED_WITHOUT_CHARGE_MWH']) or 0
    if rt > 0 and fr > 0:
        g[r['OWNERSHIP_TYPE']].append(100 * fr / rt)
for t in ('Municipal', 'Cooperative', 'Investor Owned'):
    print(t, 'n free>0', len(g[t]), 'median free% of retail', round(st.median(g[t]), 2))
plug = [r for r in ops if (num(r['FURNISHED_WITHOUT_CHARGE_MWH']) or 0) > 0 and (num(r['SALES_TO_ULTIMATE_CUSTOMERS_MWH']) or 0) > 0 and not num(r['TOTAL_ENERGY_LOSSES_MWH'])]
print('free>0 with no losses reported', len(plug))

print('=== SHORT_FORM ===')
rows = [dict(r, price=num(r['REVENUES_THOUSAND_DOLLARS']) / num(r['SALES_MWH']) * 100) for r in sf if num(r['REVENUES_THOUSAND_DOLLARS']) and num(r['SALES_MWH'])]
peer = defaultdict(list)
for x in rows:
    peer[(x['STATE'], x['OWNERSHIP'])].append(x['price'])
out = [(x['price'] / st.median(peer[(x['STATE'], x['OWNERSHIP'])]), x['UTILITY_NAME']) for x in rows if len(peer[(x['STATE'], x['OWNERSHIP'])]) >= 8]
print('priced', len(rows), 'national median', round(st.median(x['price'] for x in rows), 2), 'with >=8 peers', len(out),
      '>=2x', sum(1 for x in out if x[0] >= 2), '>=1.5x', sum(1 for x in out if x[0] >= 1.5))

print('=== CS ===')
agg = defaultdict(lambda: [0, 0, 0, 0])
for r in suc:
    if r['SERVICE_TYPE'] == 'Bundled':
        a = agg[r['STATE']]
        a[0] += num(r['COMMERCIAL_REVENUES_THOUSAND_DOLLARS']) or 0; a[1] += num(r['COMMERCIAL_SALES_MWH']) or 0
        a[2] += num(r['INDUSTRIAL_REVENUES_THOUSAND_DOLLARS']) or 0; a[3] += num(r['INDUSTRIAL_SALES_MWH']) or 0
sp = {s: (a[0] / a[1] * 100 if a[1] else None, a[2] / a[3] * 100 if a[3] else None) for s, a in agg.items()}
cm = [(num(r['COMMERCIAL_REVENUES_THOUSAND_DOLLARS']) / num(r['COMMERCIAL_SALES_MWH']) * 100, sp[r['STATE']][0]) for r in cs
      if r['STATE'] in sp and (num(r['COMMERCIAL_SALES_MWH']) or 0) > 0]
print('commercial rows', len(cm), 'median PPA c/kWh', round(st.median(x[0] for x in cm), 2), 'median state bundled', round(st.median(x[1] for x in cm), 2),
      'pct above state', round(100 * sum(1 for x in cm if x[0] > x[1]) / len(cm)))
tech = Counter()
for r in cs:
    t = fac[r['FACILITY_NUMBER']]['TECH'] or 'NO MATCH'
    tech['gas' if 'Natural Gas' in t else ('solar' if 'Solar' in t else 'other')] += num(r['TOTAL_SALES_MWH'])
tot = sum(tech.values())
print('MWh by tech', {k: (round(v), round(100 * v / tot, 1)) for k, v in tech.items()})
print('join land', sum(1 for r in fac.values() if r['GENS'] > 0), 'of', len(fac))

print('=== DR ===')
T = []
for r in dr:
    t = (num(r['TOTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS']) or 0) + (num(r['TOTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS']) or 0)
    T.append((t, r['TOTAL_ACTUAL_PEAK_DEMAND_SAVINGS_MW'], r))
tot = sum(x[0] for x in T)
blank = [x for x in T if x[0] > 0 and x[1] is None]
zero = [x for x in T if x[0] > 0 and x[1] is not None and num(x[1]) == 0]
print('total spend $M', round(tot / 1000, 1), 'blank actual', len(blank), round(sum(x[0] for x in blank) / 1000, 1),
      'zero actual', len(zero), round(sum(x[0] for x in zero) / 1000, 1))
ind = [r for r in dr if (num(r['TOTAL_POTENTIAL_PEAK_DEMAND_SAVINGS_MW']) or 0) > 0
       and (num(r['INDUSTRIAL_POTENTIAL_PEAK_DEMAND_SAVINGS_MW']) or 0) / num(r['TOTAL_POTENTIAL_PEAK_DEMAND_SAVINGS_MW']) >= 0.8
       and (num(r['TOTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS']) or 0) > 0]
print('industrial-heavy programs', len(ind), 'median $K incentive per potential MW',
      round(st.median(num(r['TOTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS']) / num(r['TOTAL_POTENTIAL_PEAK_DEMAND_SAVINGS_MW']) for r in ind), 1))
