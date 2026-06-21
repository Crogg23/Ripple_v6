{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_cfpb_complaints__complaints') }}

),

enriched as (

    select

        -- keys / cross-source join keys
        complaint_id,
        state,
        zip_code,
        company,

        -- dates + derived
        date_received,
        date_sent_to_company,
        datediff('day', date_received, date_sent_to_company)  as days_received_to_company,
        date_trunc('month', date_received)                    as received_month,
        date_trunc('year', date_received)                     as received_year,

        -- complaint taxonomy
        product,
        sub_product,
        issue,
        sub_issue,

        -- intake + outcome
        submitted_via,
        company_response,
        company_public_response,
        is_timely,
        has_narrative,
        tags,
        complaint_narrative,

        -- flags
        case when company_response ilike 'Closed%' then true else false end  as is_closed,

        -- source tag
        'fed_cfpb_complaints'                                 as source_id,

        -- metadata
        _ingested_at,
        _source_run_id

    from base

)

select * from enriched
