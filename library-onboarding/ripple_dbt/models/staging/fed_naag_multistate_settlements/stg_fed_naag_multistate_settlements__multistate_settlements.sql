{{ config(materialized='view') }}

/*
  REWRITTEN 2026-08-22 (fix session, dbt-suite ERROR triage): the 2026-08-22
  freshness re-pull landed NAAG's real database export with a completely
  different, richer schema (case number, defendants, AG coalitions, amounts).
  The prior staging targeted the old company_id/date/state shape and broke.
  Grain: one row = one multistate settlement entry; ID verified unique
  (882 = 882, zero null) against the live table on rewrite day.
  Dates arrive as M/D/YYYY text.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_NAAG_MULTISTATE_SETTLEMENTS') }}
),

renamed as (
    select
        nullif(trim(ID), '')                                   as id,
        nullif(trim(SORT_ID), '')                              as sort_id,
        nullif(trim(C_CASE), '')                               as case_number,
        try_to_number(nullif(trim(YEAR), ''))                  as year,
        try_to_date(nullif(trim(DATERESOLVED), ''), 'MM/DD/YYYY')   as date_resolved,
        try_to_date(nullif(trim(DATE_FILED), ''), 'MM/DD/YYYY')     as date_filed,
        nullif(trim(DEFENDANTS), '')                           as defendants,
        nullif(trim(ADDITIONALDEFENDANTS), '')                 as additional_defendants,
        try_to_double(nullif(trim(TOTALSETTLEMENTAMOUNT), '')) as total_settlement_amount,
        try_to_double(nullif(trim(TOTALSTATESHARE), ''))       as total_state_share,
        try_to_double(nullif(trim(TOTAL_FEDERAL_SHARE), ''))   as total_federal_share,
        nullif(trim(LEADAGS), '')                              as lead_ags,
        nullif(trim(PARTICIPATINGAGS), '')                     as participating_ags,
        nullif(trim(INDUSTRYTYPE), '')                         as industry_type,
        nullif(trim(ISSUEAREAGENERAL), '')                     as issue_area_general,
        nullif(trim(ISSUEAREASPECIFIC), '')                    as issue_area_specific,
        nullif(trim(ENFORCEMENTCAMPAIGN), '')                  as enforcement_campaign,
        nullif(trim(PRODUCT_INVOLVED), '')                     as product_involved,
        nullif(trim(DESCRIPTION), '')                          as description,
        nullif(trim(LEGAL_BASIS), '')                          as legal_basis,
        nullif(trim(SETTLEMENT_PROVISION_TYPES), '')           as settlement_provision_types,
        nullif(trim(KEYSETTLEMENTTERMS), '')                   as key_settlement_terms,
        nullif(trim(CONSUMER_RESTITUTION), '')                 as consumer_restitution,
        nullif(trim(CORPORATE_MONITOR_PROVISION), '')          as corporate_monitor_provision,
        nullif(trim(CORPORATEHEADQUARTERS), '')                as corporate_headquarters,
        nullif(trim(RELATED6DIGITNAICSCODE), '')               as naics6_code,
        nullif(trim(RELATED4DIGITNAICSCODE), '')               as naics4_code,
        nullif(trim(COURT_LEVEL), '')                          as court_level,
        nullif(trim(CITATION), '')                             as citation,
        nullif(trim(LOCATION_SETTLEMENT_FILED), '')            as location_settlement_filed,
        nullif(trim(FEDERALINVOLVEMENT), '')                   as federal_involvement,
        nullif(trim(PRESIDENTIALADMINISTRATION), '')           as presidential_administration,
        nullif(trim(SETTLEMENT_DOCUMENTS_OR_PRESS_RELEASE), '') as settlement_documents_url,
        nullif(trim(PRESS_RELEASES), '')                       as press_releases,
        to_timestamp_ntz(INGESTED_AT, 6)                       as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                        as _source_run_id
    from source
    qualify row_number() over (partition by ID order by INGESTED_AT desc) = 1
)

select * from renamed
