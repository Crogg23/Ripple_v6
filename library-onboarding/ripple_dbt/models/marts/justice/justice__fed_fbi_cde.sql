{{ config(materialized='table', schema='JUSTICE') }}

-- Rewritten 2026-08-09: the old version read the retired incident-level raw
-- shape directly (its columns no longer exist). The 2026-08-09 rebuild landed
-- state x offense x month summary counts back to 1985; this pivots the
-- OFFENSES/CLEARANCES series into columns.
-- Grain: one row = state x offense x month.

with staged as (
    select * from {{ ref('stg_fed_fbi_cde__state_month') }}
)

select
    state,
    offense,
    month_date,
    month,
    max(case when series = 'OFFENSES' then count end)           as offenses,
    max(case when series = 'OFFENSES' then rate_per_100k end)   as offense_rate_per_100k,
    max(case when series = 'CLEARANCES' then count end)         as clearances,
    max(case when series = 'CLEARANCES' then rate_per_100k end) as clearance_rate_per_100k,
    max(_ingested_at)                                           as _ingested_at
from staged
group by state, offense, month_date, month
