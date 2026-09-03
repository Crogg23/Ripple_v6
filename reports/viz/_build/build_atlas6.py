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

# ---- one organism: every district is a limb growing from a single root ----
ORDER = ['MONEY & POLITICS','FINANCE & CORPORATES','GOVERNMENT','HEALTH',
         'ENVIRONMENT & ENERGY','JUSTICE & ENFORCEMENT','SOCIETY & RESEARCH','UNCHARTED']
regions = [r for r in ORDER if r in groups]
total = sum(len(v) for dd in groups.values() for v in dd.values())
GAPA = math.radians(3)
span_total = 2 * math.pi - GAPA * len(regions)
SQ = 0.88  # vertical squash

limb = {}          # (r, d) -> (angle, length)
region_mid = {}
theta = -math.pi / 2
for r in regions:
    cnt = sum(len(v) for v in groups[r].values())
    span = span_total * cnt / total
    region_mid[r] = theta + span / 2
    dists = sorted(groups[r].items(), key=lambda kv: -len(kv[1]))
    a = theta
    for i, (d, names) in enumerate(dists):
        dspan = span * len(names) / cnt
        drad = dist_geo[(r, d)][1]
        L = 5200 + drad + 2600 * math.sqrt(len(names) / 40) + (i % 3) * 1600
        limb[(r, d)] = (a + dspan / 2, L)
        a += dspan
    theta += span + GAPA

reach = max(L + dist_geo[k][1] for k, (ang, L) in limb.items())
RX = reach + 900
ROOTX, ROOTY = RX, RX * SQ + 900

gaz, districts_out, panels, myc = {}, [], [], []
limb_end = {}
for (r, d), (ang, L) in limb.items():
    cx = ROOTX + L * math.cos(ang)
    cy = ROOTY + L * math.sin(ang) * SQ
    limb_end[(r, d)] = (cx, cy)
    pts, drad = dist_geo[(r, d)]
    names = groups[r][d]
    districts_out.append({'d': d, 'x': round(cx), 'y': round(cy - drad - 140), 'n': len(names)})
    for (ox, oy), n in zip(pts, names):
        gaz[n] = [round(cx + ox, 1), round(cy + oy, 1)]
    hubx, huby = gaz[names[0]]
    for n in names[1:]:
        myc.append([gaz[n][0], gaz[n][1], hubx, huby])
    # the limb itself: root to this district's hub
    myc.append([round(ROOTX), round(ROOTY), hubx, huby])

for r in regions:
    ends = [limb_end[(r, d)] for d in groups[r]]
    exs = [e[0] for e in ends]; eys = [e[1] for e in ends]
    pcx, pcy = sum(exs) / len(exs), sum(eys) / len(eys)
    spread = max(math.hypot(ex - pcx, ey - pcy) for ex, ey in ends) + 2200
    cang = math.atan2((pcy - ROOTY) / SQ, pcx - ROOTX)
    Lmax = max(limb[(r, d)][1] + dist_geo[(r, d)][1] for d in groups[r])
    lx = ROOTX + (Lmax + 1600) * math.cos(cang)
    ly = ROOTY + (Lmax + 1600) * math.sin(cang) * SQ
    panels.append({'r': r, 'x': round(lx), 'y': round(ly), 'rad': round(spread),
                   'n': sum(len(v) for v in groups[r].values())})

rings = [round(reach * f) for f in (0.33, 0.55, 0.77, 1.0)]

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

WD = round(ROOTX * 2)
HD = round(ROOTY * 2)
hubs = sorted(nodes, key=lambda n: -nodes[n]['deg'])[:14]
edge_count = len(aweb)
connected = sum(1 for n in nodes if nodes[n]['deg'] > 0)
data = {
    'nodes': nodes, 'adj': adj, 'start': 'FED_FEC_INDIV_CONTRIBUTIONS',
    'panels': panels, 'districts': districts_out, 'hubs': hubs, 'myc': myc,
    'aweb': aweb, 'trunks': [],
    'root': [round(ROOTX), round(ROOTY)], 'rings': rings, 'sq': SQ,
    'world': [WD, HD],
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
