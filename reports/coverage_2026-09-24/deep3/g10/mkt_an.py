import pandas as pd, numpy as np, re
pd.set_option('display.width',250); pd.set_option('display.max_columns',40); pd.set_option('display.max_rows',300); pd.set_option('display.max_colwidth',60)
m=pd.read_csv('mkt.csv',dtype=str)
print(m.CSRVARIATIONTYPE.value_counts())
print(m.METALLEVEL.value_counts())
def money(s):
    if pd.isna(s): return np.nan
    x=re.sub(r'[^0-9.]','',str(s).split('per')[0])
    return float(x) if x else np.nan
for c in ['TEHBINNTIER1_INDIVIDUALMOOP','TEHBDEDINNTIER1_INDIVIDUAL','MEHBDEDINNTIER1_INDIVIDUAL','DEHBDEDINNTIER1_INDIVIDUAL','TEHBINNTIER1_FAMILYPERGROUPMOOP','SBCHAVINGABABYDEDUCTIBLE','SBCHAVINGABABYCOPAYMENT','SBCHAVINGABABYCOINSURANCE','SBCHAVINGABABYLIMIT']:
    m[c+'_n']=m[c].map(money)
h=m[(m.DENTALONLYPLAN=='No')&(m.MARKETCOVERAGE=='Individual')]
print('health individual rows',len(h),'plans',h.STANDARDCOMPONENTID.nunique())
print('MOOP > 10600:', (h.TEHBINNTIER1_INDIVIDUALMOOP_n>10600).sum(), h[h.TEHBINNTIER1_INDIVIDUALMOOP_n>10600][['PLANID','ISSUERMARKETPLACEMARKETINGNAME','STATECODE','METALLEVEL','CSRVARIATIONTYPE','TEHBINNTIER1_INDIVIDUALMOOP']].head(20))
print('family MOOP > 21200:', (h.TEHBINNTIER1_FAMILYPERGROUPMOOP_n>21200).sum())
h=h.copy()
h['ded']=np.where(h.MEDICALDRUGDEDUCTIBLESINTEGRATED=='Yes',h.TEHBDEDINNTIER1_INDIVIDUAL_n,h.MEHBDEDINNTIER1_INDIVIDUAL_n)
std=h[h.CSRVARIATIONTYPE.str.contains('Standard',na=False)&h.CSRVARIATIONTYPE.str.contains('On Exchange',na=False)]
print('standard on-exchange variants',len(std))
print(std.groupby('METALLEVEL').agg(n=('ded','size'),med_ded=('ded','median'),max_ded=('ded','max'),med_moop=('TEHBINNTIER1_INDIVIDUALMOOP_n','median'),at_cap=('TEHBINNTIER1_INDIVIDUALMOOP_n',lambda s:(s==10600).mean()),ded_eq_moop=('ded',lambda s: np.nan)))
std=std.copy(); std['allded']=(std.ded>=std.TEHBINNTIER1_INDIVIDUALMOOP_n)&std.ded.notna()
print(std.groupby('METALLEVEL').allded.mean().round(3))
std['baby']=std[['SBCHAVINGABABYDEDUCTIBLE_n','SBCHAVINGABABYCOPAYMENT_n','SBCHAVINGABABYCOINSURANCE_n','SBCHAVINGABABYLIMIT_n']].sum(axis=1,min_count=1)
print(std.groupby('METALLEVEL').baby.describe().round(0))
std.to_csv('mkt_std.csv',index=False)
