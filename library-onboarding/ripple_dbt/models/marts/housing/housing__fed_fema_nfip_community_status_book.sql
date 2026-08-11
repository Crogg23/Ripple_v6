{{ config(materialized='table', schema='HOUSING') }}

-- Built 2026-08-10 (backlog wave 4). FEMA NFIP Community Status Book: one row
-- per community (community_id_number unique) with NFIP participation, flood
-- map dates, tribal flag, and CRS class rating / premium discounts.
-- Grain: one row = one NFIP community. Reads the staging model.
-- Re-pulled in full 2026-08-11: 25,125 rows (same publisher column set;
-- date formats verified unchanged).

select * from {{ ref('stg_fed_fema_nfip_community_status_book__communities') }}
