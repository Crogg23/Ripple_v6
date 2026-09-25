select listagg(column_name, ',') within group (order by ordinal_position) cols from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS where table_schema='HEALTH' and table_name='HEALTH__FED_CMS_HCRIS'
