{{ config(materialized='view', schema='POLITICS') }}

-- FEC candidate-committee linkage (ccl), cleaned. The official bridge between a
-- candidate (CAND_ID) and their committees (CMTE_ID), per cycle.

with source as (

    select * from {{ source('ripple_raw', 'FED_FEC_BULK_LINKAGES') }}

)

select
    nullif(trim(CAND_ID), '')                        as cand_id,
    nullif(trim(CMTE_ID), '')                        as cmte_id,
    CYCLE                                            as cycle,
    nullif(trim(CMTE_TP), '')                        as cmte_tp,
    nullif(trim(CMTE_DSGN), '')                      as cmte_dsgn,
    try_to_number(nullif(trim(CAND_ELECTION_YR), '')) as cand_election_yr,
    try_to_number(nullif(trim(FEC_ELECTION_YR), ''))  as fec_election_yr,
    nullif(trim(LINKAGE_ID), '')                     as linkage_id,
    _ingested_at
from source
where nullif(trim(CAND_ID), '') is not null
  and nullif(trim(CMTE_ID), '') is not null
