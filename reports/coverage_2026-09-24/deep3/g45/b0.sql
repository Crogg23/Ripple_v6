-- [q01_cols]
select table_name, column_name, data_type
from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
where table_schema = 'REFERENCE'
  and table_name in ('REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP','REFERENCE__CALENDAR','REFERENCE__FED_ITIS_JURISDICTION',
    'REFERENCE__FED_ITIS_OTHER_SOURCES','REFERENCE__FED_ITIS_VERN_REF_LINKS')
order by table_name, ordinal_position;
-- [q02_samples]
select 'AUTH' t, object_construct(*)::varchar o from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP limit 2)
union all select 'CAL', object_construct(*)::varchar from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__CALENDAR where date_day = '2025-10-01')
union all select 'JUR', object_construct(*)::varchar from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_JURISDICTION limit 2)
union all select 'OSRC', object_construct(*)::varchar from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_OTHER_SOURCES limit 2)
union all select 'VREF', object_construct(*)::varchar from (select * from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_VERN_REF_LINKS limit 2);
