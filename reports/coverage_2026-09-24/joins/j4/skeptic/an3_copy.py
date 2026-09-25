import csv, statistics as st, numpy as np, json
rows = list(csv.DictReader(open('../q03_county_panel.tsv'), delimiter='\t'))
dim = {r['COUNTY_FIPS']: float(r['POPULATION_2020']) for r in csv.DictReader(open('../q04_dim_county.tsv'), delimiter='\t') if r['POPULATION_2020']}
f = lambda x: float(x) if x not in ('', None) else None
for r in rows:
    for k in ['POP0612','DU_ALL','DU','O30','BASE0612','RATE_AVG','DEATHS','POPYRS','Y_OK','ROWS_ALL','BASE2015','Y0612','TOP0612']: r[k] = f(r[k])
base = [r for r in rows if r['POP0612'] and r['DU'] and r['ROWS_ALL'] == 6 and r['Y0612'] == 7]
nodim = [r['FIPS'] for r in base if r['FIPS'] not in dim]; print('no pop2020', len(nodim), nodim[:20])
for r in base:
    r['ppc'] = r['DU']/7/r['POP0612']; r['p20'] = dim.get(r['FIPS'], r['POP0612']); r['nsup'] = 6 - r['Y_OK']; r['d'] = r['DEATHS'] or 0
    r['imp5'] = (r['d'] + 5*r['nsup'])/(6*r['p20'])*1e5
def run(panel, label):
    out = {}
    p = sorted(panel, key=lambda r: r['ppc']); n = len(p); dec = []
    for i in range(10):
        g = p[i*n//10:(i+1)*n//10]; P = sum(r['p20'] for r in g)*6
        known = sum(r['d'] for r in g); ns = sum(r['nsup'] for r in g)
        dec.append(dict(decile=i+1, counties=len(g), pills_lo=round(g[0]['ppc'],1), pills_hi=round(g[-1]['ppc'],1),
            pills_pooled=round(sum(r['DU'] for r in g)/7/sum(r['POP0612'] for r in g),1),
            rate=round((known+5*ns)/P*1e5,1), rate_lo=round((known+1*ns)/P*1e5,1), rate_hi=round((known+9*ns)/P*1e5,1),
            deaths_known=int(known), sup_years=int(ns), pop2020=int(P/6),
            base0612=round(sum(r['BASE0612']*r['POP0612'] for r in g)/sum(r['POP0612'] for r in g),1),
            rate_med_county=round(st.median(r['imp5'] for r in g),1)))
    out['deciles'] = dec
    print(f'\n== {label} n={n}  D10/D1 pooled {dec[9]["rate"]/dec[0]["rate"]:.2f} (bounds {dec[9]["rate_lo"]/dec[0]["rate_hi"]:.2f}-{dec[9]["rate_hi"]/dec[0]["rate_lo"]:.2f})')
    for x in dec: print(x)
    # weighted OLS
    y = np.log(np.array([r['imp5'] for r in panel]) + 1); x1 = np.log([r['ppc'] for r in panel]); x2 = np.array([r['BASE0612'] for r in panel]); w = np.array([r['p20'] for r in panel])
    W = np.sqrt(w)
    def fit(X):
        b, *_ = np.linalg.lstsq(X*W[:,None], y*W, rcond=None); e = (y - X@b)*W
        cov = (e@e/(len(y)-X.shape[1]))*np.linalg.inv((X*W[:,None]).T@(X*W[:,None])); return b, np.sqrt(np.diag(cov))
    b0, s0 = fit(np.column_stack([np.ones(n), x1])); b1, s1 = fit(np.column_stack([np.ones(n), x1, x2]))
    out['ols'] = dict(b_alone=round(b0[1],3), t_alone=round(b0[1]/s0[1],1), b_ctrl=round(b1[1],3), t_ctrl=round(b1[1]/s1[1],1), b_base=round(b1[2],3), t_base=round(b1[2]/s1[2],1), corr_pills_base=round(float(np.corrcoef(x1,x2)[0,1]),3))
    print('pop-weighted OLS log(rate+1) on log(pills/person) [+ baseline]:', out['ols'])
    # stratified by baseline quintile (by county), pooled rates top vs bottom pill quintile within
    q = sorted(panel, key=lambda r: r['BASE0612']); m = len(q); strat = []
    for i in range(5):
        g = sorted(q[i*m//5:(i+1)*m//5], key=lambda r: r['ppc']); k = len(g)//5; lo, hi = g[:k], g[-k:]
        pr = lambda G: (sum(r['d'] for r in G)+5*sum(r['nsup'] for r in G))/(6*sum(r['p20'] for r in G))*1e5
        pp = lambda G: sum(r['DU'] for r in G)/7/sum(r['POP0612'] for r in G)
        strat.append(dict(base_quintile=i+1, base_range=f"{g and min(r['BASE0612'] for r in g):.1f}-{max(r['BASE0612'] for r in g):.1f}", counties_each_end=k,
            low_pills=round(pp(lo),1), low_rate=round(pr(lo),1), high_pills=round(pp(hi),1), high_rate=round(pr(hi),1), ratio=round(pr(hi)/pr(lo),2)))
    out['strat'] = strat
    for x in strat: print(x)
    return out
R = {'pop20k': run([r for r in base if r['POP0612'] >= 20000], 'pop>=20k'), 'all': run(base, 'all counties')}



