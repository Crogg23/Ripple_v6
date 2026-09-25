import json, statistics as st
from pathlib import Path
exec(open(Path(__file__).parent/'voeten_an2.py').read().split("print('session year")[0])
hist = []
for s in sorted({r['S'] for r in rows}):
    if (s,2) not in by: continue
    y = by[(s,2)]['Y']; ns = nato(s, y)
    if len(ns) >= 5: hist.append((s, y, round(st.median([by[(s,c)]['AG_US'] for c in ns]),3), len(ns)))
print('max NATO median 1967-2021:', max((m, y) for s,y,m,n in hist if 1968 <= y <= 2021))
print('2022:', [h for h in hist if h[1] in (2021,2022,2023,2024)])
# LA median change 23->24
LA = [160,140,70,155,100,135,150,165,130,145,101,40,95,94,90,91,92,93,42,41,110,115]
dl = [by[(79,c)]['AG_US']-by[(78,c)]['AG_US'] for c in LA if c!=160 and (79,c) in by and (78,c) in by]
print('LA ex-ARG median change 23->24: %.3f, n %d, rose %d' % (st.median(dl), len(dl), sum(1 for x in dl if x>0)))
