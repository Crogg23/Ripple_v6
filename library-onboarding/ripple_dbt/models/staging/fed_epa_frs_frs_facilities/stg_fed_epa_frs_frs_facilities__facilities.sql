{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_EPA_FRS_FRS_FACILITIES') }}

),

renamed as (

    select

        -- identifiers
        trim(REGISTRY_ID)                              as registry_id,

        -- dimensions
        trim(FAC_NAME)                                 as fac_name,
        trim(FAC_STREET)                               as fac_street,
        trim(FAC_CITY)                                 as fac_city,
        trim(FAC_STATE)                                as fac_state,
        trim(FAC_ZIP)                                  as fac_zip,
        trim(FAC_COUNTY)                               as fac_county,
        trim(FAC_EPA_REGION)                           as fac_epa_region,

        -- measures
        try_to_number(trim(LATITUDE_MEASURE), 38, 8)   as latitude_measure,
        try_to_number(trim(LONGITUDE_MEASURE), 38, 8)  as longitude_measure,

        -- metadata
        _INGESTED_AT                                   as _ingested_at,
        _SOURCE_RUN_ID                                 as _source_run_id,
        _SRC_SHA256                                    as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by registry_id
            order by _ingested_at desc
        ) as _row_num
    from renamed
    where registry_id is not null

)

select
    registry_id,
    fac_name,
    fac_street,
    fac_city,
    fac_state,
    fac_zip,
    fac_county,
    fac_epa_region,
    latitude_measure,
    longitude_measure,
    _ingested_at,
    _source_run_id,
    _src_sha256
from deduped
where _row_num = 1
