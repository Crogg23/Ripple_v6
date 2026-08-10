{{ config(materialized='view') }}

-- EIA-861 annual electric utility survey, 2024 vintage (all rows are reporting year 2024).
-- GRAIN: surrogate over (data_year, utility_number, state); grain not verifiable pre-clean.
-- The Excel loader landed the real header as the first data row; it is filtered out below
-- (rows whose first column is not a 4-digit year are dropped). Columns are renamed
-- positionally from the embedded header text.
-- Values of '.' in numeric columns mean null and are stripped via nullif before try_to_number.

with

source as (

    select * from {{ source('ripple_raw', 'FED_EIA861_DYNAMIC_PRICING') }}

),

filtered as (

    -- drop the embedded header row(s): keep only rows whose first column is a 4-digit year
    select * from source
    where regexp_like(trim(UNNAMED_0), '^[0-9]{4}$')

),

keyed as (

    -- Surrogate-key idiom (see stg_fed_fjc_idb_civil): the natural composite is near-unique,
    -- so a row_number() over the full-row hash is appended as a deterministic tiebreaker.
    select
        filtered.*,
        {{ dbt_utils.generate_surrogate_key(['UNNAMED_0', 'UNNAMED_1', 'UNNAMED_4']) }}
            || '-'
            || row_number() over (
                   partition by UNNAMED_0, UNNAMED_1, UNNAMED_4
                   order by hash(*)
               ) as record_id
    from filtered

),

renamed as (

    select

        -- identifiers
        record_id,
        try_to_number(nullif(trim(UNNAMED_0), '.'))                  as data_year,
        try_to_number(nullif(trim(UNNAMED_1), '.'))                  as utility_number,
        trim(UNNAMED_2)                                              as utility_name,
        trim(UNNAMED_3)                                              as short_form,
        trim(UNNAMED_4)                                              as state,
        trim(UNNAMED_5)                                              as ba_code,
        try_to_number(nullif(trim(CUSTOMERS_ENROLLED), '.'))         as residential_customers_enrolled,
        try_to_number(nullif(trim(UNNAMED_7), '.'))                  as commercial_customers_enrolled,
        try_to_number(nullif(trim(UNNAMED_8), '.'))                  as industrial_customers_enrolled,
        try_to_number(nullif(trim(UNNAMED_9), '.'))                  as transportation_customers_enrolled,
        try_to_number(nullif(trim(UNNAMED_10), '.'))                 as total_customers_enrolled,
        trim(TIME_OF_USE_PRICING)                                    as residential_time_of_use_pricing,
        trim(UNNAMED_12)                                             as commercial_time_of_use_pricing,
        trim(UNNAMED_13)                                             as industrial_time_of_use_pricing,
        trim(UNNAMED_14)                                             as transportation_time_of_use_pricing,
        trim(REAL_TIME_PRICING)                                      as residential_real_time_pricing,
        trim(UNNAMED_16)                                             as commercial_real_time_pricing,
        trim(UNNAMED_17)                                             as industrial_real_time_pricing,
        trim(UNNAMED_18)                                             as transportation_real_time_pricing,
        trim(VARIABLE_PEAK_PRICING)                                  as residential_variable_peak_pricing,
        trim(UNNAMED_20)                                             as commercial_variable_peak_pricing,
        trim(UNNAMED_21)                                             as industrial_variable_peak_pricing,
        trim(UNNAMED_22)                                             as transportation_variable_peak_pricing,
        trim(CRITICAL_PEAK_PRICING)                                  as residential_critical_peak_pricing,
        trim(UNNAMED_24)                                             as commercial_critical_peak_pricing,
        trim(UNNAMED_25)                                             as industrial_critical_peak_pricing,
        trim(UNNAMED_26)                                             as transportation_critical_peak_pricing,
        trim(CRITICAL_PEAK_REBATE)                                   as residential_critical_peak_rebate,
        trim(UNNAMED_28)                                             as commercial_critical_peak_rebate,
        trim(UNNAMED_29)                                             as industrial_critical_peak_rebate,
        trim(UNNAMED_30)                                             as transportation_critical_peak_rebate,

        -- metadata
        try_to_timestamp(_INGESTED_AT)                               as _loaded_at,
        _SOURCE_RUN_ID                                               as _source_run_id,
        _SRC_FILE                                                    as _src_file

    from keyed

)

select * from renamed
