import pandas as pd, numpy as np, re
pd.set_option('display.width',250); pd.set_option('display.max_rows',300); pd.set_option('display.max_colwidth',70)
BIG='AR11776064889791971329'
ST={'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY','District of Columbia':'DC'}
c=pd.read_pickle('S13_generic_house_creative_rows.pkl')
c['lo']=pd.to_numeric(c.SPEND_RANGE_MIN_USD); c['hi']=pd.to_numeric(c.SPEND_RANGE_MAX_USD); c['mid']=(c.lo+c.hi)/2
c['start']=pd.to_datetime(c.DATE_RANGE_START); c['end']=pd.to_datetime(c.DATE_RANGE_END)
g=c.GEO_TARGETING_INCLUDED.fillna('')
d=g.str.extract(r'([A-Z]{2})-(\d+|AT LARGE)')
c['dkey']=np.where(d[0].notna(), d[0]+'-'+d[1].replace('AT LARGE','0').fillna(''), None)
def kind(s):
    if re.search(r'[A-Z]{2}-(\d+|AT LARGE)',s): return 'district'
    if re.search(r'\b\d{5}\b',s): return 'zip'
    if 'County' in s: return 'county'
    if s.count(',')<=1: return 'state/country'
    return 'city/other'
c['kind']=g.map(kind)
c['nstates']=g.map(lambda s: len(set(x.strip() for x in s.split(',') if x.strip() in ST)))
print(c.groupby('kind').agg(ads=('AD_ID','size'),lo=('lo','sum'),hi=('hi','sum')))
print('multi-district ads', (g.str.count(r'[A-Z]{2}-\d+')>1).sum(), ' ads naming >1 state', (c.nstates>1).sum())
print('ad types', c.AD_TYPE.value_counts().to_dict())
# ads that ran inside a pre-general 60-day window
for y,e in {2020:'2020-11-03',2022:'2022-11-08',2024:'2024-11-05'}.items():
    e=pd.Timestamp(e); s=e-pd.Timedelta(days=60)
    x=c[(c.end>=s)&(c.start<e)]
    print(y,'ads overlapping last-60-day window',len(x),'hi-sum',x.hi.sum(), x[['DATE_RANGE_START','DATE_RANGE_END','GEO_TARGETING_INCLUDED','hi']].head(8).to_string() if len(x) else '')
c.to_pickle('generic_creatives.pkl')
# year of start by kind
print(c.pivot_table(index=c.start.dt.year,columns='kind',values='mid',aggfunc='sum',fill_value=0).round(0))
