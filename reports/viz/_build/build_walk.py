import json, csv, math, re
from collections import defaultdict

ROOT = r'c:\Code\Ripple_v6'
SP = r'C:\Users\wroge\AppData\Local\Temp\claude\c--Code-Ripple-v6\6ee210e7-d88d-4de6-85b1-9c5796ff377f\scratchpad'

payload = json.load(open(ROOT + r'\reports\viz\_build\chain\repo_payload.json', encoding='utf-8'))
atlas = json.load(open(ROOT + r'\reports\viz\_build\atlas_data.json', encoding='utf-8'))
anodes = {n['name']: n for n in atlas['nodes']}

# ---- columns ----
cols = defaultdict(dict)
for r in csv.DictReader(open(ROOT + r'\reports\_heavy\columns.csv', encoding='utf-8')):
    if r['db'] == 'LIBRARY_MARTS' and r['schema'] != 'TIMELINE':
        t = r['table'].split('__', 1)[-1]
        cols[t][int(r['ordinal'])] = r['column']
cols = {t: [c for _, c in sorted(d.items())] for t, d in cols.items()}

DESC = {
 'CMTE_ID':'FEC committee ID','CAND_ID':'FEC candidate ID','SUB_ID':"FEC's unique record ID",
 'NAME':'name, as filed','CITY':'city','STATE':'state','ZIP':'ZIP code','ZIP_CODE':'ZIP code',
 'EMPLOYER':'employer, free text','OCCUPATION':'occupation, free text','EIN':'IRS employer ID',
 'TRANSACTION_DT':'date of the transaction','TRANSACTION_AMT':'dollar amount',
 'TRANSACTION_DATE':'date of the transaction','TRANSACTION_TYPE':'kind of transaction',
 'ENTITY_TYPE':'who the party is — person, org, committee','OTHER_ID':'the other committee involved',
 'MEMO_TEXT':'free-text note from the filer','_LOADED_AT':'when Ripple landed this row',
 'CAND_NAME':'candidate name','CMTE_NM':'committee name','CMTE_NAME':'committee name',
 'ADDRESS':'street address','ADDRESS1':'street address','ADDRESS2':'address line 2',
 'COUNTY':'county','FIPS':'county FIPS code','LATITUDE':'latitude','LONGITUDE':'longitude',
 'PHONE':'phone number','COUNTRY':'country','TITLE':'title or role','AMOUNT':'dollar amount',
 'NPI':'national provider ID','CCN':'CMS certification number','CIK':'SEC filer ID',
 'UEI':'federal award entity ID','DUNS':'legacy Dun & Bradstreet ID','FRS_ID':'EPA facility registry ID',
}
def coldesc(c):
    if c in DESC: return DESC[c]
    w = c.lower().replace('_', ' ')
    for pat, rep in [(r'\bdt\b','date'),(r'\bamt\b','amount'),(r'\bnm\b','name'),
                     (r'\bnum\b','number'),(r'\bcd\b','code'),(r'\bid\b','ID'),
                     (r'\bqty\b','quantity'),(r'\bpct\b','percent'),(r'\bdesc\b','description')]:
        w = re.sub(pat, rep, w)
    return w

def human(name):
    t = (anodes.get(name, {}).get('title') or '')
    if t:
        return t.split('--')[0].split(' — ')[0].strip()
    return name.replace('_', ' ').title()

# ---- symmetric adjacency ----
adj = defaultdict(dict)
for a, lst in payload['edges'].items():
    for e in lst:
        b = e['other']
        rec = {'key': e['key'], 'rate': e['rate'], 'tier': e['tier'],
               'cs': e.get('col_self') or '', 'co': e.get('col_other') or ''}
        cur = adj[a].get(b)
        if not cur or rec['rate'] > cur['rate']:
            adj[a][b] = rec
        rev = {'key': e['key'], 'rate': e['rate'], 'tier': e['tier'],
               'cs': e.get('col_other') or '', 'co': e.get('col_self') or ''}
        cur = adj[b].get(a)
        if not cur or rev['rate'] > cur['rate']:
            adj[b][a] = rev

# ---- twins merged globally ----
TWINS = {
 'FED_FEC_BULK_COMMITTEES': 'FED_FEC_COMMITTEES',
 'FED_FEC_BULK_CANDIDATES': 'FED_FEC_CANDIDATES',
 'FED_FEC_BULK_LINKAGES': 'FED_FEC_CAND_CMTE_LINKAGE',
 'FED_EPA_RCRA_FACILITIES': 'FED_EPA_RCRA_RCRA_FACILITIES',
 'FED_EPA_FRS_FULL': 'FED_EPA_FRS_FRS_FACILITIES',
 'FED_USCG_NRC_INCIDENT_REPORTS': 'FED_USCG_NRC_INCIDENTS',
}
twin_note = {}
for a, b in TWINS.items():
    da, db = len(adj.get(a, {})), len(adj.get(b, {}))
    keep, drop = (a, b) if da >= db else (b, a)
    twin_note[keep] = drop
    for n, rec in adj.pop(drop, {}).items():
        if n == keep: continue
        cur = adj[keep].get(n)
        if not cur or rec['rate'] > cur['rate']:
            adj[keep][n] = rec
        adj[n].pop(drop, None)
        cur = adj[n].get(keep)
        if not cur or rec['rate'] > cur['rate']:
            adj[n][keep] = {**rec, 'cs': rec['co'], 'co': rec['cs']}

dropped = set(TWINS) | set(TWINS.values())
kept_names = sorted({t['name'] for t in payload['tables']} - (dropped - set(twin_note)))

# ---- node data ----
MAXC = 40
nodes = {}
for name in kept_names:
    a = anodes.get(name, {})
    clist = cols.get(name, [])[:MAXC]
    extra = max(0, len(cols.get(name, [])) - MAXC)
    d = (a.get('desc') or '')
    if len(d) > 240: d = d[:240] + '…'
    nodes[name] = {
        't': human(name), 'd': d, 'p': a.get('publisher') or '',
        'c': [[c, coldesc(c)] for c in clist], 'x': extra,
        'tw': twin_note.get(name, ''),
    }

edges_out = {a: {b: r for b, r in nb.items() if b in nodes} for a, nb in adj.items() if a in nodes}

data = {'nodes': nodes, 'adj': edges_out, 'start': 'FED_FEC_INDIV_CONTRIBUTIONS'}
blob = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
print('payload bytes:', len(blob.encode('utf-8')))

page = open(SP + r'\walk_template.html', encoding='utf-8').read()
page = page.replace('__DATA__', blob.replace('</', '<\\/'))
open(SP + r'\warehouse-map.html', 'w', encoding='utf-8').write(page)
print('nodes:', len(nodes))
