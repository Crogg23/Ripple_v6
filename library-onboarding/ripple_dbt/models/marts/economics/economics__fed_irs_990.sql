{{ config(materialized='table', schema='ECONOMICS') }}

-- GRAIN: one row per organization (EIN is unique â€” latest filing kept)
-- Answers: What are the financials of every tax-exempt org in the US?
-- Source: IRS Form 990 e-File Index (~5.5M filings, deduped to latest per EIN)
-- Key joins: spine_entity_id â†’ ENTITY_GOLDEN; ein â†’ IRS BMF for classification

select
    ein,
    trim(organizationname)                         as organization_name,
    try_to_date(taxperiodbegindt, 'YYYYMMDD')      as tax_period_begin_date,
    try_to_date(taxperiodenddt, 'YYYYMMDD')        as tax_period_end_date,
    trim(formtype)                                 as form_type,
    try_to_number(taxyr)                           as tax_year,
    try_to_number(grossreceiptsamt)                as gross_receipts_amt,
    try_to_number(totalassetseoyamt)               as total_assets_eoy_amt,
    try_to_number(totalliabilitieseoyamt)          as total_liabilities_eoy_amt,
    try_to_number(totalrevenueamt)                 as total_revenue_amt,
    try_to_number(totalexpensesamt)                as total_expenses_amt,
    try_to_number(officercompensationamt)          as officer_compensation_amt,
    trim(usaddress_stateabbreviationcd)            as state,
    trim(usaddress_zipcd)                          as zip_code,
    trim(exemptioncd)                              as exemption_code,
    spine_entity_id,
    _loaded_at,
    _source_url
from {{ ref('stg_fed_irs_990__organizations') }}
