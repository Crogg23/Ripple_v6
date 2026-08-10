{{ config(materialized='table', schema='TRANSPORT') }}

-- Built 2026-08-10 (backlog wave 4). NTSB aviation accident database, injury table: injury counts per event/aircraft/person-category/injury-level; ev_id joins to the NTSB aviation events mart.
-- Grain: one row = one event x aircraft x person category x injury level (composite exactly unique).

select * from {{ ref('stg_fed_ntsb_aviation_injury__injuries') }}
