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
join = {20:1949,200:1949,210:1949,211:1949,212:1949,220:1949,235:1949,325:1949,385:1949,390:1949,395:1949,
        350:1952,640:1952,260:1955,255:1990,230:1982,316:1999,310:1999,290:1999,355:2004,366:2004,367:2004,368:2004,360:2004,317:2004,349:2004,
        339:2009,344:2009,341:2017,343:2020,375:2023,380:2024}
name = {20:'Canada',200:'UK',210:'Netherlands',211:'Belgium',212:'Luxembourg',220:'France',230:'Spain',235:'Portugal',255:'Germany',260:'W.Germany',290:'Poland',310:'Hungary',316:'Czechia',317:'Slovakia',325:'Italy',339:'Albania',341:'Montenegro',343:'N.Macedonia',344:'Croatia',349:'Slovenia',350:'Greece',355:'Bulgaria',360:'Romania',366:'Estonia',367:'Latvia',368:'Lithuania',375:'Finland',380:'Sweden',385:'Norway',390:'Denmark',395:'Iceland',640:'Turkey',
        740:'Japan',732:'S.Korea',900:'Australia',920:'New Zealand',666:'Israel',840:'Philippines',160:'Argentina',140:'Brazil',70:'Mexico',155:'Chile',100:'Colombia',135:'Peru',150:'Paraguay',165:'Uruguay',130:'Ecuador',145:'Bolivia',101:'Venezuela',40:'Cuba',95:'Panama',94:'Costa Rica',90:'Guatemala',91:'Honduras',92:'El Salvador',93:'Nicaragua',42:'Dominican Rep',41:'Haiti',110:'Guyana',115:'Suriname',365:'Russia',710:'China',750:'India',983:'Marshall Is',986:'Palau',987:'Micronesia',970:'Nauru',947:'Tuvalu',713:'Taiwan',731:'N.Korea',652:'Syria',630:'Iran'}
def nato(s, y):
    return [c for c,j in join.items() if j <= y and (s,c) in by and by[(s,c)]['AG_US'] is not None]
print('session year | US med all | NATO(yr) med ag_us | NATO med ag_fra (excl FR) | NATO med ag_uk (excl UK) | n')
for s in range(60, 80):
    y = by[(s,2)]['Y']
    ns = nato(s, y)
    a = [by[(s,c)]['AG_US'] for c in ns]
    fr = [by[(s,c)]['AG_FRA'] for c in ns if c != 220 and by[(s,c)]['AG_FRA'] is not None]
    uk = [by[(s,c)]['AG_UK'] for c in ns if c != 200 and by[(s,c)]['AG_UK'] is not None]
    allv = [r['AG_US'] for r in rows if r['S']==s and r['AG_US'] is not None]
    print(s, y, round(st.median(allv),3), round(st.median(a),3), round(st.median(fr),3), round(st.median(uk),3), len(ns), 'US nv', by[(s,2)]['NV'])
# NATO median history (year-correct), top sessions
hist = []
for s in sorted({r['S'] for r in rows}):
    if (s,2) not in by: continue
    y = by[(s,2)]['Y']; ns = nato(s, y)
    if len(ns) >= 5: hist.append((round(st.median([by[(s,c)]['AG_US'] for c in ns]),3), s, y, len(ns)))
print('NATO median ag_us, highest sessions:', sorted(hist, reverse=True)[:8])
print('NATO median ag_us, lowest sessions:', sorted(hist)[:8])
# allies ranking 2024 with history
print('\nAlly | 2016 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | d23->24')
allies = [c for c,j in join.items() if j <= 2024 and c != 260] + [740,732,900,920,666,840]
out = []
for c in allies:
    v = {s: (by[(s,c)]['AG_US'] if (s,c) in by else None) for s in (71,74,75,76,77,78,79)}
    if v[79] is None or v[78] is None: continue
    out.append((v[79]-v[78], c, v))
for dlt, c, v in sorted(out):
    print(name.get(c,c), ' '.join('%.3f'%v[s] if v[s] is not None else '  -  ' for s in (71,74,75,76,77,78,79)), '%+.3f'%dlt)
# Argentina and Latin America
LA = [160,140,70,155,100,135,150,165,130,145,101,40,95,94,90,91,92,93,42,41,110,115]
print('\nLatin America ag_us and avg_all, 2019-2024')
for s in (74,75,76,77,78,79):
    vals = [by[(s,c)]['AG_US'] for c in LA if (s,c) in by]
    print(s, by[(s,2)]['Y'], 'LA median ag_us %.3f'%st.median(vals), 'ARG ag_us %.3f ag_isr %.3f avg_all %.4f ip %.3f'%(by[(s,160)]['AG_US'], by[(s,160)]['AG_ISR'], by[(s,160)]['AVG_ALL'], by[(s,160)]['IP']))
    rk = sorted(((by[(s,c)]['AG_US'], c) for c in LA if (s,c) in by), reverse=True)[:4]
    print('   top LA:', [(name.get(c,c), round(v,3)) for v,c in rk])
# all countries: biggest ag_us jumps 2023->2024
jumps = []
for r in rows:
    if r['S']==79 and r['C']!=2 and (78,r['C']) in by and r['AG_US'] is not None and by[(78,r['C'])]['AG_US'] is not None:
        jumps.append((r['AG_US']-by[(78,r['C'])]['AG_US'], r['C'], by[(78,r['C'])]['AG_US'], r['AG_US']))
jumps.sort()
alld = [j[0] for j in jumps]
print('\nall countries d(ag_us) 2023->2024: median %.3f, n %d, rose %d'%(st.median(alld), len(alld), sum(1 for x in alld if x>0)))
print('top rises:', [(name.get(c,c), round(a,3), round(b,3), round(dd,3)) for dd,c,a,b in jumps[-8:]])
print('top falls:', [(name.get(c,c), round(a,3), round(b,3), round(dd,3)) for dd,c,a,b in jumps[:8]])
# Argentina history of ag_us
print('\nARG ag_us by session 60-79:', [(s, round(by[(s,160)]['AG_US'],3)) for s in range(60,80)])
# rank of ARG ag_us among all countries in 79
r79 = sorted(((r['AG_US'], r['C']) for r in rows if r['S']==79 and r['C']!=2 and r['AG_US'] is not None), reverse=True)
print('2024 top ag_us:', [(name.get(c,c), round(v,3)) for v,c in r79[:12]])
