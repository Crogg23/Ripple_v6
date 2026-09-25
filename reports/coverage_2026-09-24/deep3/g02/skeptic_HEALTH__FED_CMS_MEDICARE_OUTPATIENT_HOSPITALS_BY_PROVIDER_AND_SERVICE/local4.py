import json, collections, statistics as st
H=json.load(open('../oe_hosp.json'))
S14={x['PROVIDER_CCN']:x for x in json.load(open('../S14.json'))}
def f(v):
    try: return float(v)
    except: return None
acad=[(k,h) for k,h in H.items() if h.get('exp',0)>0 and (f(S14.get(k,{}).get('RESIDENTS_FTE')) or 0)>=200]
print('academic n',len(acad))
O=sum(h['out'] for k,h in acad); E=sum(h['exp'] for k,h in acad)
oes=sorted([(h['out']/h['exp'],k,h['name']) for k,h in acad],reverse=True)
print('pooled',round(O/E,2),'median',round(st.median([t[0] for t in oes]),2))
for t in oes[:6]: print('  ',round(t[0],1),t[1],t[2])
print('academic hosp with shown $0', sum(1 for t in oes if t[0]==0), 'with $0 but hidden-outlier rows', sum(1 for k,h in acad if h['out']==0 and h.get('supout',0)>0))
# Hershey excluded pooled
O2=O-H['390256']['out']; E2=E-H['390256']['exp']; print('pooled w/o Hershey',round(O2/E2,2))
# POS new hospital test
P=collections.defaultdict(list)
for x in json.load(open('../S07.json')): P[x['CCN']].append(x)
def jd(k):
    ds=[x['ORGNL_PRTCPTN_DT'] for x in P.get(k,[]) if x['ORGNL_PRTCPTN_DT']]
    return min(str(d) for d in ds) if ds else None
print('POS rows per CCN max', max(len(v) for v in P.values()), 'CCNs with >1 POS row', sum(1 for v in P.values() if len(v)>1))
new=[(k,h) for k,h in H.items() if h.get('exp',0)>0 and (jd(k) or '0')[:4]>='2020']
old=[(k,h) for k,h in H.items() if h.get('exp',0)>0 and not ((jd(k) or '0')[:4]>='2020')]
def pool(g): return round(sum(h['out'] for k,h in g)/sum(h['exp'] for k,h in g),2)
print('new',len(new),'pooled',pool(new),'median',round(st.median([h['out']/h['exp'] for k,h in new]),2),'| older/undated',len(old),pool(old))
nn=sorted(new,key=lambda kh:-kh[1]['out'])
tot=sum(h['out'] for k,h in new)
print('new-hospital outlier $M',round(tot/1e6,2),'top 3 share',round(sum(h['out'] for k,h in nn[:3])/tot,3))
for k,h in nn[:6]: print('   ',k,h['name'][:40],h['st'],jd(k),round(h['out']/1e6,2),round(h['out']/h['exp'],1))
ex=[kh for kh in new if kh[0] not in ('390336','390339')]
print('new w/o PSH',pool(ex),'w/o top 5 by $',pool([kh for kh in new if kh not in nn[:5]]))
# 'SETON' in any PA names? any other 'HERSHEY' matches
print([ (k,h['name'],h['st']) for k,h in H.items() if 'SETON' in h['name'].upper() and h['st']=='PA'])
