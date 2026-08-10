{{ config(materialized='view') }}

/*
  Generated 2026-08-10 (backlog wave 4) from live-verified specs.
  PCAOB Form AP filings: which engagement (audit) partner signed which
  public-company audit, by audit firm and issuer. ISSUER_CIK joins to SEC
  EDGAR/DERA data.
  Grain: one row = one Form AP filing (FORM_FILING_ID verified exactly unique).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_PCAOB_FORM_AP_FILINGS') }}
),

renamed as (
    select
        -- identifiers
        nullif(trim(FORM_FILING_ID), '')                           as form_filing_id,
        nullif(trim(LATEST_FORM_AP_FILING), '')                    as latest_form_ap_filing,
        nullif(trim(ORIGINAL_FIRM_FORM_ID), '')                    as original_firm_form_id,
        nullif(trim(AMENDS_FIRM_FORM_ID), '')                      as amends_firm_form_id,

        -- audit firm
        nullif(trim(FIRM_ID), '')                                  as firm_id,
        nullif(trim(FIRM_NAME), '')                                as firm_name,
        nullif(trim(FIRM_OTHER_NAME), '')                          as firm_other_name,
        nullif(trim(FIRM_COUNTRY), '')                             as firm_country,
        nullif(trim(FIRM_ISSUING_COUNTRY), '')                     as firm_issuing_country,
        nullif(trim(FIRM_ISSUING_STATE), '')                       as firm_issuing_state,
        nullif(trim(FIRM_ISSUING_CITY), '')                        as firm_issuing_city,

        -- issuer
        nullif(trim(ISSUER_ID), '')                                as issuer_id,
        nullif(trim(ISSUER_NAME), '')                              as issuer_name,
        nullif(trim(ISSUER_CIK), '')                               as issuer_cik,
        ISSUER_TICKER_NOT_AVAILABLE                                as issuer_ticker_not_available,
        nullif(trim(ISSUER_CIK_NONE), '')                          as issuer_cik_none,
        nullif(trim(AUDIT_FUND_SERIES), '')                        as audit_fund_series,

        -- audit report
        nullif(trim(AUDIT_REPORT_TYPE), '')                        as audit_report_type,
        try_to_date(nullif(trim(AUDIT_REPORT_DATE), ''))           as audit_report_date,
        try_to_date(nullif(trim(FISCAL_PERIOD_END_DATE), ''))      as fiscal_period_end_date,
        nullif(trim(IS_MULTIPLE_AUDIT_PERIOD), '')                 as is_multiple_audit_period,
        nullif(trim(AUDIT_PERIOD_INFORMATION), '')                 as audit_period_information,
        nullif(trim(DUAL_DATED), '')                               as dual_dated,
        nullif(trim(AUDIT_DUAL_DATE), '')                          as audit_dual_date,

        -- engagement partner
        nullif(trim(ENGAGEMENT_PARTNER_ID), '')                    as engagement_partner_id,
        nullif(trim(ENGAGEMENT_PARTNER_LAST_NAME), '')             as engagement_partner_last_name,
        nullif(trim(ENGAGEMENT_PARTNER_FIRST_NAME), '')            as engagement_partner_first_name,
        nullif(trim(ENGAGEMENT_PARTNER_MIDDLE_NAME), '')           as engagement_partner_middle_name,
        nullif(trim(ENGAGEMENT_PARTNER_SUFFIX), '')                as engagement_partner_suffix,
        nullif(trim(ENGAGEMENT_PARTNER_OTHER_IDS), '')             as engagement_partner_other_ids,
        nullif(trim(SECONDARY_ENGAGEMENT_PARTNER_ID), '')          as secondary_engagement_partner_id,
        nullif(trim(SECONDARY_ENGAGEMENT_PARTNER_LAST_NAME), '')   as secondary_engagement_partner_last_name,
        nullif(trim(SECONDARY_ENGAGEMENT_PARTNER_FIRST_NAME), '')  as secondary_engagement_partner_first_name,
        nullif(trim(SECONDARY_ENGAGEMENT_PARTNER_MIDDLE_NAME), '') as secondary_engagement_partner_middle_name,
        nullif(trim(SECONDARY_ENGAGEMENT_PARTNER_SUFFIX), '')      as secondary_engagement_partner_suffix,
        nullif(trim(SECONDARY_ENGAGEMENT_PARTNER_OTHER_IDS), '')   as secondary_engagement_partner_other_ids,

        -- amendment flags
        nullif(trim(AMENDMENT_PREVIOUS_FILING), '')                as amendment_previous_filing,
        nullif(trim(AMENDMENT_FIRM_IDENTIFICATION), '')            as amendment_firm_identification,
        nullif(trim(AMENDMENT_AUDIT_REPORT), '')                   as amendment_audit_report,
        nullif(trim(AMENDMENT_OTHER_FIRMS), '')                    as amendment_other_firms,
        nullif(trim(AMENDMENT_DIVIDED_RESPONSIBILITY), '')         as amendment_divided_responsibility,
        nullif(trim(AMENDMENT_PARTICIPANTS__GT__5), '')            as amendment_participants_gt_5,
        nullif(trim(AMENDMENT_PARTICIPANTS__LT__5), '')            as amendment_participants_lt_5,
        nullif(trim(AMENDMENT_AUDIT_DIVIDED), '')                  as amendment_audit_divided,
        nullif(trim(AMENDMENT_CERTIFIED_FIRM), '')                 as amendment_certified_firm,
        nullif(trim(AMENDMENT_CERTIFIED_FIRM_INFO), '')            as amendment_certified_firm_info,

        -- divided responsibility / participants
        nullif(trim(IS_AUDIT_NOT_DIVIDED), '')                     as is_audit_not_divided,
        nullif(trim(IS_AUDIT_DIVIDED), '')                         as is_audit_divided,
        nullif(trim(USE_RANGE), '')                                as use_range,
        nullif(trim(AUDIT_NOT_DIVIDED_PERCENT_INFORMATION), '')    as audit_not_divided_percent_information,
        try_to_number(trim(NUMBER_OF_PARTICIPANTS))                as number_of_participants,
        nullif(trim(PARTICIPANT_PERCENTAGE), '')                   as participant_percentage,
        nullif(trim(PARTICIPANT_RANGE), '')                        as participant_range,
        nullif(trim(AUDIT_DIVIDED_INFORMATION), '')                as audit_divided_information,

        -- signature block
        nullif(trim(SIGNED_LAST_NAME), '')                         as signed_last_name,
        nullif(trim(SIGNED_FIRST_NAME), '')                        as signed_first_name,
        try_to_date(nullif(trim(SIGNED_DATE), ''))                 as signed_date,
        nullif(trim(SIGNED_BUSINESS_TITLE), '')                    as signed_business_title,
        nullif(trim(SIGNED_CAPACITY), '')                          as signed_capacity,
        nullif(trim(SIGNED_PHONE_NUMBER), '')                      as signed_phone_number,
        nullif(trim(SIGNED_EMAIL_ADDRESS), '')                     as signed_email_address,

        -- filing
        try_to_date(nullif(trim(FILING_DATE), ''))                 as filing_date,

        -- metadata
        to_timestamp_ntz(INGESTED_AT, 6)                           as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                            as _source_run_id
    from source
)

select * from renamed
