-- find nursing-home, staffing, cost-report, PPP, OSHA, court and relief tables with row counts
select table_catalog, table_schema, table_name, row_count from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
where table_schema not in ('TIMELINE') and (table_name ilike '%NURSING%' or table_name ilike '%SNF%' or table_name ilike '%PBJ%' or table_name ilike '%COST_REP%' or table_name ilike '%HCRIS%' or table_name ilike '%STAFFING%' or table_name ilike '%PPP%' or table_name ilike '%PROVIDER_RELIEF%' or table_name ilike '%FJC_IDB_CIVIL%' or table_name ilike '%COURTLISTENER_DOCKETS%' or table_name ilike '%OSHA_INSPECTIONS%' or table_name ilike '%FEC_INDIV%' or table_name ilike '%SKILLED%')
union all
select table_catalog, table_schema, table_name, row_count from LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
where table_name ilike '%NURSING%' or table_name ilike '%SNF%' or table_name ilike '%PBJ%' or table_name ilike '%COST_REP%' or table_name ilike '%HCRIS%' or table_name ilike '%STAFFING%' or table_name ilike '%SKILLED%'
order by 1,2,3
