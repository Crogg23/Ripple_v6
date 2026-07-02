{{ config(materialized='view') }}

with source as (

    select *
    from {{ source('ripple_raw', 'FED_US_USASPENDING_API') }}

),

renamed as (

    select

        -- Primary key
        AWARD_ID                                                        as award_id,

        -- Identifiers
        GENERATED_UNIQUE_AWARD_ID                                       as generated_unique_award_id,
        RECIPIENT_UEI                                                   as recipient_uei,
        RECIPIENT_DUNS                                                  as recipient_duns,
        RECIPIENT_EIN                                                   as recipient_ein,
        NAICS_CODE                                                      as naics_code,
        CFDA_NUMBER                                                     as cfda_number,
        TREASURY_ACCOUNT_SYMBOL                                         as treasury_account_symbol,
        FEDERAL_ACCOUNT_CODE                                            as federal_account_code,
        AWARDING_AGENCY_CODE                                            as awarding_agency_code,
        PLACE_OF_PERFORMANCE_FIPS                                       as place_of_performance_fips,
        RECIPIENT_LOCATION_FIPS                                         as recipient_location_fips,

        -- Descriptive text
        RECIPIENT_NAME                                                  as recipient_name,
        AWARDING_AGENCY_NAME                                            as awarding_agency_name,
        FUNDING_AGENCY_NAME                                             as funding_agency_name,
        AWARD_TYPE                                                      as award_type,
        NAICS_DESCRIPTION                                               as naics_description,
        CFDA_TITLE                                                      as cfda_title,
        PLACE_OF_PERFORMANCE_STATE                                      as place_of_performance_state,
        PLACE_OF_PERFORMANCE_CITY                                       as place_of_performance_city,
        RECIPIENT_LOCATION_STATE                                        as recipient_location_state,
        DEF_CODE                                                        as def_code,

        -- Numeric financials
        try_to_double(TOTAL_OBLIGATION)                                 as total_obligation,
        try_to_double(TOTAL_OUTLAY)                                     as total_outlay,
        try_to_double(AWARD_AMOUNT)                                     as award_amount,

        -- Integer counts
        try_to_number(TRANSACTION_COUNT)                                as transaction_count,
        try_to_number(SUBAWARD_COUNT)                                   as subaward_count,
        try_to_number(FISCAL_YEAR)                                      as fiscal_year,

        -- Dates
        try_to_date(START_DATE)                                         as start_date,
        try_to_date(END_DATE)                                           as end_date,
        try_to_date(LAST_MODIFIED_DATE)                                 as last_modified_date,

        -- Metadata
        _ingested_at,
        _source_run_id

    from source
    qualify row_number() over (
        partition by AWARD_ID
        order by try_to_date(LAST_MODIFIED_DATE) desc nulls last, _ingested_at desc nulls last
    ) = 1

)

select * from renamed
