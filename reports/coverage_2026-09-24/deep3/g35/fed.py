import pandas as pd, numpy as np
pd.set_option('display.width',220)
d=pd.read_csv('out_S19.csv')
d['DEPT']=d.DEPT.str.replace(' -- not otherwise classified;','',regex=False).str.strip()
key=['MAJ','AIR','WAT','RCRA']
nf=d[d.DEPT=='(not federal)'].set_index(key)
nf_rate=(nf.CHRONIC8/nf.N); nf_formal=(nf.WITH_FORMAL/nf.N); nf_any=nf.ANY_NC/nf.N
fed=d[~d.DEPT.isin(['(not federal)','(no FRS row)'])].copy()
fed=fed.join(nf_rate.rename('r_c'),on=key).join(nf_formal.rename('r_f'),on=key).join(nf_any.rename('r_a'),on=key)
fed['exp_c']=fed.N*fed.r_c; fed['exp_f']=fed.N*fed.r_f; fed['exp_a']=fed.N*fed.r_a
g=fed.groupby('DEPT').agg(n=('N','sum'),chronic=('CHRONIC8','sum'),exp_chronic=('exp_c','sum'),anync=('ANY_NC','sum'),exp_any=('exp_a','sum'),formal=('WITH_FORMAL','sum'),exp_formal=('exp_f','sum'),pen=('PENALTIES','sum'))
g.loc['ALL FEDERAL']=g.sum()
g['chronic_ratio']=g.chronic/g.exp_chronic; g['any_ratio']=g.anync/g.exp_any; g['formal_ratio']=g.formal/g.exp_formal
print(g.sort_values('n',ascending=False).round(2).to_string())
print('nonfed totals', nf.N.sum(), nf.CHRONIC8.sum(), nf.WITH_FORMAL.sum())
print('no FRS row', d[d.DEPT=='(no FRS row)'][['MAJ','AIR','WAT','RCRA','N','CHRONIC8']].to_string())
