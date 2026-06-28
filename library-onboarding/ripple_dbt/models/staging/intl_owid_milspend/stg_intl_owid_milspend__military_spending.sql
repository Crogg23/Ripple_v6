{{ config(materialized='view') }}

-- OWID / SIPRI military-expenditure panel (9,112 rows, 1949-2025).
-- One row = one (entity, year). VALUE is ABSOLUTE current US$.
--
-- Trap fixes (2026-06-27 discovery sweep, findings #74 + #90):
--
--   * is_aggregate -- 771 of 9,112 rows are NOT countries and will
--     double-/triple-count if summed. They come in TWO flavors, and
--     blank CODE alone does NOT isolate them (finding #74 correction):
--       (a) 644 SIPRI REGIONAL aggregates carry a BLANK code (CODE = '').
--       (b) 127 OWID pseudo-code rows carry CODE LIKE 'OWID_%' -- this
--           includes 'World' (OWID_WRL, 2.77e12, the table max) plus
--           historical states (USSR, Czechoslovakia, East Germany, Yemen
--           Arab Republic) that TIME-OVERLAP their successor countries,
--           and Kosovo. These are aggregates / non-standard codes too.
--     is_aggregate = TRUE when the row is blank-code OR OWID_%-code.
--     iso_code is left NULL on every aggregate row so a real ISO3 = a
--     real present-day country. DOWNSTREAM RULE: any cross-country SUM or
--     correlation MUST filter `where not is_aggregate` (equivalently
--     `where iso_code is not null`) or it will inflate the total.
--
--   * NEEDS PER-GDP / PER-CAPITA NORMALIZATION -- military_expenditure is
--     absolute current US$ with NO GDP or population column in this source
--     (finding #90). Raw cross-country correlations against it are
--     economy-SIZE artifacts, not guns-vs-butter signal (e.g. CORR with
--     life-expectancy is ~0.055, a near-zero size artifact). Normalize by
--     GDP or population (join an external denominator) before any
--     cross-country comparison. Genuine zeros exist (Costa Rica, Iceland
--     are real demilitarized 0s, not nulls) -- do not scrub them.

with source as (

    select * from {{ source('ripple_raw', 'INTL_OWID_MILSPEND') }}

),

renamed_cast as (

    select

        -- identifiers
        -- ENTITY is the natural key partner with YEAR (present on every row,
        -- unique per year incl. aggregates). Kept verbatim for lineage.
        trim(ENTITY)                                        as country,

        -- iso_code: ONLY a real 3-letter ISO3 country code. Blank-code SIPRI
        -- regions AND OWID_%-pseudo codes (World, historical states, Kosovo)
        -- collapse to NULL -- so iso_code is not null <=> a real country row.
        case
            when regexp_like(trim(CODE), '[A-Za-z]{3}')
                 and not startswith(upper(trim(CODE)), 'OWID_')
            then upper(trim(CODE))
        end                                                 as iso_code,

        -- the raw OWID code, kept for lineage (carries blanks + OWID_ pseudo).
        nullif(trim(CODE), '')                              as owid_code,

        try_to_number(trim(YEAR))                           as year,

        -- measure
        -- absolute current US$. try_to_double so any bad text -> NULL not error.
        -- (verified: 0 uncastable rows; 180 genuine '0' values are kept.)
        try_to_double(trim(MILITARY_EXPENDITURE))           as military_expenditure_usd,

        -- attributes
        nullif(trim(WORLD_REGION_ACCORDING_TO_OWID), '')    as world_region,

        -- aggregate guard: TRUE for any non-real-country row (blank code OR
        -- OWID_ pseudo-code). Downstream summation MUST exclude these.
        (
            nullif(trim(CODE), '') is null
            or startswith(upper(trim(CODE)), 'OWID_')
        )                                                   as is_aggregate,

        -- pipeline audit columns (this table landed them WITHOUT a leading
        -- underscore: INGESTED_AT is epoch-micros NUMBER, SOURCE_RUN_ID text).
        to_timestamp_ntz(INGESTED_AT, 6)                    as _ingested_at,
        nullif(trim(try_cast(SOURCE_RUN_ID as text)), '')   as _source_run_id

    from source

),

deduped as (

    select
        *,
        row_number() over (
            partition by country, year
            order by _ingested_at desc nulls last
        ) as _row_num
    from renamed_cast

)

select * exclude (_row_num)
from deduped
where _row_num = 1
