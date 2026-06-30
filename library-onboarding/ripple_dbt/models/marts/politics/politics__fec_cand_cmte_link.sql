{{ config(materialized='table', schema='POLITICS') }}

-- The candidate<->committee linkage bridge, keyed (cand_id, cmte_id, cycle).
-- Closes the identity graph: cand_id -> cmte_id -> committee master (fed_fec_bulk).

select
    cand_id, cmte_id, cycle, cmte_tp, cmte_dsgn, cand_election_yr, fec_election_yr, linkage_id
from {{ ref('stg_fed_fec_bulk_linkages__linkages') }}
qualify row_number() over (partition by cand_id, cmte_id, cycle order by linkage_id) = 1
