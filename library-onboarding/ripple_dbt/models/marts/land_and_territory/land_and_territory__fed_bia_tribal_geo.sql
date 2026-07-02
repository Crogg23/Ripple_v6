{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_bia_tribal_geo__bia_geospatial_features') }}

)

select

    -- key identifiers (exposed for cross-source joins)
    fips,

    -- descriptive attributes
    object_id,
    layer_name,
    name                                                            as feature_name,
    state,
    area_sqmi,
    geometry,
    data_source,
    last_updated,

    -- metadata
    _ingested_at,
    _source_run_id

from base
