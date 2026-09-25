import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_rows',200)
c = pd.read_csv('out_S10.csv', dtype={'CASE_ID':str}); c.columns=[x.lower() for x in c.columns]
c['era'] = pd.cut(c.term, [1945,1952,1968,1985,2004,2019,2024], labels=['Vinson 46-52','Warren 53-68','Burger 69-85','Rehnquist 86-04','Roberts 05-19','Roberts 20-24'])
arg = c[c.decision_type.isin([1,6,7])].copy()
arg['state_src'] = arg.source_state.notna()
arg['una'] = arg.min_votes==0
arg['one_vote'] = (arg.maj_votes-arg.min_votes)==1
arg['one_vote'] = arg.one_vote | ((arg.maj_votes==5)&(arg.min_votes==4))
arg['uncon_fed'] = arg.decl_uncon==2; arg['uncon_state'] = arg.decl_uncon==3
arg['prec'] = arg.prec_alt==1
g = arg.groupby('era', observed=True).agg(cases=('case_id','size'), per_term=('term', lambda s: len(s)/s.nunique()), state_src=('state_src','mean'), una=('una','mean'), one_vote=('one_vote','mean'),
    prec_n=('prec','sum'), prec_per100=('prec', lambda s: 100*s.mean()), uncon_fed=('uncon_fed','sum'), uncon_state=('uncon_state','sum'),
    cons=('dec_dir', lambda s: (s==1).sum()/s.isin([1,2]).sum()), rev=('party_winning', lambda s: (s==1).sum()/s.isin([0,1]).sum()))
print(g.round(3).to_string())
# per curiam unargued (type 2) by era, with direction
pc = c[c.decision_type==2]
print(pc.groupby('era', observed=True).agg(n=('case_id','size'), per_term=('term', lambda s: len(s)/s.nunique()), cons=('dec_dir', lambda s: (s==1).sum()/s.isin([1,2]).sum()),
     state_pet=('pet_state', lambda s: s.notna().mean()), rev=('party_winning', lambda s: (s==1).sum()/s.isin([0,1]).sum())).round(3).to_string())
t = arg.groupby('term').agg(cases=('case_id','size'), state_src=('state_src','mean'), prec=('prec','sum'), una=('una','mean')).tail(12)
print(t.round(3).to_string())
