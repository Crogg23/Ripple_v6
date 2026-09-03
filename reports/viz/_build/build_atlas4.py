import json, math, re
from collections import defaultdict

ROOT = r'c:\Code\Ripple_v6'
SP = r'C:\Users\wroge\AppData\Local\Temp\claude\c--Code-Ripple-v6\6ee210e7-d88d-4de6-85b1-9c5796ff377f\scratchpad'

src = open(SP + r'\build_walk.py', encoding='utf-8').read()
src = src.split("data = {'nodes'")[0]
ns = {}
exec(compile(src, 'build_walk_core', 'exec'), ns)
nodes = ns['nodes']
adj = {a: {b: r for b, r in nb.items() if b in nodes} for a, nb in ns['adj'].items() if a in nodes}
anodes = ns['anodes']

def region_of(n):
    return (anodes.get(n, {}).get('region') or 'UNCHARTED')

def district_of(n):
    p = nodes[n].get('p') or ''
    if p:
        p = re.sub(r'\s*\([^)]*\)', '', p).strip()
        return p[:38]
    m = re.match(r'(FED|ST|STATE|XC|INTL|IRS527|CA|UT|MO)_([A-Z0-9]+)', n)
    if m:
        return m.group(2)
    return n.split('_')[0]

def short(n):
    t = n
    for p in ('FED_', 'ST_', 'STATE_', 'XC_', 'INTL_'):
        if t.startswith(p): t = t[len(p):]; break
    return t if len(t) <= 26 else t[:25] + '…'

groups = defaultdict(lambda: defaultdict(list))
for n in nodes:
    groups[region_of(n)][district_of(n)].append(n)
for r in list(groups):
    small = [d for d, x in groups[r].items() if len(x) < 3]
    if len(small) > 1:
        merged = []
        for d in small: merged += groups[r].pop(d)
        groups[r]['OTHER SOURCES'] = groups[r].get('OTHER SOURCES', []) + merged
for r in groups:
    for d in groups[r]:
        groups[r][d].sort(key=lambda n: -len(adj.get(n, {})))

GOLD = math.radians(137.507764)
NS = 420

def bloom(k, spacing):
    pts = [(0.0, 0.0)]
    for i in range(1, k):
        r = spacing * math.sqrt(i)
        th = i * GOLD
        pts.append((r * math.cos(th), r * math.sin(th) * 0.85))
    return pts

def pack_circles(items, gap):
    placed = {}
    for idx, (k, rad) in enumerate(items):
        if idx == 0:
            placed[k] = (0.0, 0.0, rad); continue
        j = float(idx)
        while True:
            r = math.sqrt(j) * 900
            x, y = r * math.cos(j * GOLD), r * math.sin(j * GOLD) * 0.85
            if all((x-a)**2 + (y-b)**2 > (rad + rr + gap)**2 for a, b, rr in placed.values()):
                placed[k] = (x, y, rad); break
            j += 0.25
    return placed

dist_geo = {}
for r, dists in groups.items():
    for d, names in dists.items():
        pts = bloom(len(names), NS)
        rad = (max(math.hypot(x, y) for x, y in pts) + NS * 0.9) if len(pts) > 1 else NS
        dist_geo[(r, d)] = (pts, rad)

region_geo = {}
for r, dists in groups.items():
    items = sorted(((d, dist_geo[(r, d)][1]) for d in dists), key=lambda kv: -kv[1])
    placed = pack_circles(items, 240)
    rad = max(math.hypot(x, y) + rr for x, y, rr in placed.values()) + 500
    region_geo[r] = {'dpos': {d: (x, y) for d, (x, y, _) in placed.items()}, 'rad': rad}

ritems = sorted(((r, g['rad']) for r, g in region_geo.items()), key=lambda kv: -kv[1])
rplaced = pack_circles(ritems, 600)
minx = min(x - rr for x, y, rr in rplaced.values())
miny = min(y - rr for x, y, rr in rplaced.values())
SXX, SYY = -minx + 600, -miny + 600

gaz, districts_out, panels, myc = {}, [], [], []
for r, dists in groups.items():
    rx, ry, rrad = rplaced[r]
    rx += SXX; ry += SYY
    panels.append({'r': r, 'x': rx, 'y': ry, 'rad': round(rrad)})
    for d, names in dists.items():
        dx, dy = region_geo[r]['dpos'][d]
        cx, cy = rx + dx, ry + dy
        pts, drad = dist_geo[(r, d)]
        districts_out.append({'d': d, 'x': round(cx), 'y': round(cy - drad - 140), 'n': len(names)})
        for (ox, oy), n in zip(pts, names):
            gaz[n] = [round(cx + ox, 1), round(cy + oy, 1)]
        hubx, huby = gaz[names[0]]
        for n in names[1:]:
            myc.append([gaz[n][0], gaz[n][1], hubx, huby])

for r_, dists_ in groups.items():
    dh = [gaz[names_[0]] for d_, names_ in sorted(dists_.items(), key=lambda kv: -len(kv[1]))]
    for hh in dh[1:]:
        myc.append([hh[0], hh[1], dh[0][0], dh[0][1]])

json.dump(gaz, open(ROOT + r'\reports\viz\_build\gazetteer.json', 'w', encoding='utf-8'), indent=1)

RIDX = {r: i for i, r in enumerate(['MONEY & POLITICS','FINANCE & CORPORATES','GOVERNMENT','HEALTH','ENVIRONMENT & ENERGY','JUSTICE & ENFORCEMENT','SOCIETY & RESEARCH','UNCHARTED'])}
for n in nodes:
    nodes[n]['ri'] = RIDX.get(region_of(n), 7)
    nodes[n]['gx'], nodes[n]['gy'] = gaz[n]
    nodes[n]['deg'] = len(adj.get(n, {}))
    nodes[n]['s'] = short(n)

WD = max(x + rr for x, y, rr in rplaced.values()) + SXX + 600
HD = max(y + rr for x, y, rr in rplaced.values()) + SYY + 600
hubs = sorted(nodes, key=lambda n: -nodes[n]['deg'])[:14]
data = {
    'nodes': nodes, 'adj': adj, 'start': 'FED_FEC_INDIV_CONTRIBUTIONS',
    'panels': panels, 'districts': districts_out, 'hubs': hubs, 'myc': myc,
    'world': [round(WD), round(HD)],
}
blob = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
print('payload bytes:', len(blob.encode('utf-8')))
print('world:', data['world'], 'districts:', len(districts_out))

page = open(SP + r'\atlas2_template.html', encoding='utf-8').read()
page = page.replace('__DATA__', blob.replace('</', '<\\/'))
open(SP + r'\warehouse-map.html', 'w', encoding='utf-8').write(page)
