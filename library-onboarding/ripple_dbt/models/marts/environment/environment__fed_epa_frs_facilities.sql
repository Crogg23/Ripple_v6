{{ config(materialized='table', schema='ENVIRONMENT') }}

-- GRAIN: one row per EPA-registered facility (REGISTRY_ID is unique)
-- Answers: Where is every EPA-regulated facility in the US, who runs it, what programs cover it?
-- Source: EPA Facility Registry Service (~5.3M facilities)
-- Key joins: fips_code â†’ geography; primary_name â†’ entity resolution; pgm_sys_acrnms â†’ EPA program tables
--
-- KEY RE-PROOF (2026-09-20 -- same hole f41ebff9 closed in staging: 289 views
-- deduped on a key proven unique ONCE, at generation time, that silently stopped
-- identifying a row after a reload while `unique` stayed green forever, because
-- the test only ever checked the ALREADY-DEDUPED output). key_proof below re-runs
-- scripts/generate_staging_models.py's key_is_unique_within_each_load() math live,
-- every build: COUNT(*) vs COUNT(DISTINCT HASH(registry_id)), grouped by
-- _SOURCE_RUN_ID when that column is a genuine load id (>= 100 rows/run average --
-- some CMS tables stamp a per-ROW uuid there instead, which would make ANY key
-- "prove" unique; MIN_ROWS_PER_LOAD=100 mirrors the generator exactly).
-- Live-verified 2026-09-20: 5,300,149 rows, 5,300,149 distinct REGISTRY_ID, 1 load
-- to date, zero collision -- proven, so the QUALIFY below partitions by
-- registry_id alone. If a future reload ever breaks that, would_collapse > 0 and
-- the SAME QUALIFY automatically falls back to a whole-row partition (every data
-- column, so only exact copies collapse) -- schema.yml's `unique` test should be
-- dropped the day this ever shows would_collapse > 0.

with source as (
    select * from {{ source('ripple_raw', 'FED_EPA_FRS_FULL') }}
),

key_load_shape as (
    select count(*) as total_rows, count(distinct "_SOURCE_RUN_ID") as n_runs
    from source
),

key_proof as (
    select coalesce(sum(n - d), 0) as would_collapse
    from (
        select
            case when ls.n_runs > 0 and ls.total_rows / ls.n_runs >= 100
                 then s."_SOURCE_RUN_ID" else '__ALL__' end    as _load_id,
            count(*)                                            as n,
            count(distinct hash(s."REGISTRY_ID"))               as d
        from source s
        cross join key_load_shape ls
        group by 1
    )
),

renamed as (

select
    trim("REGISTRY_ID")                             as registry_id,
    trim("PRIMARY_NAME")                            as facility_name,
    trim("LOCATION_ADDRESS")                        as address,
    trim("SUPPLEMENTAL_LOCATION")                   as supplemental_location,
    trim("CITY_NAME")                               as city,
    trim("COUNTY_NAME")                             as county,
    trim("FIPS_CODE")                               as fips_code,
    trim("STATE_CODE")                              as state_code,
    trim("STATE_NAME")                              as state_name,
    trim("POSTAL_CODE")                             as postal_code,
    trim("CONGRESSIONAL_DIST_NUM")                  as congressional_district,
    trim("EPA_REGION_CODE")                         as epa_region,
    trim("SITE_TYPE_NAME")                          as site_type,
    trim("FEDERAL_FACILITY_CODE")                   as federal_facility_code,
    trim("FEDERAL_AGENCY_NAME")                     as federal_agency,
    trim("TRIBAL_LAND_CODE")                        as tribal_land_code,
    trim("TRIBAL_LAND_NAME")                        as tribal_land_name,
    {{ stg_float('"LATITUDE83"') }}                     as latitude,
    {{ stg_float('"LONGITUDE83"') }}                    as longitude,
    trim("PGM_SYS_ACRNMS")                         as program_system_acronyms,
    -- FIXED 2026-08-20 (time-index scan): EPA ships these as DD-MON-YY with a
    -- TWO-DIGIT year ('01-MAR-00', '02-JUN-16', '25-SEP-25'). A bare try_to_date
    -- read the year literally, landing all 5,300,149 create dates and 2,782,106
    -- update dates in years 0000-0026. Verified against the raw landing table.
    -- Pivot 2069: EPA's registry postdates 1990, so every 2-digit year is 20xx.
    {{ ripple_ts_from_date('"CREATE_DATE"', 'dmon2', 2069) }}::date as create_date,
    {{ ripple_ts_from_date('"UPDATE_DATE"', 'dmon2', 2069) }}::date as update_date,
    (trim("FEDERAL_FACILITY_CODE") = 'Y') as is_federal_facility,
    (trim("TRIBAL_LAND_CODE") = 'Y') as is_on_tribal_land,
    "_INGESTED_AT" as _loaded_at,
    "_SOURCE_RUN_ID" as _source_run_id
from source

)

select
    r.registry_id, r.facility_name, r.address, r.supplemental_location, r.city, r.county,
    r.fips_code, r.state_code, r.state_name, r.postal_code, r.congressional_district,
    r.epa_region, r.site_type, r.federal_facility_code, r.federal_agency, r.tribal_land_code,
    r.tribal_land_name, r.latitude, r.longitude, r.program_system_acronyms, r.create_date,
    r.update_date, r.is_federal_facility, r.is_on_tribal_land, r._loaded_at, r._source_run_id
from renamed r
cross join key_proof kp
-- partition: registry_id is unconditional; every other column only engages
-- (goes non-null) when kp.would_collapse != 0, i.e. the key is NOT proven --
-- at that point this IS a whole-row partition, same shape as
-- generate_staging_models.py's fallback.
qualify row_number() over (
    partition by
        r.registry_id,
        case when kp.would_collapse != 0 then r.facility_name else null end,
        case when kp.would_collapse != 0 then r.address else null end,
        case when kp.would_collapse != 0 then r.supplemental_location else null end,
        case when kp.would_collapse != 0 then r.city else null end,
        case when kp.would_collapse != 0 then r.county else null end,
        case when kp.would_collapse != 0 then r.fips_code else null end,
        case when kp.would_collapse != 0 then r.state_code else null end,
        case when kp.would_collapse != 0 then r.state_name else null end,
        case when kp.would_collapse != 0 then r.postal_code else null end,
        case when kp.would_collapse != 0 then r.congressional_district else null end,
        case when kp.would_collapse != 0 then r.epa_region else null end,
        case when kp.would_collapse != 0 then r.site_type else null end,
        case when kp.would_collapse != 0 then r.federal_facility_code else null end,
        case when kp.would_collapse != 0 then r.federal_agency else null end,
        case when kp.would_collapse != 0 then r.tribal_land_code else null end,
        case when kp.would_collapse != 0 then r.tribal_land_name else null end,
        case when kp.would_collapse != 0 then r.latitude else null end,
        case when kp.would_collapse != 0 then r.longitude else null end,
        case when kp.would_collapse != 0 then r.program_system_acronyms else null end,
        case when kp.would_collapse != 0 then r.create_date else null end,
        case when kp.would_collapse != 0 then r.update_date else null end,
        case when kp.would_collapse != 0 then r._source_run_id else null end
    order by r._loaded_at desc,
             -- tie-breakers 2026-09-18: the row's own values, so the same row wins every run
             r.facility_name nulls last, r.address nulls last, r.supplemental_location nulls last,
             r.city nulls last, r.county nulls last, r.fips_code nulls last,
             r.state_code nulls last, r.state_name nulls last, r.postal_code nulls last,
             r.congressional_district nulls last, r.epa_region nulls last,
             r.site_type nulls last, r.federal_facility_code nulls last,
             r.federal_agency nulls last, r.tribal_land_code nulls last,
             r.tribal_land_name nulls last, r.latitude nulls last, r.longitude nulls last,
             r.program_system_acronyms nulls last, r.create_date nulls last, r.update_date nulls last,
             r._source_run_id nulls last
) = 1
