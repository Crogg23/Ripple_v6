{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_clinicaltrials__clinical_trials') }}

),

-- Parse EudraCT number out of the secondary_ids JSON array for cross-source joins.
-- secondary_ids is stored as a JSON array of objects like:
-- [{"id": "2020-000001-11", "type": "EudraCT Number"}, ...]
eudract_parsed as (

    select
        nct_id,
        f.value:id::text as eudract_number
    from base,
    lateral flatten(
        input  => try_parse_json(secondary_ids),
        outer  => true
    ) f
    where lower(f.value:type::text) like '%eudract%'

),

final as (

    select

        -- -----------------------------------------------------------------------
        -- Key identifiers (exposed for cross-source joins)
        -- -----------------------------------------------------------------------
        b.nct_id,
        b.org_study_id,
        ep.eudract_number,
        -- NPI is not present in this source; expose as null for schema parity
        null::text                              as npi,

        -- -----------------------------------------------------------------------
        -- Study descriptors
        -- -----------------------------------------------------------------------
        b.brief_title,
        b.official_title,
        b.overall_status,
        b.phase,
        b.study_type,

        -- -----------------------------------------------------------------------
        -- Dates
        -- -----------------------------------------------------------------------
        b.first_posted_date,
        b.start_date,
        b.primary_completion_date,
        b.completion_date,
        b.results_first_posted_date,
        b.last_update_posted_date,

        -- Derived duration metrics (days)
        datediff(
            'day', b.start_date, b.completion_date
        )                                       as study_duration_days,

        datediff(
            'day', b.first_posted_date, b.results_first_posted_date
        )                                       as days_to_results_posting,

        -- -----------------------------------------------------------------------
        -- Enrollment
        -- -----------------------------------------------------------------------
        b.enrollment,

        -- -----------------------------------------------------------------------
        -- Sponsor / oversight
        -- -----------------------------------------------------------------------
        b.lead_sponsor_name,
        b.lead_sponsor_class,
        b.responsible_party,
        b.oversight_has_dmc,
        b.is_fda_regulated_drug,
        b.is_fda_regulated_device,

        -- -----------------------------------------------------------------------
        -- Eligibility
        -- -----------------------------------------------------------------------
        b.gender,
        b.minimum_age,
        b.maximum_age,
        b.eligibility_criteria,

        -- -----------------------------------------------------------------------
        -- Results & stopping
        -- -----------------------------------------------------------------------
        b.has_results,
        b.why_stopped,

        -- -----------------------------------------------------------------------
        -- Semi-structured columns (kept as variant-compatible text for BI tools)
        -- -----------------------------------------------------------------------
        b.conditions,
        b.interventions,
        b.primary_outcomes,
        b.secondary_outcomes,
        b.collaborators,
        b.locations,
        b.keywords,
        b.references,
        b.secondary_ids,

        -- -----------------------------------------------------------------------
        -- Categorisation helpers
        -- -----------------------------------------------------------------------
        case
            when b.overall_status in ('Recruiting', 'Not yet recruiting',
                                      'Enrolling by invitation')
                then 'Active'
            when b.overall_status in ('Completed')
                then 'Completed'
            when b.overall_status in ('Terminated', 'Withdrawn', 'Suspended')
                then 'Stopped'
            when b.overall_status in ('Active, not recruiting')
                then 'Active, not recruiting'
            else 'Other / Unknown'
        end                                     as status_category,

        case
            when b.phase in ('Phase 1', 'Phase 1/Phase 2')           then 'Early Phase'
            when b.phase in ('Phase 2', 'Phase 2/Phase 3')           then 'Mid Phase'
            when b.phase in ('Phase 3', 'Phase 3/Phase 4')           then 'Late Phase'
            when b.phase = 'Phase 4'                                  then 'Post-Market'
            when b.phase in ('N/A', 'Not Applicable')                 then 'N/A'
            else 'Unknown'
        end                                     as phase_category,

        -- -----------------------------------------------------------------------
        -- Source audit
        -- -----------------------------------------------------------------------
        'fed_clinicaltrials'                    as source_id,
        b._ingested_at,
        b._source_run_id

    from base b
    left join eudract_parsed ep
        on b.nct_id = ep.nct_id

)

select * from final
