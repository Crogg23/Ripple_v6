"""Hunch 27, round 4 (skeptic fix): state base rates for the 7 charted states with NO limit, so no state defaults to zero."""
import json, os
from _shared.q import run, open_log
HERE = os.path.dirname(os.path.abspath(__file__))
open_log(os.path.join(HERE, "queries.log"))
M = "LIBRARY_MARTS.HEALTH"
STATES = "('FL','NC','NV','PA','CA','TX','NY')"
R = {}
R["leie_state7"] = run(f"""
with b as (select STATE, count(*) n, round(100*count(*)/sum(count(*)) over (),2) pct
           from {M}.HEALTH__FED_HHS_OIG_LEIE where NPI<>'0000000000' and trim(NPI)<>'' group by 1)
select STATE, n, pct from b where STATE in {STATES} order by n desc""", "leie_state7")
R["pending_state7"] = run(f"""
with p as (select NPI from {M}.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS
           union select NPI from {M}.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS),
b as (select n.PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME st, count(*) n,
             round(100*count(*)/sum(count(*)) over (),2) pct
      from p join {M}.HEALTH__FED_CMS_NPPES n on n.NPI=p.NPI group by 1)
select st, n, pct from b where st in {STATES} order by n desc""", "pending_state7")
with open(os.path.join(HERE, "results4.json"), "w") as f: json.dump(R, f, indent=1, default=str)
print(json.dumps(R, indent=1, default=str))
