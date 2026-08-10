{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 (73-source backlog, wave 2). IRS Exempt Organizations
  Business Master File (EO BMF): every organization the IRS recognizes as
  tax-exempt, cumulative national extract (regions 1-4 unioned at load time
  by scripts/irs_eo_bmf_full_load.py after the 2026-08-07 sweep landed only
  region 1 / the Northeast).
  Grain: one row = one exempt organization; EIN verified unique
  (1,983,563 = 1,983,563 on the 2026-08-09 full re-ingest).
  RULING and TAX_PERIOD are YYYYMM strings; NTEE code is blank on ~29% of
  rows (typically older/church registrations) as published by the IRS.
  INGESTED_AT is epoch microseconds (write_pandas numeric timestamp).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_IRS_EO_BMF') }}
),

renamed as (
    select
        nullif(trim(EIN), '')                              as ein,
        nullif(trim(NAME), '')                             as org_name,
        nullif(trim(ICO), '')                              as in_care_of,
        nullif(trim(STREET), '')                           as street,
        nullif(trim(CITY), '')                             as city,
        nullif(trim(STATE), '')                            as state,
        nullif(trim(ZIP), '')                              as zip,
        nullif(trim(C_GROUP), '')                          as group_exemption_num,
        nullif(trim(SUBSECTION), '')                       as subsection_code,
        nullif(trim(AFFILIATION), '')                      as affiliation_code,
        nullif(trim(CLASSIFICATION), '')                   as classification_code,
        nullif(trim(RULING), '')                           as ruling_yyyymm,
        try_to_date(nullif(trim(RULING), '') || '01', 'YYYYMMDD')     as ruling_date,
        nullif(trim(DEDUCTIBILITY), '')                    as deductibility_code,
        nullif(trim(FOUNDATION), '')                       as foundation_code,
        nullif(trim(ACTIVITY), '')                         as activity_codes,
        nullif(trim(C_ORGANIZATION), '')                   as organization_code,
        nullif(trim(STATUS), '')                           as status_code,
        nullif(trim(TAX_PERIOD), '')                       as tax_period_yyyymm,
        try_to_date(nullif(trim(TAX_PERIOD), '') || '01', 'YYYYMMDD') as tax_period_month,
        nullif(trim(ASSET_CD), '')                         as asset_code,
        nullif(trim(INCOME_CD), '')                        as income_code,
        nullif(trim(FILING_REQ_CD), '')                    as filing_req_code,
        nullif(trim(PF_FILING_REQ_CD), '')                 as pf_filing_req_code,
        nullif(trim(ACCT_PD), '')                          as accounting_period_month,
        try_to_number(ASSET_AMT)                           as asset_amt,
        try_to_number(INCOME_AMT)                          as income_amt,
        try_to_number(REVENUE_AMT)                         as revenue_amt,
        nullif(trim(NTEE_CD), '')                          as ntee_code,
        nullif(trim(SORT_NAME), '')                        as sort_name,
        to_timestamp_ntz(INGESTED_AT, 6)                   as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                    as _source_run_id
    from source
)

select * from renamed
