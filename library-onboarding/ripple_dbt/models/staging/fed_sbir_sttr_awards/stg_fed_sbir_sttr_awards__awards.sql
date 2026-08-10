{{ config(materialized='view') }}

/*
  Generated 2026-08-10 (backlog wave 4) from live-verified specs.
  Federal SBIR/STTR small-business research awards across agencies, with
  company identifiers (UEI, DUNS) usable as cross-dataset join keys.
  Grain: one row = one award record.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_SBIR_STTR_AWARDS') }}
),

keyed as (
    -- The composite (AGENCY, PHASE, PROGRAM, AGENCY_TRACKING_NUMBER, CONTRACT,
    -- AWARD_YEAR) is NEAR-unique (219,376 distinct of 219,503 rows). The
    -- collisions are distinct records differing in other fields, so a
    -- row_number() over the full-row hash is appended as a deterministic
    -- provenance tiebreaker to make award_record_id fully unique.
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['AGENCY', 'PHASE', 'PROGRAM', 'AGENCY_TRACKING_NUMBER', 'CONTRACT', 'AWARD_YEAR']) }}
            || '-'
            || row_number() over (
                   partition by AGENCY, PHASE, PROGRAM, AGENCY_TRACKING_NUMBER, CONTRACT, AWARD_YEAR
                   order by hash(*)
               ) as award_record_id
    from source
),

renamed as (
    select
        -- identifiers
        award_record_id,
        nullif(trim(AGENCY), '')                                   as agency,
        nullif(trim(BRANCH), '')                                   as branch,
        nullif(trim(PHASE), '')                                    as phase,
        nullif(trim(PROGRAM), '')                                  as program,
        nullif(trim(AGENCY_TRACKING_NUMBER), '')                   as agency_tracking_number,
        nullif(trim(CONTRACT), '')                                 as contract,
        nullif(trim(UEI), '')                                      as uei,
        nullif(trim(DUNS), '')                                     as duns,

        -- award
        nullif(trim(AWARD_TITLE), '')                              as award_title,
        try_to_number(trim(AWARD_YEAR))                            as award_year,
        try_to_number(trim(AWARD_AMOUNT), 18, 2)                   as award_amount,
        try_to_date(nullif(trim(PROPOSAL_AWARD_DATE), ''))         as proposal_award_date,
        try_to_date(nullif(trim(CONTRACT_END_DATE), ''))           as contract_end_date,
        nullif(trim(SOLICITATION_NUMBER), '')                      as solicitation_number,
        try_to_number(trim(SOLICITATION_YEAR))                     as solicitation_year,
        try_to_date(nullif(trim(SOLICITATION_CLOSE_DATE), ''))     as solicitation_close_date,
        try_to_date(nullif(trim(PROPOSAL_RECEIPT_DATE), ''))       as proposal_receipt_date,
        try_to_date(nullif(trim(DATE_OF_NOTIFICATION), ''))        as date_of_notification,
        nullif(trim(TOPIC_CODE), '')                               as topic_code,

        -- company
        nullif(trim(COMPANY), '')                                  as company,
        nullif(trim(HUBZONE_OWNED), '')                            as hubzone_owned,
        nullif(trim(SOCIALLY_AND_ECONOMICALLY_DISADVANTAGED), '')  as socially_and_economically_disadvantaged,
        nullif(trim(WOMAN_OWNED), '')                              as woman_owned,
        try_to_number(trim(NUMBER_EMPLOYEES))                      as number_employees,
        nullif(trim(COMPANY_WEBSITE), '')                          as company_website,
        nullif(trim(ADDRESS1), '')                                 as address1,
        nullif(trim(ADDRESS2), '')                                 as address2,
        nullif(trim(CITY), '')                                     as city,
        nullif(trim(STATE), '')                                    as state,
        nullif(trim(ZIP), '')                                      as zip,

        -- people
        nullif(trim(CONTACT_NAME), '')                             as contact_name,
        nullif(trim(CONTACT_TITLE), '')                            as contact_title,
        nullif(trim(CONTACT_PHONE), '')                            as contact_phone,
        nullif(trim(CONTACT_EMAIL), '')                            as contact_email,
        nullif(trim(PI_NAME), '')                                  as pi_name,
        nullif(trim(PI_TITLE), '')                                 as pi_title,
        nullif(trim(PI_PHONE), '')                                 as pi_phone,
        nullif(trim(PI_EMAIL), '')                                 as pi_email,
        nullif(trim(RI_NAME), '')                                  as ri_name,
        nullif(trim(RI_POC_NAME), '')                              as ri_poc_name,
        nullif(trim(RI_POC_PHONE), '')                             as ri_poc_phone,

        -- metadata
        to_timestamp_ntz(INGESTED_AT, 6)                           as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                            as _source_run_id
    from keyed
)

select * from renamed
