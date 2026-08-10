{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_USDA_RD_MFH_ACTIVE_PROJECTS') }}

),

renamed as (

    select

        -- identifiers (composite key: borrower_id + project_id)
        trim(BORROWER_ID)                               as borrower_id,
        trim(PROJECT_ID)                                as project_id,
        trim(PROJECT_CHECK_DIGIT)                       as project_check_digit,

        -- location
        try_to_number(trim(LATITUDE), 20, 10)           as latitude,
        try_to_number(trim(LONGITUDE), 20, 10)          as longitude,
        trim(STATE_COUNTY_FIPS_CODE)                    as state_county_fips_code,
        trim(PROJECT_NAME)                              as project_name,
        trim(MAIN_ADDRESS_LINE1)                        as main_address_line1,
        trim(MAIN_ADDRESS_LINE2)                        as main_address_line2,
        trim(MAIN_ADDRESS_LINE3)                        as main_address_line3,
        trim(CITY)                                      as city,
        trim(STATE_ABBREVIATION)                        as state_abbreviation,
        trim(ZIP_CODE)                                  as zip_code,

        -- project characteristics
        try_to_number(trim(PROJECT_SIZE))               as project_size_units,
        trim(RENTAL_CODE)                               as rental_code,
        trim(LABOR_HOUSING_TYPE)                        as labor_housing_type,
        trim(REVITILIZATION_INDICATOR)                  as revitalization_indicator,
        trim(TAX_STATUS_INDICATOR)                      as tax_status_indicator,
        try_to_date(trim(DATE_TAX_CREDIT_EXPIRES), 'MM/DD/YYYY')          as date_tax_credit_expires,
        trim(PROFIT_TYPE_CODE)                          as profit_type_code,
        trim(MANAGEMENT_NAME)                           as management_name,
        try_to_date(trim(DATE_OF_OPERATION), 'MM/DD/YYYY')                as date_of_operation,
        try_to_date(trim(DATE_RESTRICTIVE_CLAUSE_EXPIRES), 'MM/DD/YYYY')  as date_restrictive_clause_expires,

        -- units
        try_to_number(trim(TOTAL_1_BEDROOM_UNITS))      as total_1_bedroom_units,
        try_to_number(trim(TOTAL_2_BEDROOM_UNITS))      as total_2_bedroom_units,
        try_to_number(trim(TOTAL_3_BEDROOM_UNITS))      as total_3_bedroom_units,
        try_to_number(trim(TOTAL_4_BEDROOM_UNITS))      as total_4_bedroom_units,
        try_to_number(trim(TOTAL_5_BEDROOM_UNITS))      as total_5_bedroom_units,
        try_to_number(trim(TOTAL_6_BEDROOM_UNITS))      as total_6_bedroom_units,
        try_to_number(trim(TOTAL_HANDICAPPED_UNITS))    as total_handicapped_units,
        try_to_number(trim(VACANT_UNITS))               as vacant_units,
        try_to_number(trim(RENTAL_ASSISTANCE_UNITS))    as rental_assistance_units,

        -- metadata
        to_timestamp_ntz(INGESTED_AT, 6)                as _ingested_at,
        SOURCE_RUN_ID                                   as _source_run_id,
        SRC_SHA256                                      as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by borrower_id, project_id
            order by _ingested_at desc
        ) as _row_num
    from renamed
    where borrower_id is not null
      and project_id is not null

)

select * exclude _row_num
from deduped
where _row_num = 1
