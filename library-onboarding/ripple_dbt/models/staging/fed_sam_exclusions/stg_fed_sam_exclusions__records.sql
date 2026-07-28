{{ config(tags=['minimal_staging']) }}

-- GRAIN: one row per exclusion record (UEI or entity + activation date)
-- Fix: NULLIF empty strings — the SAM loader lands '' for missing values,
-- which breaks downstream IS NULL checks in the mart.

with source as (

    select * from {{ source('ripple_raw', 'FED_SAM_EXCLUSIONS') }}

),

cleaned as (

    select
        nullif(trim(UEI), '')                   as uei,
        nullif(trim(CAGE), '')                  as cage,
        nullif(trim(NPI), '')                   as npi,
        nullif(trim(ENTITY_NAME), '')           as entity_name,
        nullif(trim(FIRST_NAME), '')            as first_name,
        nullif(trim(MIDDLE_NAME), '')           as middle_name,
        nullif(trim(LAST_NAME), '')             as last_name,
        nullif(trim(PREFIX), '')                as prefix,
        nullif(trim(SUFFIX), '')                as suffix,
        nullif(trim(DNB_OPEN_DATA), '')         as dnb_open_data,
        nullif(trim(CLASSIFICATION), '')        as classification,
        nullif(trim(EXCLUSION_TYPE), '')        as exclusion_type,
        nullif(trim(EXCLUSION_PROGRAM), '')     as exclusion_program,
        nullif(trim(EXCLUDING_AGENCY), '')      as excluding_agency,
        nullif(trim(ACTIVATION_DATE), '')       as activation_date,
        nullif(trim(TERMINATION_DATE), '')      as termination_date,
        nullif(trim(RECORD_STATUS), '')         as record_status,
        nullif(trim(CITY), '')                  as city,
        nullif(trim(STATE), '')                 as state,
        nullif(trim(ZIP), '')                   as zip,
        nullif(trim(COUNTRY), '')               as country,
        _INGESTED_AT                            as _loaded_at,
        'https://sam.gov/content/exclusions'    as _source_url

    from source

)

select * from cleaned
