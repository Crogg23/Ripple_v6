import json
from _shared import q
D="reports/tier1_deep_dive_2026-09-05/E68_nonprofit_charity_care"
q.open_log(f"{D}/queries.log")
r=q.run("""select column_name, data_type from LIBRARY_MARTS.information_schema.columns
where table_schema='HEALTH' and table_name='HEALTH__FED_CMS_HCRIS' order by ordinal_position""","hcris columns")
print([ (x['COLUMN_NAME'],x['DATA_TYPE']) for x in r])
r=q.run("""select table_catalog, table_schema, table_name, row_count from LIBRARY_MARTS.information_schema.tables where table_name ilike '%IRS%BMF%'
union all select table_catalog, table_schema, table_name, row_count from LIBRARY_RAW.information_schema.tables where table_name ilike '%IRS%BMF%'""","bmf tables")
print(r)
r=q.run("""select TYPE_OF_CONTROL, count(*) n from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS group by 1 order by 1""","control codes")
print(r)
