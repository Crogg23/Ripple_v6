{{ config(materialized='view') }}

-- Grain (verified live by orchestrator): one row per tsn (678,363 rows).
-- ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.

with

source as (

    select * from {{ source('ripple_raw', 'FED_ITIS_HIERARCHY') }}

),

renamed as (

    select

        trim(HIERARCHY_STRING)                                  as hierarchy_string,
        try_to_number(trim(TSN))                                as tsn,
        try_to_number(trim(PARENT_TSN))                         as parent_tsn,
        try_to_number(trim(LEVEL))                              as hierarchy_level,
        try_to_number(trim(CHILDRENCOUNT))                      as children_count,

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
    where tsn is not null

),

deduped as (

    select *,
        row_number() over (
            partition by tsn
            order by _loaded_at desc
        ) as _row_num
    from keyed

)

select
    hierarchy_string,
    tsn,
    parent_tsn,
    hierarchy_level,
    children_count,
    _loaded_at,
    _source_run_id,
    _src_sha256
from deduped
where _row_num = 1
