import json, statistics as st
from pathlib import Path
from collections import defaultdict
H = Path(__file__).parent
d = json.load(open(H/'r04_medsl_all.json'))
rows = [dict(zip(d['cols'], r)) for r in d['rows']]
g = defaultdict(lambda: {'tot':0,'maj':0,'total':0})
for r in rows:
    k = (r['ELECTION_YEAR'], r['STATE_ABBR'])
    v = int(r['CANDIDATE_VOTES'])
    g[k]['tot'] += v
    if r['PARTY'] in ('democrat','republican') or r['CANDIDATE_NAME'] in ('Clinton, Hillary','Trump, Donald J.','Obama, Barack H.','Romney, Mitt'):
        g[k]['maj'] += v
years = sorted({k[0] for k in g})
print('year | median state third-party share | top 3 states')
for y in years:
    sh = sorted(((1-g[k]['maj']/g[k]['tot']), k[1]) for k in g if k[0]==y)
    print(y, f'{100*st.median([s for s,_ in sh]):.1f}%', [(s2, f'{100*s:.1f}%') for s,s2 in sh[-3:]])
# party label check for major candidates (fusion / blank party on major candidates)
odd = [(r['ELECTION_YEAR'], r['STATE_ABBR'], r['CANDIDATE_NAME'], r['PARTY'], r['CANDIDATE_VOTES']) for r in rows if r['CANDIDATE_NAME'] in ('Trump, Donald J.','Clinton, Hillary') and r['PARTY'] not in ('democrat','republican')]
print('2016 major candidates on other lines:', len(odd), odd[:8])
# turnout growth 2012->2016 by state vs median
t = {k: g[k]['tot'] for k in g}
ch = sorted(((t[('2016',s)]/t[('2012',s)]-1), s) for (y,s) in g if y=='2016')
print('2012->2016 total votes change: median %.1f%%' % (100*st.median([c for c,_ in ch])), 'low', [(s, f'{100*c:.1f}%') for c,s in ch[:3]], 'high', [(s, f'{100*c:.1f}%') for c,s in ch[-3:]])
