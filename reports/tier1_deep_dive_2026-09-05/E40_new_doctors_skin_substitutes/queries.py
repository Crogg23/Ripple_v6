"""E40 - brand-new NPIs billing Medicare Part B for skin substitutes, DY2024.
Every query here is SELECT-only and aggregates in SQL. Results land in results.json for story.py.
Run from repo root: PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 reports/tier1_deep_dive_2026-09-05/E40_new_doctors_skin_substitutes/queries.py
"""
import json, sys
from decimal import Decimal
sys.path.insert(0, "reports/tier1_deep_dive_2026-09-05")
from _shared.q import run, open_log

D = "reports/tier1_deep_dive_2026-09-05/E40_new_doctors_skin_substitutes"
open_log(f"{D}/queries.log")
R = {}

PROV = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER"
SVC = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI"
NPPES = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES"

# skin substitute = HCPCS Q4100 and up (Q4001-Q4051 are casting supplies, Q4074/Q4081 drugs)
SKIN = "(left(HCPCS_CD,2)='Q4' and try_to_number(substr(HCPCS_CD,2),18,0) >= 4100)"
# line dollars = services x average allowed
LINE = "try_to_number(TOT_SRVCS,18,6) * AVG_MDCR_ALOWD_AMT"

# --- 0. key checks (trap: an id is not an id until counted) -------------------------------------
R["keys"] = run(f"""
select 'prov' as t, count(*) n, count(distinct RNDRNG_NPI) d, min(length(RNDRNG_NPI)) mn, max(length(RNDRNG_NPI)) mx from {PROV}
union all
select 'nppes', count(*), count(distinct NPI), min(length(NPI)), max(length(NPI)) from {NPPES}
union all
select 'svc', count(*), count(distinct RNDRNG_NPI), min(length(RNDRNG_NPI)), max(length(RNDRNG_NPI)) from {SVC}
""", "key checks")

R["nppes_type"] = run(f"""
select ENTITY_TYPE_CODE, count(*) n, min(PROVIDER_ENUMERATION_DATE) mn, max(PROVIDER_ENUMERATION_DATE) mx,
       sum(iff(PROVIDER_ENUMERATION_DATE is null,1,0)) null_dt
from {NPPES} group by 1 order by 1
""", "nppes entity type + enumeration range")

# carbon-date the two Part B files: newest enumeration year present
R["carbon"] = run(f"""
select 'prov' f, year(n.PROVIDER_ENUMERATION_DATE) y, count(distinct p.RNDRNG_NPI) npis
from {PROV} p join {NPPES} n on n.NPI = p.RNDRNG_NPI
where year(n.PROVIDER_ENUMERATION_DATE) >= 2022 group by 1,2
union all
select 'svc', year(n.PROVIDER_ENUMERATION_DATE), count(distinct s.RNDRNG_NPI)
from (select distinct RNDRNG_NPI from {SVC}) s join {NPPES} n on n.NPI = s.RNDRNG_NPI
where year(n.PROVIDER_ENUMERATION_DATE) >= 2022 group by 1,2
order by 1,2
""", "carbon date both files")

# --- 1. rebuild the first pass a different way: top 1% individual billers, enumerated 2022+ -----
COHORT = f"""
with ind as (
  select RNDRNG_NPI, TOT_MDCR_ALOWD_AMT, try_to_number(TOT_BENES,18,0) benes, RNDRNG_PRVDR_TYPE, RNDRNG_PRVDR_STATE_ABRVTN st
  from {PROV} where RNDRNG_PRVDR_ENT_CD = 'I'
), ranked as (
  select *, percent_rank() over (order by TOT_MDCR_ALOWD_AMT desc) pr from ind
), top1 as (
  select r.*, n.PROVIDER_ENUMERATION_DATE enum_dt,
         iff(n.PROVIDER_ENUMERATION_DATE >= '2022-01-01','new','veteran') grp
  from ranked r join {NPPES} n on n.NPI = r.RNDRNG_NPI and n.ENTITY_TYPE_CODE = '1'
  where r.pr < 0.01
)
"""
R["top1"] = run(COHORT + """
select grp, count(*) npis, sum(TOT_MDCR_ALOWD_AMT) allowed, min(TOT_MDCR_ALOWD_AMT) cut
from top1 group by 1 order by 1
""", "top1% split new vs veteran (loose number)")

R["top1_skin"] = run(COHORT + f"""
select t.grp, count(distinct s.RNDRNG_NPI) npis_with_skin, sum({LINE}) skin_allowed
from top1 t join {SVC} s on s.RNDRNG_NPI = t.RNDRNG_NPI
where {SKIN} group by 1 order by 1
""", "top1% skin-substitute dollars (strict number, first-pass cohort)")

# --- 2. the cleaner strict definition: EVERY 2022+ NPI, skin-substitute lines only ---------------
NEW = f"""
with newnpi as (
  select NPI, PROVIDER_ENUMERATION_DATE enum_dt, PROVIDER_CREDENTIAL_TEXT cred
  from {NPPES} where ENTITY_TYPE_CODE = '1' and PROVIDER_ENUMERATION_DATE >= '2022-01-01'
)
"""
R["all_new_skin"] = run(NEW + f"""
select count(distinct s.RNDRNG_NPI) npis, sum({LINE}) skin_allowed, sum(try_to_number(s.TOT_SRVCS,18,6)) sq_cm_units,
       count(distinct s.HCPCS_CD) codes
from {SVC} s join newnpi n on n.NPI = s.RNDRNG_NPI
where {SKIN}
""", "ALL 2022+ NPIs: skin-substitute dollars")

# everyone, for the share
R["all_skin"] = run(f"""
select iff(n.PROVIDER_ENUMERATION_DATE >= '2022-01-01','new','veteran') grp,
       count(distinct s.RNDRNG_NPI) npis, sum({LINE}) skin_allowed
from {SVC} s join {NPPES} n on n.NPI = s.RNDRNG_NPI and n.ENTITY_TYPE_CODE='1'
where {SKIN} group by 1 order by 1
""", "skin dollars new vs veteran, all individual billers")

# is Q4<4100 leaking into 'skin' anywhere for new NPIs? (trap check)
R["q4_low"] = run(NEW + f"""
select sum(iff({SKIN},1,0)) hi_lines, sum(iff(left(s.HCPCS_CD,2)='Q4' and not {SKIN},1,0)) lo_lines,
       sum(iff(left(s.HCPCS_CD,2)='Q4' and not {SKIN}, {LINE}, 0)) lo_dollars
from {SVC} s join newnpi n on n.NPI = s.RNDRNG_NPI
""", "Q4 below 4100 among new NPIs")

# the codes themselves, to prove they are grafts
R["codes"] = run(NEW + f"""
select s.HCPCS_CD, max(s.HCPCS_DESC) descr, count(distinct s.RNDRNG_NPI) npis, sum({LINE}) allowed
from {SVC} s join newnpi n on n.NPI = s.RNDRNG_NPI
where {SKIN} group by 1 order by 4 desc limit 15
""", "top skin codes among new NPIs")

# --- 3. enumeration year vs billing -------------------------------------------------------------
R["by_year"] = run(f"""
with skin as (
  select RNDRNG_NPI, sum({LINE}) skin_allowed from {SVC} where {SKIN} group by 1
)
select year(n.PROVIDER_ENUMERATION_DATE) enum_year,
       count(*) skin_billers, sum(k.skin_allowed) skin_allowed,
       sum(p.TOT_MDCR_ALOWD_AMT) total_allowed
from skin k join {PROV} p on p.RNDRNG_NPI = k.RNDRNG_NPI and p.RNDRNG_PRVDR_ENT_CD='I'
join {NPPES} n on n.NPI = k.RNDRNG_NPI and n.ENTITY_TYPE_CODE='1'
group by 1 order by 1
""", "skin billing by enumeration year")

# how many individual NPIs of each enumeration year bill Part B at all (denominator)
R["by_year_denom"] = run(f"""
select year(n.PROVIDER_ENUMERATION_DATE) enum_year, count(*) partb_billers
from {PROV} p join {NPPES} n on n.NPI = p.RNDRNG_NPI and n.ENTITY_TYPE_CODE='1'
where p.RNDRNG_PRVDR_ENT_CD='I' group by 1 order by 1
""", "Part B individual billers by enumeration year")

# --- 4. states ---------------------------------------------------------------------------------
R["states"] = run(f"""
select s.RNDRNG_PRVDR_STATE_ABRVTN st,
       iff(n.PROVIDER_ENUMERATION_DATE >= '2022-01-01','new','veteran') grp,
       count(distinct s.RNDRNG_NPI) npis, sum({LINE}) skin_allowed
from {SVC} s join {NPPES} n on n.NPI = s.RNDRNG_NPI and n.ENTITY_TYPE_CODE='1'
where {SKIN} group by 1,2
""", "skin dollars by state, new vs veteran")

# --- 5. top 10 new billers ----------------------------------------------------------------------
R["top10"] = run(NEW + f"""
, skin as (
  select s.RNDRNG_NPI, sum({LINE}) skin_allowed, sum(try_to_number(s.TOT_SRVCS,18,6)) units,
         count(distinct s.HCPCS_CD) codes
  from {SVC} s join newnpi n on n.NPI = s.RNDRNG_NPI where {SKIN} group by 1
)
select k.RNDRNG_NPI npi, p.RNDRNG_PRVDR_LAST_ORG_NAME last_name, p.RNDRNG_PRVDR_FIRST_NAME first_name,
       p.RNDRNG_PRVDR_TYPE ptype, p.RNDRNG_PRVDR_STATE_ABRVTN st, p.RNDRNG_PRVDR_CITY city,
       n.enum_dt, k.skin_allowed, p.TOT_MDCR_ALOWD_AMT total_allowed, p.TOT_MDCR_PYMT_AMT total_paid,
       try_to_number(p.TOT_BENES,18,0) benes, k.units, k.codes
from skin k join {PROV} p on p.RNDRNG_NPI = k.RNDRNG_NPI join newnpi n on n.NPI = k.RNDRNG_NPI
order by k.skin_allowed desc limit 10
""", "top 10 new NPIs by skin dollars")

# concentration: top 10 / top 50 share of new-NPI skin dollars
R["conc"] = run(NEW + f"""
, skin as (
  select s.RNDRNG_NPI, sum({LINE}) a from {SVC} s join newnpi n on n.NPI = s.RNDRNG_NPI where {SKIN} group by 1
), r as (select a, row_number() over (order by a desc) rn from skin)
select sum(iff(rn<=10,a,0)) top10, sum(iff(rn<=50,a,0)) top50, sum(a) total, count(*) npis,
       sum(iff(a>=1000000,1,0)) over_1m
from r
""", "concentration among new skin billers")

# --- 6. dollars per beneficiary, new vs established, among skin billers -------------------------
R["per_bene"] = run(f"""
with skin as (
  select RNDRNG_NPI, sum({LINE}) skin_allowed,
         sum(try_to_number(TOT_BENES,18,0)) skin_bene_lines
  from {SVC} where {SKIN} group by 1
), j as (
  select iff(n.PROVIDER_ENUMERATION_DATE >= '2022-01-01','new','veteran') grp,
         p.TOT_MDCR_ALOWD_AMT allowed, try_to_number(p.TOT_BENES,18,0) benes,
         k.skin_allowed, k.skin_bene_lines
  from skin k join {PROV} p on p.RNDRNG_NPI = k.RNDRNG_NPI and p.RNDRNG_PRVDR_ENT_CD='I'
  join {NPPES} n on n.NPI = k.RNDRNG_NPI and n.ENTITY_TYPE_CODE='1'
)
select grp, count(*) npis,
       median(allowed/nullif(benes,0)) med_allowed_per_bene,
       sum(allowed)/sum(benes) pooled_allowed_per_bene,
       median(skin_allowed/nullif(skin_bene_lines,0)) med_skin_per_skin_bene,
       sum(skin_allowed)/sum(skin_bene_lines) pooled_skin_per_skin_bene,
       median(skin_allowed/allowed) med_skin_share,
       sum(iff(skin_allowed/allowed > 0.5,1,0)) majority_skin,
       sum(iff(allowed/nullif(benes,0) > 100000,1,0)) over_100k_per_bene
from j group by 1 order by 1
""", "dollars per beneficiary new vs veteran skin billers")

# same, but veterans restricted to the same specialties (NP / PA) so the comparison is like for like
R["per_bene_np_pa"] = run(f"""
with skin as (
  select RNDRNG_NPI, sum({LINE}) skin_allowed from {SVC} where {SKIN} group by 1
), j as (
  select iff(n.PROVIDER_ENUMERATION_DATE >= '2022-01-01','new','veteran') grp, p.RNDRNG_PRVDR_TYPE ptype,
         p.TOT_MDCR_ALOWD_AMT allowed, try_to_number(p.TOT_BENES,18,0) benes, k.skin_allowed
  from skin k join {PROV} p on p.RNDRNG_NPI = k.RNDRNG_NPI and p.RNDRNG_PRVDR_ENT_CD='I'
  join {NPPES} n on n.NPI = k.RNDRNG_NPI and n.ENTITY_TYPE_CODE='1'
  where p.RNDRNG_PRVDR_TYPE in ('Nurse Practitioner','Physician Assistant')
)
select grp, count(*) npis, median(allowed/nullif(benes,0)) med_allowed_per_bene,
       sum(allowed)/sum(benes) pooled_allowed_per_bene, sum(skin_allowed) skin_allowed
from j group by 1 order by 1
""", "per-bene, NP/PA only")

# provider type mix of new skin billers
R["ptype"] = run(NEW + f"""
, skin as (
  select s.RNDRNG_NPI, sum({LINE}) a from {SVC} s join newnpi n on n.NPI = s.RNDRNG_NPI where {SKIN} group by 1
)
select p.RNDRNG_PRVDR_TYPE ptype, count(*) npis, sum(k.a) skin_allowed
from skin k join {PROV} p on p.RNDRNG_NPI = k.RNDRNG_NPI group by 1 order by 3 desc limit 8
""", "provider type of new skin billers")

# --- 7. base rates: how new is the NP/PA workforce anyway? -------------------------------------
R["np_pa_base"] = run(f"""
select p.RNDRNG_PRVDR_TYPE ptype, iff(n.PROVIDER_ENUMERATION_DATE >= '2022-01-01','new','veteran') grp,
       count(*) partb_billers, sum(p.TOT_MDCR_ALOWD_AMT) allowed
from {PROV} p join {NPPES} n on n.NPI = p.RNDRNG_NPI and n.ENTITY_TYPE_CODE='1'
where p.RNDRNG_PRVDR_ENT_CD='I' and p.RNDRNG_PRVDR_TYPE in ('Nurse Practitioner','Physician Assistant')
group by 1,2 order by 1,2
""", "NP/PA Part B billers new vs veteran (base rate)")

R["all_base"] = run(f"""
select iff(n.PROVIDER_ENUMERATION_DATE >= '2022-01-01','new','veteran') grp, count(*) partb_billers, sum(p.TOT_MDCR_ALOWD_AMT) allowed
from {PROV} p join {NPPES} n on n.NPI = p.RNDRNG_NPI and n.ENTITY_TYPE_CODE='1'
where p.RNDRNG_PRVDR_ENT_CD='I' group by 1 order by 1
""", "all individual Part B billers new vs veteran (base rate)")

# --- 8. do the new skin billers share a practice address? (rented-NPI smell) --------------------
R["addr"] = run(NEW + f"""
, skin as (
  select s.RNDRNG_NPI, sum({LINE}) a from {SVC} s join newnpi n on n.NPI = s.RNDRNG_NPI where {SKIN} group by 1
)
select upper(trim(p.RNDRNG_PRVDR_ST1)) st1, p.RNDRNG_PRVDR_CITY city, p.RNDRNG_PRVDR_STATE_ABRVTN st,
       count(*) new_npis, sum(k.a) skin_allowed
from skin k join {PROV} p on p.RNDRNG_NPI = k.RNDRNG_NPI
group by 1,2,3 having count(*) > 1 order by 4 desc, 5 desc limit 15
""", "new skin billers sharing a practice address")

R["addr_summary"] = run(NEW + f"""
, skin as (
  select s.RNDRNG_NPI, sum({LINE}) a from {SVC} s join newnpi n on n.NPI = s.RNDRNG_NPI where {SKIN} group by 1
), a as (
  select upper(trim(p.RNDRNG_PRVDR_ST1))||'|'||p.RNDRNG_PRVDR_CITY||'|'||p.RNDRNG_PRVDR_STATE_ABRVTN addr, count(*) n, sum(k.a) d
  from skin k join {PROV} p on p.RNDRNG_NPI = k.RNDRNG_NPI group by 1
)
select count(*) addresses, sum(iff(n>1,n,0)) npis_at_shared_addr, sum(iff(n>1,d,0)) dollars_at_shared_addr, sum(d) total
from a
""", "address sharing summary")

# --- 9. how many veteran NPIs sit at the same addresses as the new skin billers? -----------------
R["addr_vets"] = run(NEW + f"""
, skin as (
  select s.RNDRNG_NPI, sum({LINE}) a from {SVC} s join newnpi n on n.NPI = s.RNDRNG_NPI where {SKIN} group by 1
), newaddr as (
  select distinct upper(trim(p.RNDRNG_PRVDR_ST1)) st1, p.RNDRNG_PRVDR_CITY city, p.RNDRNG_PRVDR_STATE_ABRVTN st
  from skin k join {PROV} p on p.RNDRNG_NPI = k.RNDRNG_NPI
), vskin as (
  select RNDRNG_NPI, sum({LINE}) a from {SVC} where {SKIN} group by 1
)
select count(distinct p.RNDRNG_NPI) veteran_skin_npis_same_addr, sum(v.a) their_skin_dollars
from vskin v join {PROV} p on p.RNDRNG_NPI = v.RNDRNG_NPI
join {NPPES} n on n.NPI = v.RNDRNG_NPI and n.ENTITY_TYPE_CODE='1' and n.PROVIDER_ENUMERATION_DATE < '2022-01-01'
join newaddr x on x.st1 = upper(trim(p.RNDRNG_PRVDR_ST1)) and x.city = p.RNDRNG_PRVDR_CITY and x.st = p.RNDRNG_PRVDR_STATE_ABRVTN
""", "veteran skin billers at the new billers' addresses")

# --- 10. months between enumeration and the data year: how fast did they ramp? ------------------
R["ramp"] = run(NEW + f"""
, skin as (
  select s.RNDRNG_NPI, sum({LINE}) a from {SVC} s join newnpi n on n.NPI = s.RNDRNG_NPI where {SKIN} group by 1
)
select iff(n.enum_dt >= '2023-07-01', 'enumerated Jul 2023 or later', iff(n.enum_dt >= '2023-01-01','enumerated H1 2023','enumerated 2022')) bucket,
       count(*) npis, sum(k.a) skin_allowed, median(k.a) med_skin
from skin k join newnpi n on n.NPI = k.RNDRNG_NPI group by 1 order by 1
""", "ramp speed by enumeration half-year")

# --- 11. skeptic add: the A2xxx skin-substitute family (2023-24 codes) sits outside Q4 ---------------
R["a2"] = run(NEW + f"""
select count(*) lines, count(distinct s.RNDRNG_NPI) npis, sum({LINE}) allowed
from {SVC} s join newnpi n on n.NPI = s.RNDRNG_NPI
where s.HCPCS_CD between 'A2001' and 'A2999'
""", "A2xxx skin substitutes among new NPIs (excluded from headline)")

# --- 12. skeptic add: per-bene against ALL veteran NP/PAs, not only those in the graft business ------
R["per_bene_all_nppa"] = run(f"""
select iff(n.PROVIDER_ENUMERATION_DATE >= '2022-01-01','new','veteran') grp, count(*) npis,
       median(p.TOT_MDCR_ALOWD_AMT/nullif(try_to_number(p.TOT_BENES,18,0),0)) med_allowed_per_bene
from {PROV} p join {NPPES} n on n.NPI = p.RNDRNG_NPI and n.ENTITY_TYPE_CODE='1'
where p.RNDRNG_PRVDR_ENT_CD='I' and p.RNDRNG_PRVDR_TYPE in ('Nurse Practitioner','Physician Assistant')
group by 1 order by 1
""", "per-bene, every NP/PA Part B biller")

def enc(o):
    if isinstance(o, Decimal): return float(o)
    return str(o)
json.dump(R, open(f"{D}/results.json","w"), default=enc, indent=1)
print("wrote results.json")
