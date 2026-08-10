{{ config(materialized='table', schema='HOUSING') }}

-- Built 2026-08-10 (backlog wave 4). USDA Rural Development Multi-Family
-- Housing active projects: one row per borrower_id + project_id (exact
-- composite key) with location, management, tax-credit / restrictive-clause
-- dates, and unit counts by bedroom size incl. rental-assistance units.
-- Grain: one row = one active rural MFH project. Reads the staging model.

select * from {{ ref('stg_fed_usda_rd_mfh_active_projects__projects') }}
