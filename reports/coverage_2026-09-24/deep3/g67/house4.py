import pandas as pd, numpy as np, re
pd.set_option('display.width',250); pd.set_option('display.max_rows',300); pd.set_option('display.max_colwidth',70)
c=pd.read_pickle('generic_creatives.pkl')
for d in ['2024-09-06','2022-09-09','2020-09-04']:
    print(d,'ads ending that day',(c.DATE_RANGE_END==d).sum() if c.DATE_RANGE_END.dtype==object else (c.end==d).sum())
print('top end dates', c.end.value_counts().head(8).to_dict())
# ---- district-level 2025-26 official spend
ie=pd.read_pickle('S12_house_ie_by_district_v2.pkl'); ie['ie']=pd.to_numeric(ie.IE_USD)
ie['CYCLE_FILE']=ie.CYCLE_FILE.astype(int); ie['dnum']=pd.to_numeric(ie.CAN_OFFICE_DIS,errors='coerce').fillna(0).astype(int)
ie['dkey']=ie.CAN_OFFICE_STATE.fillna('')+'-'+ie.dnum.astype(str)
print('huge lines', ie.groupby('CYCLE_FILE').N_HUGE.sum().to_dict())
ie24=ie[ie.CYCLE_FILE==2024].groupby('dkey').ie.sum()
ie26=ie[ie.CYCLE_FILE==2026].groupby('dkey').ie.sum()
m=pd.read_pickle('S09_house_members.pkl'); m=m[(m.TERM_TYPE=='rep')&(m.TERM_END=='2027-01-03')].copy()
m['dnum']=pd.to_numeric(m.DISTRICT,errors='coerce').fillna(0).astype(int).clip(lower=0)
m['dkey']=m.STATE+'-'+m.dnum.astype(str)
m=m[~m.STATE.isin(['PR','GU','VI','AS','MP','DC'])]
print('current voting members',len(m),'distinct districts',m.dkey.nunique())
dist=pd.DataFrame({'dkey':sorted(m.dkey.unique())})
dist['ie24']=dist.dkey.map(ie24).fillna(0)
dist['ie26']=dist.dkey.map(ie26).fillna(0)
dist['rank24']=dist.ie24.rank(ascending=False,method='first')
dist['top87']=dist.rank24<=87   # top fifth of 435
# official spend 2025-26: generic account district ads that started 2025+
g=c[(c.kind=='district')&(c.start>='2025-01-01')].copy(); g['dkey']=g.dkey.str.replace('-0$','-0',regex=True)
gd=g.groupby('dkey').mid.sum()
# member-named accounts weekly 2025+
mp=pd.read_pickle('acct_member_map.pkl')
w=pd.read_pickle('S06_house_weekly.pkl'); w['usd']=pd.to_numeric(w.SPEND_USD); w['wk']=pd.to_datetime(w.WEEK_START_DATE)
w25=w[w.wk>='2025-01-01'].groupby('ADVERTISER_ID').usd.sum()
mp['usd25']=mp.id.map(w25).fillna(0)
act=mp[mp.usd25>0]
print('member-named accounts with 2025+ spend'); print(act[['name','home','usd25','n','match']].to_string())
# ---------- resolve two-candidate matches to the current member, drop unmatched
def pick(row):
    if row.n==1: return row.match.split(' 20')[0]
    if 'Delaney' in row['name']: return 'April McClain Delaney MD-6'
    if 'CARTER' in row['name']: return 'John R. Carter TX-31'
    return None
act=act.copy(); act['who']=act.apply(pick,axis=1)
act['dkey']=act.who.str.extract(r'([A-Z]{2}-\d+)$')[0]
md=act.dropna(subset=['dkey']).groupby('dkey').usd25.sum()
tot=dist.set_index('dkey')
tot['generic']=gd.reindex(tot.index).fillna(0)
tot['named']=md.reindex(tot.index).fillna(0)
tot['official']=tot.generic+tot.named
print('generic district-ad $ 2025+ (mid of range):',round(gd.sum()),' of which lands on a current district:',round(tot.generic.sum()))
print('unlanded generic keys:',sorted(set(gd.index)-set(tot.index)))
print('named $ 2025+ mapped:',tot.named.sum(),' unmapped named $:',act[act.dkey.isna()].usd25.sum())
tot['has']=tot.official>0
s=tot.groupby('top87').agg(districts=('has','size'),with_ads=('has','sum'),usd=('official','sum'),median_usd_if_any=('official',lambda x: x[x>0].median()))
s['share_with_ads']=(s.with_ads/s.districts*100).round(1)
print(s)
print('share of official $ in top-fifth IE districts', round(tot[tot.top87].official.sum()/tot.official.sum()*100,1))
# alternative yardstick: 2026-cycle IE so far
tot['rank26']=tot.ie26.rank(ascending=False,method='first'); tot['top26']=tot.rank26<=87
s2=tot.groupby('top26').agg(districts=('has','size'),with_ads=('has','sum'),usd=('official','sum')); s2['pct']=(s2.with_ads/s2.districts*100).round(1); print(s2)
print(tot[tot.has].sort_values('official',ascending=False).head(25)[['ie24','rank24','ie26','generic','named','official']].to_string())
tot.to_pickle('district_official.pkl')
