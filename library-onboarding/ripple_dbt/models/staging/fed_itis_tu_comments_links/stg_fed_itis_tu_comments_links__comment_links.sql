{{ config(materialized='view') }}

-- Grain (verified live by orchestrator): one row per tsn, comment_id (192,851 rows).
-- ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.

with

source as (

    select * from {{ source('ripple_raw', 'FED_ITIS_TU_COMMENTS_LINKS') }}

),

renamed as (

    select

        try_to_number(trim(TSN))                                as tsn,
        try_to_number(trim(COMMENT_ID))                         as comment_id,
        try_to_date(trim(UPDATE_DATE), 'YYYY-MM-DD')            as update_date,

        -- metadata (no-underscore variant on ITIS tables; INGESTED_AT is an epoch-microseconds NUMBER)
        to_timestamp_ntz(INGESTED_AT, 6)                        as _loaded_at,
        SOURCE_RUN_ID                                           as _source_run_id,
        SRC_SHA256                                              as _src_sha256

    from source

),

keyed as (

    select
        coalesce(to_varchar(tsn), '') || '|' || coalesce(to_varchar(comment_id), '') as itis_tu_comments_links_key,
        *
    from renamed
    where tsn is not null and comment_id is not null

),

deduped as (

    select *,
        row_number() over (
            partition by tsn, comment_id
            order by _loaded_at desc
        ) as _row_num
    from keyed

)

select
    itis_tu_comments_links_key,
    tsn,
    comment_id,
    update_date,
    _loaded_at,
    _source_run_id,
    _src_sha256
from deduped
where _row_num = 1
