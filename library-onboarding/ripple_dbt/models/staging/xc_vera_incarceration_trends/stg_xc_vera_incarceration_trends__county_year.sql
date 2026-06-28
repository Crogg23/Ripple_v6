{{ config(materialized='view') }}

{#
    stg_xc_vera_incarceration_trends__county_year
    -----------------------------------------------------------------------
    Vera Institute "Incarceration Trends" county-year panel (3,075 counties,
    1970-2026). One row = one (year, county_fips). Source columns are all TEXT.

    TRAPS NEUTRALIZED (verified 2026-06-27, findings #13/#32/#14/#54):

    (1) PRISON SERIES DEAD-ENDS AT 2019. Every row for year >= 2020 carries a
        BLANK '' for TOTAL_PRISON_POP / TOTAL_INCARCERATION and all the prison
        *rate* columns. Blank means MISSING, not zero -- a naive COALESCE(...,0)
        would read it as decarceration-to-zero. We hard-NULL the entire prison +
        total-incarceration block whenever year > 2019 so it can NEVER be coerced
        to 0 downstream. (Pre-2020 genuine blanks also stay NULL via try_to_*.)

    (2) JAIL SERIES is usable through 2024 -- left intact (try_to_* keeps true
        blanks as NULL).

    (3) 2025-2026 are population-only PLACEHOLDER STUBS: TOTAL_POP_15TO64 is blank
        and no prison data exists. is_stub_year flags them so a mart can filter
        (these years are also only 5-11 self-selecting states -- finding #14).

    (4) Racial-disparity columns the downstream mart consumes are exposed
        explicitly: black/white jail pop + jail rate, and the race population
        denominators (BLACK_POP_15TO64 / WHITE_POP_15TO64).

    Counts/rates cast with try_to_double so bad input -> NULL (never error);
    genuine blanks stay NULL (never coalesced to 0).
#}

with source as (

    select * from {{ source('ripple_raw', 'XC_VERA_INCARCERATION_TRENDS') }}

),

renamed_cast as (

    select

        -- ---- geography / time keys -------------------------------------
        -- composite natural key (year, county_fips) is unique across all
        -- 128,507 rows; surrogate built for a single-column unique test.
        trim(YEAR) || '|' || trim(COUNTY_FIPS)              as year_county_fips,
        try_to_number(trim(YEAR))                           as year,
        nullif(trim(COUNTY_FIPS), '')                       as county_fips,
        nullif(trim(COUNTY_NAME), '')                       as county_name,
        nullif(trim(STATE_ABBR), '')                        as state_abbr,
        nullif(trim(STATE_FIPS), '')                        as state_fips,
        nullif(trim(URBANICITY), '')                        as urbanicity,
        nullif(trim(REGION), '')                            as region,
        nullif(trim(DIVISION), '')                          as division,

        -- coverage flag: 2025-2026 are population-only placeholder stubs
        -- (no usable jail/prison data, blank population, 5-11 states only)
        case when try_to_number(trim(YEAR)) > 2024 then true else false end
                                                            as is_stub_year,

        -- ---- population denominators (15-64 working-age) ---------------
        try_to_double(trim(TOTAL_POP_15TO64))               as total_pop_15to64,
        try_to_double(trim(BLACK_POP_15TO64))               as black_pop_15to64,
        try_to_double(trim(WHITE_POP_15TO64))               as white_pop_15to64,
        try_to_double(trim(LATINX_POP_15TO64))              as latinx_pop_15to64,

        -- ---- JAIL series (usable through 2024) -------------------------
        try_to_double(trim(TOTAL_JAIL_POP))                 as total_jail_pop,
        try_to_double(trim(BLACK_JAIL_POP))                 as black_jail_pop,
        try_to_double(trim(WHITE_JAIL_POP))                 as white_jail_pop,
        try_to_double(trim(TOTAL_JAIL_POP_RATE))            as total_jail_pop_rate,
        try_to_double(trim(BLACK_JAIL_POP_RATE))            as black_jail_pop_rate,
        try_to_double(trim(WHITE_JAIL_POP_RATE))            as white_jail_pop_rate,
        try_to_double(trim(LATINX_JAIL_POP_RATE))           as latinx_jail_pop_rate,

        -- ---- PRISON + TOTAL-INCARCERATION series ------------------------
        -- TRAP: dead-ends at 2019. For year > 2019 the source stores BLANK
        -- (= missing, NOT zero). Hard-NULL the whole block so it can never be
        -- coalesced to 0 downstream. <=2019 keeps real values (blanks -> NULL).
        case when try_to_number(trim(YEAR)) <= 2019
             then try_to_double(trim(TOTAL_PRISON_POP)) end as total_prison_pop,
        case when try_to_number(trim(YEAR)) <= 2019
             then try_to_double(trim(BLACK_PRISON_POP)) end as black_prison_pop,
        case when try_to_number(trim(YEAR)) <= 2019
             then try_to_double(trim(WHITE_PRISON_POP)) end as white_prison_pop,
        case when try_to_number(trim(YEAR)) <= 2019
             then try_to_double(trim(TOTAL_PRISON_POP_RATE)) end as total_prison_pop_rate,
        case when try_to_number(trim(YEAR)) <= 2019
             then try_to_double(trim(BLACK_PRISON_POP_RATE)) end as black_prison_pop_rate,
        case when try_to_number(trim(YEAR)) <= 2019
             then try_to_double(trim(WHITE_PRISON_POP_RATE)) end as white_prison_pop_rate,
        case when try_to_number(trim(YEAR)) <= 2019
             then try_to_double(trim(TOTAL_INCARCERATION)) end as total_incarceration,
        case when try_to_number(trim(YEAR)) <= 2019
             then try_to_double(trim(TOTAL_INCARCERATION_RATE)) end as total_incarceration_rate,

        -- ---- pipeline audit columns ------------------------------------
        to_timestamp_ntz(INGESTED_AT, 6)                    as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                     as _source_run_id

    from source

),

deduped as (

    select
        *,
        row_number() over (
            partition by year, county_fips
            order by _ingested_at desc nulls last
        ) as _row_num
    from renamed_cast

)

select * exclude (_row_num)
from deduped
where _row_num = 1
