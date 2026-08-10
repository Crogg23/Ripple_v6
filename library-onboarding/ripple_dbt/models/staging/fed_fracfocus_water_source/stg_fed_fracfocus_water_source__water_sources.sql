{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_FRACFOCUS_WATER_SOURCE') }}

),

renamed as (

    select

        -- identifiers
        trim(WATERSOURCEID)                   as water_source_id,
        trim(DISCLOSUREID)                    as disclosure_id,
        trim(APINUMBER)                       as api_number,

        -- dimensions
        trim(STATENAME)                       as state_name,
        trim(COUNTYNAME)                      as county_name,
        trim(OPERATORNAME)                    as operator_name,
        trim(WELLNAME)                        as well_name,
        trim(DESCRIPTION)                     as description,

        -- measures
        try_to_number(trim(PERCENT), 38, 8)   as percent,

        -- metadata
        _INGESTED_AT                          as _ingested_at,
        _SOURCE_RUN_ID                        as _source_run_id,
        _SRC_FILE                             as _src_file

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by water_source_id
            order by _ingested_at desc
        ) as _row_num
    from renamed
    where water_source_id is not null

)

select
    water_source_id,
    disclosure_id,
    api_number,
    state_name,
    county_name,
    operator_name,
    well_name,
    description,
    percent,
    _ingested_at,
    _source_run_id,
    _src_file
from deduped
where _row_num = 1
