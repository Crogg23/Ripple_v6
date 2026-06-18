{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_intl_it_istat__istat_sdmx_observations') }}

)

select
    -- primary key
    istat_obs_id,

    -- cross-source join keys
    country,
    date,
    dataflow_id,
    dimension_keys,
    series_key,

    -- measures
    obs_value,

    -- time helpers
    year(date)                                         as obs_year,
    month(date)                                        as obs_month,
    quarter(date)                                      as obs_quarter,

    -- attributes
    obs_status,
    unit_measure,
    unit_mult,
    case
        when unit_mult = 0  then 1
        when unit_mult = 1  then 10
        when unit_mult = 2  then 100
        when unit_mult = 3  then 1000
        when unit_mult = 6  then 1000000
        when unit_mult = 9  then 1000000000
        else null
    end                                                as unit_multiplier_value,
    obs_value * case
        when unit_mult = 0  then 1
        when unit_mult = 1  then 10
        when unit_mult = 2  then 100
        when unit_mult = 3  then 1000
        when unit_mult = 6  then 1000000
        when unit_mult = 9  then 1000000000
        else 1
    end                                                as obs_value_absolute,
    freq,

    -- flags
    case when obs_status = 'A' then true else false end as is_normal_value,
    case when obs_value is null then true else false end as is_missing_value,

    -- metadata
    _ingested_at,
    _source_run_id

from base
