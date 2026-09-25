import json, collections, statistics as st
B='../'
r=json.load(open(B+'S04.json'))
def n(v):
    try: return float(v)
    except: return None
# national per-APC rates on shown rows
A=collections.defaultdict(lambda: dict(srv=0,out=0,osrv=0,pay=0,hsrv=0,hrows=0))
for x in r:
    s=n(x['CAPC_SRVCS']); o=n(x['OUTLIER_SRVCS']); oa=n(x['AVG_MDCR_OUTLIER_AMT'])
    if s is None: continue
    a=A[x['APC_CD']]
    if o is None: a['hsrv']+=s; a['hrows']+=1; continue
    a['srv']+=s; a['out']+=o*oa; a['osrv']+=o; a['pay']+=s*n(x['AVG_MDCR_PYMT_AMT'])
tot_out=sum(a['out'] for a in A.values()); tot_pay_shown=sum(a['pay'] for a in A.values())
tot_pay_all=sum(n(x['CAPC_SRVCS'])*n(x['AVG_MDCR_PYMT_AMT']) for x in r if n(x['CAPC_SRVCS']) is not None)
print('shown outlier $M',round(tot_out/1e6,2),'paid all nonstub $B',round(tot_pay_all/1e9,3),'share',round(tot_out/tot_pay_all,4))
# hidden outlier dollars bound: rows with 1-10 outliers, per-case = national APC avg outlier per outlier case
lo=hi=mid=0; hrows=0
for k,a in A.items():
    per=a['out']/a['osrv'] if a['osrv'] else None
    if per is None:
        # APC with no shown outliers at all
        continue
    lo+=a['hrows']*1*per; hi+=a['hrows']*10*per; mid+=a['hrows']*5.5*per; hrows+=a['hrows']
noout=[k for k,a in A.items() if a['osrv']==0]
print('hidden rows',hrows,'hidden $M lo/mid/hi',round(lo/1e6,1),round(mid/1e6,1),round(hi/1e6,1),'APCs w no shown outliers',len(noout),sum(A[k]['hrows'] for k in noout))
# per-hospital
H=collections.defaultdict(lambda: dict(srv=0,out=0,osrv=0,exp=0,hrows=0,hsrv=0,hlo=0,hhi=0,name='',city='',st=''))
for x in r:
    s=n(x['CAPC_SRVCS']); o=n(x['OUTLIER_SRVCS']); oa=n(x['AVG_MDCR_OUTLIER_AMT'])
    h=H[x['RNDRNG_PRVDR_CCN']]; h['name']=x['RNDRNG_PRVDR_ORG_NAME']; h['city']=x['RNDRNG_PRVDR_CITY']; h['st']=x['RNDRNG_PRVDR_STATE_ABRVTN']
    if s is None: continue
    a=A[x['APC_CD']]
    per=a['out']/a['osrv'] if a['osrv'] else 0
    if o is None:
        h['hrows']+=1; h['hsrv']+=s; h['hlo']+=per; h['hhi']+=10*per; continue
    h['srv']+=s; h['out']+=o*oa; h['osrv']+=o; h['exp']+=s*a['out']/a['srv']
L=sorted([h for h in H.values() if h['exp']>0], key=lambda h:-h['out'])
print('hospitals with exp>0',len(L),'with any shown row', sum(1 for h in H.values() if h['srv']>0))
def topshare(k, extra=0):
    return round(sum(h['out'] for h in L[:k])/(tot_out+extra),3)
for k in (10,50,100): print('top',k,'shown-only',topshare(k),'if hidden=lo',topshare(k,lo),'if hidden=mid',topshare(k,mid),'if hidden=hi',topshare(k,hi))
big=[h for h in H.values() if h['srv']>=1000]
z=[h for h in big if h['out']==0]
print('srv>=1000',len(big),'$0 shown',len(z), 'of those with >=1 suppressed-outlier row (so >= $1 outlier really)', sum(1 for h in z if h['hrows']>0), 'with 5+ such rows', sum(1 for h in z if h['hrows']>=5))
# Penn State
ps={k:h for k,h in H.items() if ('PENN STATE' in h['name'].upper() or 'HERSHEY' in h['name'].upper())}
for k,h in ps.items(): print(k,h['name'],h['city'],h['st'],'out',round(h['out']/1e6,3),'exp',round(h['exp']/1e6,3),'oe',round(h['out']/h['exp'],1) if h['exp'] else None,int(h['osrv']),'/',int(h['srv']),'hidden rows',h['hrows'],'hidden hi $M',round(h['hhi']/1e6,3))
O=sum(h['out'] for h in ps.values()); E=sum(h['exp'] for h in ps.values())
print('PSH out',round(O/1e6,3),'exp',round(E/1e6,3),'OE',round(O/E,2),'share nat',round(O/tot_out,4),'osrv',sum(h['osrv'] for h in ps.values()),'srv',sum(h['srv'] for h in ps.values()))
# other PA hospitals in Hershey/Lancaster/Camp Hill/Mechanicsburg/Reading w/o Penn State in name
for k,h in H.items():
    if h['st']=='PA' and h['city'].upper() in ('HERSHEY','LANCASTER','CAMP HILL','MECHANICSBURG','READING','ENOLA','STATE COLLEGE','HAMPDEN') and k not in ps: print('  other PA same-city', k, h['name'], h['city'], round(h['out']/1e6,3))
# median O/E, srv>=1000
oes=[h['out']/h['exp'] for h in big if h['exp']>0]
print('median O/E srv>=1000', round(st.median(oes),3), 'n', len(oes), 'rank of Hershey', 1+sum(1 for v in oes if v> ps['390256']['out']/ps['390256']['exp']) if '390256' in ps else None)
json.dump({'A':{k:dict(v) for k,v in A.items()}}, open('apc.json','w'))
