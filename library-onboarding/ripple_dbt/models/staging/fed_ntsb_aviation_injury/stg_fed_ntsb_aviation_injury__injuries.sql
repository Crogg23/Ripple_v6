{{ config(materialized='view') }}

/*
  Generated 2026-08-10 (backlog wave 4) from live-verified specs.
  NTSB aviation accident database, injury table: injury counts per event,
  aircraft, person category, and injury level. EV_ID joins to the NTSB
  aviation events mart (stg_fed_ntsb_aviation_events__events).
  Grain: one row = one event x aircraft x person category x injury level
  (verified exactly unique).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_NTSB_AVIATION_INJURY') }}
),

renamed as (
    select
        -- identifiers
        {{ dbt_utils.generate_surrogate_key(['EV_ID', 'AIRCRAFT_KEY', 'INJ_PERSON_CATEGORY', 'INJURY_LEVEL']) }}
                                                                   as injury_record_id,
        nullif(trim(EV_ID), '')                                    as ev_id,
        nullif(trim(AIRCRAFT_KEY), '')                             as aircraft_key,
        nullif(trim(INJ_PERSON_CATEGORY), '')                      as inj_person_category,
        nullif(trim(INJURY_LEVEL), '')                             as injury_level,

        -- measures
        try_to_number(nullif(trim(INJ_PERSON_COUNT), ''), 18, 4)   as inj_person_count,

        -- record maintenance
        try_to_date(left(nullif(trim(LCHG_DATE), ''), 10))         as lchg_date,
        nullif(trim(LCHG_USERID), '')                              as lchg_userid,

        -- metadata
        to_timestamp_ntz(INGESTED_AT, 6)                           as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                            as _source_run_id
    from source
)

select * from renamed
