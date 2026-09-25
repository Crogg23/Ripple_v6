"""Local join: NFIP community book (S08) x FEMA flood-damaged household aid aggregate (S09). No warehouse calls."""
import pandas as pd, re, numpy as np
b=pd.read_csv('out_S08.csv',dtype=str)
for c in ['FHBM','FIRM','CEM','REG']:
    b[c]=pd.to_datetime(b[c],errors='coerce')
ia=pd.read_csv('out_S09.csv',dtype=str)
num=['REGS','IDS','FLOOD_INS','HOME_INS','IHP_ELIG','IHP_AMT','REPAIR_AMT','REPAIR_N','RPFVL','UNMET_RP','FLOOD_DMG_AMT','PRIMARY_RES']
for c in num: ia[c]=pd.to_numeric(ia[c])
ia['DECL']=pd.to_datetime(ia.DECL)

def nrm(s):
    s=str(s).upper().replace('.','').replace("'",'')
    s=re.sub(r'\bSAINT\b','ST',s); s=re.sub(r'\bSAINTE\b','STE',s); s=re.sub(r'\bMOUNT\b','MT',s); s=re.sub(r'\bFORT\b','FT',s)
    return re.sub(r'\s+',' ',s).strip()
def ncounty(s):
    s=str(s).upper()
    s=re.sub(r'\([^)]*\)','',s)
    s=re.sub(r'\b(COUNTY|PARISH|CENSUS AREA|BOROUGH|MUNICIPIO|MUNICIPALITY|CITY AND BOROUGH|DISTRICT)\b','',s)
    return nrm(s)
m=b.COMMUNITY_NAME.str.extract(r'^(.*),\s*([^,]*)$')
b['nm']=m[0].fillna('').map(nrm); b['suf']=m[1].fillna('').str.replace(r'\s+',' ',regex=True).str.strip()
b['cty']=b.COUNTY.map(ncounty)
city_types={'CITY OF','TOWN OF','VILLAGE OF','BOROUGH OF','CITYOF','BORO OF','CITY','TOWN','VILLAGE','BOROUGH'}
b['key']=b.STATE+'|'+b.nm+'|'+b.cty
dup=b[b.nm!=''].key.value_counts(); dupk=set(dup[dup>1].index)
cand=b[b.suf.isin(city_types) & ~b.key.isin(dupk) & (b.nm!='')].copy()
print('book rows',len(b),'city-type candidates',len(cand),'ambiguous keys dropped',len(dupk))
ia['key']=ia.ST+'|'+ia.CITY.map(nrm)+'|'+ia.COUNTY.map(ncounty)
j=ia.merge(cand[['key','COMMUNITY_ID_NUMBER','COMMUNITY_NAME','STATE','PARTICIPATING_IN_NFIP_FLAG','TRIBAL_FLAG','FHBM','FIRM','CEM','CEM_RAW','REG','CRS_CLASS_RATING']],on='key',how='left')
land=j.COMMUNITY_ID_NUMBER.notna()
print('flood-damaged regs',ia.REGS.sum(),'landed on a city-type community',j[land].REGS.sum(), round(j[land].REGS.sum()/ia.REGS.sum()*100,1),'%')
print('communities hit', j[land].COMMUNITY_ID_NUMBER.nunique())
j.to_pickle('nfip_join.pkl'); b.to_pickle('book.pkl')
