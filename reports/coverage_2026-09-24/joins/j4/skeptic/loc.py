import csv, collections as C, statistics as st
P='../'
rows=list(csv.DictReader(open(P+'q03_county_panel.tsv'),delimiter='\t'))
dim={r['COUNTY_FIPS']:float(r['POPULATION_2020']) for r in csv.DictReader(open(P+'q04_dim_county.tsv'),delimiter='\t') if r['POPULATION_2020']}
f=lambda x: float(x) if x not in ('',None) else None
for r in rows:
    for k in ['POP0612','DU_ALL','DU','O30','BASE0612','DEATHS','POPYRS','Y_OK','ROWS_ALL','Y0612','RATE_AVG']: r[k]=f(r[k])
base=[r for r in rows if r['POP0612'] and r['DU'] and r['ROWS_ALL']==6 and r['Y0612']==7]
s7=list(csv.DictReader(open('s07.tsv'),delimiter='\t'))
ltc=C.defaultdict(float)
for x in s7:
    if x['K']=='ltc_like': ltc[x['FIPS']]+=float(x['DU'])
top={x['FIPS']:x for x in s7 if x['K']=='county_top'}
for r in base:
    r['p20']=dim.get(r['FIPS'],r['POP0612']); r['nsup']=6-r['Y_OK']; r['d']=r['DEATHS'] or 0
def dec(panel, key, fill=5, popkey='p20', label=''):
    p=sorted(panel,key=key); n=len(p); out=[]
    for i in range(10):
        g=p[i*n//10:(i+1)*n//10]; Pp=sum(r[popkey] for r in g)*6
        out.append((sum(r['d'] for r in g)+fill*sum(r['nsup'] for r in g))/Pp*1e5)
    print(f'{label:55s} n={n} D1={out[0]:.1f} D10={out[9]:.1f} ratio={out[9]/out[0]:.2f}  ', ' '.join(f'{x:.1f}' for x in out))
    return p
big=[r for r in base if r['POP0612']>=20000]
p=dec(big, lambda r:r['DU']/r['POP0612'], label='builder repro')
dec(big, lambda r:r['DU_ALL']/r['POP0612'], label='no mail-order exclusion at all')
dec(big, lambda r:(r['DU']-ltc.get(r['FIPS'],0))/r['POP0612'], label='also drop LTC/Kaiser/corrections >5M kept')
# pop denominators: use pop0612 for deaths too; use popyrs-implied
dec(big, lambda r:r['DU']/r['POP0612'], popkey='POP0612', label='2019-24 deaths over 2006-12 pop')
# fill with 0 / 9 already bounds. restrict to 20k by 2020 pop
dec([r for r in base if r['p20']>=20000], lambda r:r['DU']/r['POP0612'], label='20K cut on 2020 pop')
# pop growth by decile
n=len(p)
for i in range(10):
    g=p[i*n//10:(i+1)*n//10]
    gr=sum(r['p20'] for r in g)/sum(r['POP0612'] for r in g)
    sh=[float(top[r['FIPS']]['SHARE']) for r in g if r['FIPS'] in top]
    print(i+1,'pop growth 0612->2020',round(gr,3),'median top-buyer share',round(st.median(sh),3),'counties top buyer>30%',sum(s>0.3 for s in sh))
# top decile counties where top buyer >30%
g=p[9*n//10:]
for r in g:
    t=top.get(r['FIPS'])
    if t and float(t['SHARE'])>0.3: print('  ',r['COUNTY'],r['ST'],round(r['DU']/7/r['POP0612'],1),t['NM'],t['ACT'],round(float(t['SHARE']),2))
# Knox rank
rate=lambda r:(r['d']+5*r['nsup'])/(6*r['p20'])*1e5
rr=sorted(big,key=lambda r:-rate(r)); print('Knox rank',[i+1 for i,r in enumerate(rr) if r['FIPS']=='47093'], round(rate([r for r in big if r['FIPS']=='47093'][0]),1), 'Knox p20',dim['47093'])
# ranks with 2020 vs 06-12 for knox, suppression counts
print('supp yrs in 20K', sum(r['nsup'] for r in big))
print('--- suppression alternatives')
s9={x['GEOID']:x for x in csv.DictReader(open('s09.tsv'),delimiter='\t')}
def dec2(panel, fn, label):
    p=sorted(panel,key=lambda r:r['DU']/r['POP0612']); n=len(p); out=[]
    for i in range(10):
        g=p[i*n//10:(i+1)*n//10]; out.append(sum(fn(r) for r in g)/(6*sum(r['p20'] for r in g))*1e5)
    print(f'{label:55s} ratio={out[9]/out[0]:.2f}', ' '.join(f'{x:.1f}' for x in out))
def modeled(r, x1050=0):
    s=s9.get(r['FIPS']); 
    if not s: return r['d']+5*r['nsup']
    nr=int(s['SUP_NO_RATE']); n1050=int(s['N1050'] or 0)
    return r['d']+float(s['MODELED_SUP_DEATHS'])+5*nr+x1050*n1050
dec2(big, modeled, 'fill = CDC modeled rate x 2020 pop')
dec2(big, lambda r: modeled(r,25), '... plus 25 for each landing 10-50 year')
n1050_big=sum(int(s9[r['FIPS']]['N1050'] or 0) for r in big if r['FIPS'] in s9); print('10-50 rows in 20K set', n1050_big)
print('20K counties where >=3 yrs suppressed', sum(r['nsup']>=3 for r in big))
k=[r for r in big if r['FIPS']=='47093'][0]; print('knox ppc',round(k['DU']/7/k['POP0612'],1))
