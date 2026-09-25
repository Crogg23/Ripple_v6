import pandas as pd, numpy as np, re, unicodedata, difflib
pd.set_option('display.width',260); pd.set_option('display.max_colwidth',70)
c=pd.read_pickle('creative2.pkl'); v=pd.read_csv('out_S17.csv',keep_default_na=False,na_values=[''])
GEN=['US House of Representatives','US House of Reps.','US HOUSE OF REPRESENTATIVES OFFICE OF FINANCE']
def cong(d):
    y=d.year; n=(y-1789)//2+1
    if d.month==1 and d.day<3 and y%2==1: n-=1
    return n
e=c[c.kind=='district'].explode('d').copy()
e['st']=e.d.str[0].astype(str); e['dn']=e.d.str[1].replace('AL','0').astype(int); e['map']=e.d.str[2].astype(int)
e['cong0']=e.DATE_RANGE_START.apply(cong)
e['cong']=np.where(e['map']==2012,np.minimum(e.cong0,117),np.maximum(e.cong0,118))
v['dn']=v.DISTRICT_CODE.astype(int)
vv=v.groupby(['CONGRESS','STATE_ABBREV','dn']).BIONAME.apply(lambda s:' / '.join(sorted(set(s)))).reset_index()
e=e.merge(vv,left_on=['cong','st','dn'],right_on=['CONGRESS','STATE_ABBREV','dn'],how='left')
def norm(s): return unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().upper()
def hit(row):
    toks=re.findall(r'[A-Z]+',norm(row.ADVERTISER_NAME))
    for h in norm(row.BIONAME).split(' / '):
        last=h.split(',')[0]
        for L in re.findall(r'[A-Z]+',last):
            if len(L)<3: continue
            if any(difflib.SequenceMatcher(None,L,t).ratio()>=0.85 for t in toks): return True
    return False
e['name_ok']=e.apply(hit,axis=1)
e['generic']=e.ADVERTISER_NAME.isin(GEN)
print('holder found share',e.BIONAME.notna().mean())
nm=e[~e.generic]
ads=nm.groupby('AD_ID').agg(acct=('ADVERTISER_NAME','first'),mid=('mid','first'),ok=('name_ok','any'),d0=('DATE_RANGE_START','first'),d1=('DATE_RANGE_END','first'),
    tgt=('d',lambda s:', '.join(f'{x[0]}-{x[1]}' for x in s)),holders=('BIONAME',lambda s:' | '.join(sorted(set(s.fillna('?'))))))
print('named accounts: district ads',len(ads),'mid $',ads.mid.sum(),' ads aimed at a district NOT held by the named member:',(~ads.ok).sum(),' mid $',ads[~ads.ok].mid.sum(), ' accounts',ads[~ads.ok].acct.nunique(),'of',ads.acct.nunique())
bad=ads[~ads.ok].groupby(['acct','tgt','holders']).agg(ads=('mid','size'),mid=('mid','sum'),d0=('d0','min'),d1=('d1','max')).reset_index().sort_values('mid',ascending=False)
print(bad.to_string())
ge=e[e.generic]
print('\nGENERIC accounts: ads',ge.AD_ID.nunique(),'mid $',ge.drop_duplicates('AD_ID').mid.sum(),'districts',ge.d.nunique(),'members',ge.BIONAME.nunique())
print(ge.groupby('ADVERTISER_NAME').agg(ads=('AD_ID','nunique'),members=('BIONAME','nunique')).to_string())
# all generic account ads including zip/other kinds
cg=c[c.ADVERTISER_NAME.isin(GEN)]
print(cg.groupby(['ADVERTISER_NAME','kind']).agg(ads=('AD_ID','size'),mid=('mid','sum')).to_string())
# members per year served by generic account
ge['yr']=ge.DATE_RANGE_START.dt.year
print(ge[ge.ADVERTISER_NAME=='US House of Representatives'].groupby('yr').agg(members=('BIONAME','nunique'),ads=('AD_ID','nunique')).to_string())
e.to_pickle('ad_district2.pkl'); bad.to_csv('mislabelled_official_ads.csv',index=False)
