{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-10 (backlog wave 4). NYC Campaign Finance Board: contribution-level
-- campaign finance disclosure data for the 2013 NYC election cycle, 197,968 rows.
-- Grain: one row = one reported contribution transaction; exactly unique natural key (RECIPID+COMMITTEE+FILING+REFNO).
-- Reads the staging model.

select * from {{ ref('stg_st_nyc_cfb_campaign_2013_contribution__contributions') }}
