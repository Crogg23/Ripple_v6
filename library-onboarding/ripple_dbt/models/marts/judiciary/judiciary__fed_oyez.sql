{{ config(materialized='table', schema='JUDICIARY') }}

-- SAMPLE ONLY -- NOT the full dataset. A 25-case slice; Oyez covers thousands of Supreme Court cases (full audio since 1955). Use for shape/testing, never for docket-coverage claims. Labeled 2026-08-11 (verification sweep, defect class 7).

with

staging as (

    select * from {{ ref('stg_fed_oyez__scotus_cases') }}

),

final as (

    select

        -- primary key
        case_id,

        -- key identifiers for cross-source joins
        docket,
        person_name,
        decision_date                                   as date,

        -- case metadata
        case_name,
        term,
        petitioner,
        respondent,
        lower_court,

        -- timeline
        argument_date,
        decision_date,

        -- decision
        decision,
        majority_author,
        disposition,
        citation,

        -- participants
        advocate_names,
        justice_votes,

        -- narrative
        summary,

        -- media
        audio_url,
        transcript_url,

        -- derived flags
        case when audio_url is not null then true else false end     as has_audio,
        case when transcript_url is not null then true else false end as has_transcript,

        -- metadata
        scraped_at,
        _ingested_at,
        _source_run_id

    from staging

)

select * from final
