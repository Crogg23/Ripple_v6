{{ config(materialized='view', tags=['spine_generated']) }}

-- GRAIN: one row per investigation-vehicle-RECALL combination (see 2026-07-31 note)
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

-- 2026-07-28 fix: widened the key from (action_number, make, model, year_txt) to
-- add compname/mfr_name, recovering 30,748 -> 51,871 rows. That commit's own comment
-- said the grain was "still not fully verified" -- it wasn't, and the gap was real.
--
-- 2026-07-31: found via tests/test_mart_duplication.py, which caught this mart
-- disagreeing with a duplicate auto-generated copy (154,209 raw rows vs 51,871 here).
-- Root cause: recall_number was NOT in the key, so a single investigation into a
-- single vehicle/component -- e.g. action AQ09001, an HID headlight kit defect --
-- silently collapsed to whichever ONE of its (documented, real) 11 separate recall
-- campaigns happened to sort last. `resulted_in_recall` and `recall_number` in the
-- mart above were therefore correct in DIRECTION but arbitrary in WHICH campaign,
-- for every investigation that spans more than one recall.
--
-- recall_number now joins the key. Verified live: EVERY one of the 7,373 groups the
-- old key collapsed had genuine variation in recall_number, subject, or dates
-- underneath it -- none of it was noise, all of it was distinct real information.
-- Adding recall_number recovers the full 154,209 rows with ZERO further collapsing
-- (confirmed: COUNT(DISTINCT full 7-column key) == COUNT(*) == 154,209), so this key
-- is now provably exact -- not "wider and still unverified" like the last two passes.
select * from renamed
qualify row_number() over (
    partition by nhtsa_action_number, make, model, year_txt, compname, mfr_name,
                 recall_number
    order by _loaded_at desc
) = 1
