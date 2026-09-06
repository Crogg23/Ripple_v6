"""E57 probe: what columns and which tables exist. Logs to queries.log."""
import json, sys
from pathlib import Path
from _shared.q import run, open_log
HERE = Path(__file__).resolve().parent
open_log(HERE / "queries.log")

r = run("""
select table_schema, table_name, row_count
from LIBRARY_MARTS.information_schema.tables
where table_name ilike '%OPEN_PAYMENTS%' or table_name ilike '%PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER%'
order by 1,2""", "mart_tables")
print(json.dumps(r, indent=1, default=str))

r = run("""
select table_schema, table_name, row_count
from LIBRARY_RAW.information_schema.tables
where table_name ilike '%OPEN_PAYMENTS%' or table_name ilike '%PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER%'
order by 1,2""", "landing_tables")
print(json.dumps(r, indent=1, default=str))

for t in ("HEALTH__FED_CMS_OPEN_PAYMENTS", "HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER"):
    r = run(f"""
    select column_name, data_type from LIBRARY_MARTS.information_schema.columns
    where table_schema='HEALTH' and table_name='{t}' order by ordinal_position""", f"cols_{t}")
    print(t); print(", ".join(f"{x['COLUMN_NAME']}:{x['DATA_TYPE']}" for x in r))
