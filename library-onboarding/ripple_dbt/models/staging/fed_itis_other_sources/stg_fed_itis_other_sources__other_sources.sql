{{ config(materialized='view') }}

-- Grain (verified live by orchestrator): one row per source_id_prefix, source_id (1,071 rows).
-- ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.

with

source as (

    select * from {{ source('ripple_raw', 'FED_ITIS_OTHER_SOURCES') }}

),

renamed as (

    select

        trim(SOURCE_ID_PREFIX)                                  as source_id_prefix,
        try_to_number(trim(SOURCE_ID))                          as source_id,
        trim(SOURCE_TYPE)                                       as source_type,
        trim(SOURCE)                                            as source_name,
        trim(VERSION)                                           as version,
        try_to_date(trim(ACQUISITION_DATE), 'YYYY-MM-DD')       as acquisition_date,
        trim(SOURCE_COMMENT)                                    as source_comment,
        try_to_date(trim(UPDATE_DATE), 'YYYY-MM-DD')            as update_date,

        -- metadata (no-underscore variant on ITIS tables; INGESTED_AT is an epoch-microseconds NUMBER)
        to_timestamp_ntz(INGESTED_AT, 6)                        as _loaded_at,
        SOURCE_RUN_ID                                           as _source_run_id,
        SRC_SHA256                                              as _src_sha256

    from source

),

keyed as (

    select
        coalesce(to_varchar(source_id_prefix), '') || '|' || coalesce(to_varchar(source_id), '') as itis_other_sources_key,
        *
    from renamed
    where source_id_prefix is not null and source_id is not null

),

deduped as (

    select *,
        row_number() over (
            partition by source_id_prefix, source_id
            order by _loaded_at desc
        ) as _row_num
    from keyed

)

select
    itis_other_sources_key,
    source_id_prefix,
    source_id,
    source_type,
    source_name,
    version,
    acquisition_date,
    source_comment,
    update_date,
    _loaded_at,
    _source_run_id,
    _src_sha256
from deduped
where _row_num = 1
