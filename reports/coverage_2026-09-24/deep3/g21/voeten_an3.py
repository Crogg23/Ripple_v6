import json, statistics as st
from pathlib import Path
H = Path(__file__).parent
d = json.load(open(H/'r09_voeten_country_session.json'))
cols = d['cols']; rows = [dict(zip(cols, r)) for r in d['rows']]
def f(x): return None if x in (None, '') else float(x)
for r in rows:
    for k in ('S','Y','C','N_PARTNERS'): r[k] = int(float(r[k]))
    for k in ('AVG_ALL','AG_US','AG_CHN','AG_RUS','AG_ISR','AG_UK','AG_FRA','AG_GER','AG_IND','IP','NV'): r[k] = f(r[k])
by = {(r['S'], r['C']): r for r in rows}
print('IP null:', [(r['S'], r['C'], r['NV']) for r in rows if r['IP'] is None])
for c in (160, 450, 403, 950, 437, 54, 540, 983, 60, 2, 666, 640):
    print(c, [(s, by[(s,c)]['NV'], round(by[(s,c)]['AG_US'],3) if by[(s,c)]['AG_US'] is not None else None, round(by[(s,c)]['AVG_ALL'],3)) for s in (76,77,78,79) if (s,c) in by])
# NV distribution session 79
nv79 = sorted(r['NV'] for r in rows if r['S']==79)
print('nv79 median', st.median(nv79), 'min', nv79[:10], 'max', nv79[-3:])
# Ranking of ARG among countries with NV >= 60 on avg_all in 79
full = sorted(((r['AVG_ALL'], r['C'], r['NV']) for r in rows if r['S']==79 and r['NV'] >= 60))
print('lowest avg_all nv>=60, 2024:', full[:6])
# ag_us rise 23->24, only nv>=60 in both
jumps = []
for r in rows:
    if r['S']==79 and r['C']!=2 and (78,r['C']) in by and r['NV']>=60 and by[(78,r['C'])]['NV']>=60:
        jumps.append((round(r['AG_US']-by[(78,r['C'])]['AG_US'],3), r['C']))
jumps.sort()
print('n', len(jumps), 'median', st.median([j[0] for j in jumps]), 'top rises', jumps[-5:], 'top falls', jumps[:5])
# ideal point moves 23->24, all countries with nv>=60
mv = sorted(((round(by[(79,c)]['IP']-by[(78,c)]['IP'],3), c) for (s,c) in by if s==79 and (78,c) in by and by[(79,c)]['IP'] is not None and by[(78,c)]['IP'] is not None and by[(79,c)]['NV']>=60))
print('ideal point moves 2023->2024: biggest +', mv[-5:], 'biggest -', mv[:5], 'median', st.median([m[0] for m in mv]))
# biggest single-session ideal-point move by any country since 1990 (nv>=40)
big = []
for (s,c),r in by.items():
    if s>=46 and (s-1,c) in by and r['IP'] is not None and by[(s-1,c)]['IP'] is not None and r['NV']>=40 and by[(s-1,c)]['NV']>=40:
        big.append((round(r['IP']-by[(s-1,c)]['IP'],3), s, c))
big.sort()
print('largest one-session ideal point jumps since 1991:', big[-8:], 'largest drops', big[:5])
# ARG ag_us rank in 2024 among all
r79 = sorted(((r['AG_US'], r['C']) for r in rows if r['S']==79 and r['C']!=2), reverse=True)
print('ARG rank ag_us 2024:', [i for i,(v,c) in enumerate(r79,1) if c==160], 'of', len(r79))
# ARG ag_isr rank 2024
ri = sorted(((r['AG_ISR'], r['C']) for r in rows if r['S']==79 and r['C'] not in (666,) and r['AG_ISR'] is not None), reverse=True)
print('top ag_isr 2024:', ri[:6])
# ARG ag with US historic max
print('ARG max ag_us all sessions:', max((by[(s,160)]['AG_US'], s) for s in range(1,80) if (s,160) in by))
