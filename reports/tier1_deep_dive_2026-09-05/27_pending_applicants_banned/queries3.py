"""Hunch 27, round 3: state base rate for the pending list via NPPES practice state, and the 9 hits' NPPES state/deactivation."""
import json, os
from _shared.q import run, open_log
HERE = os.path.dirname(os.path.abspath(__file__))
open_log(os.path.join(HERE, "queries.log"))
M = "LIBRARY_MARTS.HEALTH"
NPPES = f"{M}.HEALTH__FED_CMS_NPPES"
PHY = f"{M}.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS"
NON = f"{M}.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS"
HITS = "('1861424954','1366450280','1225139496','1336103548','1083786099','1689740714','1386606325','1639294796','1164538013')"
R = {}
R["nppes_cols2"] = run("""
select column_name from LIBRARY_MARTS.information_schema.columns
where table_schema='HEALTH' and table_name='HEALTH__FED_CMS_NPPES' and (column_name ilike '%DEACTIV%' or column_name ilike '%ENTITY%' or column_name ilike '%TAXONOMY_CODE_1' or column_name ilike '%CREDENTIAL%') order by ordinal_position
""", "nppes_cols2")
print(R["nppes_cols2"])
R["pending_state"] = run(f"""
with p as (select NPI from {PHY} union select NPI from {NON})
select n.PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME st, count(*) n,
       round(100*count(*)/sum(count(*)) over (),1) pct
from p join {NPPES} n on n.NPI=p.NPI group by 1 order by n desc limit 12
""", "pending_state")
R["pending_nppes_cov"] = run(f"""
with p as (select NPI from {PHY} union select NPI from {NON})
select count(*) n_pending, sum(iff(n.NPI is not null,1,0)) n_in_nppes from p left join {NPPES} n on n.NPI=p.NPI
""", "pending_nppes_cov")
R["hits_nppes"] = run(f"""
select NPI, PROVIDER_LAST_NAME_LEGAL_NAME, PROVIDER_FIRST_NAME, PROVIDER_CREDENTIAL_TEXT,
       PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME st, HEALTHCARE_PROVIDER_TAXONOMY_CODE_1 tax,
       NPI_DEACTIVATION_DATE, NPI_REACTIVATION_DATE
from {NPPES} where NPI in {HITS} order by NPI
""", "hits_nppes")
with open(os.path.join(HERE, "results3.json"), "w") as f:
    json.dump(R, f, indent=1, default=str)
print(json.dumps(R, indent=1, default=str))
