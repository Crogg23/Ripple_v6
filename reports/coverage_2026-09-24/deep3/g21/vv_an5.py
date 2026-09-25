import json
from pathlib import Path
from collections import Counter, defaultdict
H = Path(__file__).parent
d = json.load(open(H/'r14_vv_senate119_close_and_warpowers.json'))
rows = [dict(zip(d['cols'], r)) for r in d['rows']]
for r in rows:
    for k in ('DY','DN','RY','RNAY','DPOS','RPOS'): r[k] = int(r[k]) if r[k] is not None else None
    r['Y'] = r['DY']+r['RY']; r['N'] = r['DN']+r['RNAY']
    r['X'] = [x.strip() for x in (r['CROSSERS'] or '').split(';') if x.strip()]
    r['wp'] = 'hostilities' in (r['DESCR'] or '')
    q = r['VOTE_QUESTION'].lower()
    r['needs60'] = ('cloture' in q) and not (r['BILL_NUMBER'] or '').startswith('PN')
def outcome(y, n, rpos):
    if y > n: return 1
    if n > y: return 6
    return rpos  # tie: VP (R) sides with R majority
piv = Counter(); pivrows = defaultdict(list); crossn = Counter()
for r in rows:
    if r['needs60'] or r['DPOS'] is None or r['RPOS'] is None or r['DPOS']==r['RPOS']: continue
    base = outcome(r['Y'], r['N'], r['RPOS'])
    for x in r['X']:
        crossn[x]+=1
        p = 'R' if '(R-' in x else 'D'
        partypos = r['RPOS'] if p=='R' else r['DPOS']
        # crosser voted opposite of party pos; flip them
        y, n = r['Y'], r['N']
        if partypos == 1: y, n = y+1, n-1
        else: y, n = y-1, n+1
        if outcome(y, n, r['RPOS']) != base:
            piv[x]+=1; pivrows[x].append((r['VOTE_DATE'], r['BILL_NUMBER'], r['VOTE_QUESTION'][:28], f"{r['Y']}-{r['N']}", r['VOTE_RESULT'], len(r['X'])))
print('pivotal crossings (simple-majority party votes, flip alone changes outcome):')
for x,n in piv.most_common(15): print(' ', n, x)
for x in [k for k,_ in piv.most_common(4)]:
    print('\n', x)
    for t in pivrows[x]: print('   ', t)
print('\n=== war powers roll calls, 119th Senate')
wp = [r for r in rows if r['wp']]
print('count', len(wp), 'results', Counter(r['VOTE_RESULT'] for r in wp))
for r in wp:
    fet = [x for x in r['X'] if 'FETTERMAN' in x]
    print(r['VOTE_DATE'], r['RN'], r['VOTE_QUESTION'][:26], r['BILL_NUMBER'], f"{r['Y']}-{r['N']}", r['VOTE_RESULT'][:26], '| D', r['DY'],'-',r['DN'], 'R', r['RY'],'-',r['RNAY'], '| X:', '; '.join(x.split(',')[0]+x[x.index('('):] for x in r['X']), '| NV:', r['NOT_VOTING'])
# distinct war-powers targets
print()
for b, desc in sorted({(r['BILL_NUMBER'], r['DESCR'][60:200]) for r in wp}): print(b, desc)
