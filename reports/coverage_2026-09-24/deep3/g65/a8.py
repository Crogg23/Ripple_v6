import pandas as pd, numpy as np, re, unicodedata
pd.set_option('display.width',260); pd.set_option('display.max_colwidth',60)
c=pd.read_pickle('creative.pkl'); a=pd.read_pickle('official.pkl')
v=pd.read_csv('out_S17.csv',keep_default_na=False,na_values=[''])
c=c.join(a[['ADVERTISER_NAME']],on='ADVERTISER_ID')
c['mid']=(c.SPEND_RANGE_MIN_USD+c.SPEND_RANGE_MAX_USD)/2
def dists(t):
    return sorted(set(re.findall(r'\b([A-Z]{2})-(\d{1,2}|AL) \((\d{4}) redistricting\)',str(t))))
c['d']=c.GEO_TARGETING_INCLUDED.apply(dists)
c['kind']=np.where(c.d.str.len()>0,'district',np.where(c.GEO_TARGETING_INCLUDED.fillna('').str.contains(r'\b\d{5},'),'zip',np.where(c.GEO_TARGETING_INCLUDED.fillna('').str.strip()=='United States','national','other')))
print(c.groupby('kind').agg(ads=('AD_ID','size'),mid=('mid','sum')).to_string())
# congress for a date: 116 = 2019-01-03..2021-01-03 etc
def cong(d):
    y=d.year; 
    n=(y-1789)//2+1
    if d.month==1 and d.day<3 and y%2==1: n-=1
    return n
e=c[c.kind=='district'].explode('d').copy()
e['st']=e.d.str[0]; e['dn']=e.d.str[1].replace('AL','0').astype(int)
e['cong']=e.DATE_RANGE_START.apply(cong)
v['dn']=v.DISTRICT_CODE.astype(int)
e['st']=e['st'].astype(str)
vv=v.groupby(['CONGRESS','STATE_ABBREV','dn']).BIONAME.apply(lambda s:' / '.join(sorted(set(s)))).reset_index()
e=e.merge(vv,left_on=['cong','st','dn'],right_on=['CONGRESS','STATE_ABBREV','dn'],how='left')
def norm(s): return unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().upper()
def surname_hit(row):
    nm=norm(row.ADVERTISER_NAME); holders=norm(row.BIONAME)
    lasts=[h.split(',')[0].strip() for h in holders.split(' / ')]
    return any(l and re.search(r'\b'+re.escape(l.split()[-1] if ' ' in l else l)+r'\b',nm) for l in lasts)
e['name_ok']=e.apply(surname_hit,axis=1)
e['generic']=~e.ADVERTISER_NAME.str.upper().str.contains(r'REP\.?\s|REPRESENTATIVE|CONGRESSMAN|OFFICE OF|THANEDAR|BUDZINSKI',regex=True)
print('district-targeted ad-district pairs',len(e),'holder found',e.BIONAME.notna().mean())
nm=e[~e.generic]
acc=nm.groupby('ADVERTISER_NAME').agg(ads=('AD_ID','nunique'),mid=('mid','sum'),ok_mid=('mid',lambda s:s[nm.loc[s.index,'name_ok']].sum()),districts=('d',lambda s:len(set(s))))
acc['bad_mid']=acc.mid-acc.ok_mid
print('named accounts with district ads',len(acc),' mid $',acc.mid.sum(),' mid on districts NOT held by the named member $',acc.bad_mid.sum())
bad=nm[~nm.name_ok].groupby(['ADVERTISER_NAME','st','dn','BIONAME']).agg(ads=('AD_ID','nunique'),mid=('mid','sum'),d0=('DATE_RANGE_START','min'),d1=('DATE_RANGE_END','max')).reset_index().sort_values('mid',ascending=False)
print(bad.to_string())
# generic accounts: which districts/members
gen=e[e.generic]
print('\ngeneric accounts',gen.ADVERTISER_NAME.unique())
gg=gen.groupby(['ADVERTISER_NAME']).agg(ads=('AD_ID','nunique'),mid=('mid','sum'),districts=('d',lambda s:len(set(s))),members=('BIONAME',lambda s:len(set(s.dropna()))))
print(gg.to_string())
top=gen.groupby(['st','dn','BIONAME']).agg(ads=('AD_ID','nunique'),mid=('mid','sum'),d0=('DATE_RANGE_START','min'),d1=('DATE_RANGE_END','max')).sort_values('mid',ascending=False)
print(top.head(15).to_string())
e.to_pickle('ad_district.pkl'); c.to_pickle('creative2.pkl')
