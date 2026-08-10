{{ config(materialized='view') }}

-- Grain (verified live by orchestrator): one row per expert_id_prefix, expert_id (197 rows).
-- ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.

with

source as (

    select * from {{ source('ripple_raw', 'FED_ITIS_EXPERTS') }}

),

renamed as (

    select

        trim(EXPERT_ID_PREFIX)                                  as expert_id_prefix,
        try_to_number(trim(EXPERT_ID))                          as expert_id,
        trim(EXPERT)                                            as expert,
        trim(EXP_COMMENT)                                       as exp_comment,
        try_to_date(trim(UPDATE_DATE), 'YYYY-MM-DD')            as update_date,

        -- metadata (no-underscore variant on ITIS tables; INGESTED_AT is an epoch-microseconds NUMBER)
        to_timestamp_ntz(INGESTED_AT, 6)                        as _loaded_at,
        SOURCE_RUN_ID                                           as _source_run_id,
        SRC_SHA256                                              as _src_sha256

    from source

),

keyed as (

    select
        coalesce(to_varchar(expert_id_prefix), '') || '|' || coalesce(to_varchar(expert_id), '') as itis_experts_key,
        *
    from renamed
    where expert_id_prefix is not null and expert_id is not null

),

deduped as (

    select *,
        row_number() over (
            partition by expert_id_prefix, expert_id
            order by _loaded_at desc
        ) as _row_num
    from keyed

)

select
    itis_experts_key,
    expert_id_prefix,
    expert_id,
    expert,
    exp_comment,
    update_date,
    _loaded_at,
    _source_run_id,
    _src_sha256
from deduped
where _row_num = 1
