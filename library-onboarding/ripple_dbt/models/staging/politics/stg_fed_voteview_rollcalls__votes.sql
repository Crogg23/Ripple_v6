{{ config(materialized='view', schema='POLITICS') }}

-- Voteview member-by-member VOTES MATRIX (the fed_voteview_rollcalls source =
-- HSall_votes.csv), 118th + 119th. One row per (congress, chamber, rollnumber, icpsr).
-- Canonical copy built by politics/loaders/build_votes_leg.py.

with source as (

    select * from {{ source('ripple_raw', 'FED_VOTEVIEW_ROLLCALLS') }}

)

select
    try_to_number(CONGRESS)   as congress,
    CHAMBER                   as chamber,
    try_to_number(ROLLNUMBER) as rollnumber,
    try_to_number(ICPSR)      as icpsr,
    try_to_number(CAST_CODE)  as cast_code,
    try_to_double(PROB)       as prob
from source
where try_to_number(ICPSR) is not null
  and try_to_number(ROLLNUMBER) is not null
