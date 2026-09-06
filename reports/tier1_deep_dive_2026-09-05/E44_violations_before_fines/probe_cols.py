from _shared.q import run, open_log
open_log("reports/tier1_deep_dive_2026-09-05/E44_violations_before_fines/queries.log")
for t in ["HEALTH__FED_NURSINGHOME411","HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES","HEALTH__FED_CMS_NURSING_HOME_PENALTIES"]:
    rows = run(f"select column_name, data_type from LIBRARY_MARTS.information_schema.columns where table_schema='HEALTH' and table_name='{t}' order by ordinal_position", f"cols {t}")
    print(t, len(rows)); print(", ".join(f"{r['COLUMN_NAME']}:{r['DATA_TYPE']}" for r in rows))
