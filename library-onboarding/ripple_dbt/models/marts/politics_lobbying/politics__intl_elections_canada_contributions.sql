{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-10 (backlog wave 3). Elections Canada: federal political contributions
-- reported on financial returns, all entity types (parties, candidates, leadership
-- contestants, etc.), 12,646,465 lines. No natural key -- repeated identical lines are
-- legitimate (identical installments, aggregated part rows); contribution_record_id is
-- a surrogate (md5 over all business columns + row_number tiebreaker).
-- Grain: one row = one reported contribution line. Reads the staging model.

select * from {{ ref('stg_intl_elections_canada_contributions__contributions') }}
