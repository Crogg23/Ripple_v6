{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-10 (backlog wave 4). NYC Campaign Finance Board: contribution-level
-- campaign finance disclosure data for the 2025 NYC election cycle, 259,537 rows.
-- Grain: one row = one reported contribution transaction; exactly unique natural key (RECIPID+COMMITTEE+FILING+REFNO).
-- Reads the staging model.

select * from {{ ref('stg_st_nyc_cfb_campaign_2025_contributions__contributions') }}
