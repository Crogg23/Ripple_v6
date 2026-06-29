{{ config(materialized='view', schema='POLITICS') }}

-- FEC candidate master (cn), cleaned. One row per (cand_id, cycle) after the mart
-- dedups. Canonical copy built by politics/loaders/build_money_spine.py.

with source as (

    select * from {{ source('ripple_raw', 'FED_FEC_BULK_CANDIDATES') }}

)

select
    nullif(trim(CAND_ID), '')                        as cand_id,
    CYCLE                                            as cycle,
    nullif(trim(CAND_NAME), '')                      as cand_name,
    nullif(trim(CAND_PTY_AFFILIATION), '')           as party,
    nullif(trim(CAND_OFFICE), '')                    as office,
    nullif(trim(CAND_OFFICE_ST), '')                 as office_state,
    nullif(trim(CAND_OFFICE_DISTRICT), '')           as office_district,
    nullif(trim(CAND_ICI), '')                       as incumbent_challenger,
    nullif(trim(CAND_STATUS), '')                    as cand_status,
    nullif(trim(CAND_PCC), '')                       as principal_cmte_id,
    try_to_number(nullif(trim(CAND_ELECTION_YR), '')) as cand_election_yr,
    _ingested_at
from source
where nullif(trim(CAND_ID), '') is not null
