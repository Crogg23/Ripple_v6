{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2b) from live-verified specs.
  IRS Form 8872 periodic reports of 527 orgs (contribution/expenditure totals; form_id_number unique).
  Grain: one row = one Form 8872 report.
*/

with source as (
    select * from {{ source('ripple_raw', 'IRS527_8872_REPORTS') }}
),

renamed as (
    select
        nullif(trim(FORM_TYPE), '')                                    as form_type,
        nullif(trim(FORM_ID_NUMBER), '')                               as form_id_number,
        try_to_date(nullif(trim(PERIOD_BEGIN_DATE), ''), 'YYYYMMDD')   as period_begin_date,
        try_to_date(nullif(trim(PERIOD_END_DATE), ''), 'YYYYMMDD')     as period_end_date,
        nullif(trim(INITIAL_REPORT_IND), '')                           as initial_report_ind,
        nullif(trim(AMENDED_REPORT_IND), '')                           as amended_report_ind,
        nullif(trim(FINAL_REPORT_IND), '')                             as final_report_ind,
        nullif(trim(CHANGE_OF_ADDRESS_IND), '')                        as change_of_address_ind,
        nullif(trim(ORGANIZATION_NAME), '')                            as organization_name,
        nullif(trim(EIN), '')                                          as ein,
        nullif(trim(MAILING_ADDR1), '')                                as mailing_addr1,
        nullif(trim(MAILING_ADDR2), '')                                as mailing_addr2,
        nullif(trim(MAILING_CITY), '')                                 as mailing_city,
        nullif(trim(MAILING_STATE), '')                                as mailing_state,
        nullif(trim(MAILING_ZIP), '')                                  as mailing_zip,
        nullif(trim(MAILING_ZIP_EXT), '')                              as mailing_zip_ext,
        nullif(trim(EMAIL_ADDRESS), '')                                as email_address,
        try_to_date(nullif(trim(ORG_FORMATION_DATE), ''), 'YYYYMMDD')  as org_formation_date,
        nullif(trim(CUSTODIAN_NAME), '')                               as custodian_name,
        nullif(trim(CUSTODIAN_ADDR1), '')                              as custodian_addr1,
        nullif(trim(CUSTODIAN_ADDR2), '')                              as custodian_addr2,
        nullif(trim(CUSTODIAN_CITY), '')                               as custodian_city,
        nullif(trim(CUSTODIAN_STATE), '')                              as custodian_state,
        nullif(trim(CUSTODIAN_ZIP), '')                                as custodian_zip,
        nullif(trim(CUSTODIAN_ZIP_EXT), '')                            as custodian_zip_ext,
        nullif(trim(CONTACT_NAME), '')                                 as contact_name,
        nullif(trim(CONTACT_ADDR1), '')                                as contact_addr1,
        nullif(trim(CONTACT_ADDR2), '')                                as contact_addr2,
        nullif(trim(CONTACT_CITY), '')                                 as contact_city,
        nullif(trim(CONTACT_STATE), '')                                as contact_state,
        nullif(trim(CONTACT_ZIP), '')                                  as contact_zip,
        nullif(trim(CONTACT_ZIP_EXT), '')                              as contact_zip_ext,
        nullif(trim(BUSINESS_ADDR1), '')                               as business_addr1,
        nullif(trim(BUSINESS_ADDR2), '')                               as business_addr2,
        nullif(trim(BUSINESS_CITY), '')                                as business_city,
        nullif(trim(BUSINESS_STATE), '')                               as business_state,
        nullif(trim(BUSINESS_ZIP), '')                                 as business_zip,
        nullif(trim(BUSINESS_ZIP_EXT), '')                             as business_zip_ext,
        nullif(trim(QTR_INDICATOR), '')                                as qtr_indicator,
        nullif(trim(MONTHLY_RPT_MONTH), '')                            as monthly_rpt_month,
        nullif(trim(PRE_ELECT_TYPE), '')                               as pre_elect_type,
        try_to_date(nullif(trim(PRE_OR_POST_ELECT_DATE), ''), 'YYYYMMDD') as pre_or_post_elect_date,
        nullif(trim(PRE_OR_POST_ELECT_STATE), '')                      as pre_or_post_elect_state,
        nullif(trim(SCHED_A_IND), '')                                  as sched_a_ind,
        try_to_number(nullif(trim(TOTAL_SCHED_A), ''), 18, 2)          as total_sched_a,
        nullif(trim(SCHED_B_IND), '')                                  as sched_b_ind,
        try_to_number(nullif(trim(TOTAL_SCHED_B), ''), 18, 2)          as total_sched_b,
        try_to_timestamp_ntz(nullif(trim(INSERT_DATETIME), ''))        as insert_datetime,
        to_timestamp_ntz(INGESTED_AT, 6)                               as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                                as _source_run_id
    from source
)

select * from renamed
