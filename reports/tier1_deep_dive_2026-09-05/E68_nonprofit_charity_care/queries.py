"""E68 - nonprofit hospitals with fat profits and thin charity care. Every query, logged to queries.log. SELECT only.
Run from repo root: PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 reports/tier1_deep_dive_2026-09-05/E68_nonprofit_charity_care/queries.py
"""
import json, sys, atexit
from _shared import q
D = "reports/tier1_deep_dive_2026-09-05/E68_nonprofit_charity_care"
q.open_log(f"{D}/queries.log")
H = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS"
B = "LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF"
out = {}
atexit.register(lambda: json.dump(out, open(f"{D}/results.json", "w"), default=str, indent=1))
STEP = sys.argv[1] if len(sys.argv) > 1 else "all"

# HCRIS control code -> owner class (CMS Worksheet S-2 line 21 codes)
OWNER = """case when TYPE_OF_CONTROL in ('1','2') then 'nonprofit'
                when TYPE_OF_CONTROL in ('3','4','5','6') then 'for-profit'
                when TYPE_OF_CONTROL in ('7','8','9','10','11','12','13') then 'government' else 'unknown' end"""
# Mart money columns are FLOAT and carry real NaN, not null. Filter with <> 'NaN'::float.
CLEAN = f"""
select PROVIDER_CCN, HOSPITAL_NAME, CITY, STATE_CODE, TYPE_OF_CONTROL, {OWNER} as owner,
       NUMBER_OF_BEDS, FISCAL_YEAR_BEGIN_DATE, FISCAL_YEAR_END_DATE,
       NET_INCOME, TOTAL_COSTS, COST_OF_CHARITY_CARE, TOTAL_BAD_DEBT_EXPENSE, COST_OF_UNCOMPENSATED_CARE,
       COST_OF_CHARITY_CARE / TOTAL_COSTS as charity_share,
       NET_INCOME / TOTAL_COSTS as margin_on_cost,
       row_number() over (partition by PROVIDER_CCN order by FISCAL_YEAR_END_DATE desc) rn
from {H}
where NET_INCOME <> 'NaN'::float and TOTAL_COSTS <> 'NaN'::float and COST_OF_CHARITY_CARE <> 'NaN'::float
  and TOTAL_COSTS > 0 and NET_INCOME <= TOTAL_COSTS
  and datediff(day, FISCAL_YEAR_BEGIN_DATE, FISCAL_YEAR_END_DATE) between 350 and 380
"""

if STEP in ("shape", "all"):
    out["bmf_columns"] = q.run(f"""select column_name, data_type from LIBRARY_MARTS.information_schema.columns
        where table_schema='CORPORATE_REGISTRY' and table_name='CORPORATE_REGISTRY__FED_IRS_EO_BMF' order by ordinal_position""", "bmf columns")
    out["hcris_shape"] = q.run(f"""
        select count(*) rows_, count(distinct PROVIDER_CCN) ccns,
          sum(iff(NET_INCOME = 'NaN'::float,1,0)) ni_nan,
          sum(iff(TOTAL_COSTS = 'NaN'::float,1,0)) tc_nan,
          sum(iff(COST_OF_CHARITY_CARE = 'NaN'::float,1,0)) cc_nan,
          sum(iff(NET_INCOME > TOTAL_COSTS,1,0)) ni_gt_tc,
          sum(iff(datediff(day, FISCAL_YEAR_BEGIN_DATE, FISCAL_YEAR_END_DATE) not between 350 and 380,1,0)) short_or_long,
          min(FISCAL_YEAR_END_DATE) min_fye, max(FISCAL_YEAR_END_DATE) max_fye,
          sum(iff(year(FISCAL_YEAR_END_DATE)=2023,1,0)) fye_2023, sum(iff(year(FISCAL_YEAR_END_DATE)=2024,1,0)) fye_2024,
          sum(iff(year(FISCAL_YEAR_BEGIN_DATE)=2023,1,0)) fyb_2023
        from {H}""", "hcris shape and nan counts")
    out["hcris_dup_ccn"] = q.run(f"""select PROVIDER_CCN, count(*) n from {H} group by 1 having count(*)>1 order by 2 desc limit 10""", "ccns with 2+ reports")
    out["filter_walk"] = q.run(f"""
        select {OWNER} as owner, count(*) all_rows, count(distinct PROVIDER_CCN) ccns,
          sum(iff(COST_OF_CHARITY_CARE <> 'NaN'::float,1,0)) charity_parses,
          sum(iff(COST_OF_CHARITY_CARE <> 'NaN'::float and NET_INCOME <> 'NaN'::float and TOTAL_COSTS <> 'NaN'::float and TOTAL_COSTS>0,1,0)) money_parses,
          sum(iff(COST_OF_CHARITY_CARE <> 'NaN'::float and NET_INCOME <> 'NaN'::float and TOTAL_COSTS <> 'NaN'::float and TOTAL_COSTS>0 and NET_INCOME<=TOTAL_COSTS,1,0)) ni_guard,
          sum(iff(COST_OF_CHARITY_CARE <> 'NaN'::float and NET_INCOME <> 'NaN'::float and TOTAL_COSTS <> 'NaN'::float and TOTAL_COSTS>0 and NET_INCOME<=TOTAL_COSTS
                  and datediff(day, FISCAL_YEAR_BEGIN_DATE, FISCAL_YEAR_END_DATE) between 350 and 380,1,0)) full_year
        from {H} group by 1 order by 1""", "filter walk by owner")
    out["clean_by_owner"] = q.run(f"""with c as ({CLEAN}) select owner, count(*) n, count(distinct PROVIDER_CCN) ccns, sum(iff(rn=1,1,0)) latest_rows from c group by 1 order by 1""", "clean rows by owner")

# ---- name normalizer for the IRS leg (own version, not the first pass's) ----
GEN = r"(THE|OF|AND|INC|LLC|CORP|CORPORATION|HOSPITAL|HOSPITALS|MEDICAL|CENTER|CENTRE|HEALTH|HEALTHCARE|SYSTEM|SERVICES|REGIONAL|COMMUNITY|MEMORIAL|GENERAL|ASSOCIATION|FOUNDATION|DBA)"
def norm(col):
    # upper, strip punctuation, drop generic words, squash spaces
    return (f"regexp_replace(regexp_replace(regexp_replace(upper({col}), '[^A-Z0-9 ]', ' '), "
            f"'\\\\b{GEN}\\\\b', ' '), ' +', ' ')")
def trimmed(col): return f"trim({norm(col)})"

TAIL = "NET_INCOME > 50e6 and charity_share < 0.01"

if STEP in ("sanity", "all"):
    out["norm_sanity"] = q.run(f"""select {trimmed("'THE COMMUNITY MEMORIAL HOSPITAL OF ST. LUKES, INC'")} as s,
        {trimmed("'STANFORD HEALTH CARE'")} as s2, {trimmed("'CEDARS-SINAI MEDICAL CENTER'")} as s3""", "normalizer sanity")
    out["bmf_ntee_sample"] = q.run(f"""select NTEE_CODE, count(*) n from {B} where NTEE_CODE like 'E2%' group by 1 order by 2 desc limit 12""", "bmf ntee E2x spellings")

if STEP in ("tail", "all"):
    # A. control-code way: nonprofit by CMS control code only, no IRS leg
    out["tail_by_owner"] = q.run(f"""with c as ({CLEAN})
        select owner, count(*) n_clean,
          sum(iff(NET_INCOME > 50e6,1,0)) n_over_50m,
          sum(iff(charity_share < 0.01,1,0)) n_under_1pct,
          sum(iff({TAIL},1,0)) n_tail,
          sum(iff(NET_INCOME > 50e6 and COST_OF_CHARITY_CARE <= 0,1,0)) n_over_50m_zero_charity
        from c where rn=1 group by 1 order by 1""", "tail counts by owner, control code only")
    out["tail_nonprofit_list"] = q.run(f"""with c as ({CLEAN})
        select PROVIDER_CCN, HOSPITAL_NAME, CITY, STATE_CODE, TYPE_OF_CONTROL, NUMBER_OF_BEDS, FISCAL_YEAR_END_DATE,
               NET_INCOME, TOTAL_COSTS, COST_OF_CHARITY_CARE, TOTAL_BAD_DEBT_EXPENSE, COST_OF_UNCOMPENSATED_CARE,
               charity_share, margin_on_cost
        from c where rn=1 and owner='nonprofit' and {TAIL} order by NET_INCOME desc""", "nonprofit-control tail list")

if STEP in ("irs", "all"):
    # B. IRS leg rebuilt: BMF NTEE E20-E22 hospitals, name prefix + city + state
    BMF = f"""select EIN, ORG_NAME, CITY, STATE, NTEE_CODE, SUBSECTION_CODE, {trimmed('ORG_NAME')} as bn
              from {B} where NTEE_CODE rlike '^E2[0-2].*'
              and ORG_NAME not rlike '.*(AUXILIARY|VOLUNTEER|FOUNDATION|GUILD|LEAGUE|FRIENDS|ALUMNI).*'"""
    PAIRS = f"""with c as ({CLEAN}), b as ({BMF}),
        h as (select c.*, {trimmed('HOSPITAL_NAME')} as hn from c where rn=1)
        select h.*, b.EIN, b.ORG_NAME, b.NTEE_CODE, b.SUBSECTION_CODE, iff(h.hn=b.bn,1,0) exact_name
        from h join b on upper(h.CITY)=upper(b.CITY) and h.STATE_CODE=b.STATE
          and length(h.hn)>=6 and length(b.bn)>=6
          and (h.hn like b.bn||'%' or b.bn like h.hn||'%')"""
    out["irs_pairs_shape"] = q.run(f"""with p as ({PAIRS})
        select count(*) pairs, count(distinct EIN) eins, count(distinct PROVIDER_CCN) ccns,
          count(distinct iff(owner='nonprofit',PROVIDER_CCN,null)) ccn_nonprofit,
          count(distinct iff(owner='for-profit',PROVIDER_CCN,null)) ccn_forprofit,
          count(distinct iff(owner='government',PROVIDER_CCN,null)) ccn_gov,
          sum(exact_name) exact_pairs from p""", "irs pairs shape")
    out["irs_tail"] = q.run(f"""with p as ({PAIRS}),
        one as (select PROVIDER_CCN, HOSPITAL_NAME, CITY, STATE_CODE, owner, NUMBER_OF_BEDS, FISCAL_YEAR_END_DATE,
                 NET_INCOME, TOTAL_COSTS, COST_OF_CHARITY_CARE, TOTAL_BAD_DEBT_EXPENSE, COST_OF_UNCOMPENSATED_CARE, charity_share, margin_on_cost,
                 count(distinct EIN) n_eins, min_by(EIN, iff(exact_name=1,0,1)) ein, min_by(ORG_NAME, iff(exact_name=1,0,1)) bmf_name, max(exact_name) any_exact
                from p group by all)
        select * from one where owner='nonprofit' and {TAIL} order by NET_INCOME desc""", "irs-matched nonprofit tail list")
    out["irs_tail_count_any_owner"] = q.run(f"""with p as ({PAIRS})
        select owner, count(distinct PROVIDER_CCN) n from p where {TAIL} group by 1""", "irs-matched tail by owner")

if STEP in ("dist", "all"):
    # C/D. distribution of charity share by owner, and by profit bucket
    out["pct_by_owner"] = q.run(f"""with c as ({CLEAN})
        select owner, count(*) n,
          percentile_cont(0.10) within group (order by charity_share) p10,
          percentile_cont(0.25) within group (order by charity_share) p25,
          percentile_cont(0.50) within group (order by charity_share) p50,
          percentile_cont(0.75) within group (order by charity_share) p75,
          percentile_cont(0.90) within group (order by charity_share) p90,
          sum(COST_OF_CHARITY_CARE)/sum(TOTAL_COSTS) dollar_weighted_share,
          sum(iff(COST_OF_CHARITY_CARE<=0,1,0)) n_zero_charity,
          sum(iff(charity_share<0.01,1,0)) n_under_1pct,
          sum(NET_INCOME) total_ni, sum(COST_OF_CHARITY_CARE) total_charity, sum(TOTAL_COSTS) total_costs,
          percentile_cont(0.5) within group (order by COST_OF_UNCOMPENSATED_CARE/TOTAL_COSTS) p50_uncomp_share
        from c where rn=1 group by 1 order by 1""", "charity share percentiles by owner")
    BUCKET = """case when NET_INCOME < 0 then '1 loss' when NET_INCOME < 10e6 then '2 $0-10M'
                     when NET_INCOME < 50e6 then '3 $10-50M' when NET_INCOME < 100e6 then '4 $50-100M' else '5 $100M+' end"""
    out["bucket_by_owner"] = q.run(f"""with c as ({CLEAN})
        select owner, {BUCKET} as profit_bucket, count(*) n,
          percentile_cont(0.5) within group (order by charity_share) p50_share,
          sum(COST_OF_CHARITY_CARE)/sum(TOTAL_COSTS) dollar_weighted_share,
          sum(iff(charity_share<0.01,1,0)) n_under_1pct,
          sum(NET_INCOME) total_ni, sum(COST_OF_CHARITY_CARE) total_charity
        from c where rn=1 group by 1,2 order by 1,2""", "charity share by owner x profit bucket")
    HIST = """case when charity_share <= 0 then '0 zero' when charity_share < 0.005 then '1 0-0.5%' when charity_share < 0.01 then '2 0.5-1%'
                   when charity_share < 0.02 then '3 1-2%' when charity_share < 0.03 then '4 2-3%' when charity_share < 0.05 then '5 3-5%'
                   when charity_share < 0.10 then '6 5-10%' else '7 10%+' end"""
    out["hist_by_owner"] = q.run(f"""with c as ({CLEAN})
        select owner, {HIST} as bin, count(*) n from c where rn=1 group by 1,2 order by 1,2""", "charity share histogram by owner")
    out["scatter_nonprofit"] = q.run(f"""with c as ({CLEAN})
        select PROVIDER_CCN, HOSPITAL_NAME, STATE_CODE, owner, NET_INCOME, charity_share, TOTAL_COSTS
        from c where rn=1 and NET_INCOME > 0 order by NET_INCOME desc limit 1200""", "scatter points, profitable hospitals, top 1200 by NI")
    # top-profit nonprofits regardless of charity: where do the 37 sit among the richest?
    out["top_profit_nonprofits"] = q.run(f"""with c as ({CLEAN})
        select count(*) n, sum(iff(charity_share<0.01,1,0)) n_under_1pct, sum(iff(charity_share<0.02,1,0)) n_under_2pct,
          percentile_cont(0.5) within group (order by charity_share) p50
        from c where rn=1 and owner='nonprofit' and NET_INCOME > 50e6""", "nonprofits over $50M: how many thin")

if STEP in ("check", "all"):
    # selection check on the for-profit comparison: who fills S-10 charity care?
    out["fp_fill_selection"] = q.run(f"""
        select {OWNER} as owner, iff(COST_OF_CHARITY_CARE <> 'NaN'::float,'charity parses','charity NaN') fill,
          count(*) n, median(TOTAL_COSTS) med_costs, median(NUMBER_OF_BEDS) med_beds,
          sum(iff(NET_INCOME <> 'NaN'::float and TOTAL_COSTS <> 'NaN'::float and NET_INCOME>50e6,1,0)) n_over_50m
        from {H} where TOTAL_COSTS <> 'NaN'::float group by 1,2 order by 1,2""", "who fills S-10 charity, by owner")
    # the 37 vs all nonprofits on the wider measure (charity + bad debt = uncompensated)
    out["tail_vs_all_uncomp"] = q.run(f"""with c as ({CLEAN})
        select iff({TAIL},'tail','rest') grp, count(*) n,
          percentile_cont(0.5) within group (order by charity_share) p50_charity,
          percentile_cont(0.5) within group (order by COST_OF_UNCOMPENSATED_CARE/TOTAL_COSTS) p50_uncomp,
          percentile_cont(0.5) within group (order by TOTAL_BAD_DEBT_EXPENSE/TOTAL_COSTS) p50_baddebt,
          sum(NET_INCOME) total_ni, sum(COST_OF_CHARITY_CARE) total_charity, sum(TOTAL_COSTS) total_costs
        from c where rn=1 and owner='nonprofit' group by 1""", "tail vs rest of nonprofits, wider measures")
    # the 52 nonprofit-control tail hospitals the IRS leg drops: who are they?
    out["tail_not_irs_matched"] = q.run(f"""with c as ({CLEAN}), b as ({BMF}),
        h as (select c.*, {trimmed('HOSPITAL_NAME')} as hn from c where rn=1 and owner='nonprofit' and {TAIL}),
        m as (select distinct h.PROVIDER_CCN from h join b on upper(h.CITY)=upper(b.CITY) and h.STATE_CODE=b.STATE
                and length(h.hn)>=6 and length(b.bn)>=6 and (h.hn like b.bn||'%' or b.bn like h.hn||'%'))
        select h.PROVIDER_CCN, h.HOSPITAL_NAME, h.CITY, h.STATE_CODE, h.NET_INCOME, h.charity_share
        from h left join m using (PROVIDER_CCN) where m.PROVIDER_CCN is null order by NET_INCOME desc""", "nonprofit-control tail not matched to IRS")
