-- S01 where the five tables live and what columns they carry
SELECT table_schema, table_name, column_name, data_type, ordinal_position
FROM LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
WHERE table_name IN ('REFERENCE__XC_OWID_FERTILITY','REFERENCE__CENSUS_CB_STATE','REF__DIM_STATE',
                     'REFERENCE__FED_USGS_TOPOVIEW','REFERENCE__FED_ITIS_TAXON_UNIT_TYPES')
ORDER BY table_name, ordinal_position
