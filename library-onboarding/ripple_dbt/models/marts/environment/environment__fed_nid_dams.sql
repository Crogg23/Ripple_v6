{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-09 (73-source backlog, wave 2). USACE National Inventory of
-- Dams. Grain: one row = one structure (NID_ID shared by a dam's associated
-- structures; not unique by design).
-- The harm lens: hazard potential x condition assessment x last inspection.

select * from {{ ref('stg_fed_nid_dams__structures') }}
