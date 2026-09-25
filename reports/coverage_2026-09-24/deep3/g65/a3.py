import pandas as pd, numpy as np, re
pd.set_option('display.width',250)
g=pd.read_csv('out_S09.csv',dtype={'SUB':str},keep_default_na=False,na_values=[''])
s=pd.read_csv('out_S10.csv',keep_default_na=False,na_values=[''])
c=pd.read_csv('out_S12.csv',keep_default_na=False,na_values=[''])
k=pd.read_csv('out_S13.csv',keep_default_na=False,na_values=[''],dtype={'CAND_OFFICE_DISTRICT':str})
s=s[s.REGIONS.fillna('').str.contains('US')]
s['fec']=s.PUBLIC_IDS_LIST.fillna('').apply(lambda t: sorted(set(re.findall(r'C[0-9]{8}',t))))
print('US advertisers',len(s),'with FEC id',(s.fec.str.len()>0).sum())
e=s[['ADVERTISER_ID','ADVERTISER_NAME','USD_TOTAL','fec']].explode('fec').dropna(subset=['fec'])
e=e.merge(c.rename(columns={'CMTE':'fec'}),on='fec',how='left')
print('adv-fec pairs',len(e),'cmte found',e.CMTE_NM.notna().sum())
cand=e[e.CMTE_TP.isin(['H','S']) & e.CAND_ID.notna()]
per=cand.groupby('ADVERTISER_ID').agg(cands=('CAND_ID','nunique'),cand_id=('CAND_ID','first'),cmte=('fec','first'),cmte_nm=('CMTE_NM','first'),tp=('CMTE_TP','first'),dsgn=('CMTE_DSGN','first'),pty=('CMTE_PTY_AFFILIATION','first'))
# advertisers that also list non-candidate committees
allf=e.groupby('ADVERTISER_ID').fec.nunique()
per['n_fec']=allf.reindex(per.index)
print('advertisers mapping to H/S candidate committees',len(per),'one candidate',(per.cands==1).sum(),'listing >1 fec id',(per.n_fec>1).sum())
per=per[per.cands==1]
# candidate home state: mode of office state across years; check vs CAND_ID letters
ks=k.groupby('CAND_ID').agg(ost=('CAND_OFFICE_ST',lambda v:v.mode().iat[0] if len(v.mode()) else None),nst=('CAND_OFFICE_ST','nunique'),
    name=('CAND_NAME','first'),ici=('CAND_ICI',lambda v:''.join(sorted(set(v.dropna())))),years=('CAND_ELECTION_YR',lambda v:','.join(str(x) for x in sorted(set(v)))),
    party=('CAND_PTY_AFFILIATION','first'),dist=('CAND_OFFICE_DISTRICT','first'))
per=per.join(ks,on='cand_id')
per['id_st']=per.cand_id.str[2:4]
print('home state missing',per.ost.isna().sum(),'office state != id letters',(per.ost.notna()&(per.ost!=per.id_st)).sum(), 'cands with >1 office state',(per.nst>1).sum())
per['hs']=per.ost.fillna(per.id_st)
# geo
gg=g.merge(per[['hs']],left_on='ADVERTISER_ID',right_index=True)
gg['kind']=np.where(gg.SUB.isna(),'blank',np.where(gg.SUB==gg.hs,'home','out'))
gg['lb']=np.where(gg.kind=='out',np.maximum(gg.USD-100,0),gg.USD)
agg=gg.pivot_table(index='ADVERTISER_ID',columns='kind',values='USD',aggfunc='sum',fill_value=0)
agg['out_lb']=gg[gg.kind=='out'].groupby('ADVERTISER_ID').lb.sum()
agg['n_out_1k']=gg[(gg.kind=='out')&(gg.USD>=1000)].groupby('ADVERTISER_ID').size()
top=gg[gg.kind=='out'].sort_values('USD',ascending=False).groupby('ADVERTISER_ID').head(1).set_index('ADVERTISER_ID')
agg['top_out']=top.SUB+':'+top.USD.astype(str)
per=per.join(agg.fillna({'out_lb':0,'n_out_1k':0}))
per['attr']=per.home+per.out
per['out_share']=per.out/per.attr
per['out_share_lb']=per.out_lb/per.attr
per=per.join(s.set_index('ADVERTISER_ID')[['ADVERTISER_NAME','USD_TOTAL']])
per.to_pickle('camp_adv.pkl')
# candidate level
cl=per.groupby('cand_id').agg(name=('name','first'),adv=('ADVERTISER_NAME','first'),n_adv=('ADVERTISER_NAME','size'),tp=('tp','first'),hs=('hs','first'),dist=('dist','first'),ici=('ici','first'),party=('party','first'),years=('years','first'),
   home_usd=('home','size'))
cl=per.groupby('cand_id')[['home','out','blank','out_lb','attr']].sum(numeric_only=True) if False else None
num=per.groupby('cand_id')[['out','blank','out_lb','attr']].sum()
num['home_usd']=per.groupby('cand_id').apply(lambda d:(d.attr-d.out).sum())
meta=per.groupby('cand_id').agg(name=('name','first'),adv=('ADVERTISER_NAME','first'),n_adv=('ADVERTISER_NAME','size'),tp=('tp','first'),hs=('hs','first'),dist=('dist','first'),ici=('ici','first'),party=('party','first'),years=('years','first'),top_out=('top_out','first'),cmte_nm=('cmte_nm','first'))
cl=meta.join(num)
cl['out_share']=cl.out/cl.attr; cl['out_share_lb']=cl.out_lb/cl.attr
cl.to_pickle('cand.pkl')
for tp in ['H','S']:
    x=cl[(cl.tp==tp)]
    for thr in [0,100000,1000000]:
        y=x[x.attr>=thr]
        print(f'\n{tp} attr>={thr}: cands {len(y)}, attr ${y.attr.sum()/1e6:.1f}M, out ${y.out.sum()/1e6:.1f}M ({y.out.sum()/y.attr.sum():.1%}), median out_share {y.out_share.median():.1%}, p75 {y.out_share.quantile(.75):.1%}, p90 {y.out_share.quantile(.9):.1%}, n>=50% {(y.out_share_lb>=.5).sum()}')
x=cl[(cl.tp=='H')&(cl.attr>=100000)].sort_values('out',ascending=False)
print(x.head(25)[['name','adv','hs','dist','ici','party','years','attr','home_usd','out','out_share','out_share_lb','top_out','n_adv']].to_string())
print('\ntop10 share of House out-of-state $ (attr>=100k):', x.out.head(10).sum()/x.out.sum(), ' all House out', cl[cl.tp=='H'].out.sum())
x2=cl[(cl.tp=='H')&(cl.attr>=100000)].sort_values('out_share',ascending=False)
print(x2.head(25)[['name','adv','hs','dist','ici','party','years','attr','out','out_share','out_share_lb','top_out']].to_string())
