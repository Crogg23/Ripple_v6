"""Hunch 27: are any pending Medicare applicants already on the OIG exclusion list (LEIE)?
Run from repo root: PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 reports/tier1_deep_dive_2026-09-05/27_pending_applicants_banned/queries.py
SELECT only. Writes results.json next to this file."""
import json, os
from _shared.q import run, open_log

HERE = os.path.dirname(os.path.abspath(__file__))
open_log(os.path.join(HERE, "queries.log"))
M = "LIBRARY_MARTS.HEALTH"
PHY = f"{M}.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS"
NON = f"{M}.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS"
LEIE = f"{M}.HEALTH__FED_HHS_OIG_LEIE"
AFF = f"{M}.HEALTH__FED_CMS_FACILITY_AFFILIATION"
R = {}

# Deduped pending list, both files, with a flag for which file(s) an NPI sits in.
PENDING = f"""
with u as (
  select NPI, LAST_NAME, FIRST_NAME, 'physician' as kind from {PHY}
  union all
  select NPI, LAST_NAME, FIRST_NAME, 'non_physician' as kind from {NON}
)
select NPI, min(LAST_NAME) LAST_NAME, min(FIRST_NAME) FIRST_NAME,
       listagg(distinct kind, '+') within group (order by kind) kind,
       count(*) n_rows
from u where NPI is not null and length(trim(NPI)) = 10 and NPI <> '0000000000'
group by NPI
"""

# 1. Shape of the pending list: rows, distinct NPIs, duplicates, NPI sanity.
R["pending_shape"] = run(f"""
with u as (
  select NPI, 'physician' kind from {PHY} union all select NPI, 'non_physician' from {NON})
select kind, count(*) n_rows, count(distinct NPI) n_npi,
       count(*) - count(distinct NPI) n_dupe_rows,
       sum(iff(NPI is null or trim(NPI)='' ,1,0)) n_blank,
       sum(iff(length(trim(NPI))<>10 or not regexp_like(trim(NPI),'^[0-9]{{10}}$'),1,0)) n_malformed
from u group by kind order by kind
""", "pending_shape")

R["pending_total"] = run(f"""
with u as (select NPI from {PHY} union all select NPI from {NON})
select count(*) n_rows, count(distinct NPI) n_npi, count(*)-count(distinct NPI) n_dupe_rows,
       sum(iff(NPI='0000000000',1,0)) n_sentinel
from u where NPI is not null and trim(NPI)<>''
""", "pending_total")

# Which NPIs repeat, and are they same person / same file or cross-file?
R["pending_dupes"] = run(f"""
with u as (
  select NPI, LAST_NAME, FIRST_NAME, 'physician' kind from {PHY} union all
  select NPI, LAST_NAME, FIRST_NAME, 'non_physician' from {NON})
select NPI, count(*) n_rows, count(distinct kind) n_files, count(distinct LAST_NAME||'|'||FIRST_NAME) n_names,
       listagg(distinct kind, '+') within group (order by kind) kinds
from u group by NPI having count(*)>1 order by n_rows desc, NPI
""", "pending_dupes")

# 2. LEIE shape: sentinel NPI, real NPI count, reinstated.
R["leie_shape"] = run(f"""
select count(*) n_rows,
       sum(iff(NPI='0000000000',1,0)) n_sentinel,
       sum(iff(NPI is null or trim(NPI)='',1,0)) n_blank,
       sum(iff(NPI_IS_REAL,1,0)) n_flag_real,
       count(distinct iff(NPI<>'0000000000' and trim(NPI)<>'', NPI, null)) n_real_distinct,
       sum(iff(WAS_REINSTATED,1,0)) n_reinstated,
       sum(iff(nullif(trim(REINSTATEMENT_DATE),'') is not null,1,0)) n_reinst_date
from {LEIE}
""", "leie_shape")

# 3. The hit list: deduped pending NPIs that sit in LEIE on a real NPI.
R["hits"] = run(f"""
with p as ({PENDING})
select p.NPI, p.LAST_NAME p_last, p.FIRST_NAME p_first, p.kind, p.n_rows pending_rows,
       l.LAST_NAME l_last, l.FIRST_NAME l_first, l.BUSINESS_NAME, l.GENERAL_CATEGORY, l.SPECIALTY,
       l.EXCLUSION_TYPE, l.EXCLUSION_DATE, nullif(trim(l.REINSTATEMENT_DATE),'') REINSTATEMENT_DATE,
       l.WAS_REINSTATED, l.HAS_WAIVER, l.IS_ENTITY_NOT_INDIVIDUAL, l.STATE, l.CITY, l.EXCLUSION_SK
from p join {LEIE} l on l.NPI = p.NPI
where l.NPI <> '0000000000'
order by l.EXCLUSION_DATE
""", "hits")

# 4. Rebuild the count a different way: EXISTS per file, no union, no dedupe step.
R["hits_rebuild"] = run(f"""
select 'physician' kind, count(distinct p.NPI) n_npi from {PHY} p
 where exists (select 1 from {LEIE} l where l.NPI=p.NPI and l.NPI<>'0000000000')
union all
select 'non_physician', count(distinct p.NPI) from {NON} p
 where exists (select 1 from {LEIE} l where l.NPI=p.NPI and l.NPI<>'0000000000')
union all
select 'either', count(distinct NPI) from (select NPI from {PHY} union select NPI from {NON}) p
 where exists (select 1 from {LEIE} l where l.NPI=p.NPI and l.NPI<>'0000000000')
""", "hits_rebuild")

# Row-level count (what a naive join returns) vs NPI-level.
R["hits_rowlevel"] = run(f"""
with u as (select NPI from {PHY} union all select NPI from {NON})
select count(*) n_join_rows, count(distinct u.NPI) n_npi, count(distinct l.EXCLUSION_SK) n_exclusions
from u join {LEIE} l on l.NPI=u.NPI and l.NPI<>'0000000000'
""", "hits_rowlevel")

# 5. Name check: does the LEIE name match the pending name? (guards against NPI typo / reuse)
R["name_check"] = run(f"""
with p as ({PENDING})
select p.NPI,
       upper(trim(p.LAST_NAME)) = upper(trim(l.LAST_NAME)) last_match,
       upper(trim(p.FIRST_NAME)) = upper(trim(l.FIRST_NAME)) first_match,
       left(upper(trim(p.FIRST_NAME)),3) = left(upper(trim(l.FIRST_NAME)),3) first3_match
from p join {LEIE} l on l.NPI=p.NPI where l.NPI<>'0000000000'
""", "name_check")

# 6. Exclusion-type legend for the codes that show up.
R["type_legend"] = run(f"""
select EXCLUSION_TYPE, count(*) n, sum(iff(WAS_REINSTATED,1,0)) n_reinst
from {LEIE} group by 1 order by n desc
""", "type_legend")

# 7. Base rates: how often is a random real-NPI LEIE row reinstated / by type, to size the 9.
R["leie_type_share"] = run(f"""
select EXCLUSION_TYPE, count(*) n
from {LEIE} where NPI<>'0000000000' and trim(NPI)<>'' group by 1 order by n desc limit 12
""", "leie_type_share")

# 8. Facility affiliation for the hits.
R["affil"] = run(f"""
with p as ({PENDING}),
h as (select distinct p.NPI from p join {LEIE} l on l.NPI=p.NPI where l.NPI<>'0000000000')
select h.NPI, a.FACILITY_TYPE, a.CCN, a.PROVIDER_LAST_NAME, a.PROVIDER_FIRST_NAME, a.IND_PAC_ID
from h left join {AFF} a on a.NPI=h.NPI
order by h.NPI, a.FACILITY_TYPE, a.CCN
""", "affil")

# Base rate: what share of all pending NPIs have any facility affiliation?
R["affil_base"] = run(f"""
with p as ({PENDING})
select count(*) n_pending, sum(iff(exists(select 1 from {AFF} a where a.NPI=p.NPI),1,0)) n_with_affil
from p
""", "affil_base")

# 9. Exclusion year histogram of the 9 vs LEIE overall (real-NPI rows), for the timeline chart.
R["leie_year"] = run(f"""
select year(EXCLUSION_DATE) yr, count(*) n from {LEIE}
where NPI<>'0000000000' and trim(NPI)<>'' and EXCLUSION_DATE is not null group by 1 order by 1
""", "leie_year")

# 10. Do the 9 NPIs appear with more than one exclusion row?
R["hits_multi"] = run(f"""
with p as ({PENDING})
select p.NPI, count(*) n_leie_rows from p join {LEIE} l on l.NPI=p.NPI and l.NPI<>'0000000000'
group by 1 having count(*)>1
""", "hits_multi")

# 11. Sanity on the affiliation table's NPI as an id.
R["aff_npi"] = run(f"select count(*) n, count(distinct NPI) n_npi, sum(iff(NPI='0000000000',1,0)) n_sent from {AFF}", "aff_npi")

with open(os.path.join(HERE, "results.json"), "w") as f:
    json.dump(R, f, indent=1, default=str)
print(json.dumps(R, indent=1, default=str))
