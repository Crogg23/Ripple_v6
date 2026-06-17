{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_MAPPING_INEQUALITY') }}

),

renamed as (

    select
        -- identifiers
        holc_id                                                        as holc_id,
        city                                                           as city,
        state                                                          as state,
        fips                                                           as fips,
        holc_grade                                                     as holc_grade,

        -- attributes
        holc_color                                                     as holc_color,
        area_description_data                                          as area_description_data,
        residential_description                                        as residential_description,
        try_to_number(year_mapped)                                     as year_mapped,
        geometry                                                       as geometry,
        try_to_double(lat)                                             as lat,
        try_to_double(lon)                                             as lon,

        -- derived composite key for deduplication / joins
        concat_ws('|', holc_id, fips, city, state, holc_grade)        as holc_neighborhood_key,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by holc_neighborhood_key
            order by _ingested_at desc
        ) as _row_num
    from renamed

)

select
    holc_id,
    city,
    state,
    fips,
    holc_grade,
    holc_color,
    area_description_data,
    residential_description,
    year_mapped,
    geometry,
    lat,
    lon,
    holc_neighborhood_key,
    _ingested_at,
    _source_run_id

from deduped
where _row_num = 1
