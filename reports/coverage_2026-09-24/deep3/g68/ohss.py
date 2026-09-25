import pandas as pd, numpy as np, re
d=pd.read_pickle('S04_ohss_whole.pkl')
d['row']=d.index
# file order: release month from name
mon={m:i for i,m in enumerate(['january','february','march','april','may','june','july','august','september','october','november','december'],1)}
def rel(f):
    m=re.search(r'tables-([a-z]+)-(\d{4})',f); return int(m.group(2))*100+mon[m.group(1)]
d['data_through']=d.SOURCE_FILE_NAME.map(rel)
out=[]
for (f,sh),g in d.groupby(['SOURCE_FILE_NAME','SOURCE_SHEET_NAME'],sort=False):
    g=g.sort_index().copy()
    fy=g.FISCAL_YEAR.where(g.FISCAL_YEAR.fillna('').str.fullmatch(r'\d{4}'))
    g['FY']=fy.ffill()
    g=g[g.MONTH.fillna('').str.strip()!='']
    out.append(g)
m=pd.concat(out)
for c in ['TOTAL','BORDER','INTERIOR','VENEZUELA','CUBA','HAITI','NICARAGUA']:
    m[c+'_n']=pd.to_numeric(m[c].astype(str).str.replace(',',''),errors='coerce')
m.to_pickle('ohss_months.pkl')
# revisions: same sheet, FY, month across releases
mm=m[m.MONTH!='Total']
k=mm.groupby(['SOURCE_SHEET_NAME','FY','MONTH']).agg(n=('TOTAL_n','count'),lo=('TOTAL_n','min'),hi=('TOTAL_n','max'))
k=k[k.n>=2]
k['chg']=(k.hi-k.lo)/k.lo.replace(0,np.nan)
print('cells seen in 2+ releases',len(k),'changed',(k.hi!=k.lo).sum())
print(k.groupby(level=0).agg(cells=('n','size'),changed=('chg',lambda s:(s>0).sum()),med=('chg','median'),mx=('chg','max')).to_string())
print(k.sort_values('chg',ascending=False).head(15).to_string())
