import json, statistics as st
from pathlib import Path
from collections import defaultdict, Counter
H = Path(__file__).parent
rows = json.load(open(H/'vv_rollcalls_typed.json'))
# Fetterman by type, both congresses, vs D aggregate
for cg in ('118','119'):
    print(f'\nFetterman {cg} Senate: type | his breaks/yn on party votes | all-D break rate')
    for t in ('nomination','amendment','motion','passage','other','ALL'):
        pv = [r for r in rows if r['CHAMBER']=='Senate' and r['CONGRESS']==cg and r['pv'] and (t=='ALL' or r['T']==t)]
        mine = [r for r in pv if r['FETT'] in ('1','6')]
        brk = sum(1 for r in mine if int(r['FETT']) != r['dpos'])
        db = sum(r['dbrk'] for r in pv); dyn = sum(r['DY']+r['DN'] for r in pv)
        print(f"  {t:12s} {brk}/{len(mine)} = {100*brk/len(mine) if mine else 0:.1f}% | D {100*db/dyn if dyn else 0:.2f}%")
# Fetterman: party votes where he was the ONLY D to break (decisive-ish) in 119
solo = [r for r in rows if r['CHAMBER']=='Senate' and r['CONGRESS']=='119' and r['pv'] and r['FETT'] in ('1','6') and int(r['FETT'])!=r['dpos'] and r['dbrk']==1]
print('\n119 party votes where Fetterman was the only Democrat to cross:', len(solo))
for r in solo[:40]: print('  ', r['VOTE_DATE'], r['T'], r['Q'][:30], r['BILL_NUMBER'], (r['DESCR'] or '')[:70], 'margin', r['DY']+r['RY'], '-', r['DN']+r['RNAY'])
# how many of 119 party votes his cross changed the outcome? yeas vs nays margin <=1 with his vote on winning side
close = [r for r in rows if r['CHAMBER']=='Senate' and r['CONGRESS']=='119' and r['pv'] and r['FETT'] in ('1','6') and int(r['FETT'])!=r['dpos'] and abs((r['DY']+r['RY'])-(r['DN']+r['RNAY']))<=2]
print('close (margin<=2) party votes where he crossed:', len(close))
for r in close: print('  ', r['VOTE_DATE'], r['Q'][:30], r['BILL_NUMBER'], (r['DESCR'] or '')[:70], r['DY']+r['RY'], '-', r['DN']+r['RNAY'], 'result', r['VOTE_RESULT'])
# House amendment roll calls by month, first 18 months of each Congress
import datetime
for cg, start in (('118', '2023-01'), ('119', '2025-01')):
    c = Counter(); allc = Counter()
    for r in rows:
        if r['CHAMBER']=='House' and r['CONGRESS']==cg:
            m = r['VOTE_DATE'][:7]; allc[m]+=1
            if r['T']=='amendment': c[m]+=1
    y0 = int(start[:4]); months = [f"{y0 + (i//12)}-{(i%12)+1:02d}" for i in range(18)]
    print(f'\nHouse {cg} first 18 months: amendment rolls {sum(c[m] for m in months)}, all rolls {sum(allc[m] for m in months)}; by month:', [(m[2:], c[m]) for m in months if c[m]])
    print('  whole congress amendment', sum(c.values()), 'all', sum(allc.values()))
# which bills got the House amendment votes in 119
am = Counter((r['BILL_NUMBER']) for r in rows if r['CHAMBER']=='House' and r['CONGRESS']=='119' and r['T']=='amendment')
print('119 House amendment votes by bill:', am.most_common(10))
am8 = Counter((r['BILL_NUMBER']) for r in rows if r['CHAMBER']=='House' and r['CONGRESS']=='118' and r['T']=='amendment')
print('118 House amendment votes by bill:', am8.most_common(12))
