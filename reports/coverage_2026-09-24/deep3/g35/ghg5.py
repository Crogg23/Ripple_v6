import pandas as pd, numpy as np, re
pd.set_option('display.width',260); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',40); pd.set_option('display.max_rows',200)
x=pd.read_pickle('x.pkl'); m=pd.read_pickle('m.pkl'); fac=pd.read_pickle('fac.pkl')
def is_lf(sub,name):
    sub=str(sub); name=str(name).upper()
    return bool(re.search(r'(^|,)\s*(HH|TT)\s*(,|$)',sub)) or 'LANDFILL' in name or ' LF' in name or 'SLF' in name
fac['landfill']=[is_lf(s,n) for s,n in zip(fac.subparts,fac.name)]
x['landfill']=[is_lf(s,n) for s,n in zip(x.subparts,x.name)]
# subpart detail for landfills
fac['hh']=fac.subparts.fillna('').str.contains(r'(^|,)\s*HH\s*(,|$)')
fac['tt']=fac.subparts.fillna('').str.contains(r'(^|,)\s*TT\s*(,|$)')
cur=m[m.YR==2023].set_index('FACILITY_ID').st
fac['s23']=cur.reindex(fac.index).fillna('NO_2023_ROW')
lf=fac[fac.landfill]
print('landfill facilities ever:',len(lf),' HH:',lf.hh.sum(),' TT:',lf.tt.sum())
print(lf.s23.value_counts())
print(lf.groupby('s23').agg(n=('peak','size'),big_last=('last_direct',lambda s:(s>=25000).sum()),med_last=('last_direct','median'),
   small3=('max_last3',lambda s:(s<15000).sum()),small5=('max_last5',lambda s:(s<25000).sum())))
# unknown landfills detail
u=x[(x.status2023=='STOPPED_REPORTING_UNKNOWN_REASON')&x.landfill].copy()
# years flagged unknown / valid for each
st=m[m.st!='REPORTED'].groupby('FACILITY_ID').apply(lambda d: ','.join(f"{int(y)}{'U' if s.endswith('UNKNOWN_REASON') else 'V'}" for y,s in zip(d.YR,d.st)))
u['flags']=st
# same city/state other facility reporting after exit (possible re-registration)
rep=m[m.st=='REPORTED']
def reregs(r):
    d=rep[(rep.STATE==r.state)&(rep.CITY.str.upper()==str(r.city).upper())&(rep.FACILITY_ID!=r.name)&(rep.YR>=r.exit_yr)]
    return '; '.join(sorted(set(d.FACILITY_NAME.astype(str).str[:30])))[:120]
u['same_city_after']=u.apply(reregs,axis=1)
cols=['name','parent','city','state','first_rep','last_rep','last_direct','max_last3','max_last5','flags','echo_IS_ACTIVE','echo_LAST_INSP','echo_FORMAL','echo_COMPLIANCE','echo_QNC','still_other','same_city_after','subparts']
print(u.sort_values('last_direct',ascending=False)[cols].to_string())
u.sort_values('last_direct',ascending=False)[cols+['frs']].to_csv('unknown_landfills.csv')
# overall unknown flips
fl=m[m.st!='REPORTED'].groupby('FACILITY_ID').st.apply(lambda s: s.iloc[0][19:22]+'>'+s.iloc[-1][19:22])
print(fl.value_counts())
fac.to_pickle('fac2.pkl'); x.to_pickle('x2.pkl')
