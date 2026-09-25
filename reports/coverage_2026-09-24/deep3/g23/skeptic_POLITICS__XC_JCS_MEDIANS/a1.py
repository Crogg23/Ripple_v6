import json, collections as C
d=json.load(open('s02.json',encoding='utf-8')); R=[dict(zip(d['cols'],r)) for r in d['rows']]
print('cases',len(R),'distinct case_id',len({r['CASE_ID'] for r in R}))
print('inconsistent within case:',{k:sum(1 for r in R if (r[k] or 0)>1) for k in ['ND_PET','ND_SRC','ND_DT','ND_PW','ND_TERM','N_DOCKET','N_RUNS']})
print('terms',min(r['TERM'] for r in R),max(r['TERM'] for r in R))
print('decision types',sorted(C.Counter(r['DT'] for r in R).items(),key=lambda x:str(x[0])))
print('null PET',sum(1 for r in R if r['PET'] is None),'null SRC',sum(1 for r in R if r['SRC'] is None))
ARG={1,6,7}
fed=lambda p: p is not None and (p in (1,27) or 300<=p<=499)
CIRC={21:'1',22:'2',23:'3',24:'4',25:'5',26:'6',27:'7',28:'8',29:'9',30:'10',31:'11',32:'DC'}
def split(lo,hi,src_ok,args=ARG):
    rs=[r for r in R if lo<=r['TERM']<=hi and r['DT'] in args and src_ok(r['SRC'])]
    return sum(1 for r in rs if fed(r['PET'])), len(rs)
for lab,(lo,hi) in {'2015-20':(2015,2020),'2021-24':(2021,2024)}.items():
    print(lab,'5th fed/all',split(lo,hi,lambda s:s==25),' other11',split(lo,hi,lambda s:s in CIRC and s!=25))
print('with type 5 (equally divided) and 2 added:')
for lab,(lo,hi) in {'2015-20':(2015,2020),'2021-24':(2021,2024)}.items():
    print(lab,'5th',split(lo,hi,lambda s:s==25,{1,5,6,7}),'other',split(lo,hi,lambda s:s in CIRC and s!=25,{1,5,6,7}))
# per term, per circuit fed-pet counts, 2005-2024
print('\nper term fed-pet / argued, 5th | 9th | DC | other-11 total')
for t in range(2005,2025):
    row=[]
    for s in (25,29,32):
        rs=[r for r in R if r['TERM']==t and r['DT'] in ARG and r['SRC']==s]
        row.append('%d/%d'%(sum(fed(r['PET']) for r in rs),len(rs)))
    rs=[r for r in R if r['TERM']==t and r['DT'] in ARG and r['SRC'] in CIRC and r['SRC']!=25]
    rs_all=[r for r in R if r['TERM']==t and r['DT'] in ARG]
    print(t,row,'other11 %d/%d'%(sum(fed(r['PET']) for r in rs),len(rs)),'all argued',len(rs_all),'fed-pet any source',sum(fed(r['PET']) for r in rs_all))
