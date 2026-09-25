-- any column anywhere in the marts or landing named like hospice (money or use by county/provider)
select 'MARTS' db, table_schema, table_name, listagg(column_name, ',') within group (order by column_name) cols
from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS where table_schema not in ('TIMELINE','INFORMATION_SCHEMA') and (column_name ilike '%HOSPC%' or column_name ilike '%HOSPICE%' or column_name ilike '%HOS\\_%')
group by 1,2,3
union all
select 'RAW', table_schema, table_name, listagg(column_name, ',') within group (order by column_name)
from LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS where table_schema='LANDING' and (column_name ilike '%HOSPC%' or column_name ilike '%HOSPICE%' or column_name ilike '%HOS\\_%')
group by 1,2,3
order by 1,2,3
