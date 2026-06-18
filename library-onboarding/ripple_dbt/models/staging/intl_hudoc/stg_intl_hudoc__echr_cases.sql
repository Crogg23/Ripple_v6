{{ config(materialized='view') }}

with source as (

    select *
    from {{ source('ripple_raw', 'INTL_HUDOC') }}

),

renamed as (

    select
        -- key identifiers
        CASE_ID                                         as case_id,
        APPNO                                           as appno,
        ECLI                                            as ecli,
        COUNTRY                                         as country,
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
        _ingested_at                                    as _ingested_at,
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
