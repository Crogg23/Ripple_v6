{{ config(materialized='table') }}

with

staging as (

    select * from {{ ref('stg_fed_fjc_idb__federal_court_cases') }}

),

enriched as (

    select

        -- primary key
        case_id,

        -- cross-source key identifiers
        file_date                                                       as date_id,
        null::text                                                      as state_id,   -- not present in source; placeholder for cross-source joins
        district || '-' || office                                       as court_id,
        judge                                                           as judge_id,

        -- court / circuit identifiers
        circuit,
        district,
        office,
        docket,
        judge,

        -- case dates
        file_date,
        term_date,
        datediff('day', file_date, term_date)                           as days_to_termination,

        -- coded attributes
        origin_code,
        judgment_code,
        nature_of_suit_code,
        jurisdiction_code,
        prose_code,
        gender_code,
        criminal_count,
        stat_year,
        tape_year,
        disposition_code,
        amount_received,
        section_code,
        subsection_code,

        -- human-readable labels for common codes
        case
            when jurisdiction_code = 1 then 'U.S. Government Plaintiff'
            when jurisdiction_code = 2 then 'U.S. Government Defendant'
            when jurisdiction_code = 3 then 'Federal Question'
            when jurisdiction_code = 4 then 'Diversity of Citizenship'
            else 'Other/Unknown'
        end                                                             as jurisdiction_label,

        case
            when prose_code = 0 then 'Not Pro Se'
            when prose_code = 1 then 'Pro Se Plaintiff'
            when prose_code = 2 then 'Pro Se Defendant'
            when prose_code = 3 then 'Both Parties Pro Se'
            else 'Unknown'
        end                                                             as prose_label,

        case
            when gender_code = 1 then 'Male'
            when gender_code = 2 then 'Female'
            else 'Unknown/Not Recorded'
        end                                                             as gender_label,

        -- metadata
        _ingested_at,
        _source_run_id

    from staging

)

select * from enriched
