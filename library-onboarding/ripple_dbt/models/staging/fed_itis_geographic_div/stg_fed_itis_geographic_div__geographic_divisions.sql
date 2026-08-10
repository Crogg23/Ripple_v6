{{ config(materialized='view') }}

-- Grain (verified live by orchestrator): one row per tsn, geographic_value (480,351 rows).
-- ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.

with

source as (

    select * from {{ source('ripple_raw', 'FED_ITIS_GEOGRAPHIC_DIV') }}

),

renamed as (

    select

        try_to_number(trim(TSN))                                as tsn,
        trim(GEOGRAPHIC_VALUE)                                  as geographic_value,
        try_to_date(trim(UPDATE_DATE), 'YYYY-MM-DD')            as update_date,

        -- metadata (no-underscore variant on ITIS tables; INGESTED_AT is an epoch-microseconds NUMBER)
        to_timestamp_ntz(INGESTED_AT, 6)                        as _loaded_at,
        SOURCE_RUN_ID                                           as _source_run_id,
        SRC_SHA256                                              as _src_sha256

    from source

),

keyed as (

    select
        coalesce(to_varchar(tsn), '') || '|' || coalesce(to_varchar(geographic_value), '') as itis_geographic_div_key,
        *
    from renamed
    where tsn is not null and geographic_value is not null

),

deduped as (

    select *,
        row_number() over (
            partition by tsn, geographic_value
            order by _loaded_at desc
        ) as _row_num
    from keyed

)

select
    itis_geographic_div_key,
    tsn,
    geographic_value,
    update_date,
    _loaded_at,
    _source_run_id,
    _src_sha256
from deduped
where _row_num = 1
