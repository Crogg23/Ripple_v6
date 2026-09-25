import json, collections as C, statistics as st
d=json.load(open('s02.json',encoding='utf-8')); R=[dict(zip(d['cols'],r)) for r in d['rows']]
ARG={1,6,7}
fed=lambda p: p is not None and (p in (1,27) or 300<=p<=499)
CIRC={21:'1',22:'2',23:'3',24:'4',25:'5',26:'6',27:'7',28:'8',29:'9',30:'10',31:'11',32:'DC'}
print('fed-pet argued cases 2015-2024 NOT from a regional circuit:')
for r in sorted(R,key=lambda r:r['CASE_ID']):
    if 2015<=r['TERM']<=2024 and r['DT'] in ARG and fed(r['PET']) and r['SRC'] not in CIRC:
        print(' ',r['CASE_ID'],r['CASE_NAME'][:70],'src',r['SRC'],'srcst',r['SRC_ST'],'orig',r['ORIG'],'origst',r['ORIG_ST'],'cert',r['CERT'])
print('\nall 5th-circuit fed-pet argued cases 2005-2024 with origin:')
for r in sorted(R,key=lambda r:r['CASE_ID']):
    if 2005<=r['TERM']<=2024 and r['DT'] in ARG|{5} and fed(r['PET']) and r['SRC']==25:
        print(' ',r['CASE_ID'],r['CASE_NAME'][:60],'pet',r['PET'],'resp',r['RESP'],'orig',r['ORIG'],'origst',r['ORIG_ST'],'pw',r['PW'],'dt',r['DT'],'darg',r['DARG'])
# share: 5th of argued, all terms
tot=C.Counter(); c5=C.Counter(); per=C.defaultdict(C.Counter)
for r in R:
    if r['DT'] in ARG:
        tot[r['TERM']]+=1
        if r['SRC'] in CIRC: per[r['TERM']][CIRC[r['SRC']]]+=1
sh=sorted(((per[t]['5']/tot[t],t,per[t]['5'],tot[t]) for t in tot),reverse=True)
print('\n5th share top 6',[(t,n,T,round(100*s,1)) for s,t,n,T in sh[:6]])
print('5th count top 8',sorted(((per[t]['5'],t) for t in tot),reverse=True)[:8])
print('median share',round(100*st.median(s for s,_,_,_ in sh),1))
print('n terms',len(tot))
for t in (2021,2022,2023,2024): print(t, per[t].most_common(4))
