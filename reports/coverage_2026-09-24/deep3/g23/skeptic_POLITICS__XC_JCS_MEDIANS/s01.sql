-- columns of the SCDB table
select column_name, data_type from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
where table_schema='JUSTICE' and table_name='JUSTICE__FED_SCDB' order by ordinal_position
