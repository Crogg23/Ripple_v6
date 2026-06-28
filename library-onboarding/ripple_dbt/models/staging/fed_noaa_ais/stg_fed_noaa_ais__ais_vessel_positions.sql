{{ config(materialized='view') }}

-- Single-day AIS snapshot: 100% of rows are DATE = '2024-01-01' (one NOAA
-- Marine Cadastre daily file, AIS_2024_01_01.zip). This is a spatial
-- cross-section, NOT a longitudinal panel -- no vessel-movement-over-time.
--
-- Trap fixes (2026-06-27 discovery sweep):
--   * imo_normalized -- AIS stores 100% 'IMO'-prefixed values (e.g. 'IMO9610664')
--     plus 2.24M placeholder/junk pings (dominant 'IMO0000000'); OFAC/OpenSanctions
--     store bare 7-digit. A naive string join returns 0 matches. normalize_imo()
--     strips the 'IMO' prefix and keeps only a valid 7-digit value -- this is the
--     real cross-source join key. The raw imo_number is preserved for lineage.
--   * heading -- 52.46% of rows carry the AIS sentinel '511.0' ('heading not
--     available'); a naive AVG returns 356.86 instead of 186.80. clean_heading()
--     nulls 511 and anything >= 360.
--   * MMSI is the PRIMARY vessel key (reliable; present on every row, 14,868
--     distinct vessels). IMO is junk-heavy and must not be the primary key.

with source as (

    select * from {{ source('ripple_raw', 'FED_NOAA_AIS') }}

),

renamed_cast as (

    select

        -- identifiers
        -- MMSI is the PRIMARY vessel key: reliable, present on every ping.
        trim(MMSI)                                          as mmsi,
        -- raw IMO kept for lineage; DO NOT join on this (carries 'IMO' prefix
        -- + 2.24M placeholder/junk pings).
        trim(IMO)                                           as imo_number,
        -- normalized IMO is the cross-source join key (bare valid 7-digit,
        -- else NULL). Joins to OFAC/OpenSanctions/GLEIF.
        {{ normalize_imo('IMO') }}                          as imo_normalized,
        try_to_date(trim(DATE))                             as date,

        -- timestamps
        try_to_timestamp(trim(BASEDATETIME))                as base_datetime,

        -- position
        try_to_double(trim(LAT))                            as latitude,
        try_to_double(trim(LON))                            as longitude,

        -- navigation
        try_to_double(trim(SOG))                            as speed_over_ground,
        try_to_double(trim(COG))                            as course_over_ground,
        -- HEADING: 511 (and anything >= 360) is the AIS 'not available' sentinel
        -- on 52% of rows -- null it so aggregates don't get dragged to ~357.
        {{ clean_heading('HEADING') }}                      as heading,

        -- vessel attributes
        trim(VESSELNAME)                                    as vessel_name,
        trim(CALLSIGN)                                      as call_sign,
        try_to_number(trim(VESSELTYPE))                     as vessel_type_code,
        trim(STATUS)                                        as nav_status,
        try_to_double(trim(LENGTH))                         as length_meters,
        try_to_double(trim(WIDTH))                          as width_meters,
        try_to_double(trim(DRAFT))                          as draft_meters,
        try_to_number(trim(CARGO))                          as cargo_type_code,

        -- metadata
        trim(TRANSCEIVER_CLASS)                             as transceiver_class,
        trim(SOURCE_FILE)                                   as source_file,

        -- pipeline audit columns
        to_timestamp_ntz(_ingested_at, 6)                   as _ingested_at,
        nullif(trim(try_cast(_source_run_id as text)), '') as _source_run_id

    from source

),

deduped as (

    select
        *,
        row_number() over (
            partition by mmsi, imo_number, date, base_datetime
            order by _ingested_at nulls last
        ) as _row_num
    from renamed_cast

)

select * exclude (_row_num)
from deduped
where _row_num = 1
