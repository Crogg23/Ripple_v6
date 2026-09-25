import pandas as pd, numpy as np
pd.set_option('display.width',240); pd.set_option('display.max_colwidth',40)
d=pd.read_pickle('oflc_prep.pkl')
cert=d[(d.CASE_STATUS=='CERTIFIED')&(d.VISA_CLASS=='H-1B')&d.w_ann.between(20000,1000000)].copy()
keys=['APPLE','WELLS FARGO','AT&T','ANTHEM','VERIZON','CISCO','FORD MOTOR','PNC','T MOBILE','COMCAST','GOOGLE','AMERICAN EXPRESS','WALMART','CAPITAL ONE','NIKE','FANNIE MAE','MICROSOFT','FIDELITY','JP MORGAN','JPMORGAN','CATERPILLAR','KAISER','UNITED AIRLINES','FEDEX','CHARTER COMMUNICATIONS','CITIGROUP','CITIBANK','KROGER','HUMANA','PFIZER','CVS','UNITED SERVICES AUTOMOBILE','SCHWAB','CHARLES SCHWAB','SYNCHRONY','QUEST DIAGNOSTICS','BANK OF AMERICA','INTEL','FACEBOOK','AMAZON','IBM','INTERNATIONAL BUSINESS MACHINES','DELL','HOME DEPOT','TARGET','STATE FARM','TOYOTA','GENERAL MOTORS','JOHNSON & JOHNSON','UNITEDHEALTH','OPTUM','MORGAN STANLEY','GOLDMAN SACHS','PAYPAL','INTUIT','ORACLE','SALESFORCE','DISCOVER','BEST BUY','LOWES','MCKESSON','CIGNA','AETNA','BARCLAYS','TD AMERITRADE','FREDDIE MAC','FEDERAL HOME LOAN MORTGAGE','FEDERAL NATIONAL MORTGAGE']
alias={'JPMORGAN':'JP MORGAN','CITIBANK':'CITIGROUP','CHARLES SCHWAB':'SCHWAB','INTERNATIONAL BUSINESS MACHINES':'IBM','FEDERAL HOME LOAN MORTGAGE':'FREDDIE MAC','FEDERAL NATIONAL MORTGAGE':'FANNIE MAE','OPTUM':'UNITEDHEALTH'}
def key(s):
    out=pd.Series('',index=s.index)
    for k in sorted(keys,key=len,reverse=True):
        m=(out=='')&((s==k)|s.str.startswith(k+' '))
        out[m]=alias.get(k,k)
    return out
cert['own_key']=key(cert.emp_n)
bad=cert.EMPLOYER_NAME.str.upper().str.contains('APPLE TREE|APPLE AMERICAN|CISCO COLLEGE|GOOGLE VENTURES',regex=True)
cert.loc[bad,'own_key']=''
print('own rows dropped as name collisions',bad.sum())
cert['cli_key']=np.where(cert.SECONDARY_ENTITY_1=='Y', key(cert.sec_n), '')
cert.to_pickle('oflc_cert_keys.pkl')
own=cert[cert.own_key!='']; ven=cert[(cert.cli_key!='')&(cert.own_key!=cert.cli_key)]
print('own rows',len(own),'vendor rows',len(ven))
IT=cert.SOC_CODE.str[:5].isin(['15-11','15-12'])
rows=[]
for k in sorted(set(own.own_key)|set(ven.cli_key)):
    o=own[(own.own_key==k)&IT.loc[own.index]]; v=ven[(ven.cli_key==k)&IT.loc[ven.index]]
    # match on SOC + worksite state; weight each cell by vendor rows
    go=o.groupby(['SOC_CODE','WORKSITE_STATE_1']).w_ann.agg(['median','size']).rename(columns={'median':'own_med','size':'own_n'})
    gv=v.groupby(['SOC_CODE','WORKSITE_STATE_1']).agg(ven_med=('w_ann','median'),ven_n=('w_ann','size'),ven_L1=('PW_WAGE_LEVEL_1',lambda s:(s=='Level I').mean()),ven_L12=('PW_WAGE_LEVEL_1',lambda s:s.isin(['Level I','Level II']).mean()))
    j=go.join(gv,how='inner'); j=j[(j.own_n>=10)&(j.ven_n>=10)]
    if len(j)==0: continue
    wv=j.ven_n
    rows.append(dict(client=k,cells=len(j),own_n=int(j.own_n.sum()),ven_n=int(wv.sum()),vendors=v.emp_n.nunique(),
        own_med_w=np.average(j.own_med,weights=wv),ven_med_w=np.average(j.ven_med,weights=wv),
        own_L12=o.PW_WAGE_LEVEL_1.isin(['Level I','Level II']).mean(), ven_L12=v.PW_WAGE_LEVEL_1.isin(['Level I','Level II']).mean()))
r=pd.DataFrame(rows); r['gap']=r.ven_med_w/r.own_med_w-1
r=r.sort_values('ven_n',ascending=False)
print(r.round(3).to_string(index=False))
print('clients',len(r),'median gap',r.gap.median().round(3),'weighted gap',np.average(r.gap,weights=r.ven_n).round(3))
r.to_csv('client_gap.csv',index=False)
