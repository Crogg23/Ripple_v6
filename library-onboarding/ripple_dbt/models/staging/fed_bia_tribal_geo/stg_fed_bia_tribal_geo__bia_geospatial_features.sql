{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_BIA_TRIBAL_GEO') }}

),

renamed_cast as (

    select

        -- primary key
        LARID                                                       as lar_id,

        -- descriptive attributes
        TRY_TO_NUMBER(OBJECTID)                                     as object_id,
        LARNAME                                                     as lar_name,
        TRY_TO_DOUBLE(GISACRES)                                     as gis_acres,
        TRY_TO_DOUBLE(SHAPE__AREA)                                  as shape_area,
        TRY_TO_DOUBLE(SHAPE__LENGTH)                                as shape_length,
        GEOMETRY_JSON                                               as geometry_json,

        -- metadata (raw columns carry no leading underscore in this table)
        INGESTED_AT                                                 as _ingested_at,
        SOURCE_RUN_ID                                                as _source_run_id,
        SRC_SHA256                                                  as _src_sha256

    from source

),

deduped as (

    -- 2026-08-26: reloaded from the real BIA AIAN-LAR FeatureServer (the
    -- registered URL was an ArcGIS Hub home page, not a dataset -- see
    -- scripts/bia_tribal_geo_reload.py). LARID is this source's real natural
    -- key (one row per Land Area Representation polygon); the old FIPS-based
    -- dedup matched the old garbage schema and no longer applies.
    select *,
        ROW_NUMBER() over (
            partition by lar_id
            order by _ingested_at desc nulls last
        ) as _row_num
    from renamed_cast
    where lar_id is not null and lar_id != ''

)

select
    object_id,
    lar_id,
    lar_name,
    gis_acres,
    shape_area,
    shape_length,
    geometry_json,
    _ingested_at,
    _source_run_id,
    _src_sha256
from deduped
where _row_num = 1
