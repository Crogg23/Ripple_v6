select table_schema, table_name, row_count from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
where (table_name ilike '%FEC%' ) order by 2
