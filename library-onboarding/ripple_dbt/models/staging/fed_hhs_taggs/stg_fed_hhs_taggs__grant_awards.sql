{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_HHS_TAGGS') }}

),

renamed as (

    select

        -- primary identifier
        trim(AWARD_NUMBER)                                          as award_number,

        -- operating division
        trim(OPDIV)                                                 as opdiv,

        -- recipient identifiers
        trim(RECIPIENT_NAME)                                        as recipient_name,
        trim(RECIPIENT_EIN)                                         as recipient_ein,
        trim(RECIPIENT_CLASS)                                       as recipient_class,

        -- dates & fiscal period
        try_to_date(trim(AWARD_DATE), 'YYYY-MM-DD')                 as award_date,
        try_to_number(trim(FISCAL_YEAR))                            as fiscal_year,

        -- financials
        try_to_double(replace(replace(trim(AWARD_AMOUNT), ',', ''), '$', '')) as award_amount,

        -- award metadata
        trim(ACTIVITY_TYPE)                                         as activity_type,
        trim(AWARD_TYPE)                                            as award_type,
        trim(PROJECT_DESCRIPTION)                                   as project_description,

        -- assistance listing (ALN / CFDA)
        trim(ASSISTANCE_LISTING_NUMBER)                             as assistance_listing_number,
        trim(ASSISTANCE_LISTING_NAME)                               as assistance_listing_name,

        -- geography
        trim(RECIPIENT_CITY)                                        as recipient_city,
        trim(RECIPIENT_STATE)                                       as recipient_state,
        trim(RECIPIENT_ZIP)                                         as recipient_zip,
        trim(RECIPIENT_FIPS)                                        as recipient_fips,
        trim(RECIPIENT_COUNTRY)                                     as recipient_country,
        trim(METRO_NONMETRO)                                        as metro_nonmetro,

        -- pipeline metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by award_number
            order by _ingested_at desc
        ) as _row_num
    from renamed

)

select
    award_number,
    opdiv,
    recipient_name,
    recipient_ein,
    recipient_class,
    award_date,
    fiscal_year,
    award_amount,
    activity_type,
    award_type,
    project_description,
    assistance_listing_number,
    assistance_listing_name,
    recipient_city,
    recipient_state,
    recipient_zip,
    recipient_fips,
    recipient_country,
    metro_nonmetro,
    _ingested_at,
    _source_run_id

from deduped
where _row_num = 1
