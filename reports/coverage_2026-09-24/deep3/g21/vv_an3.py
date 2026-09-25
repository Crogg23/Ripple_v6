import json, statistics as st
from pathlib import Path
from collections import defaultdict, Counter
H = Path(__file__).parent
d = json.load(open(H/'r11_vv_rollcall_party_split.json'))
cols = d['cols']; rows = [dict(zip(cols, r)) for r in d['rows']]
for r in rows:
    for k in ('DY','DN','RY','RNAY'): r[k] = int(r[k])
    q = (r['VOTE_QUESTION'] or r['Q2'] or '').strip()
    bill = (r['BILL_NUMBER'] or '').upper()
    ql = q.lower()
    if 'amendment' in ql and 'motion' not in ql: t = 'amendment'
    elif 'speaker' in ql: t = 'speaker'
    elif bill.startswith('PN') or 'nomination' in ql: t = 'nomination'
    elif 'previous question' in ql or (bill.startswith('HRES') and 'resolution' in ql): t = 'rule/procedural'
    elif 'recommit' in ql or 'table' in ql or 'adjourn' in ql or 'journal' in ql or 'motion to proceed' in ql or 'cloture' in ql or 'waive' in ql or 'point of order' in ql or 'instruct' in ql: t = 'motion'
    elif 'suspend' in ql: t = 'suspension'
    elif 'passage' in ql or 'agreeing to the resolution' in ql or 'concur' in ql or 'conference report' in ql or 'joint resolution' in ql or 'veto' in ql: t = 'passage'
    else: t = 'other'
    r['T'] = t; r['Q'] = q
    r['dpos'] = 1 if r['DY']>r['DN'] else (6 if r['DN']>r['DY'] else None)
    r['rpos'] = 1 if r['RY']>r['RNAY'] else (6 if r['RNAY']>r['RY'] else None)
    r['pv'] = r['dpos'] is not None and r['rpos'] is not None and r['dpos'] != r['rpos']
    r['rbrk'] = (r['RNAY'] if r['rpos']==1 else r['RY']) if r['rpos'] else 0
    r['dbrk'] = (r['DN'] if r['dpos']==1 else r['DY']) if r['dpos'] else 0
print('blank question', sum(1 for r in rows if not r['Q']))
print('other questions', Counter(r['Q'] for r in rows if r['T']=='other').most_common(12))
for ch in ('House','Senate'):
    print(f'\n== {ch}: type | 118 rolls, party votes, R break%, D break% || 119 rolls, party votes, R break%, D break%')
    types = sorted({r['T'] for r in rows if r['CHAMBER']==ch})
    for t in types + ['ALL']:
        cells = []
        for cg in ('118','119'):
            rs = [r for r in rows if r['CHAMBER']==ch and r['CONGRESS']==cg and (t=='ALL' or r['T']==t)]
            pv = [r for r in rs if r['pv']]
            rb = sum(r['rbrk'] for r in pv); ryn = sum(r['RY']+r['RNAY'] for r in pv)
            db = sum(r['dbrk'] for r in pv); dyn = sum(r['DY']+r['DN'] for r in pv)
            cells.append(f"{len(rs):4d} {len(pv):4d} R {100*rb/ryn if ryn else 0:5.2f}% D {100*db/dyn if dyn else 0:5.2f}%")
        print(f'{t:16s} | ' + ' || '.join(cells))
    # reweight: 119 R break with 118 type mix
    for p in ('R','D'):
        def rate(cg, t):
            pv = [r for r in rows if r['CHAMBER']==ch and r['CONGRESS']==cg and r['T']==t and r['pv']]
            b = sum(r['rbrk' if p=='R' else 'dbrk'] for r in pv); n = sum((r['RY']+r['RNAY']) if p=='R' else (r['DY']+r['DN']) for r in pv)
            return (b/n if n else None), n
        w118 = {t: rate('118', t)[1] for t in types}
        num = sum(w118[t]*rate('119',t)[0] for t in types if rate('119',t)[0] is not None and w118[t])
        den = sum(w118[t] for t in types if rate('119',t)[0] is not None and w118[t])
        print(f'  {ch} {p}: 119th rate reweighted to 118th vote mix = {100*num/den:.2f}%')
# party-vote share per congress
for ch in ('House','Senate'):
    for cg in ('118','119'):
        rs = [r for r in rows if r['CHAMBER']==ch and r['CONGRESS']==cg]
        print(ch, cg, 'rolls', len(rs), 'party votes', sum(r['pv'] for r in rs), f"{100*sum(r['pv'] for r in rs)/len(rs):.1f}%")
json.dump(rows, open(H/'vv_rollcalls_typed.json','w'))
