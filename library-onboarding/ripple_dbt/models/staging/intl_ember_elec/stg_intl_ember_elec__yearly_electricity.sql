{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'INTL_EMBER_ELEC') }}

),

renamed as (

    select

        -- identifiers
        trim(COUNTRY_OR_REGION)                          as country,
        trim(ISO_3_CODE)                                 as iso_3_code,
        try_to_date(trim(DATE), 'YYYY')                  as date,

        -- geography / groupings
        trim(AREA_TYPE)                                  as area_type,
        trim(CONTINENT)                                  as continent,
        trim(EMBER_REGION)                               as ember_region,
        case
            when upper(trim(EU))    = 'TRUE'  then true
            when upper(trim(EU))    = 'FALSE' then false
            else null
        end                                              as is_eu,
        case
            when upper(trim(OECD))  = 'TRUE'  then true
            when upper(trim(OECD))  = 'FALSE' then false
            else null
        end                                              as is_oecd,
        case
            when upper(trim(G20))   = 'TRUE'  then true
            when upper(trim(G20))   = 'FALSE' then false
            else null
        end                                              as is_g20,
        case
            when upper(trim(G7))    = 'TRUE'  then true
            when upper(trim(G7))    = 'FALSE' then false
            else null
        end                                              as is_g7,
        case
            when upper(trim(ASEAN)) = 'TRUE'  then true
            when upper(trim(ASEAN)) = 'FALSE' then false
            else null
        end                                              as is_asean,

        -- metric descriptors
        trim(CATEGORY)                                   as category,
        trim(SUBCATEGORY)                                as subcategory,
        trim(VARIABLE)                                   as variable,
        trim(UNIT)                                       as unit,

        -- measures
        try_to_double(VALUE)                             as value,
        try_to_double(YOY_ABSOLUTE_CHANGE)               as yoy_absolute_change,
        try_to_double(YOY___CHANGE)                      as yoy_pct_change,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *
    from renamed
    qualify row_number() over (
        partition by country, date, variable
        order by _ingested_at desc
    ) = 1

)

select * from deduped
