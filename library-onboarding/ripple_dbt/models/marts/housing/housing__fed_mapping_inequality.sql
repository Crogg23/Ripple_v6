{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_mapping_inequality__holc_neighborhood_grades') }}

)

select

    -- primary key
    holc_neighborhood_key,

    -- key identifiers (cross-source join surface)
    holc_id,
    fips,
    city,
    state,
    holc_grade,

    -- descriptive attributes
    holc_color,
    area_description_data,
    residential_description,
    year_mapped,

    -- geo
    geometry,
    lat,
    lon,

    -- derived helpers
    case holc_grade
        when 'A' then 1
        when 'B' then 2
        when 'C' then 3
        when 'D' then 4
        else null
    end                                            as holc_grade_rank,

    case holc_grade
        when 'A' then 'Best'
        when 'B' then 'Still Desirable'
        when 'C' then 'Definitely Declining'
        when 'D' then 'Hazardous'
        else 'Unknown'
    end                                            as holc_grade_label,

    -- source metadata
    'fed_mapping_inequality'                       as source_id,
    _ingested_at,
    _source_run_id

from base
