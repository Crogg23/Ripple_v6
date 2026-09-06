from _shared.q import run, open_log
open_log("reports/tier1_deep_dive_2026-09-05/E49_contracts_during_ban/queries.log")
for r in run("""select column_name, data_type from LIBRARY_MARTS.information_schema.columns
 where table_schema='PROCUREMENT' and table_name='PROCUREMENT__FED_SAM_EXCLUSIONS' order by ordinal_position""", "sam_cols"):
    print("SAM", r["COLUMN_NAME"], r["DATA_TYPE"])
for r in run("""select column_name from LIBRARY_RAW.information_schema.columns
 where table_schema='LANDING' and table_name='FED_USASPENDING_CONTRACTS_FULL_R2'
 and (lower(column_name) like '%uei%' or lower(column_name) like '%duns%' or lower(column_name) like '%date%'
  or lower(column_name) like '%agency%' or lower(column_name) like '%obligat%' or lower(column_name) like '%award_id%'
  or lower(column_name) like '%recipient_name%' or lower(column_name) like '%amount%') order by ordinal_position""", "usa_cols"):
    print("USA", r["COLUMN_NAME"])
print(run("select count(*) n from LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS", "sam_n"))
print(run("select * from LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS limit 3", "sam_sample"))
