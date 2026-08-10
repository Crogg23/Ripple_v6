{{ config(materialized='table', schema='JUSTICE') }}

-- Built 2026-08-09 (73-source backlog, wave 2). UK OFSI consolidated
-- financial sanctions list.
-- Grain: one row = one name variant of a designated target; designation_id
-- groups variants (6,315 designations).
-- Key joins: IMO number -> vessels; passport/registration numbers; names.

select * from {{ ref('stg_xc_uk_sanctions_list__designations') }}
