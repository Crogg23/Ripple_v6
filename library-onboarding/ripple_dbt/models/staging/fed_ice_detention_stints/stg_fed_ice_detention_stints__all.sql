{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 (73-source backlog). ICE detention stints
  (person-level, anonymized hash IDs), 2004-2026, from the Deportation Data
  Project's cleaned ICE releases.
  Grain: one row = one stint (one continuous hold at one facility within a
  detention stay). stint_id is NOT unique as landed: blank on 7,341 rows and
  a handful of true duplicate pairs remain even after excluding rows the
  publisher flagged duplicate_drop_row — kept as landed, no dedup; filter on
  duplicate_drop_row = 'True' downstream. Some book-out timestamps are
  future-dated (scheduled/projected releases as published).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_ICE_DETENTION_STINTS') }}
),

renamed as (
    select
        nullif(trim(STINT_ID), '')                                as stint_id,
        nullif(trim(STAY_ID), '')                                 as stay_id,
        nullif(trim(UNIQUE_IDENTIFIER), '')                       as person_hash,
        try_to_timestamp_tz(trim(STAY_BOOK_IN_DATE_TIME))::timestamp_ntz  as stay_book_in_at,
        try_to_timestamp_tz(trim(BOOK_IN_DATE_TIME))::timestamp_ntz       as book_in_at,
        try_to_timestamp_tz(trim(BOOK_OUT_DATE_TIME))::timestamp_ntz      as book_out_at,
        try_to_timestamp_tz(trim(STAY_BOOK_OUT_DATE_TIME))::timestamp_ntz as stay_book_out_at,
        try_to_date(trim(STAY_BOOK_OUT_DATE))                     as stay_book_out_date,
        nullif(trim(DETENTION_FACILITY), '')                      as detention_facility,
        nullif(trim(DETENTION_FACILITY_CODE), '')                 as detention_facility_code,
        nullif(trim(CITY), '')                                    as city,
        nullif(trim(STATE), '')                                   as state,
        nullif(trim(COUNTY), '')                                  as county,
        nullif(trim(BOOK_IN_SITE), '')                            as book_in_site,
        nullif(trim(BOOK_IN_AOR), '')                             as book_in_aor,
        nullif(trim(DETENTION_RELEASE_REASON), '')                as detention_release_reason,
        nullif(trim(STAY_RELEASE_REASON), '')                     as stay_release_reason,
        nullif(trim(GENDER), '')                                  as gender,
        try_to_number(trim(BIRTH_YEAR))                           as birth_year,
        nullif(trim(RELIGION), '')                                as religion,
        nullif(trim(MARITAL_STATUS), '')                          as marital_status,
        nullif(trim(ETHNICITY), '')                               as ethnicity,
        nullif(trim(RACE), '')                                    as race,
        nullif(trim(BIRTH_COUNTRY), '')                           as birth_country,
        nullif(trim(CITIZENSHIP_COUNTRY), '')                     as citizenship_country,
        nullif(trim(ENTRY_STATUS), '')                            as entry_status,
        try_to_date(trim(ENTRY_DATE))                             as entry_date,
        nullif(trim(KNOWN_TERRORIST_YES_NO), '')                  as known_terrorist_yes_no,
        nullif(trim(SUSPECTED_GANG_YES_NO), '')                   as suspected_gang_yes_no,
        nullif(trim(BOOK_IN_CRIMINALITY), '')                     as book_in_criminality,
        nullif(trim(FELON), '')                                   as felon,
        nullif(trim(MSC_CHARGE), '')                              as msc_charge,
        nullif(trim(MOST_SERIOUS_CONVICTION_CODE), '')            as most_serious_conviction_code,
        nullif(trim(MSC_CRIME_CLASS), '')                         as msc_crime_class,
        nullif(trim(MSC_CRIMINAL_CHARGE_STATUS), '')              as msc_criminal_charge_status,
        nullif(trim(MSC_CRIMINAL_CHARGE_STATUS_CODE), '')         as msc_criminal_charge_status_code,
        try_to_date(trim(MSC_CHARGE_DATE))                        as msc_charge_date,
        try_to_date(trim(MSC_CONVICTION_DATE))                    as msc_conviction_date,
        try_to_number(trim(MSC_SENTENCE_DAYS))                    as msc_sentence_days,
        try_to_number(trim(MSC_SENTENCE_MONTHS))                  as msc_sentence_months,
        try_to_number(trim(MSC_SENTENCE_YEARS))                   as msc_sentence_years,
        nullif(trim(OFFENSE_INA_236C_YES_NO), '')                 as offense_ina_236c_yes_no,
        nullif(trim(CASE_INA_236C_YES_NO), '')                    as case_ina_236c_yes_no,
        nullif(trim(CASE_STATUS), '')                             as case_status,
        nullif(trim(CASE_CATEGORY), '')                           as case_category,
        nullif(trim(CASE_THREAT_LEVEL), '')                       as case_threat_level,
        nullif(trim(DETAINEE_CLASSIFICATION), '')                 as detainee_classification,
        nullif(trim(FINAL_ORDER_YES_NO), '')                      as final_order_yes_no,
        try_to_date(trim(FINAL_ORDER_DATE))                       as final_order_date,
        nullif(trim(FINAL_CHARGE), '')                            as final_charge,
        nullif(trim(FINAL_PROGRAM), '')                           as final_program,
        try_to_date(trim(DEPARTED_DATE))                          as departed_date,
        nullif(trim(DEPARTURE_COUNTRY), '')                       as departure_country,
        try_to_number(trim(INITIAL_BOND_SET_AMOUNT))              as initial_bond_set_amount,
        try_to_date(trim(INITIAL_BOND_SET_DATE))                  as initial_bond_set_date,
        try_to_number(trim(BOND_POSTED_AMOUNT))                   as bond_posted_amount,
        try_to_date(trim(BOND_POSTED_DATE))                       as bond_posted_date,
        try_to_number(trim(INITIAL_BOND_SET_AMOUNT_LOWEST_SEEN))  as initial_bond_set_amount_lowest_seen,
        try_to_date(trim(INITIAL_BOND_SET_DATE_EARLIEST_SEEN))    as initial_bond_set_date_earliest_seen,
        try_to_number(trim(BOND_POSTED_AMOUNT_LOWEST_SEEN))       as bond_posted_amount_lowest_seen,
        try_to_date(trim(BOND_POSTED_DATE_EARLIEST_SEEN))         as bond_posted_date_earliest_seen,
        nullif(trim(DUPLICATE_LIKELY_BOND), '')                   as duplicate_likely_bond,
        nullif(trim(DUPLICATE_LIKELY_SAMEDAY), '')                as duplicate_likely_sameday,
        nullif(trim(DUPLICATE_DROP_ROW), '')                      as duplicate_drop_row,
        nullif(trim(DUPLICATE_LIKELY), '')                        as duplicate_likely,
        nullif(trim(FILE_ORIGINAL), '')                           as file_original,
        nullif(trim(SHEET_ORIGINAL), '')                          as sheet_original,
        nullif(trim(ROW_ORIGINAL), '')                            as row_original,
        -- FIXED 2026-08-20 (time-index scan): INGESTED_AT is MICROSECONDS since epoch
        -- (e.g. 1785965270036203). A bare to_timestamp reads it as SECONDS and
        -- lands the row in the year 56,596,956 -- which is what poisoned this
        -- table's measured date range. The `, 6` scale argument is the fix.
        to_timestamp_ntz(INGESTED_AT, 6)                             as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                           as _source_run_id
    from source
)

select * from renamed
