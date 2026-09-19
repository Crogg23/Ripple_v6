{{ config(materialized='view') }}

-- HAND-EDITED 2026-09-19: dedupe is a whole-raw-row hash (_row_hash), see the
-- comment in deduped. The staging generator skips files carrying this marker.

with source as (

    -- _row_hash: hash of every landing column except the load stamps
    select *, hash(* exclude (_INGESTED_AT, _SOURCE_RUN_ID, _SRC_SHA256)) as _row_hash
    from {{ source('ripple_raw', 'FED_NARA_AAD') }}

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
        _source_run_id,

        -- whole-raw-row hash, carried for the dedupe only
        _row_hash

    from source

),

deduped as (

    -- 2026-09-19: the old partition was (dataset_id, record_id). It hid 545 of
    -- 554 landing rows on a single load -- that pair does not identify a row.
    -- The dedupe is now the whole-raw-row hash, so only exact copies are
    -- dropped (0 exact copies in landing).
    select * exclude (_row_hash)
    from renamed
    qualify row_number() over (
        partition by _row_hash
        order by _ingested_at desc
    ) = 1

)

select * from deduped
