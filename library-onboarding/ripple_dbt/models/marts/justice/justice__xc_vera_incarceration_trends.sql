{{ config(materialized='table', schema='JUSTICE') }}

-- GRAIN: one row per county-year (year_county_fips is unique)
-- Answers: How do incarceration rates vary by county, race, and over time?
-- Source: Vera Institute Incarceration Trends (~230K county-year observations)
-- Key joins: county_fips → geography; state_fips → geography

select
    year_county_fips,
    try_to_number(year)                          as year,
    county_fips,
    state_fips,
    county_name,
    state_abbr,
    urbanicity,
    region,
    division,
    try_to_number(total_pop_15to64)              as total_pop_15to64,
    try_to_number(white_pop_15to64)              as white_pop_15to64,
    try_to_number(black_pop_15to64)              as black_pop_15to64,
    try_to_number(latinx_pop_15to64)             as latinx_pop_15to64,
    try_to_number(total_jail_pop)                as total_jail_pop,
    try_to_number(black_jail_pop)                as black_jail_pop,
    try_to_number(white_jail_pop)                as white_jail_pop,
    try_to_double(total_jail_pop_rate)           as total_jail_pop_rate,
    try_to_double(black_jail_pop_rate)           as black_jail_pop_rate,
    try_to_double(white_jail_pop_rate)           as white_jail_pop_rate,
    try_to_double(latinx_jail_pop_rate)          as latinx_jail_pop_rate,
    try_to_number(total_prison_pop)              as total_prison_pop,
    try_to_number(black_prison_pop)              as black_prison_pop,
    try_to_number(white_prison_pop)              as white_prison_pop,
    try_to_double(total_prison_pop_rate)         as total_prison_pop_rate,
    try_to_number(total_incarceration)           as total_incarceration,
    try_to_double(total_incarceration_rate)      as total_incarceration_rate,
    (is_stub_year = 'true') as is_stub_year,
    _ingested_at,
    _source_run_id
from {{ ref('stg_xc_vera_incarceration_trends__county_year') }}
