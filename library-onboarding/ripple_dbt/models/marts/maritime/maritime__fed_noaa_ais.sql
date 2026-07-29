{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_noaa_ais__ais_vessel_positions') }}

),

enriched as (

    select

        -- surrogate / natural keys
        {{ dbt_utils.generate_surrogate_key(['mmsi', 'imo_number', 'date', 'base_datetime']) }}
                                                        as ais_position_sk,
        -- mmsi is the reliable vessel key (present on every row, ~14,868 distinct
        -- vessels). raw imo_number is kept for lineage only -- ~56% of rows are
        -- blank or the 'IMO0000000' placeholder, DO NOT join on it directly
        -- (2026-07-28 audit finding). imo_normalized is the cross-source join
        -- key (bare valid 7-digit hull number, else NULL) -- already computed
        -- in staging but was never exposed here until this fix.
        mmsi,
        imo_number,
        imo_normalized,
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
