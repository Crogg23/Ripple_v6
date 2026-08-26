{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_BIA_TRIBAL_GEO') }}

),

renamed_cast as (

    select

        -- primary key
        FIPS                                                        as fips,

        -- descriptive attributes
        TRY_TO_NUMBER(OBJECTID)                                     as object_id,
        LAYER_NAME                                                  as layer_name,
        NAME                                                        as name,
        STATE                                                       as state,
        TRY_TO_DOUBLE(AREA_SQMI)                                    as area_sqmi,
        GEOMETRY                                                    as geometry,
        DATA_SOURCE                                                 as data_source,
        TRY_TO_DATE(LAST_UPDATED)                                   as last_updated,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *,
        ROW_NUMBER() over (
            partition by fips
            order by last_updated desc nulls last, _ingested_at desc nulls last
        ) as _row_num
    from renamed_cast
    -- 2026-08-25: raw source currently contains ONLY ArcGIS Hub portal-crawl
    -- catalog metadata (StoryMaps/Web Maps/Apps listed on the BIA Open Data
    -- Hub site), not real tribal-land geospatial features. Verified live:
    -- all 100 raw rows have FIPS = '' (empty string, not NULL -- so it slid
    -- past the old filter), STATE/AREA_SQMI also '', and OBJECTID is a
    -- 32-char Hub item GUID rather than the FeatureServer's numeric OBJECTID.
    -- The FIPS dedup below collapses all 100 junk rows to one survivor with
    -- a null object_id, which is what tripped this test. Excluding fips=''
    -- here until the loader is pointed at the real FeatureServer/query
    -- endpoint -- this currently zeroes out the mart pending that reload.
    where fips is not null and fips != ''

)

select
    object_id,
    layer_name,
    name,
    fips,
    state,
    area_sqmi,
    geometry,
    data_source,
    last_updated,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
