-- columns of the three tables touched, plus table metadata (row count, last altered)
select 'col' k, table_schema||'.'||table_name t, listagg(column_name||':'||left(data_type,4), ', ') within group (order by ordinal_position) v
from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
where table_name in ('HEALTH__FED_CMS_HOME_HEALTH','HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS','IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS')
group by 1,2
union all
select 'meta', table_schema||'.'||table_name, row_count::text||' rows; created '||created::text||'; altered '||last_altered::text
from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
where table_name in ('HEALTH__FED_CMS_HOME_HEALTH','HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS','IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS','HEALTH__FED_CMS_HOME_HEALTH_OWNERS')
