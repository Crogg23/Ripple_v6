{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 (73-source backlog, wave 2). US Consolidated
  Screening List (trade.gov): the merged export-control/sanctions screening
  list across 13 federal lists (BIS DPL/Entity List, OFAC SDN, State ISN...).
  Grain: one row = one list entry. ID is NOT quite unique (25,918 rows /
  25,822 distinct): ~96 ids appear twice with differing name/source as
  published -- no unique test, documented instead.
  Dates are ISO YYYY-MM-DD.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_CONSOLIDATED_SCREENING_LIST') }}
),

renamed as (
    select
        nullif(trim(ID), '')                          as entry_id,
        nullif(trim(SOURCE), '')                      as source_list,
        nullif(trim(ENTITY_NUMBER), '')               as entity_number,
        nullif(trim(TYPE), '')                        as entity_type,
        nullif(trim(PROGRAMS), '')                    as programs,
        nullif(trim(NAME), '')                        as name,
        nullif(trim(TITLE), '')                       as title,
        nullif(trim(ADDRESSES), '')                   as addresses,
        nullif(trim(FEDERAL_REGISTER_NOTICE), '')     as federal_register_notice,
        try_to_date(nullif(trim(START_DATE), ''))     as start_date,
        try_to_date(nullif(trim(END_DATE), ''))       as end_date,
        nullif(trim(STANDARD_ORDER), '')              as standard_order,
        nullif(trim(LICENSE_REQUIREMENT), '')         as license_requirement,
        nullif(trim(LICENSE_POLICY), '')              as license_policy,
        nullif(trim(CALL_SIGN), '')                   as call_sign,
        nullif(trim(VESSEL_TYPE), '')                 as vessel_type,
        nullif(trim(VESSEL_FLAG), '')                 as vessel_flag,
        nullif(trim(VESSEL_OWNER), '')                as vessel_owner,
        nullif(trim(REMARKS), '')                     as remarks,
        nullif(trim(SOURCE_LIST_URL), '')             as source_list_url,
        nullif(trim(ALT_NAMES), '')                   as alt_names,
        nullif(trim(CITIZENSHIPS), '')                as citizenships,
        nullif(trim(DATES_OF_BIRTH), '')              as dates_of_birth,
        nullif(trim(NATIONALITIES), '')               as nationalities,
        nullif(trim(PLACES_OF_BIRTH), '')             as places_of_birth,
        nullif(trim(IDS), '')                         as identifier_documents,
        -- meta columns landed UNPREFIXED by the 2026-08-22 re-pull (loader
        -- family drift); repointed 2026-08-22 after the view broke.
        to_timestamp_ntz(INGESTED_AT, 6)              as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')               as _source_run_id
    from source
)

select * from renamed
