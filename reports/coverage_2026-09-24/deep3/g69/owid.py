"""Local analysis of q14.json (OWID refugees by country of origin)."""
import json, re, statistics
from collections import Counter, defaultdict
d = json.load(open('q14.json', encoding='utf-8'))
rows = d['rows']
print('rows', len(rows))
bad = [r for r in rows if r[3] is None or not re.fullmatch(r'-?\d+(\.\d+)?', str(r[3]).strip())]
print('non-numeric refugee values', len(bad), bad[:8])
yrs = [r[2] for r in rows]
print('year non-4-digit', sum(1 for y in yrs if not re.fullmatch(r'\d{4}', str(y))), 'range', min(yrs), max(yrs))
print('dup entity-year', sum(1 for k, n in Counter((r[0], r[2]) for r in rows).items() if n > 1))
nocode = Counter(r[0] for r in rows if not r[1])
print('entities without code', len(nocode), nocode.most_common(20))
owidcodes = Counter(r[0] for r in rows if r[1] and r[1].startswith('OWID'))
print('OWID_ codes', owidcodes)
reg = Counter(r[4] for r in rows)
print('regions', reg)
val = {}
for r in rows:
    try: val[(r[0], int(r[2]))] = float(r[3])
    except: pass
ctry = sorted({r[0] for r in rows if r[1] and not r[1].startswith('OWID')})
print('countries with ISO code', len(ctry))
region_of = {r[0]: r[4] for r in rows if r[4]}
# World series
for y in range(1990, 2025):
    w = val.get(('World', y)); s = sum(val.get((c, y), 0) for c in ctry)
    if y % 5 == 0 or y >= 2019: print('year', y, 'World', w, 'sum ISO countries', s, 'n countries', sum(1 for c in ctry if (c, y) in val))
# last year per country
last = {c: max(y for (e, y) in val if e == c) for c in ctry}
stop = sorted([(last[c], c) for c in ctry if last[c] < 2024])
print('series stopping before 2024:', len(stop), stop[:30])
# top 2024, change vs 2019, peak
def v(c, y): return val.get((c, y))
tab = []
for c in ctry:
    a, b = v(c, 2019), v(c, 2024)
    pk = max(((val[(c, y)], y) for (e, y) in val if e == c), default=(None, None))
    tab.append((c, region_of.get(c), a, b, pk))
tab.sort(key=lambda t: -(t[3] or 0))
w24 = sum(val.get((e, 2024), 0) for e in {r[0] for r in rows}); print('all-entity total 2024', w24, 'no-code 2024', {e: val.get((e,2024)) for e in ['Unknown Origin','Tibetan','Serbia and Kosovo','Stateless']})
print('\nTOP 15 2024 (share of World)')
for t in tab[:15]: print(t[0], t[1], '2019', t[2], '2024', t[3], 'share', round(100 * (t[3] or 0) / w24, 1), 'peak', t[4])
top5 = sum((t[3] or 0) for t in tab[:5]); print('top5 share of world 2024', round(100 * top5 / w24, 1))
print('\nBIGGEST ABS RISE 2019->2024')
for t in sorted(tab, key=lambda t: -((t[3] or 0) - (t[2] or 0)))[:12]: print(t[0], t[1], t[2], t[3], round((t[3] or 0) - (t[2] or 0)))
print('\nBIGGEST ABS FALL 2019->2024')
for t in sorted(tab, key=lambda t: ((t[3] or 0) - (t[2] or 0)))[:8]: print(t[0], t[1], t[2], t[3], round((t[3] or 0) - (t[2] or 0)))
# peer: within region, median 2019->2024 ratio among countries with >=10k in 2019
print('\nPEER: ratio 2024/2019 within region, countries with >=10k in 2019')
byreg = defaultdict(list)
for t in tab:
    if t[2] and t[2] >= 10000 and t[3] is not None: byreg[t[1]].append((round(t[3] / t[2], 2), t[0], t[2], t[3]))
for rg, L in byreg.items():
    L.sort(reverse=True); med = statistics.median(x[0] for x in L)
    print(rg, 'n', len(L), 'median ratio', med, 'top', L[:3], 'bottom', L[-2:])
# US hemisphere peers for EOIR nationalities
print('\nEOIR nationalities, OWID refugees 2019 / 2022 / 2024')
for c in ['Venezuela','Colombia','Nicaragua','Ecuador','Cuba','India','Peru','China','Russia','Uzbekistan','Mexico','Honduras','Guatemala','El Salvador','Haiti']:
    print(c, v(c, 2019), v(c, 2022), v(c, 2024))
# single-year spikes: year-over-year jump >5x from >=1000 and falling back
print('\nONE-YEAR SPIKES (>=5x prior year, prior>=1000, next year < half of spike)')
for c in ctry:
    for y in range(1961, 2024):
        a, b, n = v(c, y - 1), v(c, y), v(c, y + 1)
        if a and b and n and a >= 1000 and b >= 5 * a and n < b / 2: print(c, y - 1, a, y, b, y + 1, n)
