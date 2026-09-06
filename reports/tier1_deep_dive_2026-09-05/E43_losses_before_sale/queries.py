"""E43 - were sold hospitals already losing money? Every query, logged to queries.log.
Run from repo root: PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 reports/tier1_deep_dive_2026-09-05/E43_losses_before_sale/queries.py
Writes results.json next to this file; story.py reads it."""
import json, os, warnings
warnings.filterwarnings("ignore")
from _shared.q import run, open_log

HERE = os.path.dirname(os.path.abspath(__file__))
open_log(os.path.join(HERE, "queries.log"))
P = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER"
H = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS"
R = {}

def q(key, sql):
    R[key] = run(sql, key)
    return R[key]

# ---------- discover: what is in each table ----------
q("pos_shape", f"select count(*) n, count(distinct ccn) ccns, count(chow_dt) chow_dt_n, count(chow_prior_dt) prior_n, min(chow_dt) mn, max(chow_dt) mx from {P}")
q("pos_cat", f"select prvdr_ctgry_cd, count(*) n, count(chow_dt) chow_n from {P} group by 1 order by 2 desc")
q("pos_chow_sw", f"select chow_sw, count(*) n from {P} group by 1")
q("pos_chow_cnt", f"select chow_cnt, count(*) n from {P} group by 1 order by 1")
q("hcris_shape", f"select count(*) n, count(distinct provider_ccn) ccns, count(net_income) ni_n, count(net_margin_ratio) nm_n, min(fiscal_year_end_date) mn, max(fiscal_year_end_date) mx, min(fiscal_year_begin_date) mnb, max(fiscal_year_begin_date) mxb from {H}")
q("hcris_years", f"select year(fiscal_year_end_date) fy, count(*) n, count(distinct provider_ccn) ccns from {H} group by 1 order by 1")
q("hcris_dupes", f"select cnt, count(*) ccns from (select provider_ccn, count(*) cnt from {H} group by 1) group by 1 order by 1")

# ---------- what is CHOW_DT: effective date or filing date? ----------
q("chow_dom", f"select day(chow_dt) d, count(*) n from {P} where chow_dt>='2015-01-01' group by 1 order by 2 desc")
q("chow_dow", f"select dayname(chow_dt) dow, count(*) n from {P} where chow_dt>='2015-01-01' group by 1 order by 2 desc")
q("chow_years_hosp", f"select year(chow_dt) y, count(*) n from {P} where prvdr_ctgry_cd='01' and chow_dt>='2015-01-01' group by 1 order by 1")

# ---------- the sold cohort: hospitals (category 01) with CHOW_DT in 2022-2024 ----------
q("sold_n", f"select count(*) n, count(distinct ccn) ccns from {P} where prvdr_ctgry_cd='01' and chow_dt between '2022-01-01' and '2024-12-31'")
q("sold_ctrl", f"select gnrl_cntl_type_cd, count(*) n from {P} where prvdr_ctgry_cd='01' and chow_dt between '2022-01-01' and '2024-12-31' group by 1 order by 2 desc")

# ---------- reproduce the first pass: naive join, no timing, fanout allowed ----------
q("repro_naive", f"""select count(*) rows_, count(distinct s.ccn) hospitals, sum(iff(h.net_income<0,1,0)) losing_rows,
  round(100*sum(iff(h.net_income<0,1,0))/count(*),1) pct
  from {P} s join {H} h on h.provider_ccn=s.ccn
  where s.prvdr_ctgry_cd='01' and s.chow_dt between '2022-01-01' and '2024-12-31'""")
q("repro_timing", f"""with s as (select ccn, chow_dt from {P} where prvdr_ctgry_cd='01' and chow_dt between '2022-01-01' and '2024-12-31')
  select case when h.provider_ccn is null then 'no HCRIS' when h.fiscal_year_end_date < s.chow_dt then 'ends before sale' else 'ends after sale' end timing,
  count(*) rows_, sum(iff(h.net_income<0,1,0)) losing, round(100*sum(iff(h.net_income<0,1,0))/nullif(count(h.net_income),0),1) pct
  from s left join {H} h on h.provider_ccn=s.ccn group by 1 order by 1""")

# ---------- the clean cohort: one row per sold hospital, last report ENDING BEFORE the sale ----------
BEFORE = f"""with s as (select ccn, fac_name, chow_dt, gnrl_cntl_type_cd from {P} where prvdr_ctgry_cd='01' and chow_dt between '2022-01-01' and '2024-12-31'),
  j as (select s.ccn, s.fac_name, s.chow_dt, s.gnrl_cntl_type_cd, h.fiscal_year_end_date fye, h.net_income, h.net_margin_ratio, h.net_income_from_service_to_patients op_income,
           h.ccn_facility_type ftype, h.type_of_control, h.net_patient_revenue,
           row_number() over (partition by s.ccn order by h.fiscal_year_end_date desc) rn
        from s join {H} h on h.provider_ccn=s.ccn and h.fiscal_year_end_date < s.chow_dt)
  select * from j where rn=1"""
q("before_cohort", f"""select count(*) hospitals, sum(iff(net_income<0,1,0)) losing, round(100*sum(iff(net_income<0,1,0))/count(*),1) pct_losing,
  sum(iff(op_income<0,1,0)) op_losing, round(100*sum(iff(op_income<0,1,0))/count(*),1) pct_op_losing,
  median(net_margin_ratio) med_margin, round(avg(datediff('month', fye, chow_dt)),1) avg_gap_months, median(datediff('month', fye, chow_dt)) med_gap_months
  from ({BEFORE})""")
q("before_by_saleyear", f"""select year(chow_dt) sale_year, count(*) hospitals, sum(iff(net_income<0,1,0)) losing, round(100*sum(iff(net_income<0,1,0))/count(*),1) pct
  from ({BEFORE}) group by 1 order by 1""")
q("before_gap", f"""select datediff('month', fye, chow_dt) gap_months, count(*) n from ({BEFORE}) group by 1 order by 1""")
q("before_by_type", f"""select ftype, count(*) n, sum(iff(net_income<0,1,0)) losing from ({BEFORE}) group by 1 order by 2 desc""")
q("before_by_ctrl", f"""select type_of_control, count(*) n, sum(iff(net_income<0,1,0)) losing from ({BEFORE}) group by 1 order by 2 desc""")
q("before_list", f"""select ccn, fac_name, chow_dt, fye, round(net_income) net_income, net_margin_ratio, ftype, type_of_control, round(net_patient_revenue) npr
  from ({BEFORE}) order by net_margin_ratio limit 400""")
# hospitals sold with NO report before the sale: what do their after-sale reports say?
q("after_only", f"""with s as (select ccn, chow_dt from {P} where prvdr_ctgry_cd='01' and chow_dt between '2022-01-01' and '2024-12-31'),
  b as (select distinct s.ccn from s join {H} h on h.provider_ccn=s.ccn and h.fiscal_year_end_date < s.chow_dt)
  select count(distinct s.ccn) hospitals, count(distinct h.provider_ccn) with_after_report,
   sum(iff(h.net_income<0,1,0)) losing_after from s left join {H} h on h.provider_ccn=s.ccn where s.ccn not in (select ccn from b)""")

# ---------- base rate: every hospital in HCRIS, same fiscal years ----------
q("base_all", f"select count(*) n, sum(iff(net_income<0,1,0)) losing, round(100*sum(iff(net_income<0,1,0))/count(*),1) pct, sum(iff(net_income_from_service_to_patients<0,1,0)) op_losing, median(net_margin_ratio) med_margin from {H}")
q("base_fy", f"select year(fiscal_year_end_date) fy, count(*) n, sum(iff(net_income<0,1,0)) losing, round(100*sum(iff(net_income<0,1,0))/count(*),1) pct, median(net_margin_ratio) med_margin from {H} group by 1 order by 1")
q("base_type", f"select ccn_facility_type ftype, count(*) n, sum(iff(net_income<0,1,0)) losing, round(100*sum(iff(net_income<0,1,0))/count(*),1) pct, median(net_margin_ratio) med_margin from {H} group by 1 order by 2 desc")
q("base_ctrl", f"select type_of_control, count(*) n, sum(iff(net_income<0,1,0)) losing, round(100*sum(iff(net_income<0,1,0))/count(*),1) pct from {H} group by 1 order by 2 desc")
# base rate excluding the sold hospitals themselves (not-sold hospitals)
q("base_notsold", f"""select count(*) n, sum(iff(net_income<0,1,0)) losing, round(100*sum(iff(net_income<0,1,0))/count(*),1) pct, median(net_margin_ratio) med_margin
  from {H} where provider_ccn not in (select ccn from {P} where chow_dt between '2022-01-01' and '2024-12-31')""")
# margin distribution buckets, sold-before vs everyone else
q("margin_buckets", f"""with b as ({BEFORE}),
  x as (select 'sold, year before' grp, net_margin_ratio m from b
        union all select 'all other hospitals', net_margin_ratio from {H} where provider_ccn not in (select ccn from b)),
  bk as (select grp, case when m < -0.20 then 'a. below -20%' when m < -0.10 then 'b. -20 to -10%' when m < 0 then 'c. -10 to 0%'
                when m < 0.05 then 'd. 0 to 5%' when m < 0.10 then 'e. 5 to 10%' else 'f. above 10%' end bucket from x where m is not null)
  select grp, bucket, count(*) n from bk group by 1,2 order by 1,2""")

# ---------- the stub trap: sellers file a terminating report that ends the day before the sale ----------
q("before_len", f"""select case when fy_len>=300 then 'full year (300+ days)' when fy_len>=180 then 'half year (180-299)' else 'stub (<180 days)' end period,
  count(*) n, sum(iff(net_income<0,1,0)) losing, round(100*sum(iff(net_income<0,1,0))/count(*),1) pct, median(net_margin_ratio) med_margin,
  sum(iff(datediff('day', fye, chow_dt)<=1,1,0)) ends_day_before_sale
  from (select b.*, h.fiscal_year_length_days fy_len from ({BEFORE}) b join {H} h on h.provider_ccn=b.ccn and h.fiscal_year_end_date=b.fye) group by 1 order by 1""")
q("before_len_hist", f"""select h.fiscal_year_length_days fy_len, datediff('day', b.fye, b.chow_dt) days_to_sale, b.net_margin_ratio, b.fac_name
  from ({BEFORE}) b join {H} h on h.provider_ccn=b.ccn and h.fiscal_year_end_date=b.fye order by 1""")
q("base_len", f"""select case when fiscal_year_length_days>=300 then 'full year (300+ days)' when fiscal_year_length_days>=180 then 'half year (180-299)' else 'stub (<180 days)' end period,
  count(*) n, sum(iff(net_income<0,1,0)) losing, round(100*sum(iff(net_income<0,1,0))/count(*),1) pct, median(net_margin_ratio) med_margin from {H} group by 1 order by 1""")
# are the 61 double-report CCNs the sold hospitals?
q("dupes_vs_sold", f"""with d as (select provider_ccn from {H} group by 1 having count(*)>1)
  select count(*) dupe_ccns, sum(iff(p.chow_dt is not null,1,0)) ever_sold, sum(iff(p.chow_dt between '2022-01-01' and '2024-12-31',1,0)) sold_2022_24,
  sum(iff(p.chow_dt between '2022-10-01' and '2024-09-30',1,0)) sold_in_hcris_window
  from d left join {P} p on p.ccn=d.provider_ccn""")
# fair comparison: full-year reports only, both sides
q("fair_full_year", f"""with b as (select b.*, h.fiscal_year_length_days fy_len from ({BEFORE}) b join {H} h on h.provider_ccn=b.ccn and h.fiscal_year_end_date=b.fye)
  select 'sold, full-year report before sale' grp, count(*) n, sum(iff(net_income<0,1,0)) losing, round(100*sum(iff(net_income<0,1,0))/count(*),1) pct, median(net_margin_ratio) med_margin from b where fy_len>=300
  union all
  select 'not sold, full-year report', count(*), sum(iff(net_income<0,1,0)), round(100*sum(iff(net_income<0,1,0))/count(*),1), median(net_margin_ratio)
  from {H} where fiscal_year_length_days>=300 and provider_ccn not in (select ccn from {P} where chow_dt between '2022-01-01' and '2024-12-31')""")
# what a stub looks like next to a full year for the same hospital (the 61 doubles)
q("stub_pairs", f"""select h.provider_ccn ccn, h.hospital_name, h.fiscal_year_begin_date fyb, h.fiscal_year_end_date fye, h.fiscal_year_length_days fy_len, h.net_margin_ratio, p.chow_dt
  from {H} h join {P} p on p.ccn=h.provider_ccn where p.chow_dt between '2022-01-01' and '2024-12-31' and p.prvdr_ctgry_cd='01'
  and h.provider_ccn in (select provider_ccn from {H} group by 1 having count(*)>1) order by 1, 3 limit 60""")

# ---------- is a CHOW a sale? proxy: did the name change between the pre-sale report and today's POS row ----------
q("name_change", f"""select case when upper(regexp_replace(h.hospital_name,'[^A-Z]',''))=upper(regexp_replace(b.fac_name,'[^A-Z]','')) then 'same name'
   when left(upper(regexp_replace(h.hospital_name,'[^A-Z]','')),8)=left(upper(regexp_replace(b.fac_name,'[^A-Z]','')),8) then 'same first 8 letters' else 'different name' end name_status,
   count(*) n, sum(iff(b.net_income<0,1,0)) losing
   from ({BEFORE}) b join {H} h on h.provider_ccn=b.ccn and h.fiscal_year_end_date=b.fye group by 1 order by 2 desc""")
q("name_change_list", f"""select b.ccn, h.hospital_name before_name, b.fac_name today_name, b.net_margin_ratio from ({BEFORE}) b join {H} h on h.provider_ccn=b.ccn and h.fiscal_year_end_date=b.fye
   where left(upper(regexp_replace(h.hospital_name,'[^A-Z]','')),8)<>left(upper(regexp_replace(b.fac_name,'[^A-Z]','')),8) order by 1""")

def default(o):
    import datetime, decimal, math
    if isinstance(o, (datetime.date, datetime.datetime)): return o.isoformat()
    if isinstance(o, decimal.Decimal): return float(o)
    if isinstance(o, float) and math.isnan(o): return None
    raise TypeError(str(type(o)))
with open(os.path.join(HERE, "results.json"), "w") as f:
    json.dump(R, f, default=default, indent=1)
print("wrote results.json")
