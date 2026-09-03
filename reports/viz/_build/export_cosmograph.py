"""Cut Cosmograph drop-files from the proven-join data.

Two CSVs: edges (source, target, join key, rate, tier, class) and
nodes (id, region, publisher, degree, connected flag). Drop the edges
file into cosmograph.app; add the nodes file as metadata.
"""
import csv, math
ROOT = r'c:\Code\Ripple_v6'
BUILD = ROOT + r'\reports\viz\_build'

src = open(BUILD + r'\build_walk.py', encoding='utf-8').read()
src = src.split("data = {'nodes'")[0]
ns = {}
exec(compile(src, 'build_walk_core', 'exec'), ns)
nodes = ns['nodes']
adj = {a: {b: r for b, r in nb.items() if b in nodes} for a, nb in ns['adj'].items() if a in nodes}
anodes = ns['anodes']

FUZZY = {'NAME@ZIP', 'NAME', 'NAME~ADDR'}
GEOK = {'ZIP', 'FIPS', 'GEO_IN', 'STATE', 'COUNTRY', 'COUNTY', 'TRACT', 'CBSA'}
def jclass(k):
    return 'name-match' if k in FUZZY else ('geography' if k in GEOK else 'identity')

with open(ROOT + r'\reports\viz\cosmograph_edges.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['source', 'target', 'join_key', 'overlap_rate', 'tier', 'join_class'])
    n_edges = 0
    for a, nb in adj.items():
        for b, rec in nb.items():
            if a >= b:
                continue
            w.writerow([a, b, rec['key'], rec['rate'], rec['tier'], jclass(rec['key'])])
            n_edges += 1

with open(ROOT + r'\reports\viz\cosmograph_nodes.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['id', 'region', 'publisher', 'degree', 'connected'])
    for n in sorted(nodes):
        deg = len(adj.get(n, {}))
        w.writerow([n, (anodes.get(n, {}).get('region') or 'UNCHARTED'),
                    nodes[n].get('p') or '', deg, 1 if deg else 0])

print('edges:', n_edges, 'nodes:', len(nodes))
