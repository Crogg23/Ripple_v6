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

        -- temporal (2026-07-28 fix: ISTAT mixes annual 'YYYY' and monthly
        -- 'YYYY-MM' notation in the same column -- confirmed live, no other
        -- shape exists (202,824 YYYY + 10,460 YYYY-MM = 213,284, matches FREQ
        -- in {'A','M'} exactly). A bare try_to_date(DATE) silently nulled every
        -- YYYY-MM row, which then collapsed the downstream dedup partition key
        -- (dataflow_id, dimension_keys, date) and dropped 157,188 real
        -- observations -- not a too-narrow dedup key, a broken date parse.
        case
            when regexp_like(trim(DATE), '^[0-9]{4}$')
                then try_to_date(trim(DATE) || '-01-01', 'YYYY-MM-DD')
            when regexp_like(trim(DATE), '^[0-9]{4}-[0-9]{2}$')
                then try_to_date(trim(DATE) || '-01', 'YYYY-MM-DD')
            else try_to_date(trim(DATE))
        end                                             as date,

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
