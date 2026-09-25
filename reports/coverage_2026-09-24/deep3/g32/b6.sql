-- @landing_dera_tables
select table_schema, table_name, row_count, table_type from LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
where table_name ilike '%DERA%' or table_name ilike '%SEC_FIN%' or table_name ilike '%FSDS%' order by 2
