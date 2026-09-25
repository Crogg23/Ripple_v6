-- [q01_coltypes]
select table_name, column_name, data_type
from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
where table_schema = 'ENVIRONMENT'
  and table_name in ('ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES','ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS',
    'ENVIRONMENT__FED_NOAA_WEATHER_API','ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS','ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES',
    'ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY','ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS',
    'ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT','ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES')
  and data_type <> 'TEXT'
order by table_name, ordinal_position

-- [q02_samples]
select 'INSP' t, object_construct(*)::varchar o from (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS limit 2)
union all select 'SDWAF', object_construct(*)::varchar from (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES where seller_pwsid is not null and seller_pwsid <> '' limit 1)
union all select 'SDWAF2', object_construct(*)::varchar from (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES where filtration_status_code is not null and filtration_status_code <> '' limit 1)
union all select 'QNCR', object_construct(*)::varchar from (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY limit 1)
union all select 'SDWAV', object_construct(*)::varchar from (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT where violation_id is not null limit 1)
union all select 'PWS', object_construct(*)::varchar from (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS limit 1)
union all select 'FRSF', object_construct(*)::varchar from (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES limit 1)
union all select 'FRSL', object_construct(*)::varchar from (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS limit 1)
union all select 'NOAA', object_construct(*)::varchar from (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NOAA_WEATHER_API limit 1)
