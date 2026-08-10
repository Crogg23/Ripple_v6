{{ config(materialized='table', schema='FINANCE') }}

-- Built 2026-08-10 (backlog wave 4). NCUA charter merger events (27 rows); both charters join to the NCUA credit-union list.
-- Grain: one row = one merger event (merging_credit_union_charter unique in this extract). Reads the staging model built alongside it.

select * from {{ ref('stg_fed_ncua_charter_merger_events__merger_events') }}
