import json, statistics as st
from pathlib import Path
from collections import defaultdict
H = Path(__file__).parent
d = json.load(open(H/'r10_vv_member_month_breaks.json'))
cols = d['cols']; rows = [dict(zip(cols, r)) for r in d['rows']]
print(len(rows), cols)
for r in rows:
    for k in ('ROLLS','YN','NV','PV_YN','PV_BREAK','ANY_BREAK','PROB_N','PROB_LT50','NO_DATE'): r[k] = int(r[k])
print('no_date total', sum(r['NO_DATE'] for r in rows), 'party O rows', sum(r['ROLLS'] for r in rows if r['P']=='O'), 'unmatched nm', sum(r['ROLLS'] for r in rows if r['NM'] is None))
print('party codes', set((r['PARTY_CODE'], r['P']) for r in rows))
# member-congress totals
M = defaultdict(lambda: defaultdict(int)); info = {}
for r in rows:
    k = (r['CONGRESS'], r['CHAMBER'], r['ICPSR'])
    for f in ('ROLLS','YN','NV','PV_YN','PV_BREAK','ANY_BREAK','PROB_N','PROB_LT50'): M[k][f] += r[f]
    info[k] = (r['NM'], r['ST'], r['P'], r['BIO'], r['DIST'])
# peers: congress x chamber x party; members with >= 100 party votes
for cg in ('118','119'):
    for ch in ('House','Senate'):
        for p in ('R','D'):
            ks = [k for k in M if k[0]==cg and k[1]==ch and info[k][2]==p and M[k]['PV_YN']>=100]
            rates = sorted(((M[k]['PV_BREAK']/M[k]['PV_YN'], k) for k in ks), reverse=True)
            vals = [x[0] for x in rates]
            pv = [M[k]['PV_YN'] for k in ks]
            print(f"\n{cg} {ch} {p}: n={len(ks)} median break {st.median(vals):.4f} p90 {sorted(vals)[int(0.9*len(vals))]:.4f} median pv {st.median(pv)}")
            for v,k in rates[:8]:
                print('   ', info[k][0], info[k][1], info[k][4], f"{v:.3f}", M[k]['PV_BREAK'], '/', M[k]['PV_YN'], 'lowprob', M[k]['PROB_LT50'], '/', M[k]['PROB_N'])
json.dump({'|'.join(map(str,k)): dict(v, nm=info[k][0], st=info[k][1], p=info[k][2], bio=info[k][3], dist=info[k][4]) for k,v in M.items()}, open(H/'vv_member_totals.json','w'))
