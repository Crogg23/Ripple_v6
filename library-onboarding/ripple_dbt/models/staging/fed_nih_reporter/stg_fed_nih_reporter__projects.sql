{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 (73-source backlog, wave 2). NIH RePORTER grant
  projects, full 27-fiscal-year crawl (FY2000-FY2026) by
  scripts/nih_reporter_load.py -- replaces the FY2000-2002-only slice the
  catalog previously mislabeled as fully landed.
  Grain: one row = one application (appl_id unique; the loader dedupes by
  appl_id both in Python and SQL before the atomic swap).
  Landing is all-VARCHAR by design (see loader header); dates are ISO
  strings; amounts are numeric strings.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_NIH_REPORTER') }}
),

renamed as (
    select
        nullif(trim(APPL_ID), '')                          as appl_id,
        nullif(trim(SUBPROJECT_ID), '')                    as subproject_id,
        try_to_number(nullif(trim(FISCAL_YEAR), ''))       as fiscal_year,
        nullif(trim(PROJECT_NUM), '')                      as project_num,
        nullif(trim(CORE_PROJECT_NUM), '')                 as core_project_num,
        nullif(trim(ORG_NAME), '')                         as org_name,
        nullif(trim(ORG_CITY), '')                         as org_city,
        nullif(trim(ORG_STATE), '')                        as org_state,
        nullif(trim(ORG_STATE_NAME), '')                   as org_state_name,
        nullif(trim(ORG_COUNTRY), '')                      as org_country,
        nullif(trim(ORG_DUNS), '')                         as org_duns,
        nullif(trim(ORG_UEI), '')                          as org_uei,
        nullif(trim(ORG_IPF_CODE), '')                     as org_ipf_code,
        nullif(trim(ORG_ZIP), '')                          as org_zip,
        nullif(trim(ORG_FIPS), '')                         as org_fips,
        nullif(trim(DEPT_TYPE), '')                        as dept_type,
        nullif(trim(ORG_DEPT), '')                         as org_dept,
        nullif(trim(PI_NAMES), '')                         as pi_names,
        nullif(trim(PI_PROFILE_IDS), '')                   as pi_profile_ids,
        nullif(trim(PO_NAMES), '')                         as po_names,
        nullif(trim(PROJECT_TITLE), '')                    as project_title,
        nullif(trim(ABSTRACT_TEXT), '')                    as abstract_text,
        try_to_date(left(nullif(trim(PROJECT_START_DATE), ''), 10)) as project_start_date,
        try_to_date(left(nullif(trim(PROJECT_END_DATE), ''), 10))   as project_end_date,
        try_to_date(left(nullif(trim(BUDGET_START_DATE), ''), 10))  as budget_start_date,
        try_to_date(left(nullif(trim(BUDGET_END_DATE), ''), 10))    as budget_end_date,
        try_to_date(left(nullif(trim(AWARD_NOTICE_DATE), ''), 10))  as award_notice_date,
        try_to_timestamp_ntz(nullif(trim(DATE_ADDED), ''))          as date_added,
        try_to_number(nullif(trim(AWARD_AMOUNT), ''), 18, 2)        as award_amount,
        try_to_number(nullif(trim(DIRECT_COST_AMT), ''), 18, 2)     as direct_cost_amt,
        try_to_number(nullif(trim(INDIRECT_COST_AMT), ''), 18, 2)   as indirect_cost_amt,
        nullif(trim(AGENCY_CODE), '')                      as agency_code,
        nullif(trim(ACTIVITY_CODE), '')                    as activity_code,
        nullif(trim(AWARD_TYPE), '')                       as award_type,
        nullif(trim(FUNDING_MECHANISM), '')                as funding_mechanism,
        nullif(trim(OPPORTUNITY_NUMBER), '')               as opportunity_number,
        nullif(trim(CFDA_CODE), '')                        as cfda_code,
        nullif(trim(ARRA_FUNDED), '')                      as arra_funded,
        nullif(trim(COVID_RESPONSE), '')                   as covid_response,
        nullif(trim(SPENDING_CATEGORIES), '')              as spending_categories,
        nullif(trim(STUDY_SECTION), '')                    as study_section,
        nullif(trim(STUDY_SECTION_NAME), '')               as study_section_name,
        nullif(trim(SRG_CODE), '')                         as srg_code,
        nullif(trim(CONG_DIST), '')                        as cong_dist,
        nullif(trim(REPORTER_PROJECT_URL), '')             as reporter_project_url,
        nullif(trim(TERMS), '')                            as terms,
        _INGESTED_AT                                       as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                   as _source_run_id
    from source
)

select * from renamed
