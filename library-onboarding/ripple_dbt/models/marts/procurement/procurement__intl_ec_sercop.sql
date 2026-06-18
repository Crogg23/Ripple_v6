{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_intl_ec_sercop__contracting_process') }}

)

select

    -- cross-source key identifiers
    'intl_ec_sercop'                    as source_id,
    'ocds-5wno2w'                       as ocds_prefix,
    ocid,
    id                                  as record_id,
    date                                as record_date,
    buyer_id                            as company_id,

    -- record metadata
    tag,
    initiation_type,
    language,

    -- buyer
    buyer_id,
    buyer_name,

    -- tender block
    tender_id,
    tender_title,
    tender_status,
    tender_procurement_method,
    tender_value_amount,
    tender_value_currency,
    tender_date_published,

    -- award block
    award_id,
    award_date,
    award_status,
    award_value_amount,
    award_value_currency,

    -- supplier
    supplier_id,
    supplier_name,

    -- contract block
    contract_id,
    contract_date_signed,
    contract_value_amount,
    contract_value_currency,

    -- parties
    parties_id,
    parties_name,
    parties_roles,

    -- planning
    planning_budget_amount,

    -- pipeline metadata
    _ingested_at,
    _source_run_id

from base
