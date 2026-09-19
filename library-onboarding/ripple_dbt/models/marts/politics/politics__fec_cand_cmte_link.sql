{{ config(materialized='table', schema='POLITICS') }}

-- The candidate<->committee linkage bridge, keyed (cand_id, cmte_id, cycle).
-- Closes the identity graph: cand_id -> cmte_id -> committee master (fed_fec_bulk).

select
    cand_id, cmte_id, cycle, cmte_tp, cmte_dsgn, cand_election_yr, fec_election_yr, linkage_id
from {{ ref('stg_fed_fec_bulk_linkages__linkages') }}
qualify row_number() over (partition by cand_id, cmte_id, cycle order by linkage_id,
             -- tie-breakers 2026-09-18: the row's own values, so the same row wins every run
             cmte_tp nulls last, cmte_dsgn nulls last, cand_election_yr nulls last,
             fec_election_yr nulls last
) = 1
