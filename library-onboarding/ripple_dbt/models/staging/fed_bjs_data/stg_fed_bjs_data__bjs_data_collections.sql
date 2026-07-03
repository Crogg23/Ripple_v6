{{ config(materialized='view') }}

with source as (

    select *
    from {{ source('ripple_raw', 'FED_BJS_DATA') }}

),

renamed as (

    select
        -- primary / foreign keys
        FIPS_CODE                                        as fips_code,
        NACJD_ID                                         as nacjd_id,

        -- descriptive attributes
        COLLECTION_NAME                                  as collection_name,
        TOPIC                                            as topic,
        DESCRIPTION                                      as description,
        GEOGRAPHIC_LEVEL                                 as geographic_level,
        UNIT_OF_ENUMERATION                              as unit_of_enumeration,
        ACCESS_LEVEL                                     as access_level,

        -- url / reference columns
        DOWNLOAD_URL                                     as download_url,
        DATA_TOOL_URL                                    as data_tool_url,

        -- date / numeric columns cast safely
        try_to_date(PUBLICATION_DATE)                    as publication_date,
        YEARS_AVAILABLE                                  as years_available,   -- kept as text; range string e.g. '2000-2022'

        -- pipeline metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by fips_code, nacjd_id
            order by _ingested_at desc
        ) as _row_num
    from renamed

)

select
    fips_code,
    nacjd_id,
    collection_name,
    topic,
    description,
    geographic_level,
    unit_of_enumeration,
    access_level,
    download_url,
    data_tool_url,
    publication_date,
    years_available,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
