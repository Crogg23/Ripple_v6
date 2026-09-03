"""Gravity settle: the layout emerges from the joins themselves.

Joined tables pull each other, all tables push apart, everything drifts
toward the center. 900 cooled ticks, deterministic seed. Isolated tables
ring the settled core afterward, grouped by region angle.
"""
import json, math, re
import numpy as np
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

def short(n):
    t = n
    for p in ('FED_', 'ST_', 'STATE_', 'XC_', 'INTL_'):
        if t.startswith(p): t = t[len(p):]; break
    return t if len(t) <= 26 else t[:25] + '…'

names = sorted(nodes)
idx = {n: i for i, n in enumerate(names)}
N = len(names)
deg = {n: len(adj.get(n, {})) for n in names}
conn = [n for n in names if deg[n] > 0]
iso = [n for n in names if deg[n] == 0]
ci = [idx[n] for n in conn]

# edge springs, weight by rate health (fanout and zero-rate get weak springs)
springs = []
for a, nb in adj.items():
    for b, rec in nb.items():
        if a >= b: continue
        r = rec['rate']
        w = 1.0 if 0 < r <= 100 else 0.25
        # hubs should not glue the world together: pull fades with degree
        w /= (min(deg[a], deg[b])) ** 0.35
        springs.append((idx[a], idx[b], w))
ei = np.array([[s[0] for s in springs], [s[1] for s in springs]])
ew = np.array([s[2] for s in springs])

rng = np.random.default_rng(42)
pos = rng.standard_normal((N, 2)) * 3.0
# seed connected nodes near center, isolates far out so they don't disturb
for n in iso:
    pos[idx[n]] *= 30.0

P = pos[ci].copy()
M = len(ci)
sub = {idx[n]: k for k, n in enumerate(conn)}
sei = np.array([[sub[a] for a, b, w in springs], [sub[b] for a, b, w in springs]])

REP, SPR, GRAV, L0 = 4.0, 0.035, 0.006, 2.4
mass = (np.array([deg[n] for n in conn], float) + 1.0) ** 0.75
mm = mass[:, None] * mass[None, :]
for it in range(900):
    cool = 1.0 - it / 900
    d = P[:, None, :] - P[None, :, :]
    dist2 = (d ** 2).sum(-1) + 0.01
    rep = (REP * mm / dist2)[:, :, None] * d
    F = rep.sum(1)
    dv = P[sei[0]] - P[sei[1]]
    dl = np.sqrt((dv ** 2).sum(-1)) + 0.01
    # spring with a rest length: past L0 it pulls, inside L0 it pushes
    pull = (SPR * ew * (1 - L0 / dl))[:, None] * dv
    np.add.at(F, sei[1], pull)
    np.add.at(F, sei[0], -pull)
    F -= GRAV * P
    step = np.clip(F, -6, 6) * cool
    P += step

# scale the settled core to world units
P -= P.mean(0)
rads = np.hypot(P[:, 0], P[:, 1])
core_r = float(np.percentile(rads, 92))
SCALE = 13500 / core_r
P *= SCALE
# rein in stray outliers so one loner cannot dwarf the frame
rads = np.hypot(P[:, 0], P[:, 1])
over = rads > 16500
P[over] *= (16500 / rads[over])[:, None]

# isolates: ring around the core, ordered by region then name
ring_r = float(np.hypot(P[:, 0], P[:, 1]).max()) + 3400
ORDER = ['MONEY & POLITICS','FINANCE & CORPORATES','GOVERNMENT','HEALTH',
         'ENVIRONMENT & ENERGY','JUSTICE & ENFORCEMENT','SOCIETY & RESEARCH','UNCHARTED']
iso.sort(key=lambda n: (ORDER.index(region_of(n)) if region_of(n) in ORDER else 9, n))
iso_pos = {}
for k, n in enumerate(iso):
    ang = 2 * math.pi * k / max(1, len(iso)) - math.pi / 2
    rr = ring_r + (k % 3) * 1300
    iso_pos[n] = (rr * math.cos(ang), rr * math.sin(ang) * 0.9)

ext = ring_r + 2 * 1300 + 2600
CXW = CYW = ext + 400
gaz = {}
for k, n in enumerate(conn):
    gaz[n] = [round(float(P[k, 0]) + CXW, 1), round(float(P[k, 1]) * 0.9 + CYW, 1)]
for n, (x, y) in iso_pos.items():
    gaz[n] = [round(x + CXW, 1), round(y + CYW, 1)]

json.dump(gaz, open(BUILD + r'\gazetteer.json', 'w', encoding='utf-8'), indent=1)

RIDX = {r: i for i, r in enumerate(ORDER)}
for n in nodes:
    nodes[n]['ri'] = RIDX.get(region_of(n), 7)
    nodes[n]['gx'], nodes[n]['gy'] = gaz[n]
    nodes[n]['deg'] = deg[n]
    nodes[n]['s'] = short(n)

# region label anchors: centroid + spread of each region's settled members
panels = []
for r in ORDER:
    mem = [n for n in conn if region_of(n) == r]
    src_pts = mem if mem else [n for n in iso if region_of(n) == r]
    if not src_pts: continue
    xs = [gaz[n][0] for n in src_pts]; ys = [gaz[n][1] for n in src_pts]
    pcx, pcy = sum(xs) / len(xs), sum(ys) / len(ys)
    spread = max(math.hypot(x - pcx, y - pcy) for x, y in zip(xs, ys)) + 1400
    total_r = sum(1 for n in names if region_of(n) == r)
    panels.append({'r': r, 'x': round(pcx), 'y': round(pcy - spread * 0.75),
                   'rad': round(spread), 'n': total_r})

FUZZY = {'NAME@ZIP', 'NAME', 'NAME~ADDR'}
GEOK = {'ZIP', 'FIPS', 'GEO_IN', 'STATE', 'COUNTRY', 'COUNTY', 'TRACT', 'CBSA'}
def kidx(k):
    return 2 if k in FUZZY else (1 if k in GEOK else 0)

aweb = []
for a, nb in adj.items():
    for b, rec in nb.items():
        if a >= b: continue
        x1, y1 = gaz[a]; x2, y2 = gaz[b]
        strong = 1 if 0 < rec['rate'] <= 100 else 0
        aweb.append([round(x1), round(y1), round(x2), round(y2), kidx(rec['key']), strong, a, b])

WD, HD = round(CXW * 2), round(CYW * 2)
hubs = sorted(nodes, key=lambda n: -nodes[n]['deg'])[:14]
edge_count = len(aweb)
connected = len(conn)
data = {
    'nodes': nodes, 'adj': adj, 'start': 'FED_FEC_INDIV_CONTRIBUTIONS',
    'panels': panels, 'districts': [], 'hubs': hubs, 'myc': [],
    'aweb': aweb, 'trunks': [],
    'world': [WD, HD],
    'stats': {'tables': len(nodes), 'edges': edge_count, 'regions': len(panels) - 1,
              'connected': connected},
}
blob = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
print('payload bytes:', len(blob.encode('utf-8')))
print('world:', data['world'], 'stats:', data['stats'])

import sys
TPL = sys.argv[1] if len(sys.argv) > 1 else 'atlas3_template.html'
page = open(BUILD + '\\' + TPL, encoding='utf-8').read()
page = page.replace('__DATA__', blob.replace('</', '<\\/'))
open(ROOT + r'\reports\viz\atlas.html', 'w', encoding='utf-8').write(page)
print('wrote reports/viz/atlas.html')
