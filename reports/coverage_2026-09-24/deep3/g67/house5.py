import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_rows',300)
t=pd.read_pickle('district_official.pkl')
ie=pd.read_pickle('S14_house_ie_general_only.pkl'); ie['CYCLE_FILE']=ie.CYCLE_FILE.astype(int); ie['ie']=pd.to_numeric(ie.IE_USD)
ie['dkey']=ie.CAN_OFFICE_STATE.fillna('')+'-'+pd.to_numeric(ie.CAN_OFFICE_DIS,errors='coerce').fillna(0).astype(int).astype(str)
print(ie.groupby(['CYCLE_FILE','ELE']).ie.sum().round(-3))
g24=ie[(ie.CYCLE_FILE==2024)&(ie.ELE=='G')].groupby('dkey').ie.sum()
t['g24']=g24.reindex(t.index).fillna(0)
t['grank']=t.g24.rank(ascending=False,method='first')
for cut in [44,87]:
    t['top']=t.grank<=cut
    s=t.groupby('top').agg(districts=('has','size'),with_ads=('has','sum'),usd=('official','sum'),med=('official',lambda x:x[x>0].median()))
    s['pct']=(s.with_ads/s.districts*100).round(1); s['usd_per_district']=(s.usd/s.districts).round(0)
    print('cut top',cut); print(s); print('share $ in top', round(t[t.top].official.sum()/t.official.sum()*100,1))
t['top']=t.grank<=87
top=t[t.top&t.has].sort_values('official',ascending=False)
print(top[['g24','grank','generic','named','official']].to_string())
print('top-fifth $ without the 4 biggest:', top.official.iloc[4:].sum(), ' rest-of-house $ without its 4 biggest:', t[~t.top&t.has].official.sort_values(ascending=False).iloc[4:].sum())
# how many top-fifth districts with ads are 2024 general 'no IE' ... also does the member party matter? skip
t.to_pickle('district_official2.pkl')
