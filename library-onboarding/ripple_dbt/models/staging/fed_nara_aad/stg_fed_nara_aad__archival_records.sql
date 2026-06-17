{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_NARA_AAD') }}

),

renamed as (

    select

        -- identifiers
        dataset_id                                        as dataset_id,
        record_id                                         as record_id,

        -- descriptive attributes
        dataset_name                                      as dataset_name,
        series_title                                      as series_title,
        description_text                                  as description_text,

        -- key identifier columns (cast to proper types)
        try_to_date(date)                                 as date,
        nullif(trim(person_name), '')                     as person_name,
        nullif(trim(geo_location), '')                    as geo_location,
        nullif(trim(record_group), '')                    as record_group_number,

        -- semi-structured passthrough
        try_parse_json(raw_fields_json)                   as raw_fields_json,

        -- pipeline metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *
    from renamed
    qualify row_number() over (
        partition by dataset_id, record_id
        order by _ingested_at desc
    ) = 1

)

select * from deduped
