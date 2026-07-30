{{ config(materialized='table', schema='FINANCE') }}

-- GRAIN: one row per candidate-committee linkage

with source as (
    select * from {{ source('ripple_raw', 'FED_FEC_LEADERSHIP_PAC') }}
)

select
    FEC_CANDIDATE_ID,
    CAND_ELECTION_YR,
    FEC_ELECTION_YR,
    FEC_COMMITTEE_ID,
    CMTE_TP,
    CMTE_DSGN,
    LINKAGE_ID
from source
