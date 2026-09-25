import json, collections, statistics as st
r=json.load(open('S04.json')); A=json.load(open('oe_apc.json')); H=json.load(open('oe_hosp.json'))
def n(v):
    try: return float(v)
    except: return None
# state pooled O/E
S=collections.defaultdict(lambda:[0,0,0])
for k,h in H.items():
    if h.get('exp'): S[h['st']][0]+=h['out']; S[h['st']][1]+=h['exp']; S[h['st']][2]+=1
tot=sum(v[0] for v in S.values())
L=sorted([(round(v[0]/v[1],2), s, round(v[0]/1e6,1), round(v[0]/tot,3), v[2]) for s,v in S.items() if v[1]>0], reverse=True)
print('state pooled O/E top:', L[:10]); print('bottom:', L[-8:])
# systems
def sysname(nm):
    u=nm.upper()
    if 'SETON' in u: return 'Ascension Seton (TX)'
    if 'PENN STATE' in u or 'HERSHEY' in u: return 'Penn State Health (PA)'
    return None
Y=collections.defaultdict(lambda: dict(out=0,exp=0,osrv=0,srv=0,h=[]))
for k,h in H.items():
    s=sysname(h['name'])
    if s and h.get('srv'):
        y=Y[s]; y['out']+=h['out']; y['exp']+=h['exp']; y['osrv']+=h['osrv']; y['srv']+=h['srv']; y['h'].append((h['name'],h['st'],round(h['out']/1e6,2),round(h['out']/h['exp'],1) if h['exp'] else None,int(h['osrv']),int(h['srv'])))
for s,y in Y.items():
    print(s, 'hospitals', len(y['h']), 'outlier $M', round(y['out']/1e6,2), 'expected $M', round(y['exp']/1e6,2), 'O/E', round(y['out']/y['exp'],1), 'outlier services', int(y['osrv']), 'of', int(y['srv']), 'share of national $', round(y['out']/tot,3))
    for hh in sorted(y['h'], key=lambda t:-t[2]): print('   ', hh)
# 5115 in TX and PA and nation
for apc in ('5115',):
    for stt in ('TX','PA',None):
        rows=[x for x in r if x['APC_CD']==apc and n(x['CAPC_SRVCS']) and (stt is None or x['RNDRNG_PRVDR_STATE_ABRVTN']==stt)]
        sh=[x for x in rows if n(x['OUTLIER_SRVCS']) is not None]
        srv=sum(n(x['CAPC_SRVCS']) for x in sh); os_=sum(n(x['OUTLIER_SRVCS']) for x in sh); od=sum(n(x['OUTLIER_SRVCS'])*n(x['AVG_MDCR_OUTLIER_AMT']) for x in sh)
        sysrows=[x for x in sh if sysname(x['RNDRNG_PRVDR_ORG_NAME'])]
        ss=sum(n(x['CAPC_SRVCS']) for x in sysrows); so=sum(n(x['OUTLIER_SRVCS']) for x in sysrows); sd=sum(n(x['OUTLIER_SRVCS'])*n(x['AVG_MDCR_OUTLIER_AMT']) for x in sysrows)
        print(apc, stt or 'US', 'hospitals shown', len(sh), 'services', int(srv), 'outlier services', int(os_), round(os_/srv,3), 'outlier $M', round(od/1e6,2), '| two systems: srv', int(ss), 'osrv', int(so), 'out $M', round(sd/1e6,2), 'share of $', round(sd/od,3) if od else None, 'median hosp rate', round(st.median([n(x['OUTLIER_SRVCS'])/n(x['CAPC_SRVCS']) for x in sh]),3))
