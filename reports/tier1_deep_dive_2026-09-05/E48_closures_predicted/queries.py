"""E48 — were terminated hospitals' cost reports already bad? Every query, logged to queries.log."""
import json, sys
from _shared.q import run, open_log
open_log("reports/tier1_deep_dive_2026-09-05/E48_closures_predicted/queries.log")
H="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS"; P="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER"
OUT={}
def q(label, sql):
    r = run(sql, label); OUT[label]=r; print(label, json.dumps(r, default=str)[:3000]); return r

# NaN guard: mart floats hold NaN where landing held the string 'nan'
NZ = lambda c: f"iff({c} = 'NaN'::float, null, {c})"

# ---- base: one report per hospital = latest 12-month report that ENDS BEFORE termination (or latest, if active)
BASE = f"""
with pos as (
  select CCN, PGM_TRMNTN_CD tcd, TRMNTN_EXPRTN_DT tdt, CHOW_DT, CHOW_CNT, nullif(trim(CROSS_REF_PROVIDER_NUMBER),'') xref, PRVDR_CTGRY_SBTYP_CD sub
  from {P} where PRVDR_CTGRY_CD='01'),
h as (
  select PROVIDER_CCN hccn, HOSPITAL_NAME nm, STATE_CODE st, CCN_FACILITY_TYPE ftype, FISCAL_YEAR_END_DATE fye, FISCAL_YEAR_LENGTH_DAYS fylen,
         {NZ('NET_INCOME')} ni, {NZ('TOTAL_COSTS')} tc, {NZ('NET_PATIENT_REVENUE')} npr, {NZ('NET_INCOME_FROM_SERVICE_TO_PATIENTS')} opi,
         {NZ('TOTAL_FUND_BALANCES')} fb, {NZ('CURRENT_RATIO')} cr, {NZ('NET_MARGIN_RATIO')} nmr, {NZ('TOTAL_INCOME')} ti
  from {H}),
j as (
  select p.*, h.*, 
    case when p.tcd='00' then 'active'
         when p.tdt >= '2024-01-01' then 'term_2024_26'
         when p.tdt >= '2023-01-01' then 'term_2023' else 'term_pre2023' end grp,
    case when p.tcd='00' then 'active' when p.tcd='07' then '07 status change' when p.tcd='01' then '01 voluntary merger/closure'
         when p.tcd='05' then '05 involuntary' else 'other ('||p.tcd||')' end tgrp,
    row_number() over (partition by p.CCN order by h.fye desc) rn
  from pos p join h on h.hccn=p.CCN
  where h.fylen between 350 and 380 and h.ni is not null and h.tc > 0
    and (p.tcd='00' or h.fye <= p.tdt)),
b as (select *, ni/tc m_cost, ni/nullif(npr,0) m_npr, datediff(day, fye, tdt) lag_days from j where rn=1)
"""

q("A_ingest_dates", f"select min(_INGESTED_AT) mn, max(_INGESTED_AT) mx, min(FISCAL_YEAR_END_DATE) fye_min, max(FISCAL_YEAR_END_DATE) fye_max from {H}")
q("A_pos_latest_term", f"select max(TRMNTN_EXPRTN_DT) latest_term, max(CHOW_DT) latest_chow from {P} where PRVDR_CTGRY_CD='01'")
q("A_nan_rows", f"select sum(iff(NET_INCOME='NaN'::float,1,0)) ni_nan, sum(iff(TOTAL_COSTS='NaN'::float,1,0)) tc_nan, sum(iff(NET_PATIENT_REVENUE='NaN'::float,1,0)) npr_nan, sum(iff(TOTAL_FUND_BALANCES='NaN'::float,1,0)) fb_nan, sum(iff(NET_MARGIN_RATIO='NaN'::float,1,0)) nmr_nan from {H}")
q("A_nmr_definition", f"select count(*) n, sum(iff(abs(NET_MARGIN_RATIO - NET_INCOME/nullif(TOTAL_INCOME,0))<0.001,1,0)) eq_ti, sum(iff(abs(NET_MARGIN_RATIO - NET_INCOME/nullif(NET_PATIENT_REVENUE,0))<0.001,1,0)) eq_npr, sum(iff(abs(NET_MARGIN_RATIO - NET_INCOME/nullif(TOTAL_COSTS,0))<0.001,1,0)) eq_tc, sum(iff(abs(NET_MARGIN_RATIO - NET_INCOME/nullif(TOTAL_PATIENT_REVENUE,0))<0.001,1,0)) eq_tpr from {H} where NET_MARGIN_RATIO<>'NaN'::float and NET_INCOME<>'NaN'::float")
q("A_reports_per_ccn", f"select cnt, count(*) hospitals from (select PROVIDER_CCN, sum(iff(FISCAL_YEAR_LENGTH_DAYS between 350 and 380,1,0)) cnt from {H} group by 1) group by 1 order by 1")

# ---- B: rebuild the first pass, then split by termination code
q("B_rebuild_68", BASE + "select grp, count(*) n, sum(iff(ni<0,1,0)) neg, round(100*neg/n,1) pct_neg, round(100*median(m_cost),2) med_m_cost, round(100*median(m_npr),2) med_m_npr from b group by 1 order by 1")
q("B_by_term_code", BASE + "select tgrp, count(*) n, sum(iff(ni<0,1,0)) neg, round(100*neg/n,1) pct_neg, round(100*median(m_cost),2) med_m_cost, sum(iff(xref is not null,1,0)) has_successor_ccn, sum(iff(fb<0,1,0)) neg_equity, round(100*neg_equity/n,1) pct_neg_equity from b where grp in ('active','term_2024_26') group by 1 order by 1")
q("B_by_successor", BASE + "select iff(xref is null,'no successor CCN','successor CCN listed') succ, tgrp, count(*) n, sum(iff(ni<0,1,0)) neg, round(100*neg/n,1) pct_neg, round(100*median(m_cost),2) med_m_cost from b where grp='term_2024_26' group by 1,2 order by 1,2")
q("B_pos_all_term24", f"select PGM_TRMNTN_CD, count(*) n, sum(iff(nullif(trim(CROSS_REF_PROVIDER_NUMBER),'') is not null,1,0)) xref from {P} where PRVDR_CTGRY_CD='01' and TRMNTN_EXPRTN_DT>='2024-01-01' group by 1 order by 1")

# ---- C: margin distribution, terminated vs active (bins on margin of cost)
BIN = "case when m_cost < -0.30 then 'a <-30%' when m_cost < -0.20 then 'b -30..-20' when m_cost < -0.10 then 'c -20..-10' when m_cost < -0.05 then 'd -10..-5' when m_cost < 0 then 'e -5..0' when m_cost < 0.05 then 'f 0..5' when m_cost < 0.10 then 'g 5..10' when m_cost < 0.20 then 'h 10..20' else 'i >20%' end"
q("C_margin_bins", BASE + f"select {BIN} bin, sum(iff(grp='active',1,0)) active, sum(iff(grp='term_2024_26',1,0)) term, sum(iff(grp='term_2024_26' and tcd<>'07',1,0)) term_closure, sum(iff(grp='term_2024_26' and tcd='07',1,0)) term_status from b where grp in ('active','term_2024_26') group by 1 order by 1")
q("C_percentiles", BASE + "select grp, count(*) n, round(100*percentile_cont(0.10) within group (order by m_cost),1) p10, round(100*percentile_cont(0.25) within group (order by m_cost),1) p25, round(100*median(m_cost),1) p50, round(100*percentile_cont(0.75) within group (order by m_cost),1) p75, round(100*percentile_cont(0.90) within group (order by m_cost),1) p90 from b where grp in ('active','term_2024_26') group by 1 order by 1")
q("C_percentiles_closure_only", BASE + "select tgrp, count(*) n, round(100*percentile_cont(0.10) within group (order by m_cost),1) p10, round(100*percentile_cont(0.25) within group (order by m_cost),1) p25, round(100*median(m_cost),1) p50, round(100*percentile_cont(0.75) within group (order by m_cost),1) p75, round(100*percentile_cont(0.90) within group (order by m_cost),1) p90 from b where grp='term_2024_26' group by 1 order by 1")

# ---- D: threshold test. Years of losses is capped by the file (see A_reports_per_ccn); use the cross-section:
#      of every hospital whose latest report shows X, what share was terminated 2024-26?
q("D_threshold_by_bin", BASE + f"select {BIN} bin, count(*) n, sum(iff(grp='term_2024_26',1,0)) term, sum(iff(grp='term_2024_26' and tcd<>'07',1,0)) closure, round(100*term/n,2) pct_term, round(100*closure/n,2) pct_closure from b where grp in ('active','term_2024_26') group by 1 order by 1")
q("D_threshold_cum", BASE + "select t.thr, count(*) n, sum(iff(grp='term_2024_26',1,0)) term, sum(iff(grp='term_2024_26' and tcd<>'07',1,0)) closure, round(100*term/n,2) pct_term, round(100*closure/n,2) pct_closure from b, (select $1 thr from values (0),(-0.05),(-0.10),(-0.20),(-0.30)) t where grp in ('active','term_2024_26') and m_cost < t.thr group by 1 order by 1 desc")
q("D_stacked_signals", BASE + """select (iff(ni<0,1,0)+iff(opi<0,1,0)+iff(fb<0,1,0)+iff(cr<1,1,0)) signals, count(*) n, sum(iff(grp='term_2024_26',1,0)) term, sum(iff(grp='term_2024_26' and tcd<>'07',1,0)) closure, round(100*term/n,2) pct_term, round(100*closure/n,2) pct_closure
 from b where grp in ('active','term_2024_26') and opi is not null and fb is not null and cr is not null group by 1 order by 1""")
q("D_signal_fill", BASE + "select grp, count(*) n, count(opi) opi, count(fb) fb, count(cr) cr, sum(iff(fb<0,1,0)) neg_equity, sum(iff(opi<0,1,0)) op_loss, sum(iff(cr<1,1,0)) cr_lt1 from b where grp in ('active','term_2024_26') group by 1")
# D_two_year_streak: not runnable -- A_reports_per_ccn shows no hospital has two 12-month reports in this file
q("D_lag_buckets", BASE + "select case when lag_days<=90 then 'a 0-90d' when lag_days<=365 then 'b 91-365d' when lag_days<=730 then 'c 366-730d' else 'd >730d' end lag, count(*) n, sum(iff(ni<0,1,0)) neg, round(100*neg/n,1) pct_neg from b where grp='term_2024_26' group by 1 order by 1")
q("D_worst_closures", BASE + "select CCN, nm, st, ftype, tcd, tdt, fye, round(100*m_cost,1) m_cost, round(100*m_npr,1) m_npr, round(ni) ni, round(npr) npr, round(fb) fund_bal from b where grp='term_2024_26' and npr is not null and npr>0 order by m_cost limit 12")
q("D_term_no_report", f"""select PGM_TRMNTN_CD, count(*) n, sum(iff(h.PROVIDER_CCN is null,1,0)) no_report_at_all, sum(iff(h.PROVIDER_CCN is not null and h.full12=0,1,0)) short_report_only
 from {P} p left join (select PROVIDER_CCN, max(iff(FISCAL_YEAR_LENGTH_DAYS between 350 and 380,1,0)) full12 from {H} group by 1) h on h.PROVIDER_CCN=p.CCN
 where p.PRVDR_CTGRY_CD='01' and p.TRMNTN_EXPRTN_DT>='2024-01-01' group by 1 order by 1""")
q("D_by_ftype", BASE + "select ftype, sum(iff(grp='active',1,0)) active, sum(iff(grp='active' and ni<0,1,0)) active_neg, sum(iff(grp='term_2024_26',1,0)) term, sum(iff(grp='term_2024_26' and ni<0,1,0)) term_neg from b where grp in ('active','term_2024_26') group by 1 order by 2 desc")
json.dump(OUT, open("reports/tier1_deep_dive_2026-09-05/E48_closures_predicted/results.json","w"), default=str, indent=1)
