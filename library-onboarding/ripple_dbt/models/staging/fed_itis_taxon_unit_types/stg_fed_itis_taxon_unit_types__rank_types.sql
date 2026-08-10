{{ config(materialized='view') }}

-- Grain (verified live by orchestrator): one row per kingdom_id, rank_id (182 rows).
-- ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.

with

source as (

    select * from {{ source('ripple_raw', 'FED_ITIS_TAXON_UNIT_TYPES') }}

),

renamed as (

    select

        try_to_number(trim(KINGDOM_ID))                         as kingdom_id,
        try_to_number(trim(RANK_ID))                            as rank_id,
        trim(RANK_NAME)                                         as rank_name,
        try_to_number(trim(DIR_PARENT_RANK_ID))                 as dir_parent_rank_id,
        try_to_number(trim(REQ_PARENT_RANK_ID))                 as req_parent_rank_id,
        try_to_date(trim(UPDATE_DATE), 'YYYY-MM-DD')            as update_date,

        -- metadata (no-underscore variant on ITIS tables; INGESTED_AT is an epoch-microseconds NUMBER)
        to_timestamp_ntz(INGESTED_AT, 6)                        as _loaded_at,
        SOURCE_RUN_ID                                           as _source_run_id,
        SRC_SHA256                                              as _src_sha256

    from source

),

keyed as (

    select
        coalesce(to_varchar(kingdom_id), '') || '|' || coalesce(to_varchar(rank_id), '') as itis_taxon_unit_types_key,
        *
    from renamed
    where kingdom_id is not null and rank_id is not null

),

deduped as (

    select *,
        row_number() over (
            partition by kingdom_id, rank_id
            order by _loaded_at desc
        ) as _row_num
    from keyed

)

select
    itis_taxon_unit_types_key,
    kingdom_id,
    rank_id,
    rank_name,
    dir_parent_rank_id,
    req_parent_rank_id,
    update_date,
    _loaded_at,
    _source_run_id,
    _src_sha256
from deduped
where _row_num = 1
