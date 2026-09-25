"""Local math on S13 (sanction-coded rows) and the S08 x S09 join: where the FEMA sanction code lands, size-matched insured gap, case towns."""
import pandas as pd, numpy as np, json, re, warnings; warnings.filterwarnings('ignore')
def nrm(s):
    s=str(s).upper().replace('.','').replace("'",'')
    s=re.sub(r'\bSAINT\b','ST',s); s=re.sub(r'\bSAINTE\b','STE',s); s=re.sub(r'\bMOUNT\b','MT',s); s=re.sub(r'\bFORT\b','FT',s)
    return re.sub(r'\s+',' ',s).strip()
def ncounty(s):
    s=str(s).upper(); s=re.sub(r'\([^)]*\)','',s)
    s=re.sub(r'\b(COUNTY|PARISH|CENSUS AREA|BOROUGH|MUNICIPIO|MUNICIPALITY|CITY AND BOROUGH|DISTRICT)\b','',s); return nrm(s)
b=pd.read_pickle('book.pkl')
r=json.load(open('out_S13.json')); isc=pd.DataFrame(r['rows'],columns=r['cols'])
isc['key']=isc.ST+'|'+isc.CITY.map(nrm)+'|'+isc.COUNTY.map(ncounty)
k=b.drop_duplicates('key').set_index('key')
for c in ['PARTICIPATING_IN_NFIP_FLAG','REG']: isc[c]=isc.key.map(k[c])
print('sanction-coded rows',len(isc),'on a book town',isc.PARTICIPATING_IN_NFIP_FLAG.notna().sum(),'on out-of-program town',(isc.PARTICIPATING_IN_NFIP_FLAG=='0').sum())
cty=b[b.COMMUNITY_NAME.str.contains(r'COUNTY\s*\*|PARISH\s*\*',regex=True,na=False)].copy()
cty['cn']=cty.COMMUNITY_NAME.str.replace(r'\s*(COUNTY|PARISH)\s*\*.*$','',regex=True).str.strip()
isc['cn']=isc.COUNTY.str.replace(r'\s*\(.*\)','',regex=True).str.upper().str.strip()
m=isc.merge(cty[['STATE','cn','PARTICIPATING_IN_NFIP_FLAG']].rename(columns={'PARTICIPATING_IN_NFIP_FLAG':'county_p'}),left_on=['ST','cn'],right_on=['STATE','cn'],how='left')
print('sanction-coded rows in a county whose unincorporated area is out of the program',(m.county_p=='0').sum())
j=pd.read_pickle('nfip_join.pkl'); L=j[j.COMMUNITY_ID_NUMBER.notna()].copy()
L['p0']=L.PARTICIPATING_IN_NFIP_FLAG=='0'
L['strict']=L.p0 & L.REG.notna() & (L.DECL>L.REG) & ((L.CEM.isna())|(L.DECL>L.CEM))
own=L[L.OWN_RENT=='O']
td=own.groupby(['DISASTER_NUMBER','COMMUNITY_ID_NUMBER']).agg(regs=('REGS','sum'),ins=('FLOOD_INS','sum'),strict=('strict','max'),p0=('p0','max')).reset_index()
td=td[td.strict | ~td.p0]
dz=td[td.strict].DISASTER_NUMBER.unique(); t2=td[td.DISASTER_NUMBER.isin(dz)].copy()
t2['bin']=pd.cut(t2.regs,[0,5,15,40,100,1e9],labels=['1-5','6-15','16-40','41-100','100+'])
g=t2.groupby(['bin','strict']).agg(towns=('regs','size'),regs=('regs','sum'),ins=('ins','sum')); g['pct']=(g.ins/g.regs*100).round(1); print(g.to_string())
t3=t2[t2.regs>=5].copy(); t3['pct']=t3.ins/t3.regs*100
print('median town insured %', t3.groupby('strict').pct.median().round(1).to_dict(),'towns zero insured %',{k_:round((v.ins==0).mean()*100,1) for k_,v in t3.groupby('strict')})
