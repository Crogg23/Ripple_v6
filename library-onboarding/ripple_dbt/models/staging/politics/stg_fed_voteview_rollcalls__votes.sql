{{ config(materialized='view', schema='POLITICS') }}

-- Voteview member-by-member VOTES MATRIX (the fed_voteview_rollcalls source =
-- HSall_votes.csv), 118th + 119th. One row per (congress, chamber, rollnumber, icpsr).
-- Canonical copy built by politics/loaders/build_votes_leg.py.

with source as (

    select * from {{ source('ripple_raw', 'FED_VOTEVIEW_ROLLCALLS') }}

)

select
    {{ stg_int('CONGRESS') }}   as congress,
    CHAMBER                   as chamber,
    {{ stg_int('ROLLNUMBER') }} as rollnumber,
    {{ stg_int('ICPSR') }}      as icpsr,
    {{ stg_int('CAST_CODE') }}  as cast_code,
    {{ stg_float('PROB') }}       as prob
from source
where {{ stg_int('ICPSR') }} is not null
  and {{ stg_int('ROLLNUMBER') }} is not null
