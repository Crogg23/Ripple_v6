{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_USGS_WBD_HUC8') }}

),

renamed as (

    -- This landing table arrived with typed NUMBER/FLOAT columns already;
    -- only trims and epoch conversions are needed.
    select

        -- identifiers
        trim(HUC8)                                     as huc8,
        trim(TNMID)                                    as tnm_id,
        trim(GLOBALID)                                 as global_id,
        OBJECTID                                       as object_id,

        -- dimensions
        trim(NAME)                                     as watershed_name,
        trim(STATES)                                   as states,
        trim(REFERENCEGNIS_IDS)                        as reference_gnis_ids,

        -- source lineage
        trim(METASOURCEID)                             as meta_source_id,
        trim(SOURCEDATADESC)                           as source_data_desc,
        trim(SOURCEORIGINATOR)                         as source_originator,
        SOURCEFEATUREID                                as source_feature_id,
        -- LOADDATE is a FLOAT epoch in milliseconds; /1000 -> seconds
        to_timestamp_ntz(cast(LOADDATE / 1000 as bigint)) as load_date,

        -- measures
        AREAACRES                                      as area_acres,
        AREASQKM                                       as area_sq_km,
        SHAPE_LENGTH                                   as shape_length,
        SHAPE_AREA                                     as shape_area,

        -- metadata (INGESTED_AT is a NUMBER epoch in microseconds)
        to_timestamp_ntz(INGESTED_AT, 6)               as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by huc8
            order by _loaded_at desc
        ) as _row_num
    from renamed
    where huc8 is not null

)

select * exclude (_row_num)
from deduped
where _row_num = 1
