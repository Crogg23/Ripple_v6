{{ config(tags=['minimal_staging']) }}

-- GRAIN: NOT YET DETERMINED (passthrough -- needs manual review before mart use)
-- This is a passthrough staging view: select * from the raw landing table, no
-- dedup, no renaming (source columns already came in snake_case-able as-is).
-- Written by hand for the 2026-08-05 housing/health ingestion phase.
--
-- REPOINTED 2026-08-18: the raw table this view originally pointed at
-- (LIBRARY_RAW.LANDING.FED_COLLEGE_SCORECARD_INSTITUTION) was DROP TABLE'd on
-- 2026-08-09. That was not data loss -- a separate, newer load of the same
-- College Scorecard institution-level source had already landed two days
-- earlier under this repo's FED_ED_* Dept-of-Education naming convention
-- (FED_ED_COLLEGE_SCORECARD_INSTITUTION: same 6,273 rows, same UNITID values).
-- This view now points at that table. The metadata columns differ between the
-- two loads -- the old table had a ready-made _INGESTED_AT timestamp column;
-- the new one only has INGESTED_AT as an epoch-microseconds NUMBER, converted
-- below the same way the curated staging model does it.
-- Note there is already a curated, tested staging model + mart for this same
-- source: stg_fed_ed_college_scorecard_institution__institutions ->
-- education__fed_ed_college_scorecard_institution (~60 curated columns, deduped
-- on unitid). This view has no downstream mart; it exists only as a raw,
-- full-width (3,311-column) passthrough for ad-hoc access to columns the
-- curated model doesn't select.

with source as (

    select * from {{ source('ripple_raw', 'FED_ED_COLLEGE_SCORECARD_INSTITUTION') }}

),

renamed as (

    select
        *,
        to_timestamp_ntz(INGESTED_AT, 6) as _loaded_at,
        'https://collegescorecard.ed.gov/data/' as _source_url

    from source

)

select * from renamed
