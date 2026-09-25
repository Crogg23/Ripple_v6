import csv, statistics as st, numpy as np, json
rows = list(csv.DictReader(open('q03_county_panel.tsv'), delimiter='\t'))
f = lambda x: float(x) if x not in ('', None) else None
for r in rows:
    for k in ['POP0612','DU_ALL','DU','O30','BASE0612','RATE_AVG','DEATHS','POPYRS','Y_OK','ROWS_ALL','BASE2015','Y0612','TOP0612']: r[k] = f(r[k])
base = [r for r in rows if r['POP0612'] and r['DU'] and r['ROWS_ALL'] == 6 and r['Y0612'] == 7]
for r in base:
    r['ppc'] = r['DU']/7/r['POP0612']
    nsup = 6 - r['Y_OK']; d = r['DEATHS'] or 0
    r['imp5'] = (d + 5*nsup)/(6*r['POP0612'])*1e5
    r['imp1'] = (d + 1*nsup)/(6*r['POP0612'])*1e5
    r['imp9'] = (d + 9*nsup)/(6*r['POP0612'])*1e5
def deciles(panel, key):
    p = sorted(panel, key=lambda r: r['ppc']); n = len(p); out = []
    for i in range(10):
        g = p[i*n//10:(i+1)*n//10]
        out.append(dict(decile=i+1, counties=len(g), ppc_lo=round(g[0]['ppc'],1), ppc_hi=round(g[-1]['ppc'],1),
            ppc_med=round(st.median(r['ppc'] for r in g),1), rate_med=round(st.median(r[key] for r in g),1),
            rate_mean=round(st.mean(r[key] for r in g),1), base_med=round(st.median(r['BASE0612'] for r in g),1),
            pop=round(sum(r['POP0612'] for r in g))))
    return out
comp = [r for r in base if r['Y_OK'] == 6]
for r in comp: r['pooled'] = r['DEATHS']/r['POPYRS']*1e5 if r['POPYRS'] else 0
res = {}
print('base', len(base), 'complete', len(comp))
for name, panel, key in [('complete_avg', comp, 'RATE_AVG'), ('all_imp5', base, 'imp5'), ('all_imp1', base, 'imp1'), ('all_imp9', base, 'imp9')]:
    d = deciles(panel, key); res[name] = d
    print('\n', name, 'D10/D1 median', round(d[9]['rate_med']/d[0]['rate_med'],2), 'mean', round(d[9]['rate_mean']/d[0]['rate_mean'],2))
    for x in d: print(x)
# control for baseline
def ols(panel, key, logs=True):
    y = np.array([r[key] for r in panel]); x1 = np.array([r['ppc'] for r in panel]); x2 = np.array([r['BASE0612'] for r in panel])
    if logs: y = np.log(y+1); x1 = np.log(x1)
    X = np.column_stack([np.ones(len(y)), x1, x2]); b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X@b; s2 = e@e/(len(y)-3); se = np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    X0 = np.column_stack([np.ones(len(y)), x1]); b0, *_ = np.linalg.lstsq(X0, y, rcond=None)
    r2 = 1 - e@e/((y-y.mean())@(y-y.mean()))
    return dict(n=len(y), b_pills_alone=round(b0[1],3), b_pills=round(b[1],3), se=round(se[1],3), t=round(b[1]/se[1],1), b_base=round(b[2],3), t_base=round(b[2]/se[2],1), r2=round(r2,3))
for name, panel, key in [('complete_avg', comp, 'RATE_AVG'), ('all_imp5', base, 'imp5')]:
    print('\nOLS log(rate+1) ~ log(pills/person) + baseline', name, ols(panel, key))
    # corr
    a = np.log([r['ppc'] for r in panel]); bb = np.array([r['BASE0612'] for r in panel]); print(' corr log pills vs baseline', round(np.corrcoef(a, bb)[0,1],3))
# stratified: within baseline quintiles, top pills quintile vs bottom pills quintile
for name, panel, key in [('complete_avg', comp, 'RATE_AVG'), ('all_imp5', base, 'imp5')]:
    print('\nstratified', name)
    p = sorted(panel, key=lambda r: r['BASE0612']); n = len(p); strat = []
    for i in range(5):
        g = p[i*n//5:(i+1)*n//5]; g2 = sorted(g, key=lambda r: r['ppc']); m = len(g2)
        lo = g2[:m//5]; hi = g2[-(m//5):]
        row = dict(base_q=i+1, base_range=f"{g[0]['BASE0612']:.1f}-{g[-1]['BASE0612']:.1f}", counties=m,
                   lo_pills_med=round(st.median(r['ppc'] for r in lo),1), lo_rate_med=round(st.median(r[key] for r in lo),1),
                   hi_pills_med=round(st.median(r['ppc'] for r in hi),1), hi_rate_med=round(st.median(r[key] for r in hi),1))
        row['ratio'] = round(row['hi_rate_med']/row['lo_rate_med'],2) if row['lo_rate_med'] else None
        strat.append(row); print(row)
    res['strat_'+name] = strat
json.dump(res, open('results.json','w'), indent=1)
# Knox and neighbors
knox = {'47093':'Knox','47001':'Anderson','47173':'Union','47057':'Grainger','47089':'Jefferson','47155':'Sevier','47009':'Blount','47105':'Loudon','47145':'Roane','47013':'Campbell','47025':'Claiborne','47129':'Morgan'}
allp = sorted(base, key=lambda r: r['ppc']); rank = {r['FIPS']: i for i, r in enumerate(allp)}
print('\nKnox area')
for r in base:
    if r['FIPS'] in knox:
        print(r['FIPS'], r['COUNTY'], int(r['POP0612']), 'ppc', round(r['ppc'],1), 'decile', rank[r['FIPS']]*10//len(allp)+1, 'o30', int(r['O30']), 'yok', int(r['Y_OK']), 'rate_avg', r['RATE_AVG'], 'imp5', round(r['imp5'],1), 'deaths', r['DEATHS'], 'base0612', r['BASE0612'], 'base2015', r['BASE2015'])
tn = [r for r in base if r['ST']=='TN']
print('TN median ppc', round(st.median(r['ppc'] for r in tn),1), 'TN median imp5', round(st.median(r['imp5'] for r in tn),1), 'US median ppc', round(st.median(r['ppc'] for r in base),1), 'US median imp5', round(st.median(r['imp5'] for r in base),1))
