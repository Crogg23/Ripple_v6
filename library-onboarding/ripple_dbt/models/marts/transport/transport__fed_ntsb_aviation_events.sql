{{ config(materialized='table', schema='TRANSPORT') }}

-- Built 2026-08-09 (73-source backlog, wave 2c). NTSB aviation accident database, events table: one row per accident/incident (ev_id unique) with location, weather, and injury totals.
-- Grain: one row = one aviation event.

select * from {{ ref('stg_fed_ntsb_aviation_events__events') }}
