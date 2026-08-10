{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_FEMA_NFIP_COMMUNITY_STATUS_BOOK') }}

),

renamed as (

    select

        -- identifiers
        trim(COMMUNITYIDNUMBER)                          as community_id_number,
        trim(COMMUNITYNAME)                              as community_name,
        trim(COUNTY)                                     as county,
        trim(STATE)                                      as state,

        -- map / program dates (ISO timestamps for some, MM/DD/YY for others;
        -- the currently-effective map date can carry a "(M)" suffix, so the
        -- raw text is kept alongside the parsed date)
        try_to_date(left(trim(INITIALFLOODHAZARDBOUNDARYMAP), 10), 'YYYY-MM-DD')  as initial_flood_hazard_boundary_map_date,
        try_to_date(left(trim(INITIALFLOODINSURANCERATEMAP), 10), 'YYYY-MM-DD')   as initial_flood_insurance_rate_map_date,
        trim(CURRENTLYEFFECTIVEMAPDATE)                  as currently_effective_map_date_raw,
        try_to_date(regexp_substr(trim(CURRENTLYEFFECTIVEMAPDATE), '^[0-9]{2}/[0-9]{2}/[0-9]{2}'), 'MM/DD/YY')
                                                         as currently_effective_map_date,
        try_to_date(trim(REGULAREMERGENCYPROGRAMDATE), 'MM/DD/YY')                as regular_emergency_program_date,
        try_to_date(left(trim(ORIGINALENTRYDATE), 10), 'YYYY-MM-DD')              as original_entry_date,

        -- participation / rating
        trim(TRIBAL)                                     as tribal_flag,
        trim(PARTICIPATINGINNFIP)                        as participating_in_nfip_flag,
        try_to_date(left(trim(CLASSRATINGEFFECTIVEDATE), 10), 'YYYY-MM-DD')       as class_rating_effective_date,
        trim(CLASSRATING)                                as crs_class_rating,
        try_to_number(trim(SFHADISCOUNT))                as sfha_discount_pct,
        try_to_number(trim(NONSFHADISCOUNT))             as non_sfha_discount_pct,
        try_to_timestamp_ntz(left(trim(LASTREFRESH), 23), 'YYYY-MM-DD"T"HH24:MI:SS.FF3') as last_refresh_at,

        -- metadata
        to_timestamp_ntz(INGESTED_AT, 6)                 as _ingested_at,
        SOURCE_RUN_ID                                    as _source_run_id,
        SRC_SHA256                                       as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by community_id_number
            order by _ingested_at desc
        ) as _row_num
    from renamed
    where community_id_number is not null

)

select * exclude _row_num
from deduped
where _row_num = 1
