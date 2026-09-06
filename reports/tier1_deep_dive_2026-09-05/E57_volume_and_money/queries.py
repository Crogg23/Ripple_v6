"""E57 - Do the top Medicare Part B billers also take the most industry money?
Part B DY2024 (one snapshot) x Open Payments PY2024 general payments (year-aligned).
Every query logs to queries.log; results land in results.json for story.html / findings.md.
Run from repo root: PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 .../queries.py
"""
import json
from pathlib import Path
from _shared.q import run, open_log
HERE = Path(__file__).resolve().parent
open_log(HERE / "queries.log")
OP = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS"
PB = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER"
R = {}

# Money buckets. Research payments are a separate CMS file that is NOT landed; only general payments exist here.
BUCKET = """case
  when nature_of_payment_or_transfer_of_value = 'Royalty or License' then 'royalty'
  when nature_of_payment_or_transfer_of_value in ('Consulting Fee','Honoraria')
    or nature_of_payment_or_transfer_of_value like 'Compensation for serv%' then 'services'
  when nature_of_payment_or_transfer_of_value in ('Food and Beverage','Travel and Lodging','Education','Gift','Entertainment') then 'hospitality'
  else 'other' end"""

# One row per NPI with money by bucket, PY2024, blank NPIs dropped (48,059 rows carry '' not null).
# NOTE: neither this CTE nor SCORED filters PROGRAM_YEAR. The mart is 100% PY2024 today (probe op_profile);
# the day a second year lands in this table, every number below silently doubles up. Add `and program_year = 2024` then.
OP_NPI = f"""
op as (
  select npi,
         sum(total_amount_of_payment_usdollars) usd,
         sum(case when {BUCKET}='royalty'     then total_amount_of_payment_usdollars else 0 end) royalty,
         sum(case when {BUCKET}='services'    then total_amount_of_payment_usdollars else 0 end) services,
         sum(case when {BUCKET}='hospitality' then total_amount_of_payment_usdollars else 0 end) hospitality,
         sum(case when {BUCKET}='other'       then total_amount_of_payment_usdollars else 0 end) other,
         count(*) n_pay
  from {OP}
  where npi is not null and trim(npi) <> ''
  group by npi)"""

# Part B individuals scored within specialty. Money decile is over Part B individuals with money coalesced to 0,
# same as the first pass, PLUS a positive-money flag so the zero-dollar "top decile" artifact can be removed.
SCORED = f"""
scored as (
  select b.rndrng_npi npi, b.rndrng_prvdr_type spec, b.rndrng_prvdr_state_abrvtn st,
         b.rndrng_prvdr_last_org_name last_name, b.rndrng_prvdr_first_name first_name,
         b.tot_mdcr_alowd_amt allowed, try_to_number(b.tot_srvcs) srvcs, try_to_number(b.tot_benes) benes,
         b.drug_mdcr_alowd_amt drug_allowed,
         coalesce(o.usd,0) usd, coalesce(o.royalty,0) royalty, coalesce(o.services,0) services,
         coalesce(o.hospitality,0) hospitality, coalesce(o.other,0) other, coalesce(o.n_pay,0) n_pay,
         ntile(10) over (partition by b.rndrng_prvdr_type order by b.tot_mdcr_alowd_amt) bill_dec,
         ntile(10) over (partition by b.rndrng_prvdr_type order by coalesce(o.usd,0)) money_dec,
         percent_rank() over (partition by b.rndrng_prvdr_type order by b.tot_mdcr_alowd_amt) bill_pr,
         percent_rank() over (partition by b.rndrng_prvdr_type order by coalesce(o.usd,0)) money_pr
  from {PB} b
  left join op o on o.npi = b.rndrng_npi
  where b.rndrng_prvdr_ent_cd = 'I')"""

# 1. Headline, first-pass method (ntile), year-aligned PY2024.
R["headline_ntile"] = run(f"""with {OP_NPI}, {SCORED}
select count(*) individuals,
       sum(case when bill_dec=10 then 1 else 0 end) top_billers,
       sum(case when bill_dec=10 and money_dec=10 then 1 else 0 end) both_top,
       sum(case when bill_dec=10 and money_dec=10 and usd>0 then 1 else 0 end) both_top_real_money,
       sum(case when bill_dec<10 and money_dec=10 then 1 else 0 end) peers_top_money,
       sum(case when bill_dec<10 then 1 else 0 end) peers,
       sum(case when money_dec=10 and usd=0 then 1 else 0 end) zero_dollar_top_money,
       sum(case when usd>0 then 1 else 0 end) any_money
from scored""", "headline_ntile")

# 2. Rebuild a DIFFERENT way: percent_rank, top 10% = pr >= 0.9, and money must be > 0.
R["headline_prank"] = run(f"""with {OP_NPI}, {SCORED}
select sum(case when bill_pr>=0.9 then 1 else 0 end) top_billers,
       sum(case when bill_pr>=0.9 and money_pr>=0.9 and usd>0 then 1 else 0 end) both_top,
       sum(case when bill_pr<0.9 then 1 else 0 end) peers,
       sum(case when bill_pr<0.9 and money_pr>=0.9 and usd>0 then 1 else 0 end) peers_top_money
from scored""", "headline_prank")

# 3. Money split by bucket: whole file (all NPIs) vs Part B individuals vs top billers vs both-top.
R["bucket_split"] = run(f"""with {OP_NPI}, {SCORED}
select 'all OP NPIs' cohort, count(*) people, sum(usd) usd, sum(royalty) royalty, sum(services) services, sum(hospitality) hospitality, sum(other) other,
       sum(case when royalty>0 then 1 else 0 end) royalty_people
from op
union all
select 'Part B individuals', count(*), sum(usd), sum(royalty), sum(services), sum(hospitality), sum(other), sum(case when royalty>0 then 1 else 0 end) from scored
union all
select 'top-decile billers', count(*), sum(usd), sum(royalty), sum(services), sum(hospitality), sum(other), sum(case when royalty>0 then 1 else 0 end) from scored where bill_dec=10
union all
select 'lower-decile billers', count(*), sum(usd), sum(royalty), sum(services), sum(hospitality), sum(other), sum(case when royalty>0 then 1 else 0 end) from scored where bill_dec<10
union all
select 'both-top', count(*), sum(usd), sum(royalty), sum(services), sum(hospitality), sum(other), sum(case when royalty>0 then 1 else 0 end) from scored where bill_dec=10 and money_dec=10 and usd>0
union all
select 'top money, not top biller', count(*), sum(usd), sum(royalty), sum(services), sum(hospitality), sum(other), sum(case when royalty>0 then 1 else 0 end) from scored where bill_dec<10 and money_dec=10 and usd>0
""", "bucket_split")

# 4. Overlap by specialty: rate, peer rate, dollars by bucket, for specialties with 200+ top billers.
R["by_specialty"] = run(f"""with {OP_NPI}, {SCORED}
select spec, count(*) individuals,
       sum(case when bill_dec=10 then 1 else 0 end) top_billers,
       sum(case when bill_dec=10 and money_dec=10 and usd>0 then 1 else 0 end) both_top,
       round(100.0*sum(case when bill_dec=10 and money_dec=10 and usd>0 then 1 else 0 end)/nullif(sum(case when bill_dec=10 then 1 else 0 end),0),1) rate_pct,
       round(100.0*sum(case when bill_dec<10 and money_dec=10 and usd>0 then 1 else 0 end)/nullif(sum(case when bill_dec<10 then 1 else 0 end),0),1) peer_pct,
       sum(case when bill_dec=10 and money_dec=10 and usd>0 then usd else 0 end) both_usd,
       sum(case when bill_dec=10 and money_dec=10 and usd>0 then royalty else 0 end) both_royalty,
       sum(case when bill_dec=10 and money_dec=10 and usd>0 then services else 0 end) both_services,
       sum(case when bill_dec=10 and money_dec=10 and usd>0 then hospitality else 0 end) both_hospitality,
       sum(case when bill_dec=10 and money_dec=10 and usd>0 then other else 0 end) both_other,
       sum(case when bill_dec=10 and money_dec=10 and usd>0 then allowed else 0 end) both_allowed,
       sum(case when money_dec=10 and usd=0 then 1 else 0 end) zero_dollar_top_money
from scored group by 1 having sum(case when bill_dec=10 then 1 else 0 end) >= 200 order by both_top desc""", "by_specialty")

# 5. Top 10 people by BOTH measures: rank product of national percent ranks (allowed x money), money > 0.
R["top10_both"] = run(f"""with {OP_NPI}, {SCORED},
nat as (select s.*, rank() over (order by allowed desc) r_allowed, rank() over (order by usd desc) r_money from scored s where usd>0)
select npi, first_name, last_name, spec, st, allowed, srvcs, benes, drug_allowed, usd, royalty, services, hospitality, other, n_pay, r_allowed, r_money, r_allowed*r_money rank_product
from nat order by rank_product limit 10""", "top10_both")

# 6. Top 10 among both-top by industry money, and top 10 by allowed - the two ends of the same cohort.
R["top10_money"] = run(f"""with {OP_NPI}, {SCORED}
select npi, first_name, last_name, spec, st, allowed, usd, royalty, services, hospitality, other
from scored where bill_dec=10 and money_dec=10 and usd>0 order by usd desc limit 10""", "top10_money")
R["top10_allowed"] = run(f"""with {OP_NPI}, {SCORED}
select npi, first_name, last_name, spec, st, allowed, drug_allowed, usd, royalty, services, hospitality, other
from scored where bill_dec=10 and money_dec=10 and usd>0 order by allowed desc limit 10""", "top10_allowed")

# 7. Concentration: how much of both-top money sits in the top 100 / top 10 people.
R["concentration"] = run(f"""with {OP_NPI}, {SCORED},
bt as (select usd, royalty, row_number() over (order by usd desc) rn, sum(usd) over () tot from scored where bill_dec=10 and money_dec=10 and usd>0)
select max(tot) tot, sum(case when rn<=10 then usd end) top10, sum(case when rn<=100 then usd end) top100, sum(case when rn<=1000 then usd end) top1000,
       count(*) n, median(usd) median_usd, sum(case when royalty>0 then 1 else 0 end) royalty_people
from bt""", "concentration")

# 8. Same overlap test with royalties REMOVED: is the overlap still there when the money is lunches and consulting?
R["headline_no_royalty"] = run(f"""with {OP_NPI},
scored2 as (
  select b.rndrng_npi npi, b.rndrng_prvdr_type spec, b.tot_mdcr_alowd_amt allowed, coalesce(o.usd,0)-coalesce(o.royalty,0) usd_nr,
         ntile(10) over (partition by b.rndrng_prvdr_type order by b.tot_mdcr_alowd_amt) bill_dec,
         ntile(10) over (partition by b.rndrng_prvdr_type order by coalesce(o.usd,0)-coalesce(o.royalty,0)) money_dec
  from {PB} b left join op o on o.npi=b.rndrng_npi where b.rndrng_prvdr_ent_cd='I')
select sum(case when bill_dec=10 then 1 else 0 end) top_billers,
       sum(case when bill_dec=10 and money_dec=10 and usd_nr>0 then 1 else 0 end) both_top,
       sum(case when bill_dec<10 then 1 else 0 end) peers,
       sum(case when bill_dec<10 and money_dec=10 and usd_nr>0 then 1 else 0 end) peers_top_money
from scored2""", "headline_no_royalty")

# 9. Gradient: for each billing decile, what share sits in the top money decile, and mean money.
R["by_bill_decile"] = run(f"""with {OP_NPI}, {SCORED}
select bill_dec, count(*) people,
       round(100.0*sum(case when money_dec=10 and usd>0 then 1 else 0 end)/count(*),2) top_money_pct,
       round(100.0*sum(case when usd>0 then 1 else 0 end)/count(*),1) any_money_pct,
       round(avg(usd),0) mean_usd, round(median(usd),0) median_usd, sum(usd) usd, sum(royalty) royalty, sum(services) services, sum(hospitality) hospitality
from scored group by 1 order by 1""", "by_bill_decile")

# 10. Buy-and-bill check: allowed charges include drug cost. Re-rank billing on the NON-drug (MED) allowed amount.
R["headline_med_only"] = run(f"""with {OP_NPI},
scored3 as (
  select b.rndrng_npi npi, b.rndrng_prvdr_type spec, coalesce(b.med_mdcr_alowd_amt,0) med_allowed, coalesce(o.usd,0) usd,
         ntile(10) over (partition by b.rndrng_prvdr_type order by coalesce(b.med_mdcr_alowd_amt,0)) bill_dec,
         ntile(10) over (partition by b.rndrng_prvdr_type order by coalesce(o.usd,0)) money_dec
  from {PB} b left join op o on o.npi=b.rndrng_npi where b.rndrng_prvdr_ent_cd='I')
select sum(case when bill_dec=10 then 1 else 0 end) top_billers,
       sum(case when bill_dec=10 and money_dec=10 and usd>0 then 1 else 0 end) both_top,
       sum(case when bill_dec<10 then 1 else 0 end) peers,
       sum(case when bill_dec<10 and money_dec=10 and usd>0 then 1 else 0 end) peers_top_money
from scored3""", "headline_med_only")
R["drug_share"] = run(f"""with {OP_NPI}, {SCORED}
select case when bill_dec=10 and money_dec=10 and usd>0 then 'both-top' when bill_dec=10 then 'top biller only' else 'rest' end cohort,
       count(*) people, sum(allowed) allowed, sum(coalesce(drug_allowed,0)) drug_allowed,
       round(100.0*sum(coalesce(drug_allowed,0))/sum(allowed),1) drug_pct
from scored group by 1""", "drug_share")

# 11. The named people: every payment nature and the top payer, so each name carries what KIND of money it is.
NAMED = ",".join("'%s'" % r["NPI"] for r in R["top10_both"] + R["top10_money"] + R["top10_allowed"])
R["named_nature"] = run(f"""
select npi, nature_of_payment_or_transfer_of_value nature, count(*) n, sum(total_amount_of_payment_usdollars) usd
from {OP} where npi in ({NAMED}) group by 1,2 order by 1, 4 desc""", "named_nature")
R["named_payer"] = run(f"""
select npi, applicable_manufacturer_or_applicable_gpo_making_payment_name payer, count(*) n, sum(total_amount_of_payment_usdollars) usd,
       rank() over (partition by npi order by sum(total_amount_of_payment_usdollars) desc) rk
from {OP} where npi in ({NAMED}) group by 1,2 qualify rk<=2 order by 1, 4 desc""", "named_payer")
# 12. Name-collision check: one NPI must be one profile and one name in Open Payments.
R["named_identity"] = run(f"""
select npi, count(distinct covered_recipient_profile_id) profiles, count(distinct covered_recipient_last_name) last_names,
       min(covered_recipient_first_name) first_name, min(covered_recipient_last_name) last_name, min(covered_recipient_specialty_1) op_specialty,
       min(recipient_state) op_state, count(*) rows_
from {OP} where npi in ({NAMED}) group by 1""", "named_identity")

# 13. Trap check on the landing twin: the column with PAYMENT_ID in its name is an id, not money.
R["mfr_id_trap"] = run("""
select count(*) rows_, count(distinct APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_ID) distinct_ids,
       min(APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_ID) min_id, max(APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_ID) max_id,
       sum(try_to_number(APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_ID)) bogus_sum
from LIBRARY_RAW.LANDING.FED_CMS_OPEN_PAYMENTS""", "mfr_id_trap")

json.dump(R, open(HERE / "results.json", "w"), indent=1, default=str)
print("saved", HERE / "results.json")
