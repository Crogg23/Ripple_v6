{{ config(materialized='table', schema='FINANCE') }}

-- GRAIN: one row per individual contribution (sub_id is unique)
-- Answers: Who donates to whom, how much, and from which employer?
-- Source: FEC Individual Contributions (~84M records)
-- Key joins: cmte_id → fec_pac_summary/committees; employer → entity resolution

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
    _loaded_at
from {{ ref('stg_fed_fec_indiv_contributions__records') }}
