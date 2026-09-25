select 'COL' kind, table_catalog db, table_schema sch, table_name tbl, listagg(distinct column_name, ',') cols
from SNOWFLAKE.ACCOUNT_USAGE.COLUMNS
where deleted is null and (column_name ilike '%HOSPC%' or column_name ilike '%HSPC%' or column_name ilike '%HOSPICE%' or column_name ilike 'HOS\_%' or column_name ilike '%\_HOS\_%' or column_name ilike '%HOSP_CARE%')
group by 1,2,3,4
union all
select 'TBL', table_catalog, table_schema, table_name, row_count::string
from SNOWFLAKE.ACCOUNT_USAGE.TABLES
where deleted is null and (table_name ilike '%HOSPIC%' or table_name ilike '%HCRIS%' or table_name ilike '%COST_REP%' or table_name ilike '%POST_ACUTE%' or table_name ilike '%PAC\_%' or table_name ilike '%\_PAC%' or table_name ilike '%GEO%VAR%' or table_name ilike '%PART_A%' or table_name ilike '%MDCR_SPND%' or table_name ilike '%SPENDING_BY%' or table_name ilike '%HHA%' or table_name ilike '%UTILIZ%' or table_name ilike '%PROVIDER_SUMMARY%')
order by 1,2,3,4
