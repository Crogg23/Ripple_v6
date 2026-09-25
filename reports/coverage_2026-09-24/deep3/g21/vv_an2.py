import json, statistics as st
from pathlib import Path
from collections import defaultdict
H = Path(__file__).parent
d = json.load(open(H/'r10_vv_member_month_breaks.json'))
cols = d['cols']; rows = [dict(zip(cols, r)) for r in d['rows']]
for r in rows:
    for k in ('ROLLS','YN','NV','PV_YN','PV_BREAK','ANY_BREAK','PROB_N','PROB_LT50','NO_DATE'): r[k] = int(r[k])
    r['MON'] = r['MON'][:7]
def series(match, cg, ch):
    out = {}
    for r in rows:
        if r['CONGRESS']==cg and r['CHAMBER']==ch and r['NM'] and match in r['NM']:
            out[r['MON']] = out.get(r['MON'], (0,0))
            out[r['MON']] = (out[r['MON']][0]+r['PV_BREAK'], out[r['MON']][1]+r['PV_YN'])
    return out
def peer_month(cg, ch, p):
    per = defaultdict(list)
    for r in rows:
        if r['CONGRESS']==cg and r['CHAMBER']==ch and r['P']==p and r['PV_YN']>=5:
            per[r['MON']].append(r['PV_BREAK']/r['PV_YN'])
    return {m: st.median(v) for m,v in per.items()}
for cg, ch, p, names in (('119','House','D',['CUELLAR','GONZALEZ, Vicente','GOLDEN','PEREZ, Marie','DAVIS, Don','GRAY, Adam']),
                          ('119','House','R',['FITZPATRICK','MASSIE','GREENE','BACON','LAWLER']),
                          ('119','Senate','D',['FETTERMAN','SHAHEEN']),
                          ('118','Senate','D',['FETTERMAN'])):
    pm = peer_month(cg, ch, p)
    months = sorted(pm)
    print(f'\n{cg} {ch} {p}  month: peer-median | ' + ' | '.join(names))
    ser = {n: series(n, cg, ch) for n in names}
    for m in months:
        cells = []
        for n in names:
            b, t = ser[n].get(m, (0,0))
            cells.append(f'{b}/{t}' if t else '-')
        print(m, f'{pm[m]:.3f}', ' | '.join(cells))
