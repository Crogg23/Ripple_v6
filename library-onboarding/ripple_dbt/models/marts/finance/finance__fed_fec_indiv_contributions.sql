{{ config(materialized='table', schema='FINANCE') }}

-- GRAIN: one row per individual contribution. sub_id is unique.
-- Answers: Who donates to whom, how much, and from which employer?
-- Source: FEC Individual Contributions, 283,771,819 rows over 14 two-year
--   cycles, 2000 to 2026. It was 84M and two cycles until 2026-09-06.
--   Always filter or group by cycle_file; the whole table is 3.4x what any
--   query written against the old two-cycle version expected.
-- Key joins: cmte_id â†’ fec_pac_summary/committees; employer â†’ entity resolution

select
    sub_id,
    cmte_id,
    trim(name)                                     as donor_name,
    trim(city)                                     as city,
    trim(state)                                    as state,
    trim(zip_code)                                 as zip_code,
    trim(employer)                                 as employer,
    trim(occupation)                               as occupation,
    try_to_date(transaction_dt, 'MMDDYYYY')        as transaction_date,
    try_to_double(transaction_amt)                  as transaction_amt,
    trim(transaction_tp)                           as transaction_type,
    trim(entity_tp)                                as entity_type,
    trim(other_id)                                 as other_id,
    trim(memo_text)                                as memo_text,
    cycle_file,
    _loaded_at
from {{ ref('stg_fed_fec_indiv_contributions__records') }}
