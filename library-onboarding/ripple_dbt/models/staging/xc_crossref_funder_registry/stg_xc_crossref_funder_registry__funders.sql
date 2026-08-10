{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'XC_CROSSREF_FUNDER_REGISTRY') }}

),

renamed as (

    select

        -- identifiers
        trim(URI)                                      as funder_uri,

        -- dimensions
        trim(PRIMARY_NAME_DISPLAY)                     as funder_name,
        trim(REPLACED)                                 as replaced_by_uri,

        -- metadata (INGESTED_AT is a NUMBER epoch in microseconds)
        to_timestamp_ntz(INGESTED_AT, 6)               as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by funder_uri
            order by _loaded_at desc
        ) as _row_num
    from renamed
    where funder_uri is not null

)

select * exclude (_row_num)
from deduped
where _row_num = 1
