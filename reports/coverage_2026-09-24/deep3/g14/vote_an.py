import pandas as pd, numpy as np, re
pd.set_option('display.width',250); pd.set_option('display.max_rows',300)
v=pd.read_csv('vote.csv')
v['ICPSR']=v.ICPSRS.map(lambda s:[int(x) for x in re.findall(r'\d+',s)])
R118={'G000574':'Gallego AZ S','T000483':'Trone MD S','B001299':'Banks IN S','P000618':'Porter CA S','L000551':'Lee CA S','C001114':'Curtis UT S',
      'M001195':'Mooney WV S','B001303':'Blunt Rochester DE S','S001150':'Schiff CA S','A000376':'Allred TX S','R000103':'Rosendale MT S','S001208':'Slotkin MI S','P000616':'Phillips MN P'}
R119={'C001103':'Carter GA','B001282':'Barr KY','C001119':'Craig MN','H001096':'Hageman WY','K000391':'Krishnamoorthi IL','H001091':'Hinson IA','K000385':'Kelly IL',
      'M001196':'Moulton MA','C001130':'Crockett TX','M001212':'Moore AL','H001095':'Hunt TX','C001129':'Collins GA','S001215':'Stevens MI','P000614':'Pappas NH','H001082':'Hern OK','L000595':'Letlow LA'}
DELEG={'AS','GU','PR','MP','VI','DC'}
h=v[(v.CHAMBER=='House')&(~v.STATE.isin(DELEG))].copy()
mx=h.groupby('CONGRESS').VOTES_ELIGIBLE.transform('max')
h['full']=h.VOTES_ELIGIBLE>=0.9*mx
h['run']=[(b in R118) if c==118 else (b in R119) for b,c in zip(h.BIOGUIDE,h.CONGRESS)]
print('Delegate rows dropped:', ((v.CHAMBER=='House')&(v.STATE.isin(DELEG))).sum())
for c in (118,119):
    g=h[(h.CONGRESS==c)]
    print(f'\n=== {c} House voting members: {len(g)}, full-service {g.full.sum()}; runners {g.run.sum()} (full {g[g.run].full.sum()})')
    gf=g[g.full]
    r=gf[gf.run]; o=gf[~gf.run]
    print('runner median missed pct %.2f, mean %.2f ; others median %.2f mean %.2f ; ratio of medians %.2f'%(r.MISSED_VOTE_PCT.median(),r.MISSED_VOTE_PCT.mean(),o.MISSED_VOTE_PCT.median(),o.MISSED_VOTE_PCT.mean(),r.MISSED_VOTE_PCT.median()/o.MISSED_VOTE_PCT.median()))
    print('runners total missed', r.MISSED_VOTES.sum(), 'eligible', r.VOTES_ELIGIBLE.sum(), 'pooled %.2f'%(100*r.MISSED_VOTES.sum()/r.VOTES_ELIGIBLE.sum()), '; others pooled %.2f'%(100*o.MISSED_VOTES.sum()/o.VOTES_ELIGIBLE.sum()))
    p75=o.MISSED_VOTE_PCT.quantile(.75); p90=o.MISSED_VOTE_PCT.quantile(.9)
    print('others p75 %.2f p90 %.2f ; runners above p75: %d/%d ; above p90: %d/%d ; above others median: %d/%d'%(p75,p90,(r.MISSED_VOTE_PCT>p75).sum(),len(r),(r.MISSED_VOTE_PCT>p90).sum(),len(r),(r.MISSED_VOTE_PCT>o.MISSED_VOTE_PCT.median()).sum(),len(r)))
    # rank within the chamber
    gf=gf.assign(rk=gf.MISSED_VOTE_PCT.rank(ascending=False,method='min'))
    names=R118 if c==118 else R119
    rr=gf[gf.run].sort_values('MISSED_VOTE_PCT',ascending=False)
    rr=rr.assign(label=rr.BIOGUIDE.map(names))
    # same-state peers
    st=gf[~gf.run].groupby('STATE').MISSED_VOTE_PCT.agg(['median','count'])
    rr=rr.join(st,on='STATE')
    print(rr[['BIOGUIDE','label','PARTY','VOTES_ELIGIBLE','MISSED_VOTES','MISSED_VOTE_PCT','rk','median','count']].to_string())
    print('runners above own-state median: %d/%d'%((rr.MISSED_VOTE_PCT>rr['median']).sum(),rr['median'].notna().sum()))
    # drop top 3
    r3=r.sort_values('MISSED_VOTE_PCT',ascending=False).iloc[3:]
    print('drop top 3 runners -> median %.2f'%r3.MISSED_VOTE_PCT.median())
# within-member: 119 runners, their 118 vs 119
w=h[h.full].pivot_table(index='BIOGUIDE',columns='CONGRESS',values='MISSED_VOTE_PCT')
w=w.dropna()
w['run26']=w.index.isin(R119)
w['d']=w[119]-w[118]
print('\nContinuing full-service House members in both: %d; 2026 Senate runners among them %d'%(len(w),w.run26.sum()))
print(w.groupby('run26')[[118,119,'d']].median())
print('runners whose rate rose: %d/%d ; others rose: %d/%d'%((w[w.run26].d>0).sum(),w.run26.sum(),(w[~w.run26].d>0).sum(),(~w.run26).sum()))
x=w[w.run26].copy(); x['who']=x.index.map(R119); print(x.sort_values('d',ascending=False).to_string())
h.to_csv('house_flagged.csv',index=False)
