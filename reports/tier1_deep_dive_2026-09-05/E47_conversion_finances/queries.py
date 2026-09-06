"""E47 - were REH converters already broke? Every query, logged to queries.log. SELECT only."""
import json, sys
from _shared import q
D = "reports/tier1_deep_dive_2026-09-05/E47_conversion_finances"
q.open_log(f"{D}/queries.log")
H = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS"
E = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS"
P = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER"
out = {}
import atexit; atexit.register(lambda: json.dump(out, open(f"{D}/results.json","w"), default=str, indent=1))

# clean HCRIS: full-year, revenue readable (FLOAT NaN survives the mart), cost > 0
CLEAN = f"""
select PROVIDER_CCN, HOSPITAL_NAME, STATE_CODE, RURAL_VERSUS_URBAN, CCN_FACILITY_TYPE, NUMBER_OF_BEDS,
       FISCAL_YEAR_BEGIN_DATE, FISCAL_YEAR_END_DATE, FISCAL_YEAR_LENGTH_DAYS,
       NET_INCOME, TOTAL_COSTS, NET_PATIENT_REVENUE, TOTAL_FUND_BALANCES, CURRENT_RATIO,
       CASH_ON_HAND_AND_IN_BANKS, TOTAL_OPERATING_EXPENSE, NET_MARGIN_RATIO,
       NET_INCOME / nullif(TOTAL_COSTS,0) as m_cost,
       NET_INCOME / nullif(NET_PATIENT_REVENUE,0) as m_rev,
       (CASH_ON_HAND_AND_IN_BANKS) / nullif(TOTAL_OPERATING_EXPENSE/365.0,0) as days_cash,
       row_number() over (partition by PROVIDER_CCN order by FISCAL_YEAR_END_DATE desc) rn
from {H}
where datediff(day, FISCAL_YEAR_BEGIN_DATE, FISCAL_YEAR_END_DATE) between 350 and 380
  and NET_PATIENT_REVENUE <> 'NaN'::float and NET_INCOME <> 'NaN'::float
  and TOTAL_COSTS <> 'NaN'::float and TOTAL_COSTS > 0
"""
# REH cohort: predecessor CCN split on '/'
REH = f"""
select CCN as reh_ccn, ORGANIZATION_NAME, STATE, REH_CONVERSION_DATE, CAH_OR_HOSPITAL_CCN,
       split_part(CAH_OR_HOSPITAL_CCN,'|',1) as pred_ccn
from {E} where REH_CONVERSION_FLAG='Y'
"""

out["reh_cohort"] = q.run(f"""
with r as ({REH}) select count(*) n, count(distinct reh_ccn) reh_ccns, count(REH_CONVERSION_DATE) dated,
  count(pred_ccn) with_pred, count(distinct pred_ccn) distinct_pred,
  sum(iff(CAH_OR_HOSPITAL_CCN like '%|%',1,0)) piped from r""", "reh cohort shape")

out["reh_pred_hcris_raw"] = q.run(f"""
with r as ({REH}) select count(distinct r.pred_ccn) matched_any_report, count(*) report_rows
from r join {H} h on h.PROVIDER_CCN = r.pred_ccn""", "pred ccn in hcris any report")


out["reh_filter_walk"] = q.run(f"""
with r as ({REH}),
j as (select r.reh_ccn, r.REH_CONVERSION_DATE, h.*, row_number() over (partition by r.reh_ccn order by h.FISCAL_YEAR_END_DATE desc) k
      from r join {H} h on h.PROVIDER_CCN=r.pred_ccn)
select count(*) all_rows, count(distinct reh_ccn) reh_any,
  sum(iff(k=1,1,0)) latest_rows,
  sum(iff(k=1 and datediff(day,FISCAL_YEAR_BEGIN_DATE,FISCAL_YEAR_END_DATE) between 350 and 380,1,0)) latest_fullyear,
  sum(iff(k=1 and datediff(day,FISCAL_YEAR_BEGIN_DATE,FISCAL_YEAR_END_DATE) between 350 and 380 and NET_PATIENT_REVENUE<>'NaN'::float,1,0)) latest_fy_rev,
  sum(iff(k=1 and datediff(day,FISCAL_YEAR_BEGIN_DATE,FISCAL_YEAR_END_DATE) between 350 and 380 and NET_PATIENT_REVENUE<>'NaN'::float and TOTAL_COSTS<>'NaN'::float and TOTAL_COSTS>0,1,0)) latest_fy_rev_cost,
  sum(iff(k=1 and FISCAL_YEAR_END_DATE<=REH_CONVERSION_DATE,1,0)) latest_before_conv,
  sum(iff(datediff(day,FISCAL_YEAR_BEGIN_DATE,FISCAL_YEAR_END_DATE) between 350 and 380,1,0)) any_fullyear_rows,
  count(distinct iff(datediff(day,FISCAL_YEAR_BEGIN_DATE,FISCAL_YEAR_END_DATE) between 350 and 380, reh_ccn, null)) reh_with_fullyear,
  sum(iff(TOTAL_COSTS='NaN'::float,1,0)) tc_nan, sum(iff(TOTAL_COSTS<=0,1,0)) tc_le0
from j""", "reh filter walk")
out["reh_short_periods"] = q.run(f"""
with r as ({REH})
select r.reh_ccn, r.ORGANIZATION_NAME, r.REH_CONVERSION_DATE, h.FISCAL_YEAR_BEGIN_DATE, h.FISCAL_YEAR_END_DATE, datediff(day,h.FISCAL_YEAR_BEGIN_DATE,h.FISCAL_YEAR_END_DATE) len_days,
  h.NET_INCOME, h.TOTAL_COSTS, h.NET_PATIENT_REVENUE
from r join {H} h on h.PROVIDER_CCN=r.pred_ccn order by 1, h.FISCAL_YEAR_END_DATE""", "all predecessor reports listed")

# main REH table: last clean full-year report before conversion
out["reh_rows"] = q.run(f"""
with r as ({REH}), c as ({CLEAN}),
j as (select r.*, c.*, row_number() over (partition by r.reh_ccn order by c.FISCAL_YEAR_END_DATE desc) k
      from r join c on c.PROVIDER_CCN = r.pred_ccn
      where r.REH_CONVERSION_DATE is null or c.FISCAL_YEAR_END_DATE <= r.REH_CONVERSION_DATE)
select reh_ccn, ORGANIZATION_NAME, STATE, REH_CONVERSION_DATE, pred_ccn, HOSPITAL_NAME, CCN_FACILITY_TYPE, RURAL_VERSUS_URBAN,
  NUMBER_OF_BEDS, FISCAL_YEAR_END_DATE, datediff(day, FISCAL_YEAR_END_DATE, REH_CONVERSION_DATE) days_gap,
  NET_INCOME, TOTAL_COSTS, NET_PATIENT_REVENUE, m_cost, m_rev, NET_MARGIN_RATIO, TOTAL_FUND_BALANCES, CURRENT_RATIO, days_cash
from j where k=1 order by m_cost""", "reh last clean pre-conversion report")

# same cohort, no period/revenue filter (the loose version, to reproduce 28 of 35)
out["reh_loose"] = q.run(f"""
with r as ({REH}),
j as (select r.reh_ccn, h.NET_INCOME, h.TOTAL_COSTS, h.NET_PATIENT_REVENUE,
        row_number() over (partition by r.reh_ccn order by h.FISCAL_YEAR_END_DATE desc) k
      from r join {H} h on h.PROVIDER_CCN = r.pred_ccn)
select count(*) n, sum(iff(NET_INCOME<0,1,0)) neg, median(NET_INCOME/nullif(TOTAL_COSTS,0)) med_m_cost,
  sum(iff(NET_PATIENT_REVENUE='NaN'::float,1,0)) blank_rev from j where k=1""", "reh loose (all reports) reproduce 28/35")

# base rates: latest clean report per CCN, several comparison groups
BASE = f"""
with c as ({CLEAN}), r as ({REH}),
b as (select c.*, iff(c.PROVIDER_CCN in (select pred_ccn from r where pred_ccn is not null),1,0) is_reh_pred from c where rn=1)
"""
out["base_groups"] = q.run(BASE + """
select grp, count(*) n, sum(iff(NET_INCOME<0,1,0)) neg, round(100.0*sum(iff(NET_INCOME<0,1,0))/count(*),1) pct_neg,
  round(median(m_cost)*100,2) med_m_cost, round(median(m_rev)*100,2) med_m_rev,
  sum(iff(TOTAL_FUND_BALANCES<0,1,0)) neg_equity, sum(iff(CURRENT_RATIO<1,1,0)) cr_under1, round(median(days_cash),1) med_days_cash,
  count(CURRENT_RATIO) cr_filled, count(days_cash) dc_filled
from (
  select 'all hospitals' grp, * from b
  union all select 'rural, all types', * from b where RURAL_VERSUS_URBAN='R'
  union all select 'rural CAH+STH (not REH)', * from b where RURAL_VERSUS_URBAN='R' and CCN_FACILITY_TYPE in ('CAH','STH') and is_reh_pred=0
  union all select 'rural CAH (not REH)', * from b where RURAL_VERSUS_URBAN='R' and CCN_FACILITY_TYPE='CAH' and is_reh_pred=0
  union all select 'rural STH (not REH)', * from b where RURAL_VERSUS_URBAN='R' and CCN_FACILITY_TYPE='STH' and is_reh_pred=0
  union all select 'rural CAH+STH <=25 beds (not REH)', * from b where RURAL_VERSUS_URBAN='R' and CCN_FACILITY_TYPE in ('CAH','STH') and NUMBER_OF_BEDS<=25 and is_reh_pred=0
  union all select 'rural CAH+STH <=50 beds (not REH)', * from b where RURAL_VERSUS_URBAN='R' and CCN_FACILITY_TYPE in ('CAH','STH') and NUMBER_OF_BEDS<=50 and is_reh_pred=0
  union all select 'REH predecessors', * from b where is_reh_pred=1
) group by 1 order by n desc""", "base rates by group")

# margin distribution buckets, REH vs rural small
out["buckets"] = q.run(BASE + """
select grp, bucket, count(*) n from (
  select iff(is_reh_pred=1,'REH predecessors','rural CAH+STH (not REH)') grp,
    case when m_cost < -0.20 then 'a. under -20%' when m_cost < -0.10 then 'b. -20% to -10%' when m_cost < 0 then 'c. -10% to 0'
         when m_cost < 0.05 then 'd. 0 to +5%' when m_cost < 0.10 then 'e. +5% to +10%' else 'f. over +10%' end bucket
  from b where RURAL_VERSUS_URBAN='R' and CCN_FACILITY_TYPE in ('CAH','STH')
) group by 1,2 order by 1,2""", "margin buckets")

# rural base rate by fiscal year end, to see if 2023 vs 2024 differ
out["base_by_fy"] = q.run(BASE + """
select year(FISCAL_YEAR_END_DATE) fy, count(*) n, sum(iff(NET_INCOME<0,1,0)) neg, round(100.0*sum(iff(NET_INCOME<0,1,0))/count(*),1) pct_neg, round(median(m_cost)*100,2) med
from b where RURAL_VERSUS_URBAN='R' and CCN_FACILITY_TYPE in ('CAH','STH') and is_reh_pred=0 group by 1 order by 1""", "rural base by FY")

# multi-year check: how many CCNs have 2+ clean reports (trend feasibility)
out["multi_year"] = q.run(f"""
with c as ({CLEAN}) select reports_per_ccn, count(*) ccns from (select PROVIDER_CCN, count(*) reports_per_ccn from c group by 1) group by 1 order by 1""", "reports per ccn")

# post-conversion: new REH CCN reports in HCRIS
out["post"] = q.run(f"""
with r as ({REH})
select r.reh_ccn, r.ORGANIZATION_NAME, r.STATE, r.REH_CONVERSION_DATE, h.FISCAL_YEAR_BEGIN_DATE, h.FISCAL_YEAR_END_DATE,
  datediff(day,h.FISCAL_YEAR_BEGIN_DATE,h.FISCAL_YEAR_END_DATE) len_days, h.NET_INCOME, h.TOTAL_COSTS,
  iff(h.NET_PATIENT_REVENUE='NaN'::float, null, h.NET_INCOME/nullif(h.TOTAL_COSTS,0)) m_cost
from r join {H} h on h.PROVIDER_CCN = r.reh_ccn order by 1, h.FISCAL_YEAR_END_DATE""", "post-conversion reports under REH ccn")

# before/after pairs
out["pairs"] = q.run(f"""
with r as ({REH}), c as ({CLEAN}),
pre as (select r.reh_ccn, c.m_cost pre_m, c.FISCAL_YEAR_END_DATE pre_fy, row_number() over (partition by r.reh_ccn order by c.FISCAL_YEAR_END_DATE desc) k
        from r join c on c.PROVIDER_CCN=r.pred_ccn where r.REH_CONVERSION_DATE is null or c.FISCAL_YEAR_END_DATE <= r.REH_CONVERSION_DATE),
post as (select r.reh_ccn, h.NET_INCOME/nullif(h.TOTAL_COSTS,0) post_m, h.FISCAL_YEAR_END_DATE post_fy, datediff(day,h.FISCAL_YEAR_BEGIN_DATE,h.FISCAL_YEAR_END_DATE) post_len,
         row_number() over (partition by r.reh_ccn order by h.FISCAL_YEAR_END_DATE desc) k
         from r join {H} h on h.PROVIDER_CCN=r.reh_ccn where h.NET_PATIENT_REVENUE<>'NaN'::float and h.TOTAL_COSTS>0)
select r.reh_ccn, r.ORGANIZATION_NAME, pre.pre_fy, round(pre.pre_m*100,1) pre_pct, post.post_fy, post.post_len, round(post.post_m*100,1) post_pct
from r join pre on pre.reh_ccn=r.reh_ccn and pre.k=1 join post on post.reh_ccn=r.reh_ccn and post.k=1 order by pre_pct""", "before/after pairs")

# POS: termination of predecessor
out["pos"] = q.run(f"""
with r as ({REH})
select count(*) n, sum(iff(p.CCN is not null,1,0)) in_pos, sum(iff(p.PGM_TRMNTN_CD not in ('00'),1,0)) terminated,
  sum(iff(p.TRMNTN_EXPRTN_DT is not null,1,0)) term_dated
from r left join (select * from {P} where PRVDR_CTGRY_CD='01') p on p.CCN=r.pred_ccn""", "pos predecessor status")

for k,v in out.items():
    print("==", k, len(v)); 
    for row in v[:60]: print(row)

# ---- round 2 ----
# before/after on the loose predecessor set (any period length, revenue readable)
out["pairs_loose"] = q.run(f"""
with r as ({REH}),
pre as (select r.reh_ccn, h.NET_INCOME/nullif(h.TOTAL_COSTS,0) pre_m, h.FISCAL_YEAR_END_DATE pre_fy, datediff(day,h.FISCAL_YEAR_BEGIN_DATE,h.FISCAL_YEAR_END_DATE) pre_len,
        row_number() over (partition by r.reh_ccn order by h.FISCAL_YEAR_END_DATE desc) k
        from r join {H} h on h.PROVIDER_CCN=r.pred_ccn where h.NET_PATIENT_REVENUE<>'NaN'::float and h.TOTAL_COSTS>0),
post as (select r.reh_ccn, h.NET_INCOME/nullif(h.TOTAL_COSTS,0) post_m, h.FISCAL_YEAR_END_DATE post_fy, datediff(day,h.FISCAL_YEAR_BEGIN_DATE,h.FISCAL_YEAR_END_DATE) post_len,
         row_number() over (partition by r.reh_ccn order by h.FISCAL_YEAR_END_DATE desc) k
         from r join {H} h on h.PROVIDER_CCN=r.reh_ccn where h.NET_PATIENT_REVENUE<>'NaN'::float and h.TOTAL_COSTS>0)
select r.reh_ccn, r.ORGANIZATION_NAME, r.STATE, r.REH_CONVERSION_DATE, pre.pre_fy, pre.pre_len, round(pre.pre_m*100,1) pre_pct, post.post_fy, post.post_len, round(post.post_m*100,1) post_pct
from r join pre on pre.reh_ccn=r.reh_ccn and pre.k=1 join post on post.reh_ccn=r.reh_ccn and post.k=1 order by pre_pct""", "before/after pairs, loose pre")

# different-way rebuild: the mart's own NET_MARGIN_RATIO column, sign only
out["nmr_check"] = q.run(BASE + """
select grp, count(NET_MARGIN_RATIO) n, sum(iff(NET_MARGIN_RATIO<0,1,0)) neg_nmr, sum(iff(NET_INCOME<0,1,0)) neg_ni,
  sum(iff(sign(NET_MARGIN_RATIO)<>sign(NET_INCOME),1,0)) sign_disagree, round(median(NET_MARGIN_RATIO)*100,2) med_nmr,
  round(median(NUMBER_OF_BEDS),0) med_beds
from (select 'REH predecessors' grp, * from b where is_reh_pred=1
      union all select 'rural CAH+STH (not REH)', * from b where RURAL_VERSUS_URBAN='R' and CCN_FACILITY_TYPE in ('CAH','STH') and is_reh_pred=0)
where NET_MARGIN_RATIO <> 'NaN'::float group by 1""", "net_margin_ratio sign rebuild")

# is the predecessor the same hospital? POS termination date vs REH conversion date
out["pos_timing"] = q.run(f"""
with r as ({REH})
select r.reh_ccn, r.pred_ccn, r.REH_CONVERSION_DATE, p.FAC_NAME, p.PGM_TRMNTN_CD, p.TRMNTN_EXPRTN_DT,
  datediff(day, r.REH_CONVERSION_DATE, p.TRMNTN_EXPRTN_DT) term_minus_conv
from r join (select * from {P} where PRVDR_CTGRY_CD='01') p on p.CCN=r.pred_ccn order by 7""", "pos termination vs conversion")
