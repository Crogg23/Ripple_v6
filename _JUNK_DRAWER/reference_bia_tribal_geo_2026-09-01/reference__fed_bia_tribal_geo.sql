{{ config(materialized='table', schema='REFERENCE') }}

-- 2026-08-26: was reading straight off raw landing, skipping staging entirely --
-- the same auto-gen-mart-skips-staging bug already root-caused and fixed for 6
-- other duplicate mart pairs on 2026-07-31 (see CHRIS_DECISIONS.md). Now reads
-- the deduped, correctly-keyed staging model instead, same as the hand-built
-- land_and_territory__fed_bia_tribal_geo mart.

with base as (
    select * from {{ ref('stg_fed_bia_tribal_geo__bia_geospatial_features') }}
)

select
    object_id as objectid,
    lar_id,
    lar_name,
    gis_acres,
    shape_area,
    shape_length,
    geometry_json
from base
