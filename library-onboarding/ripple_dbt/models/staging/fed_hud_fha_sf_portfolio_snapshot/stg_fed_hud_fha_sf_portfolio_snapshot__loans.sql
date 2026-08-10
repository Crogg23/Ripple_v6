{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT') }}

),

keyed as (

    -- This snapshot is loan-level with NO natural key in the file (no case
    -- number is published). A deterministic surrogate is built from the
    -- coarse composite (state, zip, originating mortgagee number, endorsement
    -- year/month) plus a row_number() over the full-row hash as a provenance
    -- tiebreaker, making loan_record_id fully unique.
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['PROPERTY_STATE', 'PROPERTY_ZIP', 'ORIGINATING_MORTGAGEE_NUMBER', 'ENDORSEMENT_YEAR', 'ENDORSEMENT_MONTH']) }}
            || '-'
            || row_number() over (
                   partition by PROPERTY_STATE, PROPERTY_ZIP, ORIGINATING_MORTGAGEE_NUMBER, ENDORSEMENT_YEAR, ENDORSEMENT_MONTH
                   order by hash(*)
               ) as loan_record_id
    from source

),

renamed as (

    select

        -- identifiers
        loan_record_id,
        trim(ORIGINATING_MORTGAGEE_NUMBER)             as originating_mortgagee_number,
        trim(SPONSOR_NUMBER)                           as sponsor_number,
        trim(NON_PROFIT_NUMBER)                        as non_profit_number,

        -- property location
        trim(PROPERTY_STATE)                           as property_state,
        trim(PROPERTY_CITY)                            as property_city,
        trim(PROPERTY_COUNTY)                          as property_county,
        trim(PROPERTY_ZIP)                             as property_zip,

        -- parties
        trim(ORIGINATION_MORTGAGEE_SPONSOR_ORIGINATOR) as originating_mortgagee_name,
        trim(SPONSOR_NAME)                             as sponsor_name,

        -- loan characteristics
        trim(DOWN_PAYMENT_SOURCE)                      as down_payment_source,
        trim(PRODUCT_TYPE)                             as product_type,
        trim(LOAN_PURPOSE)                             as loan_purpose,
        trim(PROPERTY_TYPE)                            as property_type,
        try_to_number(trim(INTEREST_RATE), 10, 4)      as interest_rate,
        try_to_number(trim(ORIGINAL_MORTGAGE_AMOUNT))  as original_mortgage_amount,
        try_to_number(trim(ENDORSEMENT_YEAR))          as endorsement_year,
        try_to_number(trim(ENDORSEMENT_MONTH))         as endorsement_month,

        -- metadata
        to_timestamp_ntz(INGESTED_AT, 6)               as _ingested_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from keyed

)

select * from renamed
