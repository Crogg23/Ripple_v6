{{ config(materialized='view') }}

-- Repointed 2026-09-20: INTL_HUDOC was a page-capped landing pull (2,000
-- rows, live-confirmed). INTL_HUDOC_FULL is the corrected full reload
-- (211,778 rows, live-confirmed 2026-09-20) and carries the identical
-- 21-column set (DESCRIBE TABLE compared column-for-column, same names) --
-- no select-list changes needed, source() swap only.

with source as (

    select *
    from {{ source('ripple_raw', 'INTL_HUDOC_FULL') }}

),

renamed as (

    select
        -- key identifiers
        CASE_ID                                         as case_id,
        {{ null_junk('APPNO') }}                         as appno,
        {{ null_junk('ECLI') }}                          as ecli,
        {{ null_junk('COUNTRY') }}                       as country,
        PERSON_NAME                                     as person_name,
        try_to_date(DATE, 'YYYY-MM-DD')                 as date,

        -- descriptive attributes
        CASE_TITLE                                      as case_title,
        DOC_TYPE                                        as doc_type,
        try_to_number(IMPORTANCE)                       as importance,
        ARTICLES                                        as articles,
        VIOLATION                                       as violation,
        NONVIOLATION                                    as nonviolation,
        ORIGINATING_BODY                                as originating_body,
        RESPONDENT                                      as respondent,
        KEYWORDS                                        as keywords,
        CONCLUSION                                      as conclusion,
        LANGUAGE                                        as language,
        URL                                             as url,

        -- metadata
        -- landing _INGESTED_AT is a TIMESTAMP that swallowed epoch micros as seconds (year 56 million); re-read the epoch
        {{ landing_parse_audit_epoch('date_part(epoch_second, _ingested_at)') }} as _ingested_at,
        _source_run_id                                  as _source_run_id,

        -- deduplication helper
        row_number() over (
            partition by CASE_ID, APPNO, ECLI
            order by _ingested_at desc
        )                                               as _row_num

    from source

),

deduped as (

    select *
    from renamed
    where _row_num = 1

)

select
    case_id,
    appno,
    ecli,
    country,
    person_name,
    date,
    case_title,
    doc_type,
    importance,
    articles,
    violation,
    nonviolation,
    originating_body,
    respondent,
    keywords,
    conclusion,
    language,
    url,
    _ingested_at,
    _source_run_id
from deduped
