{{ config(materialized='table', schema='ECONOMICS') }}

-- GRAIN: one row per organization (EIN is unique)
-- Answers: What is the current IRS classification and financial tier of every tax-exempt org?
-- Source: IRS Business Master File Extract (~1.97M organizations)
-- Key joins: spine_entity_id â†’ ENTITY_GOLDEN; ein â†’ IRS 990 for financials; ntee_cd â†’ NTEE classification

select
    ein,
    trim(name)                                     as organization_name,
    trim(sort_name)                                as sort_name,
    trim(ico)                                      as in_care_of,
    trim(street)                                   as street,
    trim(city)                                     as city,
    trim(state)                                    as state,
    trim(zip)                                      as zip,
    trim(subsection)                               as subsection_code,
    trim(classification)                           as classification_code,
    trim(affiliation)                              as affiliation_code,
    trim(deductibility)                            as deductibility_code,
    trim(foundation)                               as foundation_code,
    trim(activity)                                 as activity_code,
    trim(status)                                   as irs_status,
    trim(tax_period)                               as tax_period,
    try_to_number(asset_amt)                       as asset_amt,
    try_to_number(income_amt)                      as income_amt,
    try_to_number(revenue_amt)                     as revenue_amt,
    trim(ntee_cd)                                  as ntee_code,
    trim(ruling)                                   as ruling_date,
    trim(c_group)                                  as group_exemption_number,
    spine_entity_id,
    _loaded_at,
    _source_url
from {{ ref('stg_fed_irs_bmf__organizations') }}
