{{ config(materialized='view') }}

-- EIA-861 annual electric utility survey, 2024 vintage (all rows are reporting year 2024).
-- GRAIN: surrogate over (data_year, utility_number, state).
-- CAVEAT: One record is missing: the loader consumed the first data row as the column header.
-- Columns are renamed positionally; landed column names were the first data record's values.
-- Values of '.' in numeric columns mean null and are stripped via nullif before try_to_number.

with

source as (

    select * from {{ source('ripple_raw', 'FED_EIA861_SHORT_FORM') }}

),

keyed as (

    -- Surrogate-key idiom (see stg_fed_fjc_idb_civil): the natural composite is near-unique,
    -- so a row_number() over the full-row hash is appended as a deterministic tiebreaker.
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['C_2024', 'C_192', 'AK']) }}
            || '-'
            || row_number() over (
                   partition by C_2024, C_192, AK
                   order by hash(*)
               ) as record_id
    from source

),

renamed as (

    select

        -- identifiers
        record_id,
        try_to_number(nullif(trim(C_2024), '.'))                     as data_year,
        try_to_number(nullif(trim(C_192), '.'))                      as utility_number,
        trim(AKIACHAK_NATIVE_COMMUNITY_ELECTRIC)                     as utility_name,
        trim(COOPERATIVE)                                            as ownership,
        trim(AK)                                                     as state,
        trim(NA)                                                     as ba_code,
        try_to_number(nullif(trim(C_1269_4), '.'))                   as revenues_thousand_dollars,
        try_to_number(nullif(trim(C_1976), '.'))                     as sales_mwh,
        try_to_number(nullif(trim(C_254), '.'))                      as customers,
        trim(COL)                                                    as unrecovered_metric_10,
        trim(N)                                                      as unrecovered_flag_11,
        trim(N_1)                                                    as unrecovered_flag_12,
        trim(N_2)                                                    as unrecovered_flag_13,

        -- metadata
        try_to_timestamp(_INGESTED_AT)                               as _loaded_at,
        _SOURCE_RUN_ID                                               as _source_run_id,
        _SRC_FILE                                                    as _src_file

    from keyed

)

select * from renamed
