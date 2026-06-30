{{ config(materialized='table', schema='POLITICS') }}

-- FEC candidate identity, keyed (cand_id, cycle). Dedup keeps the latest election-year row.

select
    cand_id, cycle, cand_name, party, office, office_state, office_district,
    incumbent_challenger, cand_status, principal_cmte_id, cand_election_yr
from {{ ref('stg_fed_fec_bulk_candidates__candidates') }}
qualify row_number() over (partition by cand_id, cycle order by cand_election_yr desc nulls last) = 1
