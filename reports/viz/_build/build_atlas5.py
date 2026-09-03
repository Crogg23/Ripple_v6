import json, math, re
from collections import defaultdict

ROOT = r'c:\Code\Ripple_v6'
BUILD = ROOT + r'\reports\viz\_build'

src = open(BUILD + r'\build_walk.py', encoding='utf-8').read()
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

# colored regions pack the center; UNCHARTED is pushed to the outer rim
colored = [r for r in region_geo if r != 'UNCHARTED']
ritems = sorted(((r, region_geo[r]['rad']) for r in colored), key=lambda kv: -kv[1])
rplaced = pack_circles(ritems, 600)
core_r = max(math.hypot(x, y) + rr for x, y, rr in rplaced.values())
if 'UNCHARTED' in region_geo:
    urad = region_geo['UNCHARTED']['rad']
    ang = math.radians(24)
    ux = (core_r + urad + 900) * math.cos(ang)
    uy = (core_r + urad + 900) * math.sin(ang) * 0.85
    rplaced['UNCHARTED'] = (ux, uy, urad)

minx = min(x - rr for x, y, rr in rplaced.values())
miny = min(y - rr for x, y, rr in rplaced.values())
SXX, SYY = -minx + 600, -miny + 600

gaz, districts_out, panels, myc = {}, [], [], []
for r, dists in groups.items():
    rx, ry, rrad = rplaced[r]
    rx += SXX; ry += SYY
    panels.append({'r': r, 'x': rx, 'y': ry, 'rad': round(rrad), 'n': sum(len(v) for v in dists.values())})
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

json.dump(gaz, open(BUILD + r'\gazetteer.json', 'w', encoding='utf-8'), indent=1)

RIDX = {r: i for i, r in enumerate(['MONEY & POLITICS','FINANCE & CORPORATES','GOVERNMENT','HEALTH','ENVIRONMENT & ENERGY','JUSTICE & ENFORCEMENT','SOCIETY & RESEARCH','UNCHARTED'])}
for n in nodes:
    nodes[n]['ri'] = RIDX.get(region_of(n), 7)
    nodes[n]['gx'], nodes[n]['gy'] = gaz[n]
    nodes[n]['deg'] = len(adj.get(n, {}))
    nodes[n]['s'] = short(n)

# the full join web: every proven edge, drawn once, plus region trunks
FUZZY = {'NAME@ZIP', 'NAME', 'NAME~ADDR'}
GEOK = {'ZIP', 'FIPS', 'GEO_IN', 'STATE', 'COUNTRY', 'COUNTY', 'TRACT', 'CBSA'}
def kidx(k):
    return 2 if k in FUZZY else (1 if k in GEOK else 0)

aweb, trunk_count = [], defaultdict(int)
for a, nbrs in adj.items():
    for b, rec in nbrs.items():
        if a >= b:
            continue
        x1, y1 = gaz[a]; x2, y2 = gaz[b]
        strong = 1 if 0 < rec['rate'] <= 100 else 0
        aweb.append([round(x1), round(y1), round(x2), round(y2), kidx(rec['key']), strong])
        ra, rb = sorted((region_of(a), region_of(b)))
        if ra != rb:
            trunk_count[(ra, rb)] += 1

pcenter = {p['r']: (p['x'], p['y']) for p in panels}
trunks = []
for (ra, rb), cnt in sorted(trunk_count.items(), key=lambda kv: -kv[1]):
    ax, ay = pcenter[ra]; bx, by = pcenter[rb]
    trunks.append([round(ax), round(ay), round(bx), round(by), cnt])

WD = max(x + rr for x, y, rr in rplaced.values()) + SXX + 600
HD = max(y + rr for x, y, rr in rplaced.values()) + SYY + 600
hubs = sorted(nodes, key=lambda n: -nodes[n]['deg'])[:14]
edge_count = len(aweb)
connected = sum(1 for n in nodes if nodes[n]['deg'] > 0)
data = {
    'nodes': nodes, 'adj': adj, 'start': 'FED_FEC_INDIV_CONTRIBUTIONS',
    'panels': panels, 'districts': districts_out, 'hubs': hubs, 'myc': myc,
    'aweb': aweb, 'trunks': trunks,
    'world': [round(WD), round(HD)],
    'core': [round(min(x - rr for x, y, rr in (rplaced[r] for r in colored)) + SXX),
             round(min(y - rr for x, y, rr in (rplaced[r] for r in colored)) + SYY),
             round(max(x + rr for x, y, rr in (rplaced[r] for r in colored)) + SXX),
             round(max(y + rr for x, y, rr in (rplaced[r] for r in colored)) + SYY)],
    'stats': {'tables': len(nodes), 'edges': edge_count, 'regions': len(panels) - 1,
              'connected': connected},
}
blob = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
print('payload bytes:', len(blob.encode('utf-8')))
print('world:', data['world'], 'stats:', data['stats'])

page = open(BUILD + r'\atlas3_template.html', encoding='utf-8').read()
page = page.replace('__DATA__', blob.replace('</', '<\\/'))
open(ROOT + r'\reports\viz\atlas.html', 'w', encoding='utf-8').write(page)
print('wrote reports/viz/atlas.html')
