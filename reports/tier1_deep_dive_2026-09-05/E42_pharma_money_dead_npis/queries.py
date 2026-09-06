"""E42 - Open Payments PY2024 money to NPPES-deactivated NPIs. Every query logged to queries.log."""
import json, sys
from _shared.q import run, open_log
D = "reports/tier1_deep_dive_2026-09-05/E42_pharma_money_dead_npis"
open_log(f"{D}/queries.log")
OP = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS"
OP23 = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2023"
OP22 = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2022"
NP = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES"
SUP = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT"
OUT = {}

# deactivated, never reactivated
DEAD = f"(select NPI, NPI_DEACTIVATION_DATE d from {NP} where NPI_DEACTIVATION_DATE is not null and NPI_REACTIVATION_DATE is null)"
# per-payment rows with parsed date, restricted to dead NPIs
def after(op=OP):
    return f"""(select o.NPI, try_to_date(o.DATE_OF_PAYMENT,'MM/DD/YYYY') pd, n.d,
        o.TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS amt, o.NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE nature,
        o.APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME payer,
        o.COVERED_RECIPIENT_FIRST_NAME fn, o.COVERED_RECIPIENT_LAST_NAME ln, o.RECIPIENT_STATE st,
        o.COVERED_RECIPIENT_SPECIALTY_1 spec, o.COVERED_RECIPIENT_PROFILE_ID pid
        from {op} o join {DEAD} n on n.NPI = o.NPI
        where try_to_date(o.DATE_OF_PAYMENT,'MM/DD/YYYY') > n.d)"""

# Q1 rebuild the first pass a different way: aggregate payments per NPI+day first, then join and test the date
OUT["q1_rebuild"] = run(f"""
with byday as (select NPI, try_to_date(DATE_OF_PAYMENT,'MM/DD/YYYY') pd, sum(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) amt, count(*) n
               from {OP} where NPI is not null group by 1,2)
select count(distinct b.NPI) dead_npis_paid_2024,
       count(distinct case when b.pd > n.d then b.NPI end) npis_paid_after,
       sum(case when b.pd > n.d then b.amt end) dollars_after,
       sum(case when b.pd > n.d then b.n end) payments_after,
       sum(b.amt) dollars_all, sum(b.n) payments_all,
       count(distinct case when b.pd > dateadd(day,90,n.d) then b.NPI end) npis_paid_90plus
from byday b join {DEAD} n on n.NPI = b.NPI""", "q1_rebuild")

# Q2 concentration and the top 10
OUT["q2_top"] = run(f"""
with per as (select NPI, sum(amt) tot, count(*) n, min(pd) first_pd, max(pd) last_pd, min(d) d,
                    count(distinct payer) payers, max(fn) fn, max(ln) ln, max(st) st, max(spec) spec, max(pid) pid
             from {after()} group by 1)
select NPI, fn, ln, st, spec, pid, d deact, first_pd, last_pd, datediff(day, d, first_pd) days_to_first, datediff(day, d, last_pd) days_to_last,
       n payments, payers, tot, round(100*tot/sum(tot) over (),2) pct, round(100*sum(tot) over (order by tot desc rows unbounded preceding)/sum(tot) over (),2) cum_pct,
       row_number() over (order by tot desc) rk
from per qualify rk <= 25 order by rk""", "q2_top25")

# Q3 distribution of per-NPI after-deactivation totals
OUT["q3_dist"] = run(f"""
with per as (select NPI, sum(amt) tot from {after()} group by 1)
select case when tot < 25 then 'a <$25' when tot < 100 then 'b $25-100' when tot < 1000 then 'c $100-1k'
            when tot < 10000 then 'd $1k-10k' when tot < 100000 then 'e $10k-100k' else 'f $100k+' end bucket,
       count(*) npis, sum(tot) dollars, median(tot) med
from per group by 1 order by 1""", "q3_dist")

# Q4 nature of payment: whole after-deactivation set vs top 10
TOP10 = f"(select NPI from (select NPI, sum(amt) tot from {after()} group by 1 order by tot desc limit 10))"
OUT["q4_nature"] = run(f"""
select nature, case when NPI in {TOP10} then 'top10' else 'rest' end grp,
       count(distinct NPI) npis, count(*) payments, sum(amt) dollars
from {after()} group by 1,2 order by dollars desc""", "q4_nature")

# Q5 top-10 detail: nature x payer per NPI
OUT["q5_top_detail"] = run(f"""
select NPI, ln, nature, payer, count(*) payments, sum(amt) dollars, min(pd) first_pd, max(pd) last_pd
from {after()} where NPI in {TOP10} group by 1,2,3,4 order by NPI, dollars desc""", "q5_top_detail")

# Q6 NPPES row for the top 10: what survived the strip, and was it ever reactivated
OUT["q6_nppes"] = run(f"""
select NPI, ENTITY_TYPE_CODE, PROVIDER_LAST_NAME_LEGAL_NAME, PROVIDER_ENUMERATION_DATE, LAST_UPDATE_DATE,
       NPI_DEACTIVATION_REASON_CODE, NPI_DEACTIVATION_DATE, NPI_REACTIVATION_DATE, REPLACEMENT_NPI, CERTIFICATION_DATE,
       HEALTHCARE_PROVIDER_TAXONOMY_CODE_1, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME
from {NP} where NPI in {TOP10}""", "q6_nppes_top10")

# Q7 same 10 NPIs in the PY2023 and PY2022 files: is the stream continuous
OUT["q7_prior"] = run(f"""
select NPI, 2023 py, count(*) payments, sum(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) dollars,
       min(try_to_date(DATE_OF_PAYMENT,'MM/DD/YYYY')) first_pd, max(try_to_date(DATE_OF_PAYMENT,'MM/DD/YYYY')) last_pd
from {OP23} where NPI in {TOP10} group by 1
union all
select NPI, 2022, count(*), sum(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS),
       min(try_to_date(DATE_OF_PAYMENT,'MM/DD/YYYY')), max(try_to_date(DATE_OF_PAYMENT,'MM/DD/YYYY'))
from {OP22} where NPI in {TOP10} group by 1 order by 1,2""", "q7_prior_years")

# Q8 does the person hold a second, live NPI? name+state search on NPPES (deactivated rows are name-stripped, so this only finds live ones)
OUT["q8_second_npi"] = run(f"""
with t as (select NPI dead_npi, max(fn) fn, max(ln) ln, max(st) st from {after()} where NPI in {TOP10} group by 1)
select t.dead_npi, t.ln, t.fn, t.st, p.NPI live_npi, p.PROVIDER_ENUMERATION_DATE enum_dt, p.NPI_DEACTIVATION_DATE live_deact,
       p.PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME live_st, p.HEALTHCARE_PROVIDER_TAXONOMY_CODE_1 tax
from t left join {NP} p on upper(p.PROVIDER_LAST_NAME_LEGAL_NAME) = upper(t.ln) and upper(p.PROVIDER_FIRST_NAME) = upper(t.fn)
      and p.ENTITY_TYPE_CODE = '1'
order by t.dead_npi""", "q8_second_npi_by_name")

# Q9 the profile supplement for the 10
OUT["q9_sup"] = run(f"""
select PROFILE_ID, NPI, FIRST_NAME, LAST_NAME, STATE, PRIMARY_SPECIALTY, ASSOCIATED_PROFILE_ID_1, ASSOCIATED_PROFILE_ID_2, LICENSE_STATE_CODE_1
from {SUP} where NPI in {TOP10}""", "q9_supplement_top10")

# Q10 the reactivated angle: NPIs deactivated AND reactivated, paid inside the dead window in PY2024
OUT["q10_react"] = run(f"""
with r as (select NPI, NPI_DEACTIVATION_DATE d, NPI_REACTIVATION_DATE rd from {NP}
           where NPI_DEACTIVATION_DATE is not null and NPI_REACTIVATION_DATE is not null)
select count(distinct o.NPI) npis_in_window, count(*) payments, sum(o.TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) dollars,
       max(o.TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) biggest, median(datediff(day, r.d, r.rd)) med_gap_days
from {OP} o join r on r.NPI = o.NPI
where try_to_date(o.DATE_OF_PAYMENT,'MM/DD/YYYY') > r.d and try_to_date(o.DATE_OF_PAYMENT,'MM/DD/YYYY') < r.rd""", "q10_reactivated_window")

# Q11 timing: for all after-deactivation NPIs, years between deactivation and first 2024 payment
OUT["q11_gap"] = run(f"""
with per as (select NPI, min(d) d, min(pd) first_pd, sum(amt) tot from {after()} group by 1)
select least(floor(datediff(day, d, first_pd)/365.25), 10) yrs, count(*) npis, sum(tot) dollars
from per group by 1 order by 1""", "q11_gap_years")

# Q12 deactivation month vs payment month for the 10, per payment: how far after the deactivation is each dollar
OUT["q12_top_timeline"] = run(f"""
select NPI, ln, date_trunc(month, pd) m, sum(amt) dollars, count(*) n
from {after()} where NPI in {TOP10} group by 1,2,3 order by 1,3""", "q12_top10_monthly")

json.dump(OUT, open(f"{D}/results.json","w"), indent=1, default=str)
for k,v in OUT.items():
    print("==", k, len(v))
    for r in v[:40]: print(r)
