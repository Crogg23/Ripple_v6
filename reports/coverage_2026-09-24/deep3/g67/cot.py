import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_rows',300)
c=pd.read_pickle('S05_cot_all.pkl'); c['d']=pd.to_datetime(c.AS_OF_DATE_IN_FORM_YYMMDD); c['k']=c.CFTC_CONTRACT_MARKET_CODE.str.strip()
num=lambda s: pd.to_numeric(s.astype(str).str.strip().replace({'.':None,'':None}),errors='coerce')
for col in ['OPEN_INTEREST_ALL','LEV_MONEY_POSITIONS_LONG_ALL','LEV_MONEY_POSITIONS_SHORT_ALL','LEV_MONEY_POSITIONS_SPREAD_ALL','ASSET_MGR_POSITIONS_LONG_ALL','ASSET_MGR_POSITIONS_SHORT_ALL','DEALER_POSITIONS_LONG_ALL','DEALER_POSITIONS_SHORT_ALL','TOT_REPT_POSITIONS_LONG_ALL','NONREPT_POSITIONS_LONG_ALL','TOT_REPT_POSITIONS_SHORT_ALL','NONREPT_POSITIONS_SHORT_ALL','TRADERS_LEV_MONEY_SHORT_ALL','CONC_GROSS_LE_4_TDR_SHORT_ALL']:
    c[col]=num(c[col])
# consistency: reportable + nonreportable = OI
c['chkL']=c.TOT_REPT_POSITIONS_LONG_ALL+c.NONREPT_POSITIONS_LONG_ALL-c.OPEN_INTEREST_ALL
print('rows where long side != OI:',(c.chkL.abs()>0).sum(),' >1 contract:',(c.chkL.abs()>1).sum(), c[c.chkL.abs()>1].MARKET_AND_EXCHANGE_NAMES.str.strip().value_counts().head(5).to_dict())
T={'042601':'2Y','044601':'5Y','043602':'10Y','043607':'U10','020601':'Bond','020604':'UBond'}
t=c[c.k.isin(T)].copy(); t['ten']=t.k.map(T)
t['net_short']=t.LEV_MONEY_POSITIONS_SHORT_ALL-t.LEV_MONEY_POSITIONS_LONG_ALL
t['am_net_long']=t.ASSET_MGR_POSITIONS_LONG_ALL-t.ASSET_MGR_POSITIONS_SHORT_ALL
w=t.groupby('d').agg(lev_short=('LEV_MONEY_POSITIONS_SHORT_ALL','sum'),lev_long=('LEV_MONEY_POSITIONS_LONG_ALL','sum'),net_short=('net_short','sum'),am_net_long=('am_net_long','sum'),oi=('OPEN_INTEREST_ALL','sum'),n=('k','size'))
w['short_pct_oi']=(w.lev_short/w.oi*100).round(1)
print('weeks',len(w),'weeks with <6 tenors',(w.n<6).sum(),'(Ultra 10Y starts 2016-03)')
w6=w[w.index>='2016-03-08']
print('peak net short', w6.net_short.idxmax().date(), int(w6.net_short.max()))
print('peak lev gross short', w6.lev_short.idxmax().date(), int(w6.lev_short.max()), 'pct oi then', w6.loc[w6.lev_short.idxmax(),'short_pct_oi'])
for d in ['2019-12-31','2020-02-25','2020-03-10','2020-03-17','2020-03-31','2020-06-30','2022-12-27','2023-12-26','2024-12-31','2025-03-25','2025-04-01','2025-04-08','2025-04-15','2025-04-22','2025-12-30','2026-06-30','2026-08-04']:
    r=w.loc[w.index[w.index.get_indexer([pd.Timestamp(d)],method='nearest')[0]]]
    print(d, r.name.date(), 'net_short',int(r.net_short),'gross short',int(r.lev_short),'pct_oi',r.short_pct_oi,'AM net long',int(r.am_net_long),'OI',int(r.oi))
# same-week comparison across years: first Tuesday of August
for y in range(2016,2027):
    s=w6[(w6.index.year==y)&(w6.index.month==8)]
    if len(s): r=s.iloc[0]; print(y,'Aug wk1',r.name.date(),'net short',int(r.net_short),'gross short',int(r.lev_short),'pct',r.short_pct_oi)
w.to_pickle('cot_treasury_weekly.pkl')
