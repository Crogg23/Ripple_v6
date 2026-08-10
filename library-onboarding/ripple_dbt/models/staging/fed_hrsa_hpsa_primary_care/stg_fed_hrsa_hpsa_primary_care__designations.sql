{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_HRSA_HPSA_PRIMARY_CARE') }}

),

keyed as (

    -- The composite (HPSA_ID, HPSA_GEOGRAPHY_IDENTIFICATION_NUMBER) is
    -- NEAR-unique (79,153 distinct of 79,158 rows). The handful of collisions
    -- are genuinely distinct records, so a row_number() over the full-row hash
    -- is appended as a deterministic provenance tiebreaker to make
    -- hpsa_component_id fully unique.
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['HPSA_ID', 'HPSA_GEOGRAPHY_IDENTIFICATION_NUMBER']) }}
            || '-'
            || row_number() over (
                   partition by HPSA_ID, HPSA_GEOGRAPHY_IDENTIFICATION_NUMBER
                   order by hash(*)
               ) as hpsa_component_id
    from source

),

renamed as (

    select

        -- identifiers
        hpsa_component_id,
        trim(HPSA_ID)                                          as hpsa_id,
        trim(HPSA_GEOGRAPHY_IDENTIFICATION_NUMBER)             as hpsa_geography_id,
        trim(HPSA_COMPONENT_SOURCE_IDENTIFICATION_NUMBER)      as hpsa_component_source_id,
        trim(BHCMIS_ORGANIZATION_IDENTIFICATION_NUMBER)        as bhcmis_organization_id,

        -- designation
        trim(HPSA_NAME)                                        as hpsa_name,
        trim(DESIGNATION_TYPE)                                 as designation_type,
        trim(HPSA_DISCIPLINE_CLASS)                            as hpsa_discipline_class,
        try_to_number(trim(DISCIPLINE_CLASS_NUMBER))           as discipline_class_number,
        try_to_number(trim(HPSA_SCORE))                        as hpsa_score,
        try_to_number(trim(PC_MCTA_SCORE))                     as pc_mcta_score,
        trim(HPSA_STATUS)                                      as hpsa_status,
        trim(HPSA_STATUS_CODE)                                 as hpsa_status_code,
        trim(HPSA_TYPE_CODE)                                   as hpsa_type_code,
        try_to_date(trim(HPSA_DESIGNATION_DATE), 'MM/DD/YYYY') as designation_date,
        try_to_date(trim(HPSA_DESIGNATION_LAST_UPDATE_DATE), 'MM/DD/YYYY')
                                                               as designation_last_update_date,
        try_to_date(trim(WITHDRAWN_DATE), 'MM/DD/YYYY')        as withdrawn_date,
        trim(HPSA_WITHDRAWN_DATE_STRING)                       as withdrawn_date_string,
        trim(BREAK_IN_DESIGNATION)                             as break_in_designation,
        trim(HPSA_DEGREE_OF_SHORTAGE)                          as degree_of_shortage,

        -- population / shortage measures
        try_to_number(trim(HPSA_FTE), 12, 4)                   as hpsa_fte,
        try_to_number(trim(HPSA_DESIGNATION_POPULATION), 14, 1) as designation_population,
        try_to_number(trim(OF_POPULATION_BELOW_100_POVERTY), 8, 2)
                                                               as pct_population_below_poverty,
        trim(HPSA_FORMAL_RATIO)                                as formal_ratio,
        trim(HPSA_PROVIDER_RATIO_GOAL)                         as provider_ratio_goal,
        try_to_number(trim(HPSA_ESTIMATED_SERVED_POPULATION))  as estimated_served_population,
        try_to_number(trim(HPSA_ESTIMATED_UNDERSERVED_POPULATION))
                                                               as estimated_underserved_population,
        try_to_number(trim(HPSA_RESIDENT_CIVILIAN_POPULATION), 14, 2)
                                                               as resident_civilian_population,
        try_to_number(trim(HPSA_SHORTAGE), 12, 2)              as hpsa_shortage,
        trim(HPSA_POPULATION_TYPE)                             as population_type,
        trim(HPSA_POPULATION_TYPE_CODE)                        as population_type_code,
        trim(HPSA_DESIGNATION_POPULATION_TYPE_DESCRIPTION)     as designation_population_type_description,
        trim(PROVIDER_TYPE)                                    as provider_type,

        -- geography flags
        trim(METROPOLITAN_INDICATOR)                           as metropolitan_indicator,
        trim(HPSA_METROPOLITAN_INDICATOR_CODE)                 as metropolitan_indicator_code,
        trim(RURAL_STATUS)                                     as rural_status,
        trim(RURAL_STATUS_CODE)                                as rural_status_code,
        trim(U_S_MEXICO_BORDER_100_KILOMETER_INDICATOR)        as us_mexico_border_100km_indicator,
        trim(U_S_MEXICO_BORDER_COUNTY_INDICATOR)               as us_mexico_border_county_indicator,

        -- component
        trim(HPSA_COMPONENT_NAME)                              as component_name,
        trim(HPSA_COMPONENT_TYPE_CODE)                         as component_type_code,
        trim(HPSA_COMPONENT_TYPE_DESCRIPTION)                  as component_type_description,
        trim(HPSA_COMPONENT_STATE_ABBREVIATION)                as component_state_abbreviation,

        -- location
        trim(HPSA_ADDRESS)                                     as hpsa_address,
        trim(HPSA_CITY)                                        as hpsa_city,
        trim(HPSA_POSTAL_CODE)                                 as hpsa_postal_code,
        try_to_number(trim(LATITUDE), 12, 8)                   as latitude,
        try_to_number(trim(LONGITUDE), 12, 8)                  as longitude,

        -- state / county rollups
        trim(PRIMARY_STATE_ABBREVIATION)                       as primary_state_abbreviation,
        trim(PRIMARY_STATE_NAME)                               as primary_state_name,
        trim(PRIMARY_STATE_FIPS_CODE)                          as primary_state_fips_code,
        trim(STATE_ABBREVIATION)                               as state_abbreviation,
        trim(STATE_NAME)                                       as state_name,
        trim(STATE_FIPS_CODE)                                  as state_fips_code,
        trim(COMMON_STATE_ABBREVIATION)                        as common_state_abbreviation,
        trim(COMMON_STATE_NAME)                                as common_state_name,
        trim(COMMON_STATE_FIPS_CODE)                           as common_state_fips_code,
        trim(COMMON_COUNTY_NAME)                               as common_county_name,
        trim(COMMON_STATE_COUNTY_FIPS_CODE)                    as common_state_county_fips_code,
        trim(COMMON_POSTAL_CODE)                               as common_postal_code,
        trim(COMMON_REGION_NAME)                               as common_region_name,
        trim(COUNTY_EQUIVALENT_NAME)                           as county_equivalent_name,
        trim(COUNTY_OR_COUNTY_EQUIVALENT_FEDERAL_INFORMATION_PROCESSING_STANDARD_CODE)
                                                               as county_fips_code,
        trim(STATE_AND_COUNTY_FEDERAL_INFORMATION_PROCESSING_STANDARD_CODE)
                                                               as state_county_fips_code,

        -- record dates
        try_to_date(trim(DATA_WAREHOUSE_RECORD_CREATE_DATE), 'MM/DD/YYYY')
                                                               as record_create_date,
        trim(DATA_WAREHOUSE_RECORD_CREATE_DATE_TEXT)           as record_create_date_text,

        -- metadata
        to_timestamp_ntz(INGESTED_AT, 6)                       as _ingested_at,
        SOURCE_RUN_ID                                          as _source_run_id,
        SRC_SHA256                                             as _src_sha256

    from keyed

)

select * from renamed
