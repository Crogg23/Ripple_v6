{{ config(materialized='view') }}

-- Grain (verified live by orchestrator): one row per tsn, doc_id_prefix, documentation_id, vern_id (93,078 rows).
-- ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.

with

source as (

    select * from {{ source('ripple_raw', 'FED_ITIS_VERN_REF_LINKS') }}

),

renamed as (

    select

        try_to_number(trim(TSN))                                as tsn,
        trim(DOC_ID_PREFIX)                                     as doc_id_prefix,
        try_to_number(trim(DOCUMENTATION_ID))                   as documentation_id,
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
        coalesce(to_varchar(tsn), '') || '|' || coalesce(to_varchar(doc_id_prefix), '') || '|' || coalesce(to_varchar(documentation_id), '') || '|' || coalesce(to_varchar(vern_id), '') as itis_vern_ref_links_key,
        *
    from renamed
    where tsn is not null and doc_id_prefix is not null and documentation_id is not null and vern_id is not null

),

deduped as (

    select *,
        row_number() over (
            partition by tsn, doc_id_prefix, documentation_id, vern_id
            order by _loaded_at desc
        ) as _row_num
    from keyed

)

select
    itis_vern_ref_links_key,
    tsn,
    doc_id_prefix,
    documentation_id,
    update_date,
    vern_id,
    _loaded_at,
    _source_run_id,
    _src_sha256
from deduped
where _row_num = 1
