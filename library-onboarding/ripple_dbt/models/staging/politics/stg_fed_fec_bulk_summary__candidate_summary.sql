{{ config(materialized='view', schema='POLITICS') }}

-- FEC all-candidates financial summary (weball), cleaned + typed. The ONLY FEC
-- bulk file with dollar amounts. net_receipts strips inter-committee transfers
-- (TTL_RECEIPTS - TRANS_FROM_AUTH) so money-raised is not double-counted.

with source as (

    select * from {{ source('ripple_raw', 'FED_FEC_BULK_SUMMARY') }}

)

select
    nullif(trim(CAND_ID), '')                                  as cand_id,
    CYCLE                                                      as cycle,
    nullif(trim(CAND_NAME), '')                                as cand_name,
    nullif(trim(CAND_ICI), '')                                 as incumbent_challenger,
    nullif(trim(CAND_PTY_AFFILIATION), '')                     as party,
    try_to_decimal(nullif(trim(TTL_RECEIPTS), ''), 18, 2)      as ttl_receipts,
    try_to_decimal(nullif(trim(TRANS_FROM_AUTH), ''), 18, 2)   as trans_from_auth,
    try_to_decimal(nullif(trim(TTL_DISB), ''), 18, 2)          as ttl_disb,
    try_to_decimal(nullif(trim(TRANS_TO_AUTH), ''), 18, 2)     as trans_to_auth,
    try_to_decimal(nullif(trim(COH_COP), ''), 18, 2)           as cash_on_hand_close,
    try_to_decimal(nullif(trim(TTL_INDIV_CONTRIB), ''), 18, 2) as ttl_indiv_contrib,
    try_to_decimal(nullif(trim(DEBTS_OWED_BY), ''), 18, 2)     as debts_owed_by,
    nullif(trim(CVG_END_DT), '')                               as coverage_end_date,
    coalesce(try_to_decimal(nullif(trim(TTL_RECEIPTS), ''), 18, 2), 0)
      - coalesce(try_to_decimal(nullif(trim(TRANS_FROM_AUTH), ''), 18, 2), 0) as net_receipts,
    coalesce(try_to_decimal(nullif(trim(TTL_DISB), ''), 18, 2), 0)
      - coalesce(try_to_decimal(nullif(trim(TRANS_TO_AUTH), ''), 18, 2), 0)   as net_disbursements,
    _ingested_at
from source
where nullif(trim(CAND_ID), '') is not null
