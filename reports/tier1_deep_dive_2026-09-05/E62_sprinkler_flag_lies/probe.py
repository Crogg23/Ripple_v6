from _shared.q import run, open_log
open_log("reports/tier1_deep_dive_2026-09-05/E62_sprinkler_flag_lies/queries.log")
r = run("""select table_schema, table_name, row_count from LIBRARY_MARTS.information_schema.tables
 where table_name ilike '%NURSING%' order by 1,2""", "mart tables")
for x in r: print(x)
r = run("""select table_name, row_count from LIBRARY_RAW.information_schema.tables
 where table_schema='LANDING' and table_name ilike '%NURSING%' order by 1""", "landing tables")
for x in r: print(x)
r = run("""select table_schema, table_name, column_name from LIBRARY_RAW.information_schema.columns
 where column_name ilike '%SPRINKLER%' union all
 select table_schema, table_name, column_name from LIBRARY_MARTS.information_schema.columns
 where column_name ilike '%SPRINKLER%'""", "sprinkler cols anywhere")
for x in r: print(x)
for db,sch,t in [("LIBRARY_MARTS","HEALTH","HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES"),("LIBRARY_MARTS","HEALTH","HEALTH__FED_NURSINGHOME411")]:
    r = run(f"select column_name, data_type from {db}.information_schema.columns where table_schema='{sch}' and table_name='{t}' order by ordinal_position", f"cols {t}")
    print(t); print([ (x['COLUMN_NAME'],x['DATA_TYPE']) for x in r])
