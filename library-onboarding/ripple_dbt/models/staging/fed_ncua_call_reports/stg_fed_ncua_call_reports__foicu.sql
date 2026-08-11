{{ config(materialized='view') }}
-- GRAIN: one row = one federally insured credit union for the 2026-03 cycle (cu_number unique).
-- PROVENANCE: NCUA Call Report quarterly download, FOICU.txt (credit union roster/profile).
-- Loaded 2026-08-11 to replace the broken FED_NCUA_CALL_REPORTS table (which held a data dictionary).
-- Dates arrive as 'M/D/YYYY H:MI:SS' strings, but the MIX of 24-hour and 12-hour-with-AM/PM varies
-- WITHIN columns (verified 2026-08-11: 3 ISSUE_DATE and 1 AM_DATEHELD rows use the other style), so
-- every date column coalesces both explicit formats. A bare try_to_date is the epoch-date bug -- never.

with

source as (
    select * from {{ source('ripple_raw', 'FED_NCUA_CALL_REPORTS_FOICU') }}
),

renamed as (

    select
        nullif(trim(CU_NUMBER), '')                                    as cu_number,
        coalesce(
            try_to_timestamp(nullif(trim(CYCLE_DATE), ''), 'MM/DD/YYYY HH24:MI:SS'),
            try_to_timestamp(nullif(trim(CYCLE_DATE), ''), 'MM/DD/YYYY HH12:MI:SS AM')
        )::date                                                        as cycle_date,
        nullif(trim(JOIN_NUMBER), '')                                  as join_number,
        nullif(trim(RSSD), '')                                         as rssd,
        nullif(trim(CU_TYPE), '')                                      as cu_type,
        nullif(trim(CU_NAME), '')                                      as cu_name,
        nullif(trim(CITY), '')                                         as city,
        nullif(trim(STATE), '')                                        as state,
        nullif(trim(CHARTERSTATE), '')                                 as charterstate,
        nullif(trim(STATE_CODE), '')                                   as state_code,
        nullif(trim(ZIP_CODE), '')                                     as zip_code,
        nullif(trim(COUNTY_CODE), '')                                  as county_code,
        nullif(trim(CONG_DIST), '')                                    as cong_dist,
        nullif(trim(SMSA), '')                                         as smsa,
        nullif(trim(ATTENTION_OF), '')                                 as attention_of,
        nullif(trim(STREET), '')                                       as street,
        nullif(trim(REGION), '')                                       as region,
        nullif(trim(SE), '')                                           as se,
        nullif(trim(DISTRICT), '')                                     as district,
        try_to_number(nullif(trim(YEAR_OPENED), ''))                   as year_opened,
        nullif(trim(TOM_CODE), '')                                     as tom_code,
        nullif(trim(LIMITED_INC), '')                                  as limited_inc,
        coalesce(
            try_to_timestamp(nullif(trim(ISSUE_DATE), ''), 'MM/DD/YYYY HH24:MI:SS'),
            try_to_timestamp(nullif(trim(ISSUE_DATE), ''), 'MM/DD/YYYY HH12:MI:SS AM')
        )::date                                                        as issue_date,
        nullif(trim(PEER_GROUP), '')                                   as peer_group,
        nullif(trim(QUARTER_FLAG), '')                                 as quarter_flag,
        nullif(trim(ISMDI), '')                                        as ismdi,
        coalesce(
            try_to_timestamp(nullif(trim(INSURED_DATE), ''), 'MM/DD/YYYY HH24:MI:SS'),
            try_to_timestamp(nullif(trim(INSURED_DATE), ''), 'MM/DD/YYYY HH12:MI:SS AM')
        )::date                                                        as insured_date,
        coalesce(
            try_to_timestamp(nullif(trim(AM_DATEHELD), ''), 'MM/DD/YYYY HH12:MI:SS AM'),
            try_to_timestamp(nullif(trim(AM_DATEHELD), ''), 'MM/DD/YYYY HH24:MI:SS')
        )                                                              as am_dateheld,
        _INGESTED_AT                                   as _loaded_at,
        _SOURCE_RUN_ID                                 as _source_run_id,
        _SRC_SHA256                                    as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by cu_number
            order by _loaded_at desc
        ) as _row_num
    from renamed
    where cu_number is not null

)

select * exclude (_row_num) from deduped
where _row_num = 1
