{{ config(materialized='view') }}

-- GRAIN: one row per solar generator (plant_code + generator_id) -- verified exact-unique
-- (7,154 rows) against the 2024-vintage landing table. EIA-860 Schedule 3.3: solar
-- technology detail (tracking, panel material, net metering).
-- Upgraded 2026-08-10 from auto-generated minimal passthrough (wave 4).

with source as (

    select * from {{ source('ripple_raw', 'FED_EIA860_3_3_SOLAR') }}

),

renamed as (

    select

        -- identifiers
        {{ stg_int('trim(PLANT_CODE)') }}                        as plant_code,
        trim(GENERATOR_ID)                                     as generator_id,
        {{ stg_int('trim(UTILITY_ID)') }}                        as utility_id,

        -- dimensions
        trim(UTILITY_NAME)                                     as utility_name,
        trim(PLANT_NAME)                                       as plant_name,
        trim(STATE)                                            as state,
        trim(COUNTY)                                           as county,
        trim(STATUS)                                           as status,
        trim(TECHNOLOGY)                                       as technology,
        trim(PRIME_MOVER)                                      as prime_mover,
        trim(SECTOR_NAME)                                      as sector_name,
        trim(SECTOR)                                           as sector,
        trim(LENSES_MIRRORS)                                   as lenses_mirrors,
        trim(SINGLE_AXIS_TRACKING)                             as single_axis_tracking,
        trim(DUAL_AXIS_TRACKING)                               as dual_axis_tracking,
        trim(FIXED_TILT)                                       as fixed_tilt,
        trim(BIFACIAL)                                         as bifacial,
        trim(EAST_WEST_FIXED_TILT)                             as east_west_fixed_tilt,
        trim(PARABOLIC_TROUGH)                                 as parabolic_trough,
        trim(LINEAR_FRESNEL)                                   as linear_fresnel,
        trim(POWER_TOWER)                                      as power_tower,
        trim(DISH_ENGINE)                                      as dish_engine,
        trim(OTHER_SOLAR_TECHNOLOGY)                           as other_solar_technology,
        trim(CRYSTALLINE_SILICON)                              as crystalline_silicon,
        trim(THIN_FILM_CDTE)                                   as thin_film_cdte,
        trim(THIN_FILM_A_SI)                                   as thin_film_a_si,
        trim(THIN_FILM_CIGS)                                   as thin_film_cigs,
        trim(THIN_FILM_OTHER)                                  as thin_film_other,
        trim(OTHER_MATERIALS)                                  as other_materials,
        trim(NET_METERING_AGREEMENT)                           as net_metering_agreement,
        trim(VIRTUAL_NET_METERING_AGREEMENT)                   as virtual_net_metering_agreement,

        -- measures
        {{ stg_float('trim(NAMEPLATE_CAPACITY_MW)') }}             as nameplate_capacity_mw,
        {{ stg_float('trim(SUMMER_CAPACITY_MW)') }}                as summer_capacity_mw,
        {{ stg_float('trim(WINTER_CAPACITY_MW)') }}                as winter_capacity_mw,
        {{ stg_int('trim(OPERATING_MONTH)') }}                   as operating_month,
        {{ stg_int('trim(OPERATING_YEAR)') }}                    as operating_year,
        {{ stg_float('trim(AZIMUTH_ANGLE)') }}                     as azimuth_angle,
        {{ stg_float('trim(TILT_ANGLE)') }}                        as tilt_angle,
        {{ stg_float('trim(DC_NET_CAPACITY_MW)') }}                as dc_net_capacity_mw,
        {{ stg_float('trim(NET_METERING_DC_CAPACITY_MW)') }}       as net_metering_dc_capacity_mw,
        {{ stg_float('trim(VIRTUAL_NET_METERING_DC_CAPACITY_MW)') }}
                                                               as virtual_net_metering_dc_capacity_mw,

        -- metadata
        {{ stg_ts('_INGESTED_AT') }}                         as _loaded_at,
        _SOURCE_RUN_ID                                         as _source_run_id,
        _SRC_FILE                                              as _src_file

    from source

)

select * from renamed
where plant_code is not null
  and generator_id is not null
