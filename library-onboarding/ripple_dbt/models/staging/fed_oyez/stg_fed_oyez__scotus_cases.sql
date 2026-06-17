{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_OYEZ') }}

),

renamed as (

    select

        -- identifiers
        CASE_ID                                         as case_id,
        DOCKET                                          as docket,
        CASE_NAME                                       as case_name,

        -- dates
        try_to_date(ARGUMENT_DATE)                      as argument_date,
        try_to_date(DECISION_DATE)                      as decision_date,
        try_to_number(TERM)                             as term,

        -- decision details
        DECISION                                        as decision,
        MAJORITY_AUTHOR                                 as majority_author,
        DISPOSITION                                     as disposition,
        CITATION                                        as citation,

        -- media
        AUDIO_URL                                       as audio_url,
        TRANSCRIPT_URL                                  as transcript_url,

        -- case narrative
        SUMMARY                                         as summary,
        ADVOCATE_NAMES                                  as advocate_names,
        PETITIONER                                      as petitioner,
        RESPONDENT                                      as respondent,
        LOWER_COURT                                     as lower_court,

        -- voting detail (raw JSON / delimited string preserved as text)
        JUSTICE_VOTES                                   as justice_votes,

        -- person identifier derived from majority author (primary person key)
        MAJORITY_AUTHOR                                 as person_name,

        -- metadata
        try_to_timestamp(SCRAPED_AT)                    as scraped_at,
        current_timestamp()                             as _ingested_at,
        null::text                                      as _source_run_id

    from source

),

deduped as (

    select *
    from renamed
    qualify row_number() over (
        partition by case_id, docket
        order by scraped_at desc nulls last
    ) = 1

)

select * from deduped
