import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_rows',200)
c = pd.read_csv('out_S10.csv', dtype={'CASE_ID':str})
c.columns = [x.lower() for x in c.columns]
print('variants>1:', (c.n_variants>1).sum(), 'rows per case', c.n_rows.describe().to_dict())
print(c.decision_type.value_counts().sort_index().to_dict())
arg = c[c.decision_type.isin([1,6,7])].copy()
print('argued cases', len(arg))
# federal party
def fed(x): return x in (1,27) or (300<=x<=499) if pd.notna(x) else False
arg['fed_pet'] = arg.pet.apply(fed); arg['fed_res'] = arg.res.apply(fed)
arg['fed_party'] = arg.fed_pet | arg.fed_res
arg['fed_win'] = np.where(arg.fed_pet, arg.party_winning==1, np.where(arg.fed_res, arg.party_winning==0, np.nan))
arg = arg[arg.party_winning.isin([0,1])| ~arg.fed_party]
t = arg[arg.fed_party & ~(arg.fed_pet & arg.fed_res)].groupby('term').agg(n=('fed_win','size'), won=('fed_win','sum'))
t['rate']=t.won/t.n
t['roll3_rate'] = t.won.rolling(3).sum()/t.n.rolling(3).sum()
print(t.tail(20).to_string())
print('lowest 3-term windows:'); print(t.sort_values('roll3_rate').head(6).to_string())
arg.to_pickle('scdb_arg.pkl')
