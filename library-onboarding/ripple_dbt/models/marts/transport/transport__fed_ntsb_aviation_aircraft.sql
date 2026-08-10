{{ config(materialized='table', schema='TRANSPORT') }}

-- Built 2026-08-09 (73-source backlog, wave 2c). NTSB aviation accident database, aircraft table: one row per aircraft involved in an event (ev_id + aircraft_key unique). Registration, make/model, owner/operator, certification.
-- Grain: one row = one aircraft in one event.

select * from {{ ref('stg_fed_ntsb_aviation_aircraft__aircraft') }}
