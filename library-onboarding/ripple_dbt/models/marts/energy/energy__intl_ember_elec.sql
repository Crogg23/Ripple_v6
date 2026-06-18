{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_intl_ember_elec__yearly_electricity') }}

)

select

    -- key identifiers (exposed for cross-source joins)
    country,
    iso_3_code,
    date,
    year(date)                          as year,

    -- geography / groupings
    area_type,
    continent,
    ember_region,
    is_eu,
    is_oecd,
    is_g20,
    is_g7,
    is_asean,

    -- metric descriptors
    category,
    subcategory,
    variable,
    unit,

    -- measures
    value,
    yoy_absolute_change,
    yoy_pct_change,

    -- metadata
    _ingested_at,
    _source_run_id

from base
