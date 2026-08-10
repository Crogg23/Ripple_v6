{{ config(materialized='view') }}

-- Grain (verified live by orchestrator): one row per tsn, vern_id (166,778 rows).
-- ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.

with

source as (

    select * from {{ source('ripple_raw', 'FED_ITIS_VERNACULARS') }}

),

renamed as (

    select

        try_to_number(trim(TSN))                                as tsn,
        trim(VERNACULAR_NAME)                                   as vernacular_name,
        trim(LANGUAGE)                                          as language,
        trim(APPROVED_IND)                                      as approved_ind,
        try_to_date(trim(UPDATE_DATE), 'YYYY-MM-DD')            as update_date,
        try_to_number(trim(VERN_ID))                            as vern_id,

        -- metadata (no-underscore variant on ITIS tables; INGESTED_AT is an epoch-microseconds NUMBER)
        to_timestamp_ntz(INGESTED_AT, 6)                        as _loaded_at,
        SOURCE_RUN_ID                                           as _source_run_id,
        SRC_SHA256                                              as _src_sha256

    from source

),

keyed as (

    select
        coalesce(to_varchar(tsn), '') || '|' || coalesce(to_varchar(vern_id), '') as itis_vernaculars_key,
        *
    from renamed
    where tsn is not null and vern_id is not null

),

deduped as (

    select *,
        row_number() over (
            partition by tsn, vern_id
            order by _loaded_at desc
        ) as _row_num
    from keyed

)

select
    itis_vernaculars_key,
    tsn,
    vernacular_name,
    language,
    approved_ind,
    update_date,
    vern_id,
    _loaded_at,
    _source_run_id,
    _src_sha256
from deduped
where _row_num = 1
