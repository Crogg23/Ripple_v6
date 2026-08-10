{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-10 (73-source backlog, wave 3). CMS Open Payments covered-recipient profile supplement: the roster/demographics companion to the already-modeled Open Payments payment tables (physicians + non-physician practitioners; 1,697,025 profiles).
-- Grain: one row = one covered recipient profile, unique on profile_id. npi joins to NPI-keyed provider tables.

select * from {{ ref('stg_fed_cms_open_payments_profile_supplement__recipient_profiles') }}
