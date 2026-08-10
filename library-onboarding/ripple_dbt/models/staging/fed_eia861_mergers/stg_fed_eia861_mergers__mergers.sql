{{ config(materialized='view') }}

-- EIA-861 annual electric utility survey, 2024 vintage (all rows are reporting year 2024).
-- GRAIN: surrogate over (data_year, utility_number).
-- CAVEAT: One record is missing: the loader consumed the first data row as the column header.
-- Columns are renamed positionally; landed column names were the first data record's values.
-- Values of '.' in numeric columns mean null and are stripped via nullif before try_to_number.

with

source as (

    select * from {{ source('ripple_raw', 'FED_EIA861_MERGERS') }}

),

keyed as (

    -- Surrogate-key idiom (see stg_fed_fjc_idb_civil): the natural composite is near-unique,
    -- so a row_number() over the full-row hash is appended as a deterministic tiebreaker.
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['C_2024', 'C_6389']) }}
            || '-'
            || row_number() over (
                   partition by C_2024, C_6389
                   order by hash(*)
               ) as record_id
    from source

),

renamed as (

    select

        -- identifiers
        record_id,
        try_to_number(nullif(trim(C_2024), '.'))                     as data_year,
        try_to_number(nullif(trim(C_6389), '.'))                     as utility_number,
        trim(ENERGY_HARBOR_GENERATION_LLC)                           as utility_name,
        try_to_date(trim(C_03_01_2024), 'MM/DD/YYYY')                as effective_date,
        trim(VISTRA_CORP)                                            as new_parent,
        trim(VISTRA_CORP_1)                                          as new_utility_name,
        trim(C_6555_SIERRA_DR)                                       as address,
        trim(IRVING)                                                 as city,
        trim(TX)                                                     as state,
        trim(C_75039)                                                as zip_code,

        -- metadata
        try_to_timestamp(_INGESTED_AT)                               as _loaded_at,
        _SOURCE_RUN_ID                                               as _source_run_id,
        _SRC_FILE                                                    as _src_file

    from keyed

)

select * from renamed
