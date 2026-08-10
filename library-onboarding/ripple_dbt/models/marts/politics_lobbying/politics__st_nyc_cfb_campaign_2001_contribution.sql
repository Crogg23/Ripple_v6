{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-10 (backlog wave 4). NYC Campaign Finance Board: contribution-level
-- campaign finance disclosure data for the 2001 NYC election cycle, 193,741 rows.
-- Grain: one row = one reported contribution transaction; near-unique natural key (CANDID+COMMITTEE+FILING+REFNO; 248 collisions broken by a row_number tiebreaker).
-- Reads the staging model.

select * from {{ ref('stg_st_nyc_cfb_campaign_2001_contribution__contributions') }}
