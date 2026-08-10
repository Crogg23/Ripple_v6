{{ config(materialized='view') }}

-- Grain (verified live by orchestrator): one row per taxon_author_id (214,445 rows).
-- ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.

with

source as (

    select * from {{ source('ripple_raw', 'FED_ITIS_STRIPPEDAUTHOR') }}

),

renamed as (

    select

        try_to_number(trim(TAXON_AUTHOR_ID))                    as taxon_author_id,
        trim(SHORTAUTHOR)                                       as short_author,

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
    where taxon_author_id is not null

),

deduped as (

    select *,
        row_number() over (
            partition by taxon_author_id
            order by _loaded_at desc
        ) as _row_num
    from keyed

)

select
    taxon_author_id,
    short_author,
    _loaded_at,
    _source_run_id,
    _src_sha256
from deduped
where _row_num = 1
