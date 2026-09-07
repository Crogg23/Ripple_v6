{{ config(materialized='view') }}

/*
  FDIC Enforcement Decisions and Orders, one row per order, landed 2026-09-07
  by scripts/fdic_enforcement_load.py off the orders.fdic.gov Aura endpoint.
  10,838 orders, 1975-06-11 to 2026-07-31, 23 with no issued date.

  This is NOT FED_FDIC_ENFORCEMENT (14 rows): that table is the fdic.gov
  navigation menu scraped as data and stays disabled.

  Grain: ORDER_ID (Salesforce Id) is unique on all 10,838 rows. DOCKET_NUMBER
  is NOT: 8,302 distinct, because one docket carries an order, a modification
  and a termination as separate rows, and some rows hold two dockets in one
  string ("FDIC-21-0034e, FDIC-22-0024k").

  CERT_NUMBER is the first bank named on the order. 183 rows read 'N/A' and 49
  are blank (adjudicated decisions with the bank redacted, and Section 19
  letters about a person with no bank). try_to_number turns those to NULL.
  10,606 rows carry a numeric cert; 10,565 of them match a CERT in
  FED_FDIC_BANK_DATA (27,836 institutions, CERT unique there).

  ORDER_TYPE is a semicolon list on 202+ rows ("Assessment of Civil Money
  Penalty;Removal/Prohibition Order"). Filter with LIKE or split; equality on
  the whole string undercounts each type.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_FDIC_ENFORCEMENT_ORDERS') }}
),

renamed as (
    select
        nullif(trim(ORDER_ID), '')                                 as order_id,
        try_to_date(nullif(trim(ORDER_ISSUED_DATE), ''))           as order_date,
        nullif(trim(ORDER_TITLE), '')                              as order_title,
        nullif(trim(DOCKET_NUMBER), '')                            as docket_number,
        nullif(trim(ORDER_CATEGORY), '')                           as order_category,
        nullif(trim(ORDER_TYPE), '')                               as order_type,
        nullif(nullif(trim(BANK_NAME), ''), 'N/A')                 as institution_name,
        nullif(nullif(trim(BANK_CITY), ''), 'N/A')                 as city,
        nullif(nullif(trim(BANK_STATE), ''), 'N/A')                as state,
        nullif(nullif(trim(CERT_NUMBER), ''), 'N/A')               as cert_number_raw,
        try_to_number(nullif(trim(CERT_NUMBER), ''))               as cert_number,
        try_to_number(nullif(trim(BANK_COUNT), ''))                as bank_count,
        nullif(trim(BANKS_ALL), '')                                as banks_all,
        nullif(trim(RESPONDENTS), '')                              as respondents,
        try_to_number(nullif(trim(RESPONDENT_COUNT), ''))          as respondent_count,
        try_to_number(nullif(trim(CMP_AMOUNT_TOTAL), ''), 18, 2)   as cmp_amount_total,
        try_to_number(nullif(trim(RESTITUTION_AMOUNT_TOTAL), ''), 18, 2) as restitution_amount_total,
        nullif(nullif(trim(NMLS_IDS), ''), 'N/A')                  as nmls_ids,
        try_to_date(nullif(trim(TERMINATION_DATE), ''))            as termination_date,
        nullif(trim(TERMINATION_COMMENTS), '')                     as termination_comments,
        nullif(trim(PUBLIC_ORDER_ACTION), '')                      as public_order_action,
        nullif(trim(STATUS), '')                                   as status,
        nullif(trim(DOCUMENT_URL), '')                             as document_url,
        RAW_JSON                                                   as raw_json,
        try_to_timestamp_tz(INGESTED_AT)                           as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                           as _source_run_id
    from source
)

select * from renamed
