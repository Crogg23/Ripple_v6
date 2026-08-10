{{ config(materialized='view') }}

-- EIA-861 annual electric utility survey, 2024 vintage (all rows are reporting year 2024).
-- GRAIN: surrogate over (data_year, utility_number).
-- CAVEAT: One record is missing: the loader consumed the first data row as the column header.
-- Columns are renamed positionally; landed column names were the first data record's values.
-- Values of '.' in numeric columns mean null and are stripped via nullif before try_to_number.

with

source as (

    select * from {{ source('ripple_raw', 'FED_EIA861_FRAME') }}

),

keyed as (

    -- Surrogate-key idiom (see stg_fed_fjc_idb_civil): the natural composite is near-unique,
    -- so a row_number() over the full-row hash is appended as a deterministic tiebreaker.
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['C_2024', 'C_34']) }}
            || '-'
            || row_number() over (
                   partition by C_2024, C_34
                   order by hash(*)
               ) as record_id
    from source

),

renamed as (

    select

        -- identifiers
        record_id,
        try_to_number(nullif(trim(C_2024), '.'))                     as data_year,
        try_to_number(nullif(trim(C_34), '.'))                       as utility_number,
        trim(CITY_OF_ABBEVILLE_SC)                                   as utility_name,
        trim(Y)                                                      as short_form,
        trim(M)                                                      as ownership_code,
        trim(MUNICIPAL)                                              as ownership,
        trim(UNNAMED_6)                                              as schedule_flag_01,
        trim(X)                                                      as schedule_flag_02,
        trim(UNNAMED_8)                                              as schedule_flag_03,
        trim(UNNAMED_9)                                              as schedule_flag_04,
        trim(UNNAMED_10)                                             as schedule_flag_05,
        trim(UNNAMED_11)                                             as schedule_flag_06,
        trim(UNNAMED_12)                                             as schedule_flag_07,
        trim(UNNAMED_13)                                             as schedule_flag_08,
        trim(UNNAMED_14)                                             as schedule_flag_09,
        trim(UNNAMED_15)                                             as schedule_flag_10,
        trim(UNNAMED_16)                                             as schedule_flag_11,
        trim(UNNAMED_17)                                             as schedule_flag_12,
        trim(UNNAMED_18)                                             as schedule_flag_13,
        trim(X_1)                                                    as schedule_flag_14,
        trim(UNNAMED_20)                                             as schedule_flag_15,

        -- metadata
        try_to_timestamp(_INGESTED_AT)                               as _loaded_at,
        _SOURCE_RUN_ID                                               as _source_run_id,
        _SRC_FILE                                                    as _src_file

    from keyed

)

select * from renamed
