{{ config(materialized='view') }}

-- Grain (verified live by orchestrator): one row per pub_id_prefix, publication_id (30,772 rows).
-- ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.

with

source as (

    select * from {{ source('ripple_raw', 'FED_ITIS_PUBLICATIONS') }}

),

renamed as (

    select

        trim(PUB_ID_PREFIX)                                     as pub_id_prefix,
        try_to_number(trim(PUBLICATION_ID))                     as publication_id,
        trim(REFERENCE_AUTHOR)                                  as reference_author,
        trim(TITLE)                                             as title,
        trim(PUBLICATION_NAME)                                  as publication_name,
        try_to_date(trim(LISTED_PUB_DATE), 'YYYY-MM-DD')        as listed_pub_date,
        try_to_date(trim(ACTUAL_PUB_DATE), 'YYYY-MM-DD')        as actual_pub_date,
        trim(PUBLISHER)                                         as publisher,
        trim(PUB_PLACE)                                         as pub_place,
        trim(ISBN)                                              as isbn,
        trim(ISSN)                                              as issn,
        trim(PAGES)                                             as pages,
        trim(PUB_COMMENT)                                       as pub_comment,
        try_to_date(trim(UPDATE_DATE), 'YYYY-MM-DD')            as update_date,

        -- metadata (no-underscore variant on ITIS tables; INGESTED_AT is an epoch-microseconds NUMBER)
        to_timestamp_ntz(INGESTED_AT, 6)                        as _loaded_at,
        SOURCE_RUN_ID                                           as _source_run_id,
        SRC_SHA256                                              as _src_sha256

    from source

),

keyed as (

    select
        coalesce(to_varchar(pub_id_prefix), '') || '|' || coalesce(to_varchar(publication_id), '') as itis_publications_key,
        *
    from renamed
    where pub_id_prefix is not null and publication_id is not null

),

deduped as (

    select *,
        row_number() over (
            partition by pub_id_prefix, publication_id
            order by _loaded_at desc
        ) as _row_num
    from keyed

)

select
    itis_publications_key,
    pub_id_prefix,
    publication_id,
    reference_author,
    title,
    publication_name,
    listed_pub_date,
    actual_pub_date,
    publisher,
    pub_place,
    isbn,
    issn,
    pages,
    pub_comment,
    update_date,
    _loaded_at,
    _source_run_id,
    _src_sha256
from deduped
where _row_num = 1
