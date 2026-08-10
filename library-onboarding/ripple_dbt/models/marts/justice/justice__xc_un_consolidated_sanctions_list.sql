{{ config(materialized='table', schema='JUSTICE') }}

-- Built 2026-08-09 (73-source backlog, wave 2c). UN Security Council consolidated sanctions list: one row per designated individual/entity (dataid unique); RECORD_TYPE distinguishes the two shapes. LAST_DAY_UPDATED is a JSON blob kept raw.
-- Grain: one row = one UN designation. Reads the pre-existing staging model.

select * from {{ ref('stg_xc_un_consolidated_sanctions_list__designated_party') }}
