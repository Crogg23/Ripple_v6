{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_noaa_ais__ais_vessel_positions') }}

),

enriched as (

    select

        -- surrogate / natural keys
        {{ dbt_utils.generate_surrogate_key(['mmsi', 'imo_number', 'date', 'base_datetime']) }}
                                                        as ais_position_sk,
        mmsi,
        imo_number,
        date,

        -- timestamps
        base_datetime,
        date_trunc('hour', base_datetime)               as base_datetime_hour,

        -- position
        latitude,
        longitude,

        -- navigation
        speed_over_ground,
        course_over_ground,
        heading,

        -- vessel attributes
        vessel_name,
        call_sign,
        vessel_type_code,
        nav_status,
        length_meters,
        width_meters,
        draft_meters,
        cargo_type_code,

        -- derived / convenience
        case
            when speed_over_ground = 0                   then 'moored'
            when speed_over_ground < 3                   then 'slow'
            when speed_over_ground < 14                  then 'underway'
            else                                              'fast'
        end                                             as speed_category,

        -- geography (Snowflake native)
        try_to_geography(
            'POINT(' || longitude || ' ' || latitude || ')'
        )                                               as position_geography,

        -- metadata
        transceiver_class,
        source_file,
        _ingested_at,
        _source_run_id,

        -- cross-source join helpers
        'fed_noaa_ais'                                  as source_id

    from base

)

select * from enriched
