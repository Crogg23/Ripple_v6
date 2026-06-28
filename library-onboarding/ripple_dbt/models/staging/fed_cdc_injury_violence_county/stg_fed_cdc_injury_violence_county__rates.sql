{{ config(materialized='view') }}

{#
    CDC injury/violence county death rates (132k rows).

    TRAP (findings #12 / #33): RATE carries a -999 suppression sentinel on
    6,549 rows -- CDC's documented placeholder for suppressed/unstable rates,
    always paired with COUNT_SUP='1-9'. A naive AVG(RATE) returns -38.5 instead
    of +11.6 (a ~50-point swing). We null the sentinel BEFORE casting so the
    cleaned rate column is honest. The landed value is the full-precision string
    '-999.0000000000000', so we feed that exact form to null_sentinel.

    COUNT_SUP is NOT a clean integer: it is the literal string '1-9' (70,549
    rows, 53%) and '10-50' (51 rows) -- low-count privacy-suppression ranges --
    alongside numeric strings. We keep COUNT_SUP as TEXT (count_suppression_flag)
    and do NOT cast the suppressed count to a number; a numeric_count column is
    exposed for the rows that ARE plain integers.

    RATE_M_CI also carries the literal '-999' on the same 6,549 suppressed rows.

    Natural key (verified unique, 132,000/132,000): geoid + intent + period.
#}

with source as (

    select * from {{ source('ripple_raw', 'FED_CDC_INJURY_VIOLENCE_COUNTY') }}

),

renamed_cast as (

    select

        -- geography / join keys (GEOID is the 5-digit county FIPS, already
        -- zero-padded; ST_GEOID is the 2-digit state FIPS)
        nullif(trim(GEOID), '')                                 as fips_county,
        nullif(trim(ST_GEOID), '')                              as fips_state,
        nullif(trim(NAME), '')                                  as county_name,
        nullif(trim(ST_NAME), '')                               as state_name,

        -- dimensions
        nullif(trim(INTENT), '')                                as intent,
        nullif(trim(PERIOD), '')                                as period,

        -- count suppression flag: KEEP AS TEXT. '1-9' / '10-50' are range
        -- markers, not numbers -- never cast the whole column to a number.
        nullif(trim(COUNT_SUP), '')                             as count_suppression_flag,

        -- only the rows whose flag is a plain integer get a numeric count;
        -- the '1-9'/'10-50' suppression ranges stay NULL here by design.
        try_to_number(trim(COUNT_SUP))                          as numeric_count,

        -- RATE: null the -999 suppression sentinel (exact landed string
        -- '-999.0000000000000') BEFORE casting, so the double is clean.
        try_to_double({{ null_sentinel('RATE', '-999.0000000000000') }})
                                                                as rate,

        -- modeled-rate flag (1 = age-adjusted modeled rate, 0 = crude/zero)
        try_to_double(trim(RATE_M))                             as rate_modeled_flag,

        -- modeled-rate confidence interval text; '-999' is the same suppression
        -- sentinel, so null it (kept as text -- it's a 'lo-hi' range string).
        {{ null_sentinel('RATE_M_CI', '-999') }}                as rate_modeled_ci,

        -- as-of / coverage metadata
        try_to_timestamp(trim(DATA_AS_OF))                      as data_as_of,
        nullif(trim(TTM_DATE_RANGE), '')                        as ttm_date_range,

        -- pipeline audit columns (this table landed them without leading
        -- underscores: INGESTED_AT is a microsecond-epoch NUMBER, not a string)
        to_timestamp_ntz(INGESTED_AT, 6)                        as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                         as _source_run_id

    from source

),

deduped as (

    select
        *,
        row_number() over (
            partition by fips_county, intent, period
            order by _ingested_at desc nulls last
        ) as _row_num
    from renamed_cast

)

select * exclude (_row_num)
from deduped
where _row_num = 1
