import pandas as pd, numpy as np, warnings; warnings.filterwarnings('ignore')
j=pd.read_pickle('nfip_join.pkl')
L=j[j.COMMUNITY_ID_NUMBER.notna()].copy()
# stricter sanction timing: declared after BOTH the book's reg date and the current map date
L['p0']=L.PARTICIPATING_IN_NFIP_FLAG=='0'
L['sanct_strict']=L.p0 & L.REG.notna() & (L.DECL>L.REG) & ((L.CEM.isna())|(L.DECL>L.CEM))
own=L[L.OWN_RENT=='O']
s=own[own.sanct_strict]
print('STRICT sanctioned owners',s.REGS.sum(),'ins',s.FLOOD_INS.sum(),round(s.FLOOD_INS.sum()/s.REGS.sum()*100,1),'repair n',s.REPAIR_N.sum(),'repair $',round(s.REPAIR_AMT.sum()),'comms',s.COMMUNITY_ID_NUMBER.nunique(),'disasters',s.DISASTER_NUMBER.nunique())
dz=s.DISASTER_NUMBER.unique(); p=own[(~own.p0)&own.DISASTER_NUMBER.isin(dz)]
print('same-disaster participating owners',p.REGS.sum(),round(p.FLOOD_INS.sum()/p.REGS.sum()*100,1),'repair rate',round(p.REPAIR_N.sum()/p.REGS.sum()*100,1),'vs sanct',round(s.REPAIR_N.sum()/s.REGS.sum()*100,1))
# median community: per-community insured share
cs=s.groupby('COMMUNITY_ID_NUMBER').agg(r=('REGS','sum'),i=('FLOOD_INS','sum'));cs['pct']=cs.i/cs.r*100
print('sanct comms',len(cs),'median comm insured %',cs.pct.median(),'comms w/ >=10 regs',(cs.r>=10).sum(),'median among those',cs[cs.r>=10].pct.median())
print('top 4 comms share of sanct owner regs', round(cs.r.nlargest(4).sum()/cs.r.sum()*100,1))
print('by state', s.groupby('ST').REGS.sum().sort_values(ascending=False).head(8).to_dict())
# ---- map age at event, participating only, map in force at event known (current map predates the declaration)
P=own[(~own.p0) & own.CEM.notna() & (own.CEM<own.DECL)].copy()
P['age']=(P.DECL-P.CEM).dt.days/365.25
P['bucket']=pd.cut(P.age,[0,5,10,20,30,100],labels=['0-5','5-10','10-20','20-30','30+'])
g=P.groupby('bucket').agg(regs=('REGS','sum'),ins=('FLOOD_INS','sum'),comms=('COMMUNITY_ID_NUMBER','nunique'))
g['pct']=(g.ins/g.regs*100).round(1); print(g.to_string())
# within-disaster: for each disaster, 30+ vs <10 insured share
rows=[]
for d,gg in P.groupby('DISASTER_NUMBER'):
    o=gg[gg.age>=30]; n=gg[gg.age<10]
    if o.REGS.sum()>=20 and n.REGS.sum()>=20:
        rows.append((d,gg.ST.iloc[0],gg.DECL.min().year,o.REGS.sum(),o.FLOOD_INS.sum()/o.REGS.sum()*100,n.REGS.sum(),n.FLOOD_INS.sum()/n.REGS.sum()*100))
w=pd.DataFrame(rows,columns=['dis','st','yr','old_regs','old_pct','new_regs','new_pct'])
print('disasters compared',len(w),'old lower in',(w.old_pct<w.new_pct).sum(),'median diff',round((w.old_pct-w.new_pct).median(),1))
print('pooled old',round((w.old_pct*w.old_regs).sum()/w.old_regs.sum(),1),'pooled new',round((w.new_pct*w.new_regs).sum()/w.new_regs.sum(),1),'old regs',w.old_regs.sum(),'new regs',w.new_regs.sum())
print(w.sort_values('old_regs',ascending=False).head(15).round(1).to_string())
# how many participating communities are on 30+yr-old maps today
b=pd.read_pickle('book.pkl')
bp=b[(b.PARTICIPATING_IN_NFIP_FLAG=='1')&b.CEM.notna()]
bp['age_now']=(pd.Timestamp('2026-09-24')-bp.CEM).dt.days/365.25
print('participating with a map date',len(bp),'map 30+ yrs old',(bp.age_now>=30).sum(),round((bp.age_now>=30).mean()*100,1))
st=bp.groupby('STATE').agg(n=('age_now','size'),old=('age_now',lambda x:(x>=30).sum()));st['pct']=(st.old/st.n*100).round(1)
print('state median pct',st.pct.median()); print(st[st.n>=50].sort_values('pct',ascending=False).head(12).to_string())
w.to_csv('mapage_by_disaster.csv',index=False)
