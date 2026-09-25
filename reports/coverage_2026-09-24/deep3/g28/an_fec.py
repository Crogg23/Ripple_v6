import pandas as pd
pd.set_option('display.width',250); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',60)
d=pd.read_pickle('out_S01.pkl')
print(d.shape, d.FEC_CMTE_ID.nunique())
for c in ['CMTE_DSGN','CMTE_TP','CMTE_FILING_FREQ','ORG_TP','CMTE_PTY_AFFILIATION']:
    print(c, d[c].fillna('<null>').replace('', '<blank>').value_counts().head(15).to_dict())
print('names top', d.CMTE_NM.value_counts().head(10).to_dict())
print('tres top', d.TRES_NM.fillna('<null>').str.upper().str.strip().value_counts().head(15).to_dict())
d['addr']=(d.CMTE_ST1.fillna('').str.upper().str.strip()+' | '+d.CMTE_CITY.fillna('').str.upper().str.strip()+' '+d.CMTE_ST.fillna(''))
print('addr top'); print(d.addr.value_counts().head(25).to_string())
print('cand id filled', (d.FEC_CAND_ID.fillna('').str.strip()!='').sum())
