{{ config(materialized='table') }}

--
-- justice__county_double_burden
-- ---------------------------------------------------------------------------
-- One row per US county (FIPS). Crosses two independent county-level signals
-- and flags counties that sit in the top decile of BOTH:
--
--   Axis A -- drug-overdose intensity
--     Source: stg_fed_cdc_drug_poisoning_county__rates
--     The CDC publishes the county death rate as a BINNED TEXT band
--     (e.g. '14.1-16', '>30'); the staging model carries an ordinal
--     (RATE_BAND_ORDINAL, 1=lowest .. 16='>30'=highest). The source has
--     multiple rows per county, so we collapse to the MAX band per FIPS
--     (the county's peak observed overdose intensity) and rank on that.
--
--   Axis B -- jail incarceration rate
--     Source: stg_xc_vera_incarceration_trends__county_year
--     County-year panel. We take the LATEST valid jail-rate year per county
--     (jail series is valid through 2024), excluding stub years and
--     null/zero rates. TOTAL_JAIL_POP_RATE = jail population per 100k
--     residents 15-64.
--
-- THE RULE (reusable, clean):
--     percent_rank() within the joined county universe on each axis, then
--     double_burden = (overdose_pctile >= 0.9 AND jail_pctile >= 0.9).
--     percent_rank() is robust to the coarse tied overdose ordinal: a tie
--     group inherits the percentile of its lowest member, so a county only
--     clears 0.9 if its band genuinely sits in the top decile.
--
-- Reproduces (2026-06-27 discovery sweep):
--   #20 -- Eastern Kentucky is the overdose+jail double-extreme epicenter.
--          KY is ~4% of joined counties (120/3029) but ~24% of the
--          double-burden set (13 of 54) -- ~6x over-represented, #1 state.
--   #7  -- West Virginia is the mirror: essentially the same (worst)
--          overdose intensity as KY but ~half the jail rate, so it barely
--          lands in the double-extreme set while KY dominates.
-- ---------------------------------------------------------------------------

with

-- Axis A: peak overdose band per county (collapse duplicate source rows)
overdose as (

    select
        fips                                as fips,
        any_value(state_abbr)               as state_abbr,
        any_value(state_name)               as state_name,
        any_value(county_name)              as county_name,
        max(rate_band_ordinal)              as overdose_band_ordinal,
        max_by(rate_band, rate_band_ordinal) as overdose_rate_band
    from {{ ref('stg_fed_cdc_drug_poisoning_county__rates') }}
    where fips is not null
      and rate_band_ordinal is not null
    group by fips

),

-- Axis B: latest valid jail-rate year per county (exclude stub years + null/zero)
jail_ranked as (

    select
        county_fips                         as fips,
        year                                as jail_year,
        county_name                         as vera_county_name,
        state_abbr                          as vera_state_abbr,
        total_jail_pop_rate                 as jail_rate,
        total_jail_pop                      as jail_population,
        black_jail_pop_rate                 as black_jail_rate,
        white_jail_pop_rate                 as white_jail_rate,
        row_number() over (
            partition by county_fips
            order by year desc
        )                                   as rn
    from {{ ref('stg_xc_vera_incarceration_trends__county_year') }}
    where county_fips is not null
      and is_stub_year = false
      and total_jail_pop_rate is not null
      and total_jail_pop_rate > 0

),

jail as (

    select *
    from jail_ranked
    where rn = 1

),

-- Inner join: only counties with BOTH a valid overdose band and a valid jail rate
joined as (

    select
        o.fips                                          as fips,
        coalesce(o.state_abbr, j.vera_state_abbr)       as state_abbr,
        o.state_name                                    as state_name,
        coalesce(o.county_name, j.vera_county_name)     as county_name,
        o.overdose_rate_band                            as overdose_rate_band,
        o.overdose_band_ordinal                         as overdose_band_ordinal,
        j.jail_rate                                     as jail_rate,
        j.jail_year                                     as jail_rate_year,
        j.jail_population                               as jail_population,
        j.black_jail_rate                               as black_jail_rate,
        j.white_jail_rate                               as white_jail_rate
    from overdose o
    join jail   j on o.fips = j.fips

),

-- The reusable p90 cross-axis ranking
ranked as (

    select
        *,
        percent_rank() over (order by overdose_band_ordinal) as overdose_pctile,
        percent_rank() over (order by jail_rate)             as jail_pctile
    from joined

),

final as (

    select

        -- ---------------------------------------------------------------
        -- Grain key + geography
        -- ---------------------------------------------------------------
        fips                                as fips,            -- primary key (one row = one county)
        state_abbr                          as state_abbr,
        state_name                          as state_name,
        county_name                         as county_name,

        -- ---------------------------------------------------------------
        -- Axis A: overdose intensity (CDC drug-poisoning band)
        -- ---------------------------------------------------------------
        overdose_rate_band                  as overdose_rate_band,     -- e.g. '14.1-16', '>30'
        overdose_band_ordinal               as overdose_metric,        -- ranked metric (1..16, higher=worse)
        round(overdose_pctile, 4)           as overdose_pctile,        -- 0..1 within joined universe

        -- ---------------------------------------------------------------
        -- Axis B: jail incarceration rate (Vera, latest valid year)
        -- ---------------------------------------------------------------
        jail_rate                           as jail_rate,              -- jail pop per 100k residents 15-64
        jail_rate_year                      as jail_rate_year,         -- year the jail rate is drawn from
        jail_population                     as jail_population,
        black_jail_rate                     as black_jail_rate,
        white_jail_rate                     as white_jail_rate,
        round(jail_pctile, 4)               as jail_pctile,            -- 0..1 within joined universe

        -- ---------------------------------------------------------------
        -- The double-burden flags
        -- ---------------------------------------------------------------
        (overdose_pctile >= 0.9)                            as is_overdose_top_decile,
        (jail_pctile     >= 0.9)                            as is_jail_top_decile,
        (overdose_pctile >= 0.9 and jail_pctile >= 0.9)     as double_burden

    from ranked

)

select * from final
