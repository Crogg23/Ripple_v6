{{ config(materialized='table', schema='JUSTICE') }}

-- Built 2026-08-09 (73-source backlog, wave 2). US Consolidated Screening
-- List (trade.gov merged export-control/sanctions screening list).
-- Grain: one row = one list entry (entry_id has ~96 published doubles).
-- Key joins: names/alt names; vessel call signs; identifier documents.

select * from {{ ref('stg_fed_consolidated_screening_list__entries') }}
