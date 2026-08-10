{{ config(materialized='view') }}

-- Grain (verified live by orchestrator): one row per comment_id (70,524 rows).
-- ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.

with

source as (

    select * from {{ source('ripple_raw', 'FED_ITIS_COMMENTS') }}

),

renamed as (

    select

        try_to_number(trim(COMMENT_ID))                         as comment_id,
        trim(COMMENTATOR)                                       as commentator,
        trim(COMMENT_DETAIL)                                    as comment_detail,
        try_to_timestamp_ntz(trim(COMMENT_TIME_STAMP))          as comment_time_stamp,
        try_to_date(trim(UPDATE_DATE), 'YYYY-MM-DD')            as update_date,

        -- metadata (no-underscore variant on ITIS tables; INGESTED_AT is an epoch-microseconds NUMBER)
        to_timestamp_ntz(INGESTED_AT, 6)                        as _loaded_at,
        SOURCE_RUN_ID                                           as _source_run_id,
        SRC_SHA256                                              as _src_sha256

    from source

),

keyed as (

    select
        *
    from renamed
    where comment_id is not null

),

deduped as (

    select *,
        row_number() over (
            partition by comment_id
            order by _loaded_at desc
        ) as _row_num
    from keyed

)

select
    comment_id,
    commentator,
    comment_detail,
    comment_time_stamp,
    update_date,
    _loaded_at,
    _source_run_id,
    _src_sha256
from deduped
where _row_num = 1
