-- column names and types for my 5 tables plus the ICIS-Air / RCRA tables I may join to
select table_name, listagg(column_name || ':' || data_type, ', ') within group (order by ordinal_position) cols, max(row_count) rc
from (select c.table_name, c.column_name, c.data_type, c.ordinal_position, t.row_count
      from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS c
      join LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES t on t.table_schema=c.table_schema and t.table_name=c.table_name
      where c.table_schema='ENVIRONMENT' and c.table_name in (
        'ENVIRONMENT__FED_EPA_RCRA_RCRA_NAICS','ENVIRONMENT__FED_USGS_WBD_HUC8','ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS',
        'ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAM_SUBPARTS','ENVIRONMENT__XC_OWID_CO2','ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES',
        'ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS','ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY',
        'ENVIRONMENT__FED_EPA_RCRA_FACILITIES','ENVIRONMENT__FED_EPA_RCRA_VIOLATIONS','ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS'))
group by 1 order by 1
