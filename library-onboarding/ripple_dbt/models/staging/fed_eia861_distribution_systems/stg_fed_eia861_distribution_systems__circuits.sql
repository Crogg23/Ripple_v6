{{ config(materialized='view') }}

-- EIA-861 annual electric utility survey, 2024 vintage (all rows are reporting year 2024).
-- GRAIN: surrogate over (data_year, utility_number, state).
-- CAVEAT: One record is missing: the loader consumed the first data row as the column header.
-- Columns are renamed positionally; landed column names were the first data record's values.
-- Values of '.' in numeric columns mean null and are stripped via nullif before try_to_number.

with

source as (

    select * from {{ source('ripple_raw', 'FED_EIA861_DISTRIBUTION_SYSTEMS') }}

),

keyed as (

    -- Surrogate-key idiom (see stg_fed_fjc_idb_civil): the natural composite is near-unique,
    -- so a row_number() over the full-row hash is appended as a deterministic tiebreaker.
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['C_2024', 'C_55', 'MS']) }}
            || '-'
            || row_number() over (
                   partition by C_2024, C_55, MS
                   order by hash(*)
               ) as record_id
    from source

),

renamed as (

    select

        -- identifiers
        record_id,
        try_to_number(nullif(trim(C_2024), '.'))                     as data_year,
        try_to_number(nullif(trim(C_55), '.'))                       as utility_number,
        trim(CITY_OF_ABERDEEN_MS)                                    as utility_name,
        trim(MS)                                                     as state,
        try_to_number(nullif(trim(C_8), '.'))                        as distribution_circuits,
        try_to_number(nullif(trim(C_8_1), '.'))                      as circuits_with_voltage_optimization,

        -- metadata
        try_to_timestamp(_INGESTED_AT)                               as _loaded_at,
        _SOURCE_RUN_ID                                               as _source_run_id,
        _SRC_FILE                                                    as _src_file

    from keyed

)

select * from renamed
