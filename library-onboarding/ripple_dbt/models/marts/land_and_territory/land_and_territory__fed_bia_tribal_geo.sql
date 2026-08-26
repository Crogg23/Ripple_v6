{{ config(materialized='table', schema='LAND_AND_TERRITORY') }}

with base as (

    select * from {{ ref('stg_fed_bia_tribal_geo__bia_geospatial_features') }}

)

select

    -- key identifiers (exposed for cross-source joins)
    lar_id,

    -- descriptive attributes
    object_id,
    lar_name,
    gis_acres,
    shape_area,
    shape_length,
    geometry_json,

    -- metadata
    _ingested_at,
    _source_run_id

from base
