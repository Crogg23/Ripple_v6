import pandas as pd, numpy as np
j=pd.read_pickle('nfip_join.pkl')
L=j[j.COMMUNITY_ID_NUMBER.notna()].copy()
L['p0']=L.PARTICIPATING_IN_NFIP_FLAG=='0'
# event-time status: sanctioned if p0 and declared after the book's REG date (sanction date = map + 1 yr)
L['sanct_at_event']=L.p0 & L.REG.notna() & (L.DECL>L.REG)
L['p0_before']=L.p0 & ~L.sanct_at_event
print('p0 registrations total',L[L.p0].REGS.sum(),'after sanction date',L[L.sanct_at_event].REGS.sum(),'communities',L[L.sanct_at_event].COMMUNITY_ID_NUMBER.nunique())
own=L[L.OWN_RENT=='O']
def agg(d):
    return pd.Series({'regs':d.REGS.sum(),'ins':d.FLOOD_INS.sum(),'ins_pct':round(d.FLOOD_INS.sum()/d.REGS.sum()*100,1) if d.REGS.sum() else np.nan,
      'repair_n':d.REPAIR_N.sum(),'repair_amt':d.REPAIR_AMT.sum(),'ihp':d.IHP_AMT.sum(),'rpfvl':d.RPFVL.sum(),'unmet':d.UNMET_RP.sum(),'comms':d.COMMUNITY_ID_NUMBER.nunique()})
own['grp']=np.where(own.sanct_at_event,'sanctioned_at_event',np.where(own.p0,'p0_not_yet_sanctioned','participating'))
print(own.groupby('grp').apply(agg).to_string())
# same-disaster comparison: disasters with >=1 sanctioned owner registration
dz=own[own.sanct_at_event].DISASTER_NUMBER.unique()
o2=own[own.DISASTER_NUMBER.isin(dz)]
print('same disasters',len(dz)); print(o2.groupby('grp').apply(agg).to_string())
# per-disaster paired insured share
rows=[]
for d,g in o2.groupby('DISASTER_NUMBER'):
    s=g[g.grp=='sanctioned_at_event']; p=g[g.grp=='participating']
    if s.REGS.sum()>=10 and p.REGS.sum()>=10:
        rows.append((d,g.ST.iloc[0],g.DECL.min().date(),s.REGS.sum(),round(s.FLOOD_INS.sum()/s.REGS.sum()*100,1),p.REGS.sum(),round(p.FLOOD_INS.sum()/p.REGS.sum()*100,1),s.REPAIR_AMT.sum(),s.REPAIR_N.sum()))
pr=pd.DataFrame(rows,columns=['dis','st','decl','s_regs','s_ins%','p_regs','p_ins%','s_repair$','s_repair_n'])
print(pr.sort_values('s_regs',ascending=False).to_string())
print('disasters where sanctioned share < participating share:',(pr['s_ins%']<pr['p_ins%']).sum(),'of',len(pr))
# top sanctioned communities
top=own[own.sanct_at_event].groupby(['COMMUNITY_ID_NUMBER','COMMUNITY_NAME','STATE','FIRM','CEM_RAW','REG']).apply(agg).sort_values('regs',ascending=False)
print(top.head(25).to_string())
# all tenures for sanctioned
allt=L[L.sanct_at_event]
print('sanctioned all tenure regs',allt.REGS.sum(),'ins',allt.FLOOD_INS.sum(),'repair $',allt.REPAIR_AMT.sum(),'repair n',allt.REPAIR_N.sum(),'ihp',allt.IHP_AMT.sum(),'unmet',allt.UNMET_RP.sum())
top.to_csv('sanctioned_top.csv'); pr.to_csv('sanctioned_by_disaster.csv',index=False)
