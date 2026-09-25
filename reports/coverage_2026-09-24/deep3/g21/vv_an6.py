import json
from pathlib import Path
from collections import Counter
H = Path(__file__).parent
rows = json.load(open(H/'vv_rollcalls_typed.json'))
for cg in ('118','119'):
    pv = [r for r in rows if r['CHAMBER']=='Senate' and r['CONGRESS']==cg and r['pv']]
    solo = [r for r in pv if r['dbrk']==1]
    fs = [r for r in solo if r['FETT'] in ('1','6') and int(r['FETT'])!=r['dpos']]
    print(cg, 'Senate party votes', len(pv), 'with exactly one D crossing', len(solo), 'of which Fetterman', len(fs))
    # months of Fetterman solo crossings
    print('   by year-month', sorted(Counter(r['VOTE_DATE'][:7] for r in fs).items()))
# Fetterman 119 break rate by half-year
for lo, hi in (('2025-01','2025-06'),('2025-07','2025-12'),('2026-01','2026-06')):
    pv = [r for r in rows if r['CHAMBER']=='Senate' and r['CONGRESS']=='119' and r['pv'] and lo <= r['VOTE_DATE'][:7] <= hi]
    mine = [r for r in pv if r['FETT'] in ('1','6')]
    b = sum(1 for r in mine if int(r['FETT'])!=r['dpos'])
    db = sum(r['dbrk'] for r in pv); dyn = sum(r['DY']+r['DN'] for r in pv)
    print(lo, hi, f'Fetterman {b}/{len(mine)} = {100*b/len(mine):.1f}%  all-D {100*db/dyn:.2f}%')
