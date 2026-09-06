from _shared.q import run, open_log
open_log("reports/tier1_deep_dive_2026-09-05/E42_pharma_money_dead_npis/queries.log")
for t in ["HEALTH__FED_CMS_OPEN_PAYMENTS","HEALTH__FED_CMS_NPPES","HEALTH__FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT"]:
    rows = run(f"select column_name, data_type from LIBRARY_MARTS.information_schema.columns where table_schema='HEALTH' and table_name='{t}' order by ordinal_position", f"cols {t}")
    print(t, len(rows)); print(", ".join(f"{r['COLUMN_NAME']}:{r['DATA_TYPE']}" for r in rows))
