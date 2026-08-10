{{ config(materialized='view') }}

-- Grain (verified live by orchestrator): one row per nodc_id, tsn (209,565 rows).
-- ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.

with

source as (

    select * from {{ source('ripple_raw', 'FED_ITIS_NODC_IDS') }}

),

renamed as (

    select

        trim(NODC_ID)                                           as nodc_id,
        try_to_date(trim(UPDATE_DATE), 'YYYY-MM-DD')            as update_date,
        try_to_number(trim(TSN))                                as tsn,

        -- metadata (no-underscore variant on ITIS tables; INGESTED_AT is an epoch-microseconds NUMBER)
        to_timestamp_ntz(INGESTED_AT, 6)                        as _loaded_at,
        SOURCE_RUN_ID                                           as _source_run_id,
        SRC_SHA256                                              as _src_sha256

    from source

),

keyed as (

    select
        coalesce(to_varchar(nodc_id), '') || '|' || coalesce(to_varchar(tsn), '') as itis_nodc_ids_key,
        *
    from renamed
    where nodc_id is not null and tsn is not null

),

deduped as (

    select *,
        row_number() over (
            partition by nodc_id, tsn
            order by _loaded_at desc
        ) as _row_num
    from keyed

)

select
    itis_nodc_ids_key,
    nodc_id,
    update_date,
    tsn,
    _loaded_at,
    _source_run_id,
    _src_sha256
from deduped
where _row_num = 1
