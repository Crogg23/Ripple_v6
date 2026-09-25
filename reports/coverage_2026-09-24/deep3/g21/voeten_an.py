import json, statistics as st
from pathlib import Path
H = Path(__file__).parent
d = json.load(open(H/'r09_voeten_country_session.json'))
cols = d['cols']; rows = [dict(zip(cols, r)) for r in d['rows']]
def f(x):
    return None if x in (None, '') else float(x)
for r in rows:
    for k in ('S','Y','C','N_PARTNERS'): r[k] = int(float(r[k]))
    for k in ('AVG_ALL','AG_US','AG_CHN','AG_RUS','AG_ISR','AG_UK','AG_FRA','AG_GER','AG_IND','IP','NV'): r[k] = f(r[k])
by = {}
for r in rows: by[(r['S'], r['C'])] = r
sessions = sorted({r['S'] for r in rows})
NATO24 = {20:'Canada',200:'UK',210:'Netherlands',211:'Belgium',212:'Luxembourg',220:'France',230:'Spain',235:'Portugal',255:'Germany',290:'Poland',310:'Hungary',316:'Czechia',317:'Slovakia',325:'Italy',339:'Albania',341:'Montenegro',343:'N.Macedonia',344:'Croatia',349:'Slovenia',350:'Greece',355:'Bulgaria',360:'Romania',366:'Estonia',367:'Latvia',368:'Lithuania',375:'Finland',380:'Sweden',385:'Norway',390:'Denmark',395:'Iceland',640:'Turkey'}
PAC = {740:'Japan',732:'S.Korea',900:'Australia',920:'New Zealand',666:'Israel',840:'Philippines',800:'Thailand'}
print('ip_vals>1 rows:', sum(1 for r in rows if int(r['IP_VALS'])>1))
print('US ideal point, avg_all, median ag_us all, median NATO, n')
for s in sessions:
    us = by.get((s,2))
    allv = [r['AG_US'] for r in rows if r['S']==s and r['AG_US'] is not None]
    nat = [by[(s,c)]['AG_US'] for c in NATO24 if (s,c) in by and by[(s,c)]['AG_US'] is not None]
    avgs = sorted([(r['AVG_ALL'], r['C']) for r in rows if r['S']==s])
    print(s, us['Y'] if us else '', us['IP'] if us else '', us['AVG_ALL'] if us else '', round(st.median(allv),3) if allv else '', round(st.median(nat),3) if nat else '', len(nat), 'lowest avg_all:', avgs[:4])
