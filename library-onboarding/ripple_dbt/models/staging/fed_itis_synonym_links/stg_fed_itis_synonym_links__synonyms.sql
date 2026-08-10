{{ config(materialized='view') }}

-- Grain (verified live by orchestrator): one row per tsn, tsn_accepted (315,254 rows).
-- ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.

with

source as (

    select * from {{ source('ripple_raw', 'FED_ITIS_SYNONYM_LINKS') }}

),

renamed as (

    select

        try_to_number(trim(TSN))                                as tsn,
        try_to_number(trim(TSN_ACCEPTED))                       as tsn_accepted,
        try_to_date(trim(UPDATE_DATE), 'YYYY-MM-DD')            as update_date,

        -- metadata (no-underscore variant on ITIS tables; INGESTED_AT is an epoch-microseconds NUMBER)
        to_timestamp_ntz(INGESTED_AT, 6)                        as _loaded_at,
        SOURCE_RUN_ID                                           as _source_run_id,
        SRC_SHA256                                              as _src_sha256

    from source

),

keyed as (

    select
        coalesce(to_varchar(tsn), '') || '|' || coalesce(to_varchar(tsn_accepted), '') as itis_synonym_links_key,
        *
    from renamed
    where tsn is not null and tsn_accepted is not null

),

deduped as (

    select *,
        row_number() over (
            partition by tsn, tsn_accepted
            order by _loaded_at desc
        ) as _row_num
    from keyed

)

select
    itis_synonym_links_key,
    tsn,
    tsn_accepted,
    update_date,
    _loaded_at,
    _source_run_id,
    _src_sha256
from deduped
where _row_num = 1
