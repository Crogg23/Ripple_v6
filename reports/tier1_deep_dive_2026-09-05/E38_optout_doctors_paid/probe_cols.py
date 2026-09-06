from _shared.q import run, open_log
open_log("reports/tier1_deep_dive_2026-09-05/E38_optout_doctors_paid/queries.log")
for t in ["HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS","HEALTH__FED_CMS_OPEN_PAYMENTS","HEALTH__FED_CMS_OPEN_PAYMENTS_2023"]:
    rows = run(f"select column_name, data_type from LIBRARY_MARTS.information_schema.columns where table_schema='HEALTH' and table_name='{t}' order by ordinal_position", f"cols {t}")
    print(t, len(rows)); print(", ".join(f"{r['COLUMN_NAME']}:{r['DATA_TYPE']}" for r in rows))
rows = run("select table_name, row_count from LIBRARY_MARTS.information_schema.tables where table_schema='HEALTH' and (table_name like '%OPEN_PAYMENTS%' or table_name like '%OPT_OUT%')", "tables")
for r in rows: print(r)
