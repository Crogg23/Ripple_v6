{{ config(materialized='view', schema='POLITICS') }}

-- Voteview HSall_members: one row per member-congress with DW-NOMINATE ideology,
-- keyed by ICPSR. Canonical copy built by politics/loaders/build_skeleton.py.

with source as (

    select * from {{ source('ripple_raw', 'FED_VOTEVIEW_MEMBERS') }}

)

select
    try_to_number(nullif(trim(ICPSR), ''))           as icpsr,
    nullif(trim(BIOGUIDE_ID), '')                    as bioguide_id,
    try_to_number(nullif(trim(CONGRESS), ''))        as congress,
    nullif(trim(CHAMBER), '')                        as chamber,
    nullif(trim(PARTY_CODE), '')                     as party_code,
    nullif(trim(STATE_ABBREV), '')                   as state_abbrev,
    try_to_double(nullif(trim(NOMINATE_DIM1), ''))   as nominate_dim1,
    try_to_double(nullif(trim(NOMINATE_DIM2), ''))   as nominate_dim2,
    nullif(trim(BIONAME), '')                        as bioname,
    _ingested_at,
    _source_run_id
from source
