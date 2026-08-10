{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (73-source backlog, wave 3). USGS Geographic Names Information System AllNames file: one row = one name-citation for a geographic feature (~1.25M rows; 6 exact duplicate raw rows dropped in staging).
-- Grain: one row = one name-citation, unique on the surrogate key over (feature_id, feature_name, citation). feature_id (981,699 distinct) joins name variants of the same feature.

select * from {{ ref('stg_fed_usgs_gnis_all_names__name_citations') }}
