{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_USASPENDING_TAS_FILTER_TREE') }}

),

renamed as (

    select

        -- identifiers
        trim(ID)                                       as node_id,

        -- dimensions
        trim(DESCRIPTION)                              as description,
        ANCESTORS                                      as ancestors,  -- VARIANT array, passed through

        -- measures
        "COUNT"                                        as account_count,
        CHILDREN                                       as child_count,

        -- metadata (INGESTED_AT is a NUMBER epoch in microseconds)
        to_timestamp_ntz(INGESTED_AT, 6)               as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by node_id
            order by _loaded_at desc
        ) as _row_num
    from renamed
    where node_id is not null

)

select * exclude (_row_num)
from deduped
where _row_num = 1
