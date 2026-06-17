{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_doj_fca_settlements__fca_settlements') }}

)

select
    -- primary key
    fca_settlement_id,

    -- key identifiers for cross-source joins
    company_id,
    person_name,
    date                        as settlement_date,

    -- case details
    case_title,
    case_number,
    district,
    fiscal_year,

    -- financial
    settlement_amount,
    is_qui_tam,
    relator_name,
    relator_share,

    -- classification
    fraud_type,
    agency_defrauded,

    -- reference links
    press_release_url,
    source_url,

    -- metadata
    _ingested_at,
    _source_run_id

from base
