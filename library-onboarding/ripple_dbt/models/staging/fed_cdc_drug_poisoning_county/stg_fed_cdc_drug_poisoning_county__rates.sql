{{ config(materialized='view') }}

{#
    stg_fed_cdc_drug_poisoning_county__rates

    CDC drug-poisoning mortality by US county-year (NCHS Data Brief data file).
    TRAP (finding #68): the rate column
    ESTIMATED_AGE_ADJUSTED_DEATH_RATE_11_CATEGORIES_IN_RANGES is a BINNED TEXT
    RANGE -- exactly 16 ordinal bins ('0-2', '2.1-4', ... '28.1-30', '>30'), and
    0 of 53,387 rows parse as a number. It is NOT a numeric death rate. Do NOT
    cast it. We keep it as rate_band (ordinal category text) and add
    rate_band_ordinal (1..16) mapped in natural order. There are ZERO blank rate
    rows -- every present county-year carries a bin (no in-county suppression).

    POPULATION *is* numeric (53,383 / 53,387 parse) so it casts cleanly.

    KEY: fips || year is the natural key (53,387 distinct pairs = 53,387 rows,
    verified unique). 3,141 distinct FIPS = full US county count. The
    3139/3140/3141 county-per-year wobble is 3 real FIPS-lifecycle counties
    (08014 Broomfield CO created 2001, 51515 Bedford city VA merged 2013,
    02068 Denali Borough AK), NOT statistical suppression -- so we just expose
    fips cleanly and let downstream balance the panel if needed.
#}

with source as (

    select * from {{ source('ripple_raw', 'FED_CDC_DRUG_POISONING_COUNTY') }}

),

renamed_cast as (

    select

        -- geography (join keys)
        nullif(trim(FIPS), '')                                  as fips,
        try_to_number(trim(YEAR))                               as year,
        nullif(trim(STATE), '')                                 as state_name,
        nullif(trim(ST), '')                                    as state_abbr,
        nullif(trim(FIPS_STATE), '')                            as fips_state,
        nullif(trim(COUNTY), '')                                as county_name,

        -- population (genuinely numeric)
        try_to_number(trim(POPULATION))                         as population,

        -- TRAP: binned text range -- ordinal category, NOT a numeric rate.
        nullif(trim(ESTIMATED_AGE_ADJUSTED_DEATH_RATE_11_CATEGORIES_IN_RANGES), '')
                                                                as rate_band,

        -- ordinal rank of the band in natural (low->high) order, 1..16.
        case nullif(trim(ESTIMATED_AGE_ADJUSTED_DEATH_RATE_11_CATEGORIES_IN_RANGES), '')
            when '0-2'     then 1
            when '2.1-4'   then 2
            when '4.1-6'   then 3
            when '6.1-8'   then 4
            when '8.1-10'  then 5
            when '10.1-12' then 6
            when '12.1-14' then 7
            when '14.1-16' then 8
            when '16.1-18' then 9
            when '18.1-20' then 10
            when '20.1-22' then 11
            when '22.1-24' then 12
            when '24.1-26' then 13
            when '26.1-28' then 14
            when '28.1-30' then 15
            when '>30'     then 16
        end                                                     as rate_band_ordinal,

        -- pipeline audit columns (landed without leading underscore here;
        -- INGESTED_AT is microsecond epoch -> NTZ timestamp).
        to_timestamp_ntz(INGESTED_AT, 6)                        as _ingested_at,
        nullif(trim(try_cast(SOURCE_RUN_ID as text)), '')       as _source_run_id

    from source

),

deduped as (

    select
        *,
        row_number() over (
            partition by fips, year
            order by _ingested_at desc nulls last
        ) as _row_num
    from renamed_cast

)

select * exclude (_row_num)
from deduped
where _row_num = 1
