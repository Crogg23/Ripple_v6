{{ config(materialized='table') }}

-- =============================================================================
-- justice__racial_jail_disparity
-- -----------------------------------------------------------------------------
-- Black/White JAIL-rate disparity per county-year, built from Vera's own
-- published per-race jail-rate columns (point-in-time jail population per
-- 100k working-age residents of each race).
--
-- Grain: one row = one county x one year.
-- Key:   county_year_key  (county_fips || '-' || year)
--
-- Headline (finding #54, 2019 cross-section, measurable cohort):
--   Black residents jailed at a higher rate than White in 612 of 637 counties
--   (96%) with >= 5,000 Black working-age residents; median Black/White
--   jail-rate ratio = 3.16x.
--
-- The measurable cohort (is_measurable_cohort) reproduces that 637-county set:
--   year = 2019, both race rates > 0, black_working_age_pop >= 5000.
-- 2019 is the canonical cross-section (most measurable counties / last good
-- Vera reporting year); is_canonical_year flags it but ALL years are kept.
--
-- Caveat: jail rate is point-in-time held population over county-resident race
-- denominators. For centralized-jail jurisdictions (e.g. NYC boroughs) the
-- held population may not map 1:1 to county residents, inflating the most
-- extreme borough ratios. Direction is unambiguous; frame extreme ratios
-- carefully.
-- =============================================================================

with

base as (

    select * from {{ ref('stg_xc_vera_incarceration_trends__county_year') }}

),

final as (

    select

        -- -------------------------------------------------------
        -- Grain key + identifiers exposed for cross-source joins
        -- -------------------------------------------------------
        county_fips || '-' || year         as county_year_key,   -- primary key (one row = one county-year)
        county_fips                         as fips,              -- county FIPS (GEO join key)
        year                                as year,
        county_name,
        state_abbr,
        state_fips,
        region,
        division,
        urbanicity,
        is_stub_year,

        -- -------------------------------------------------------
        -- Per-race jail rates (per 100k working-age residents)
        -- -------------------------------------------------------
        black_jail_pop_rate                 as black_jail_rate,   -- Black jail pop per 100k Black working-age
        white_jail_pop_rate                 as white_jail_rate,   -- White jail pop per 100k White working-age
        latinx_jail_pop_rate                as latinx_jail_rate,
        total_jail_pop_rate                 as total_jail_rate,

        -- -------------------------------------------------------
        -- The disparity signal
        -- -------------------------------------------------------
        round(
            black_jail_pop_rate / nullif(white_jail_pop_rate, 0)
        , 4)                                as bw_ratio,          -- Black:White jail-rate ratio

        case
            when black_jail_pop_rate is null
              or white_jail_pop_rate is null then null
            when black_jail_pop_rate > white_jail_pop_rate then true
            else false
        end                                 as is_black_rate_higher,

        round(
            black_jail_pop_rate - white_jail_pop_rate
        , 2)                                as bw_rate_gap,       -- absolute gap (Black minus White, per 100k)

        -- -------------------------------------------------------
        -- Working-age populations (the rate denominators)
        -- -------------------------------------------------------
        black_pop_15to64                    as black_working_age_pop,
        white_pop_15to64                    as white_working_age_pop,
        latinx_pop_15to64                   as latinx_working_age_pop,
        total_pop_15to64                    as total_working_age_pop,

        -- -------------------------------------------------------
        -- Raw jail population counts (context for the rates)
        -- -------------------------------------------------------
        black_jail_pop,
        white_jail_pop,
        total_jail_pop,

        -- -------------------------------------------------------
        -- Cohort / canonical-year flags
        -- -------------------------------------------------------
        -- Measurable cohort: big enough Black working-age population that the
        -- ratio is not a small-number artifact, and both rates are non-zero.
        case
            when black_pop_15to64 >= 5000
             and black_jail_pop_rate > 0
             and white_jail_pop_rate > 0 then true
            else false
        end                                 as is_measurable_cohort,

        -- Canonical cross-section year for the headline (most complete).
        case when year = 2019 then true else false end
                                            as is_canonical_year,

        -- -------------------------------------------------------
        -- Metadata
        -- -------------------------------------------------------
        _ingested_at,
        _source_run_id

    from base

)

select * from final
