-- s01: every column of every ICIS-Air table in the environment schema, to find informal actions, pollutant class, dates
select table_name, listagg(column_name || ':' || data_type, ', ') within group (order by ordinal_position) cols
from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
where table_schema = 'ENVIRONMENT' and table_name ilike '%ICIS_AIR%'
group by 1 order by 1;
