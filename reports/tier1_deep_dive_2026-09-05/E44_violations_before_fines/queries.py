"""E44 - did Bria's violations climb before the fines? Every query here, logged to queries.log.
Run from repo root: PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 reports/tier1_deep_dive_2026-09-05/E44_violations_before_fines/queries.py
"""
import json
from _shared.q import run, open_log

D = "reports/tier1_deep_dive_2026-09-05/E44_violations_before_fines"
open_log(f"{D}/queries.log")
NH = "LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411"
DEF = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES"
PEN = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES"
R = {}

# --- 0. the actor: which chain rows say Bria, is CHAIN_ID one value -------------------------
R["bria_chain"] = run(f"""
select CHAIN_ID, CHAIN_NAME, count(*) homes, count(distinct CMS_CERTIFICATION_NUMBER_CCN) ccns,
       min(length(CMS_CERTIFICATION_NUMBER_CCN)) minlen, max(length(CMS_CERTIFICATION_NUMBER_CCN)) maxlen,
       max(PROCESSING_DATE) roster_date
from {NH} where CHAIN_NAME ilike '%bria%' group by 1,2 order by 3 desc""", "bria chain rows")

# TRAP: CHAIN_NAME ilike '%bria%' also catches BRIAR HILL MANAGEMENT (chain 89, 6 Mississippi homes). Pin on CHAIN_ID='88'.
R["bria_homes"] = run(f"""
select CMS_CERTIFICATION_NUMBER_CCN ccn, PROVIDER_NAME, STATE, NUMBER_OF_CERTIFIED_BEDS beds,
       PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS chg_own, SPECIAL_FOCUS_STATUS sff, ABUSE_ICON
from {NH} where CHAIN_ID = '88' order by 1""", "bria homes")

# --- 1. ID trap: is CCN a key on both sides -------------------------------------------------
R["ccn_shape"] = run(f"""
select 'nh411' t, count(*) n, count(distinct CMS_CERTIFICATION_NUMBER_CCN) d, min(CMS_CERTIFICATION_NUMBER_CCN) lo, max(CMS_CERTIFICATION_NUMBER_CCN) hi from {NH}
union all select 'deficiencies', count(*), count(distinct CMS_CERTIFICATION_NUMBER_CCN), min(CMS_CERTIFICATION_NUMBER_CCN), max(CMS_CERTIFICATION_NUMBER_CCN) from {DEF}
union all select 'penalties', count(*), count(distinct CMS_CERTIFICATION_NUMBER_CCN), min(CMS_CERTIFICATION_NUMBER_CCN), max(CMS_CERTIFICATION_NUMBER_CCN) from {PEN}""", "ccn shape")

R["date_ranges"] = run(f"""
select 'deficiencies' t, min(SURVEY_DATE) lo, max(SURVEY_DATE) hi, count(*) n, count(SURVEY_DATE) dated from {DEF}
union all select 'penalties', min(PENALTY_DATE), max(PENALTY_DATE), count(*), count(PENALTY_DATE) from {PEN}""", "date ranges")

R["sev_codes"] = run(f"""
select SCOPE_SEVERITY_CODE, count(*) n from {DEF} group by 1 order by 1""", "severity letters in file")

R["pen_types"] = run(f"""
select PENALTY_TYPE, count(*) n, count(FINE_AMOUNT) with_amt, sum(FINE_AMOUNT) usd from {PEN} group by 1 order by 2 desc""", "penalty types")

# --- 2. the rolling window: when does each home's retained record start ----------------------
R["window_start"] = run(f"""
with h as (select CMS_CERTIFICATION_NUMBER_CCN ccn, min(SURVEY_DATE) first_dt from {DEF} group by 1),
b as (select CMS_CERTIFICATION_NUMBER_CCN ccn from {NH} where CHAIN_ID = '88')
select case when b.ccn is not null then 'bria' else 'national' end grp,
       year(first_dt) first_year, count(*) homes
from h left join b using(ccn) group by 1,2 order by 1,2""", "earliest retained survey per home")

# --- 3. monthly deficiency rate per home, Bria vs national -----------------------------------
# denominator = homes whose retained record had started by that month (rolling-window fix), same rule both sides
R["monthly"] = run(f"""
with b as (select CMS_CERTIFICATION_NUMBER_CCN ccn from {NH} where CHAIN_ID = '88'),
h as (select CMS_CERTIFICATION_NUMBER_CCN ccn, min(SURVEY_DATE) first_dt from {DEF} group by 1),
m as (select dateadd(month, seq4(), '2023-01-01'::date) mo from table(generator(rowcount=>36))),
den as (select m.mo, iff(b.ccn is not null,'bria','national') grp, count(*) homes
        from m join h on h.first_dt < dateadd(month,1,m.mo) left join b on b.ccn=h.ccn group by 1,2),
num as (select date_trunc(month, SURVEY_DATE) mo, iff(b.ccn is not null,'bria','national') grp,
               count(*) defs,
               sum(iff(SCOPE_SEVERITY_CODE in ('G','H','I','J','K','L'),1,0)) gplus,
               sum(iff(SCOPE_SEVERITY_CODE in ('J','K','L'),1,0)) ij,
               sum(iff(COMPLAINT_DEFICIENCY='Y',1,0)) complaint,
               count(distinct CMS_CERTIFICATION_NUMBER_CCN) homes_cited
        from {DEF} d left join b on b.ccn=d.CMS_CERTIFICATION_NUMBER_CCN
        where SURVEY_DATE >= '2023-01-01' and SURVEY_DATE < '2026-01-01' group by 1,2)
select den.mo, den.grp, den.homes, coalesce(defs,0) defs, coalesce(gplus,0) gplus, coalesce(ij,0) ij,
       coalesce(complaint,0) complaint, coalesce(homes_cited,0) homes_cited
from den left join num on num.mo=den.mo and num.grp=den.grp order by 2,1""", "monthly defs by group")

# --- 4. severity letters by year, Bria vs national -------------------------------------------
R["sev_year"] = run(f"""
with b as (select CMS_CERTIFICATION_NUMBER_CCN ccn from {NH} where CHAIN_ID = '88')
select year(SURVEY_DATE) yr, iff(b.ccn is not null,'bria','national') grp, SCOPE_SEVERITY_CODE sev, count(*) n
from {DEF} d left join b on b.ccn=d.CMS_CERTIFICATION_NUMBER_CCN
where SURVEY_DATE >= '2023-01-01' and SURVEY_DATE < '2026-01-01' and SCOPE_SEVERITY_CODE is not null
group by 1,2,3 order by 2,1,3""", "severity letters by year")

# --- 5. rebuild the first-pass number a different way: per-home shares, then the chain --------
# first pass counted chain-level G+/total. Here: each Bria home's own G+ share, then the mean and the
# pooled share from the per-home rows. Same answer = reproduces.
R["rebuild_home"] = run(f"""
with b as (select CMS_CERTIFICATION_NUMBER_CCN ccn, PROVIDER_NAME nm from {NH} where CHAIN_ID = '88')
select year(SURVEY_DATE) yr, b.ccn, b.nm, count(*) defs,
       sum(iff(SCOPE_SEVERITY_CODE >= 'G' and SCOPE_SEVERITY_CODE <= 'L',1,0)) gplus,
       min(SURVEY_DATE) first_dt, count(distinct SURVEY_DATE) surveys
from {DEF} d join b on b.ccn=d.CMS_CERTIFICATION_NUMBER_CCN
where SURVEY_DATE >= '2023-01-01' and SURVEY_DATE < '2026-01-01' group by 1,2,3 order by 2,1""", "per-home rebuild")

# --- 6. fines: monthly dollars and count per home, Bria vs national --------------------------
R["fines_monthly"] = run(f"""
with b as (select CMS_CERTIFICATION_NUMBER_CCN ccn from {NH} where CHAIN_ID = '88'),
h as (select CMS_CERTIFICATION_NUMBER_CCN ccn, min(SURVEY_DATE) first_dt from {DEF} group by 1),
m as (select dateadd(month, seq4(), '2023-01-01'::date) mo from table(generator(rowcount=>36))),
den as (select m.mo, iff(b.ccn is not null,'bria','national') grp, count(*) homes
        from m join h on h.first_dt < dateadd(month,1,m.mo) left join b on b.ccn=h.ccn group by 1,2),
num as (select date_trunc(month, PENALTY_DATE) mo, iff(b.ccn is not null,'bria','national') grp,
               count(*) penalties, sum(iff(PENALTY_TYPE ilike 'fine%',1,0)) fines, sum(FINE_AMOUNT) usd,
               count(distinct p.CMS_CERTIFICATION_NUMBER_CCN) homes_fined
        from {PEN} p left join b on b.ccn=p.CMS_CERTIFICATION_NUMBER_CCN
        where PENALTY_DATE >= '2023-01-01' and PENALTY_DATE < '2026-01-01' group by 1,2)
select den.mo, den.grp, den.homes, coalesce(penalties,0) penalties, coalesce(fines,0) fines,
       coalesce(usd,0) usd, coalesce(homes_fined,0) homes_fined
from den left join num on num.mo=den.mo and num.grp=den.grp order by 2,1""", "monthly fines by group")

# --- 7. the first-pass fine totals, straight -------------------------------------------------
R["fines_period"] = run(f"""
with b as (select CMS_CERTIFICATION_NUMBER_CCN ccn from {NH} where CHAIN_ID = '88')
select iff(b.ccn is not null,'bria','national') grp,
       case when PENALTY_DATE < '2024-01-01' then '2023 H2' else to_char(year(PENALTY_DATE)) end period,
       count(*) penalties, sum(FINE_AMOUNT) usd, count(distinct p.CMS_CERTIFICATION_NUMBER_CCN) homes_hit
from {PEN} p left join b on b.ccn=p.CMS_CERTIFICATION_NUMBER_CCN
where PENALTY_DATE >= '2023-01-01' and PENALTY_DATE < '2026-01-01' group by 1,2 order by 1,2""", "fines by period")

# --- 8. penalties by home: does the money land on the homes whose G+ climbed ----------------
R["home_fines"] = run(f"""
with b as (select CMS_CERTIFICATION_NUMBER_CCN ccn, PROVIDER_NAME nm from {NH} where CHAIN_ID = '88')
select b.ccn, b.nm, year(PENALTY_DATE) yr, count(*) penalties, sum(FINE_AMOUNT) usd
from {PEN} p join b on b.ccn=p.CMS_CERTIFICATION_NUMBER_CCN
where PENALTY_DATE >= '2023-01-01' and PENALTY_DATE < '2026-01-01' group by 1,2,3 order by 1,3""", "fines per Bria home per year")

# --- 9. trap check: the complaint flag reads 0 for every month before 2023-06 -------------------
R["complaint_flag"] = run(f"""
select date_trunc(quarter, SURVEY_DATE) q, COMPLAINT_DEFICIENCY, STANDARD_DEFICIENCY, count(*) n
from {DEF} where SURVEY_DATE >= '2022-07-01' and SURVEY_DATE < '2024-01-01' group by 1,2,3 order by 1,2,3""", "complaint flag by quarter")

json.dump(R, open(f"{D}/results.json", "w"), default=str, indent=1)
print("saved", {k: len(v) for k, v in R.items()})
