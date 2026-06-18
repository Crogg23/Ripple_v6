{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'INTL_IT_ISTAT') }}

),

renamed as (

    select
        -- identifiers
        DATAFLOW_ID                                    as dataflow_id,
        DIMENSION_KEYS                                 as dimension_keys,
        SERIES_KEY                                     as series_key,

        -- temporal
        try_to_date(DATE)                              as date,

        -- measures
        try_to_double(OBS_VALUE)                       as obs_value,

        -- attributes
        OBS_STATUS                                     as obs_status,
        UNIT_MEASURE                                   as unit_measure,
        try_to_number(UNIT_MULT)                       as unit_mult,
        FREQ                                           as freq,

        -- country derived from DIMENSION_KEYS convention (IT = Italy ISTAT source)
        'IT'                                           as country,

        -- metadata
        try_to_timestamp(FETCHED_AT)                   as _ingested_at,
        {{ dbt_utils.generate_surrogate_key(['DATAFLOW_ID', 'DIMENSION_KEYS', 'DATE']) }} as _source_run_id

    from source

),

deduped as (

    select *
    from (
        select
            *,
            row_number() over (
                partition by dataflow_id, dimension_keys, date
                order by _ingested_at desc nulls last
            ) as _row_num
        from renamed
    )
    where _row_num = 1

)

select
    -- surrogate primary key
    {{ dbt_utils.generate_surrogate_key(['dataflow_id', 'dimension_keys', 'date']) }} as istat_obs_id,

    -- identifiers
    country,
    date,
    dataflow_id,
    dimension_keys,
    series_key,

    -- measures
    obs_value,

    -- attributes
    obs_status,
    unit_measure,
    unit_mult,
    freq,

    -- metadata
    _ingested_at,
    _source_run_id

from deduped
