{{ config(materialized='table', schema='POLITICS') }}

-- DELIVERABLE #1 (bridge): one row per (member, fec_id). `fec` is ONE-TO-MANY in
-- congress-legislators (a member can carry several FEC candidate IDs across races)
-- -- this bridge preserves that; it is NEVER flattened into a single column. Join
-- a member's FEC candidate IDs to FEC data via fec_id -> FED_FEC_BULK.FEC_CAND_ID.

select
    x.member_key,
    x.bioguide,
    f.value::string   as fec_id,
    x.full_name,
    x.last_party      as party,
    x.last_state      as state,
    x.last_term_type
from {{ ref('politics__member_crosswalk') }} x,
     lateral flatten(input => x.fec_ids) f
where nullif(trim(f.value::string), '') is not null
