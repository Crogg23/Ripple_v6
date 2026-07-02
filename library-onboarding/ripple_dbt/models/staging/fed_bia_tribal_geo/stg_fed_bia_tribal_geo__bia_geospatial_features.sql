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
    where fips is not null

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
