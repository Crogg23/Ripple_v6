{{ config(materialized='table', schema='POLITICS') }}

-- Candidate financial summary, keyed (cand_id, cycle). net_receipts/net_disbursements
-- are computed in staging (net of inter-committee transfers).

select
    cand_id, cycle, cand_name, incumbent_challenger, party,
    ttl_receipts, trans_from_auth, ttl_disb, trans_to_auth,
    cash_on_hand_close, ttl_indiv_contrib, debts_owed_by, coverage_end_date,
    net_receipts, net_disbursements
from {{ ref('stg_fed_fec_bulk_summary__candidate_summary') }}
-- Ties on coverage date break on the row's own money values, so the same row wins every run.
qualify row_number() over (
    partition by cand_id, cycle
    order by coverage_end_date desc nulls last, ttl_receipts desc nulls last, ttl_disb desc nulls last,
             cash_on_hand_close desc nulls last, debts_owed_by desc nulls last, cand_name nulls last,
             ttl_indiv_contrib desc nulls last, trans_from_auth desc nulls last, trans_to_auth desc nulls last,
             net_receipts desc nulls last, net_disbursements desc nulls last,
             party nulls last, incumbent_challenger nulls last
) = 1
