"""Hunch 27, round 2: date the snapshots, find the reinstatement data (mart says 0 reinstated on 83,747 rows),
check LANDING for the sentinel and extra columns, and pull base rates for the charts."""
import json, os
from _shared.q import run, open_log
HERE = os.path.dirname(os.path.abspath(__file__))
open_log(os.path.join(HERE, "queries.log"))
M = "LIBRARY_MARTS.HEALTH"
LEIE = f"{M}.HEALTH__FED_HHS_OIG_LEIE"
R = {}

# Where are the landing tables?
R["landing_names"] = run("""
select table_schema, table_name, row_count from LIBRARY_RAW.information_schema.tables
where (table_name ilike '%LEIE%' or table_name ilike '%PENDING_INITIAL%' or table_name ilike '%REINSTAT%')
order by 1,2
""", "landing_names")
print(json.dumps(R["landing_names"], indent=1, default=str))

L = "LIBRARY_RAW.LANDING"
# Landing columns for all three (audit columns may be unprefixed on LEIE - trap 2026-08-31).
for t in ["FED_HHS_OIG_LEIE", "FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS", "FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS"]:
    R[f"cols_{t}"] = run(f"select column_name from LIBRARY_RAW.information_schema.columns where table_schema='LANDING' and table_name='{t}' order by ordinal_position", f"cols_{t}")

# LEIE landing: sentinel count, REINDATE fill, snapshot date, and why the mart is 95 rows short.
R["leie_landing_shape"] = run(f"""
select count(*) n_rows,
       sum(iff(NPI='0000000000',1,0)) n_sentinel,
       sum(iff(nullif(trim(NPI),'') is null,1,0)) n_blank,
       count(distinct iff(NPI<>'0000000000' and nullif(trim(NPI),'') is not null, NPI, null)) n_real_distinct,
       sum(iff(nullif(trim(REINDATE),'') is not null and REINDATE<>'00000000',1,0)) n_reindate,
       min(REINDATE) min_reindate, max(REINDATE) max_reindate,
       min(EXCLDATE) min_excl, max(EXCLDATE) max_excl,
       max(INGESTED_AT) ingested_at
from {L}.FED_HHS_OIG_LEIE
""", "leie_landing_shape")

R["leie_reindate_sample"] = run(f"select REINDATE, count(*) n from {L}.FED_HHS_OIG_LEIE group by 1 order by n desc limit 5", "leie_reindate_sample")

# Do the 9 NPIs carry any REINDATE in landing?
R["hits_landing"] = run(f"""
select NPI, LASTNAME, FIRSTNAME, EXCLTYPE, EXCLDATE, REINDATE, WAIVERDATE, STATE, CITY
from {L}.FED_HHS_OIG_LEIE
where NPI in ('1861424954','1366450280','1225139496','1336103548','1083786099','1689740714','1386606325','1639294796','1164538013')
order by EXCLDATE
""", "hits_landing")

# Pending snapshot date: any audit column in landing?
R["pending_landing_meta"] = run(f"""
select 'phy' f, count(*) n, min(_INGESTED_AT) mn, max(_INGESTED_AT) mx from {L}.FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS
union all
select 'non', count(*), min(_INGESTED_AT), max(_INGESTED_AT) from {L}.FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS
""", "pending_landing_meta")

# Base rates over real-NPI LEIE rows: mandatory (1128a*) vs permissive (1128b*), and state share.
R["leie_mand_perm"] = run(f"""
select iff(EXCLUSION_TYPE like '1128a%' or EXCLUSION_TYPE like '1128A%','mandatory (1128a)',
       iff(EXCLUSION_TYPE like '1128b%','permissive (1128b)','other')) grp, count(*) n
from {LEIE} where NPI<>'0000000000' and trim(NPI)<>'' group by 1 order by n desc
""", "leie_mand_perm")

R["leie_state"] = run(f"""
select STATE, count(*) n, round(100*count(*)/sum(count(*)) over (),1) pct
from {LEIE} where NPI<>'0000000000' and trim(NPI)<>'' group by 1 order by n desc limit 10
""", "leie_state")

# Pending-list base rate by state is impossible (no state column) - confirm no other table gives it cheaply:
# NPPES has state for every NPI. Pending NPIs by NPPES practice state, top 10.
R["nppes_cols"] = run("""
select column_name from LIBRARY_MARTS.information_schema.columns
where table_schema='HEALTH' and table_name='HEALTH__FED_CMS_NPPES' and (column_name ilike '%STATE%' or column_name='NPI') order by ordinal_position
""", "nppes_cols")

with open(os.path.join(HERE, "results2.json"), "w") as f:
    json.dump(R, f, indent=1, default=str)
print(json.dumps({k:v for k,v in R.items() if k!='landing_names'}, indent=1, default=str))
