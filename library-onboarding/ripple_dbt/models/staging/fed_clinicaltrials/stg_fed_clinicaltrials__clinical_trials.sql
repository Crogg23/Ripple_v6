{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_CLINICALTRIALS') }}

),

renamed as (

    select

        -- primary key
        nct_id,

        -- identifiers
        org_study_id,
        secondary_ids,

        -- study metadata
        brief_title,
        official_title,
        overall_status,
        phase,
        study_type,

        -- dates
        try_to_date(start_date, 'YYYY-MM-DD')                  as start_date,
        try_to_date(completion_date, 'YYYY-MM-DD')             as completion_date,
        try_to_date(primary_completion_date, 'YYYY-MM-DD')     as primary_completion_date,
        try_to_date(results_first_posted_date, 'YYYY-MM-DD')   as results_first_posted_date,
        try_to_date(last_update_posted_date, 'YYYY-MM-DD')     as last_update_posted_date,
        try_to_date(first_posted_date, 'YYYY-MM-DD')           as first_posted_date,

        -- numeric
        try_to_number(enrollment)                              as enrollment,

        -- sponsor / oversight
        lead_sponsor_name,
        lead_sponsor_class,
        responsible_party,

        -- boolean flags (stored as text 'true'/'false' or 'Yes'/'No')
        case
            when lower(has_results) in ('true', 'yes', '1')        then true
            when lower(has_results) in ('false', 'no', '0')        then false
            else null
        end                                                    as has_results,

        case
            when lower(oversight_has_dmc) in ('true', 'yes', '1')  then true
            when lower(oversight_has_dmc) in ('false', 'no', '0')  then false
            else null
        end                                                    as oversight_has_dmc,

        case
            when lower(is_fda_regulated_drug) in ('true', 'yes', '1')  then true
            when lower(is_fda_regulated_drug) in ('false', 'no', '0')  then false
            else null
        end                                                    as is_fda_regulated_drug,

        case
            when lower(is_fda_regulated_device) in ('true', 'yes', '1')  then true
            when lower(is_fda_regulated_device) in ('false', 'no', '0')  then false
            else null
        end                                                    as is_fda_regulated_device,

        -- eligibility
        gender,
        minimum_age,
        maximum_age,
        eligibility_criteria,

        -- semi-structured / free text
        collaborators,
        conditions,
        interventions,
        primary_outcomes,
        secondary_outcomes,
        locations,
        keywords,
        references,
        why_stopped,

        -- audit
        _ingested_at,
        _source_run_id

    from source
    qualify row_number() over (
        partition by nct_id
        order by try_to_date(last_update_posted_date, 'YYYY-MM-DD') desc nulls last,
                 _ingested_at desc
    ) = 1

)

select * from renamed
