{{ config(materialized='table', schema='POLITICS') }}

-- Candidate financial summary, keyed (cand_id, cycle). net_receipts/net_disbursements
-- are computed in staging (net of inter-committee transfers).

select
    cand_id, cycle, cand_name, incumbent_challenger, party,
    ttl_receipts, trans_from_auth, ttl_disb, trans_to_auth,
    cash_on_hand_close, ttl_indiv_contrib, debts_owed_by, coverage_end_date,
    net_receipts, net_disbursements
from {{ ref('stg_fed_fec_bulk_summary__candidate_summary') }}
qualify row_number() over (partition by cand_id, cycle order by coverage_end_date desc nulls last) = 1
