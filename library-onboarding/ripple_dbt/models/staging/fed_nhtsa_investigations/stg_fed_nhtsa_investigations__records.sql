{{ config(materialized='view', tags=['spine_generated']) }}

-- GRAIN: one row per investigation-make-model-year combination
-- SPINE_ENTITY: not determined (investigation records, not a single entity)
-- Source: NHTSA ODI Investigations — ~154K records
-- Key joins: nhtsa_action_number → links to recalls; mfr_name → manufacturer entities

with source as (
    select * from {{ source('ripple_raw', 'FED_NHTSA_INVESTIGATIONS') }}
),

renamed as (
    select
        trim(C1)                               as nhtsa_action_number,
        trim(C2)                               as make,
        trim(C3)                               as model,
        trim(C4)                               as year_txt,
        trim(C5)                               as compname,
        trim(C6)                               as mfr_name,
        try_to_date(trim(C7), 'YYYYMMDD')      as open_date,
        try_to_date(trim(C8), 'YYYYMMDD')      as close_date,
        trim(C9)                               as recall_number,
        trim(C10)                              as subject,
        C11                                    as summary,
        "_INGESTED_AT"                         as _loaded_at,
        "_SOURCE_RUN_ID"                       as _source_run_id
    from source
)

-- 2026-07-28 fix: the original key (nhtsa_action_number, make, model, year_txt)
-- ignored compname/mfr_name, which ARE exposed as distinct columns downstream --
-- one investigation commonly covers multiple components/manufacturers under the
-- same action number. Confirmed live: widening the key recovers 30,748 -> 51,871
-- distinct rows (real rows, not just theoretical). Grain is still not fully
-- verified -- a sample showed some rows identical across all 6 of these fields
-- too, so genuine exact-duplicate rows likely remain beyond this fix.
select * from renamed
qualify row_number() over (
    partition by nhtsa_action_number, make, model, year_txt, compname, mfr_name
    order by _loaded_at desc
) = 1
