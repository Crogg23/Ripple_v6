from _shared.q import run, open_log
open_log("reports/tier1_deep_dive_2026-09-05/30_penalty_then_new_owner/queries.log")
for t in ["HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS","HEALTH__FED_CMS_NURSING_HOME_PENALTIES"]:
    rows = run(f"select column_name, data_type from LIBRARY_MARTS.information_schema.columns where table_schema='HEALTH' and table_name='{t}' order by ordinal_position", f"cols {t}")
    print(t, len(rows)); print(", ".join(f"{r['COLUMN_NAME']}:{r['DATA_TYPE']}" for r in rows))
rows = run("select table_schema, table_name, row_count from LIBRARY_MARTS.information_schema.tables where table_name ilike '%SKILLED_NURSING%' or table_name ilike '%NURSING_HOME_PENALT%' or table_name ilike '%SNF%' or table_name ilike '%CHOW%' or table_name ilike '%OWNER%'", "mart tables like snf/chow/owner")
for r in rows: print(r)
rows = run("select table_schema, table_name, row_count from LIBRARY_RAW.information_schema.tables where table_name ilike '%SKILLED_NURSING%' or table_name ilike '%NURSING_HOME_PENALT%' or table_name ilike '%SNF%' or table_name ilike '%CHOW%' or table_name ilike '%OWNER%'", "raw tables like snf/chow/owner")
for r in rows: print(r)
