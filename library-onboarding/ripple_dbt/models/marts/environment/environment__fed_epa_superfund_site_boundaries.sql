{{ config(materialized='table', schema='ENVIRONMENT') }}

-- EPA Superfund site boundary features, full pull (2,114 features / 1,908
-- sites), attributes only. Grain: boundary_feature_id. Built 2026-08-10.

select * from {{ ref('stg_fed_epa_superfund_site_boundaries__boundaries') }}
