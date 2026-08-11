{{ config(tags=['minimal_staging']) }}

-- GRAIN: one row per exclusion record (SAM_NUMBER, unique in the landing table).
-- Re-pulled in full 2026-08-11 into FED_SAM_EXCLUSIONS_FULL_R2 (167,928 rows;
-- old capped table held ~9K). The full publisher file renamed several columns:
-- UEI->UNIQUE_ENTITY_ID, ENTITY_NAME->NAME, FIRST_NAME->FIRST (etc.),
-- ACTIVATION_DATE->ACTIVE_DATE, STATE->STATE_PROVINCE, ZIP->ZIP_CODE,
-- DNB_OPEN_DATA->OPEN_DATA_FLAG, and added ADDRESS_1..4, CT_CODE,
-- ADDITIONAL_COMMENTS, CROSS_REFERENCE, SAM_NUMBER, CREATION_DATE.
-- NULLIF empty strings — the loader lands '' for missing values.

with source as (

    select * from {{ source('ripple_raw', 'FED_SAM_EXCLUSIONS_FULL_R2') }}

),

cleaned as (

    select
        nullif(trim(SAM_NUMBER), '')            as sam_number,
        nullif(trim(UNIQUE_ENTITY_ID), '')      as uei,
        nullif(trim(CAGE), '')                  as cage,
        nullif(trim(NPI), '')                   as npi,
        nullif(trim(NAME), '')                  as entity_name,
        nullif(trim(FIRST), '')                 as first_name,
        nullif(trim(MIDDLE), '')                as middle_name,
        nullif(trim(LAST), '')                  as last_name,
        nullif(trim(PREFIX), '')                as prefix,
        nullif(trim(SUFFIX), '')                as suffix,
        nullif(trim(OPEN_DATA_FLAG), '')        as open_data_flag,
        nullif(trim(CLASSIFICATION), '')        as classification,
        nullif(trim(EXCLUSION_TYPE), '')        as exclusion_type,
        nullif(trim(EXCLUSION_PROGRAM), '')     as exclusion_program,
        nullif(trim(EXCLUDING_AGENCY), '')      as excluding_agency,
        nullif(trim(CT_CODE), '')               as ct_code,
        nullif(trim(ADDITIONAL_COMMENTS), '')   as additional_comments,
        nullif(trim(ACTIVE_DATE), '')           as activation_date,
        nullif(trim(TERMINATION_DATE), '')      as termination_date,
        nullif(trim(RECORD_STATUS), '')         as record_status,
        nullif(trim(CROSS_REFERENCE), '')       as cross_reference,
        nullif(trim(CREATION_DATE), '')         as creation_date,
        nullif(trim(ADDRESS_1), '')             as address_1,
        nullif(trim(ADDRESS_2), '')             as address_2,
        nullif(trim(CITY), '')                  as city,
        nullif(trim(STATE_PROVINCE), '')        as state,
        nullif(trim(ZIP_CODE), '')              as zip,
        nullif(trim(COUNTRY), '')               as country,
        _INGESTED_AT                            as _loaded_at,
        'https://sam.gov/content/exclusions'    as _source_url

    from source

)

select * from cleaned
