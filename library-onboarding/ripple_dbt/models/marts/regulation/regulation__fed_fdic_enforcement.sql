{{ config(materialized='table') }}

with base as (

    select *
    from {{ ref('stg_fed_fdic_enforcement__enforcement_orders') }}

)

select

    -- surrogate / natural keys
    {{ dbt_utils.generate_surrogate_key(['docket_number', 'fdic_cert_number', "coalesce(person_name, respondent_name)"]) }}
                                    as enforcement_order_id,

    -- cross-source join identifiers
    company_id,
    fdic_cert_number,
    docket_number,
    nmls_id,
    respondent_name,
    person_name,
    date                            as order_date,

    -- descriptive attributes
    institution_name,
    city,
    state,
    action_type,
    termination_date,

    -- source reference
    order_url,
    raw_text,

    -- metadata
    _ingested_at,
    _source_run_id,

    -- source system tag for cross-source federation
    'fed_fdic_enforcement'          as source_id

from base
