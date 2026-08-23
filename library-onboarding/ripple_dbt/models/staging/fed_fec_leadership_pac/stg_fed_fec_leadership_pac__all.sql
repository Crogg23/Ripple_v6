{{ config(materialized='view') }}

-- FIXED 2026-08-22 (dbt-suite ERROR triage): the landing table now carries the
-- already-renamed columns (FEC_CANDIDATE_ID etc.) from the FEC-ids wiring
-- batch; the old staging still selected the raw bulk-file names (CAND_ID,
-- CMTE_ID) and could never build. Also corrected the dedupe grain: this is the
-- candidate-committee LINKAGE file (ccl), one row per LINKAGE_ID — deduping on
-- candidate alone silently kept one committee per candidate.

with source as (
    select * from {{ source('ripple_raw', 'FED_FEC_LEADERSHIP_PAC') }}
)

select
    FEC_CANDIDATE_ID,
    FEC_COMMITTEE_ID,
    CAND_ELECTION_YR as cand_election_yr,
    FEC_ELECTION_YR  as fec_election_yr,
    CMTE_TP          as cmte_tp,
    CMTE_DSGN        as cmte_dsgn,
    LINKAGE_ID       as linkage_id,
    _INGESTED_AT,
    _SOURCE_RUN_ID
from source
qualify row_number() over (
    partition by LINKAGE_ID
    order by _INGESTED_AT desc
) = 1
