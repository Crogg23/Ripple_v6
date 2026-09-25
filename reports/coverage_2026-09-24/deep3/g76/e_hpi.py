"""Local math on S10 (FHFA HPI): metro change from post-2020 peak and year over year, state peers, flavor sensitivity."""
import pandas as pd, numpy as np, warnings; warnings.filterwarnings('ignore')
h=pd.read_csv('out_S10.csv',dtype=str,keep_default_na=False); h['v']=pd.to_numeric(h.INDEX_NSA,errors='coerce')
q=h[(h.HPI_TYPE=='traditional')&(h.FREQUENCY=='quarterly')].copy(); q['t']=q.YR.astype(int)*10+q.PERIOD.astype(int)
for flavor in ['all-transactions','expanded-data']:
    s=q[(q.HPI_FLAVOR==flavor)&(q.LEVEL=='MSA')].pivot_table(index=['PLACE_ID','PLACE_NAME'],columns='t',values='v')
    post=s[[c for c in s.columns if c>=20200]]
    o=pd.DataFrame({'yoy':(s[20261]/s[20251]-1)*100,'from_peak':(s[20261]/post.max(axis=1)-1)*100,'peak_t':post.idxmax(axis=1),'since2019':(s[20261]/s[20194]-1)*100}).reset_index()
    o['st']=o.PLACE_NAME.str.extract(r',\s*([A-Z]{2})')[0]
    print(flavor,'metros',len(o),'median yoy',round(o.yoy.median(),2),'falling',(o.yoy<0).sum(),'5%+ below peak',(o.from_peak<-5).sum())
    for pid in ['12420','39460','15980']:
        r=o[o.PLACE_ID==pid].iloc[0]; peers=o[(o.st==r.st)&(o.PLACE_ID!=pid)]
        print('  ',r.PLACE_NAME,'peak',r.peak_t,'from peak',round(r.from_peak,1),'yoy',round(r.yoy,1),'| same-state metros n',len(peers),'median yoy',round(peers.yoy.median(),1),'median from peak',round(peers.from_peak.median(),1))
