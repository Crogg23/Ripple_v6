import pandas as pd, numpy as np, re
pd.set_option('display.width',250); pd.set_option('display.max_rows',300); pd.set_option('display.max_colwidth',70)
a=pd.read_pickle('S02_adv_all.pkl'); a['usd']=pd.to_numeric(a.SPEND_USD)
keep=set(a[a.PUBLIC_IDS_LIST.fillna('').str.contains('53-6002523')].ADVERTISER_ID)|{'AR10517496269264388097','AR18236540952539824129'}
BIG='AR11776064889791971329'
m=pd.read_pickle('S09_house_members.pkl'); m=m[m.TERM_TYPE=='rep'].copy()
m['dist']=pd.to_numeric(m.DISTRICT,errors='coerce').fillna(0).astype(int).clip(lower=0)
geo=pd.read_pickle('S07_house_geo.pkl'); geo['usd']=pd.to_numeric(geo.SPEND_USD)
home=geo[geo.COUNTRY_SUBDIVISION_PRIMARY.notna()].sort_values('usd',ascending=False).groupby('ADVERTISER_ID').COUNTRY_SUBDIVISION_PRIMARY.first()
# --- map member-named accounts to a member by last name + home state
acc=a[a.ADVERTISER_ID.isin(keep)&(a.ADVERTISER_ID!=BIG)][['ADVERTISER_ID','ADVERTISER_NAME','usd']].copy()
acc['home']=acc.ADVERTISER_ID.map(home)
def cands(name,st):
    n=re.sub(r'[^A-Z ]',' ',name.upper())
    toks=set(n.split())-{'REP','US','U','S','HOUSE','OF','REPRESENTATIVES','OFFICE','THE','REPS','FINANCE','CONGRESSMAN','CONGRESSWOMAN'}
    hit=m[(m.STATE==st)]
    out=[r for r in hit.itertuples() if str(r.NAME_LAST).upper().replace('-',' ').split()[-1] in toks or str(r.NAME_LAST).upper() in n]
    return out
res=[]
for r in acc.itertuples():
    c=cands(r.ADVERTISER_NAME,r.home)
    res.append((r.ADVERTISER_ID,r.ADVERTISER_NAME[:55],r.home,r.usd,len(c),'; '.join(f'{x.NAME_OFFICIAL_FULL or x.NAME_LAST} {x.STATE}-{x.dist} {x.TERM_END}' for x in c)))
res=pd.DataFrame(res,columns=['id','name','home','usd','n','match'])
print(res.n.value_counts()); print(res[res.n!=1].to_string())
res.to_pickle('acct_member_map.pkl')
