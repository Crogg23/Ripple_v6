import json, collections as C, statistics as st
d=json.load(open('q10.json',encoding='utf-8')); R=[dict(zip(d['cols'],r)) for r in d['rows']]
def i(x):
    try: return int(float(x))
    except: return None
CIRC={21:'1st',22:'2nd',23:'3rd',24:'4th',25:'5th',26:'6th',27:'7th',28:'8th',29:'9th',30:'10th',31:'11th',32:'DC',8:'Fed'}
ARG={1,6,7}
def stats(filt):
    out=C.defaultdict(lambda:C.Counter())
    for r in R:
        if i(r['DECISION_TYPE_CODE']) not in ARG: continue
        c=i(r['CASE_SOURCE_CODE']); t=i(r['TERM'])
        k=filt(c,t)
        if k is None: continue
        pw=i(r['PARTY_WINNING']); n=r['N_CASES']
        o=out[k]; o['n']+=n
        if pw==1: o['win']+=n; o['win_unan']+=r['N_UNANIMOUS']
        if pw==0: o['loss']+=n
        lcd=i(r['LC_DISPOSITION_DIRECTION_CODE']); dd=i(r['DECISION_DIRECTION_CODE'])
        if lcd==1: o['lc_cons']+=n
        if lcd==2: o['lc_lib']+=n
        if pw==1 and lcd==1: o['rev_of_cons']+=n
        if pw==1 and lcd==2: o['rev_of_lib']+=n
    return out
def pr(out,keys):
    for k in keys:
        o=out.get(k)
        if not o: print(' ',k,'none'); continue
        dec=o['win']+o['loss']
        print('  %-14s n=%4d  reversed(petitioner won)=%3d/%3d=%5.1f%%  unanimous-rev=%3d  lc_cons=%3d lc_lib=%3d  rev_of_cons=%3d rev_of_lib=%3d'%(k,o['n'],o['win'],dec,100*o['win']/dec if dec else 0,o['win_unan'],o['lc_cons'],o['lc_lib'],o['rev_of_cons'],o['rev_of_lib']))
print('== all circuits, argued cases, terms 2020-2024')
out=stats(lambda c,t: CIRC.get(c) if 2020<=t<=2024 else None); pr(out,CIRC.values())
rates=[100*o['win']/(o['win']+o['loss']) for o in out.values() if o['win']+o['loss']>=10]
print('  median circuit rate (n>=10):',st.median(rates))
allc=C.Counter()
for o in out.values(): allc.update(o)
print('  all circuits pooled: win',allc['win'],'of',allc['win']+allc['loss'],round(100*allc['win']/(allc['win']+allc['loss']),1))
print('\n== all circuits, argued, terms 2010-2019')
out2=stats(lambda c,t: CIRC.get(c) if 2010<=t<=2019 else None); pr(out2,CIRC.values())
print('\n== 5th Circuit by 5-term block')
out3=stats(lambda c,t: (t-1946)//5*5+1946 if c==25 else None); pr(out3,sorted(out3))
print('\n== 9th Circuit by 5-term block')
out4=stats(lambda c,t: (t-1946)//5*5+1946 if c==29 else None); pr(out4,sorted(out4))
print('\n== 5th Circuit by term 2015-2024')
out5=stats(lambda c,t: t if c==25 and t>=2015 else None); pr(out5,sorted(out5))
print('\n== all non-5th circuits, by term 2015-2024')
out6=stats(lambda c,t: t if c in CIRC and c!=25 and t>=2015 else None); pr(out6,sorted(out6))
print('\n== 11th Circuit by term 2015-2024')
out7=stats(lambda c,t: t if c==31 and t>=2015 else None); pr(out7,sorted(out7))
