{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_NARA_WRA_AAD') }}

),

renamed_cast as (

    select

        -- identifiers
        RECORD_ID                                          as record_id,
        SERIES_ID                                         as series_id,

        -- key dimensions
        PERSON_NAME                                       as person_name,
        try_to_date(DATE, 'YYYY-MM-DD')                   as record_date,
        DATE                                              as raw_date,
        CAMP_LOCATION                                     as camp_location,
        FIPS                                              as fips,
        GEO                                               as geo,

        -- person attributes
        try_to_number(AGE)                                as age,
        upper(trim(SEX))                                  as sex,
        upper(trim(CITIZENSHIP_STATUS))                   as citizenship_status,
        FAMILY_NUMBER                                     as family_number,

        -- supplemental
        NOTES_FIELD                                       as notes_field,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by record_id
            order by _ingested_at desc
        ) as _row_num
    from renamed_cast

)

select
    record_id,
    series_id,
    person_name,
    record_date,
    raw_date,
    camp_location,
    fips,
    geo,
    age,
    sex,
    citizenship_status,
    family_number,
    notes_field,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
