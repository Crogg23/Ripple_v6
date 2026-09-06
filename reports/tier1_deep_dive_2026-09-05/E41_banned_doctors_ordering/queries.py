"""E41 — banned doctors still on CMS's Order and Referring list.

Every query the deep dive ran, in order. Run from repo root:
    PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 reports/tier1_deep_dive_2026-09-05/E41_banned_doctors_ordering/queries.py
Logs to queries.log beside this file, dumps results.json for build_story.py.
"""
from __future__ import annotations
import json, datetime, decimal
from pathlib import Path
from _shared.q import run, open_log

HERE = Path(__file__).resolve().parent
open_log(HERE / "queries.log")

L = "LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE"
LL = "LIBRARY_RAW.LANDING.FED_HHS_OIG_LEIE"
O = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING"
OL = "LIBRARY_RAW.LANDING.FED_CMS_ORDER_AND_REFERRING"
N = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES"
D = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER"
LOAD = "2026-08-05"   # ordering file landed (landing _INGESTED_AT, one run, one timestamp)

REAL = "l.npi <> '0000000000' and nullif(trim(l.npi), '') is not null"
R: dict = {}

# --- 1. shape of both tables ------------------------------------------------
R["leie_profile"] = run(f"""
select count(*) n, count(distinct npi) distinct_npi,
       sum(iff(npi = '0000000000', 1, 0)) sentinel_rows,
       sum(iff(nullif(trim(npi), '') is null, 1, 0)) blank_rows,
       sum(iff(npi_is_real, 1, 0)) npi_is_real_rows,
       min(exclusion_date) min_excl, max(exclusion_date) max_excl,
       count(distinct _source_run_id) runs
from {L}""", "leie mart profile")

R["leie_landing"] = run(f"""
select count(*) n, sum(iff(npi = '0000000000', 1, 0)) sentinel_rows,
       min(ingested_at) ingest_epoch_micros, max(excldate) max_excl,
       count(distinct source_run_id) runs
from {LL}""", "leie landing profile (INGESTED_AT is epoch micros)")

R["leie_reinstate"] = run(f"select reindate, count(*) n from {LL} group by 1 order by 2 desc limit 5", "leie REINDATE values")
R["leie_waiver"] = run(f"""
select nullif(trim(waiverdate), '') waiverdate, nullif(trim(wvrstate), '') wvrstate, count(*) n
from {LL} group by 1, 2 order by 3 desc limit 6""", "leie waiver values")

R["order_profile"] = run(f"""
select count(*) n, count(distinct npi) distinct_npi,
       sum(iff(nullif(trim(npi), '') is null, 1, 0)) blank,
       min(length(npi)) len_min, max(length(npi)) len_max
from {O}""", "ordering mart profile")
R["order_landing"] = run(f"""
select min(_ingested_at) ingest_min, max(_ingested_at) ingest_max, count(distinct _source_run_id) runs
from {OL}""", "ordering landing ingest")
R["order_categories"] = run(f"""
select sum(iff(partb = 'Y', 1, 0)) partb, sum(iff(dme = 'Y', 1, 0)) dme, sum(iff(hha = 'Y', 1, 0)) hha,
       sum(iff(pmd = 'Y', 1, 0)) pmd, sum(iff(hospice = 'Y', 1, 0)) hospice, count(*) n
from {O}""", "ordering file category totals")

# --- 2. the join, two ways ---------------------------------------------------
R["join_mart"] = run(f"""
select count(*) rows_, count(distinct l.npi) leie_npis, count(distinct o.npi) order_npis
from {L} l join {O} o on o.npi = l.npi where {REAL}""", "join on marts")
R["join_landing"] = run(f"""
select count(*) rows_, count(distinct l.npi) leie_npis
from {LL} l where l.npi <> '0000000000' and exists (select 1 from {OL} o where o.npi = l.npi)""", "join on landing (second way)")

R["buckets"] = run(f"""
select case when l.exclusion_date < '2025-01-01' then 'a. excluded before 2025'
            when l.exclusion_date < '{LOAD}' then 'b. excluded 2025-01-01 to 2026-08-04'
            else 'c. excluded on/after load {LOAD}' end bucket,
       count(*) n, min(l.exclusion_date) min_excl, max(l.exclusion_date) max_excl
from {L} l join {O} o on o.npi = l.npi where {REAL} group by 1 order by 1""", "matches by date bucket vs load date")

R["buckets_landing"] = run(f"""
select sum(iff(l.excldate < '20250101', 1, 0)) before_2025,
       sum(iff(l.excldate < '20260805', 1, 0)) before_load, count(*) total
from {LL} l where l.npi <> '0000000000' and exists (select 1 from {OL} o where o.npi = l.npi)""", "7 and 26 rebuilt on landing text dates")

# --- 3. the 38, one row each --------------------------------------------------
R["matches"] = run(f"""
select l.npi, l.last_name, l.first_name, l.general_category, l.specialty, l.exclusion_type, l.exclusion_date,
       l.state leie_state, ll.waiverdate, nullif(trim(ll.wvrstate), '') wvrstate, ll.reindate,
       o.last_name order_last_name, o.partb, o.dme, o.hha, o.pmd, o.hospice,
       n.provider_last_name_legal_name nppes_last_name, n.provider_credential_text credential,
       n.provider_business_practice_location_address_state_name nppes_state,
       n.npi_deactivation_date deact_date, n.npi_reactivation_date react_date, n.last_update_date nppes_updated
from {L} l
join {O} o on o.npi = l.npi
left join {LL} ll on ll.npi = l.npi and ll.excldate = to_char(l.exclusion_date, 'YYYYMMDD')
left join {N} n on n.npi = l.npi
where {REAL} order by l.exclusion_date, l.last_name""", "the 38 with waiver, NPPES identity, categories")

# --- 4. rate by exclusion year, with denominators ---------------------------
R["by_year"] = run(f"""
with x as (select npi, min(exclusion_date) first_excl from {L} l where {REAL} group by 1)
select year(x.first_excl) y, count(*) excluded_npis,
       sum(iff(n.npi is not null, 1, 0)) in_nppes,
       sum(iff(n.npi is not null and nullif(trim(n.npi_deactivation_date), '') is null, 1, 0)) nppes_active,
       sum(iff(o.npi is not null, 1, 0)) in_ordering
from x left join {O} o on o.npi = x.npi left join {N} n on n.npi = x.npi
where year(x.first_excl) >= 2010 group by 1 order by 1""", "match rate by first exclusion year")

R["by_month_2026"] = run(f"""
select l.exclusion_date, count(distinct l.npi) excluded_npis, count(distinct o.npi) in_ordering
from {L} l left join {O} o on o.npi = l.npi
where {REAL} and l.exclusion_date >= '2025-07-01' group by 1 order by 1""", "2025-07 onward by exclusion date")

# --- 5. exclusion type and state mix ----------------------------------------
R["type_mix"] = run(f"""
select l.exclusion_type, count(distinct l.npi) all_real_npis, count(distinct o.npi) in_ordering
from {L} l left join {O} o on o.npi = l.npi where {REAL} group by 1 order by 2 desc""", "exclusion type: list vs matches")
R["state_mix"] = run(f"""
select l.state, count(distinct l.npi) all_real_npis, count(distinct o.npi) in_ordering
from {L} l left join {O} o on o.npi = l.npi where {REAL} group by 1 having count(distinct o.npi) > 0 order by 3 desc, 2 desc""", "state: list vs matches")

# --- 6. did they order? DME-by-referrer (one data year, no year column) -----
R["dme_refer"] = run(f"""
select l.npi, l.last_name, l.exclusion_date, d.rfrg_prvdr_state_abrvtn dme_state,
       d.tot_suplr_srvcs srvcs, d.suplr_mdcr_pymt_amt paid
from {L} l join {O} o on o.npi = l.npi join {D} d on d.rfrg_npi = l.npi
where {REAL} order by l.exclusion_date""", "the 38 as paid DME referrers")
R["dme_size"] = run(f"select count(*) n, count(distinct rfrg_npi) d from {D}", "DME referrer file size")


def _j(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    if isinstance(o, decimal.Decimal):
        return float(o)
    return str(o)

(HERE / "results.json").write_text(json.dumps(R, default=_j, indent=1))
print("wrote", HERE / "results.json")
