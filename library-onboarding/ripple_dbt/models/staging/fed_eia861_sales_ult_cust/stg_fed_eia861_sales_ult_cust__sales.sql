{{ config(materialized='view') }}

-- EIA-861 annual electric utility survey, 2024 vintage (all rows are reporting year 2024).
-- GRAIN: surrogate over (data_year, utility_number, state, part, service_type); grain not verifiable pre-clean.
-- The Excel loader landed the real header as the first data row; it is filtered out below
-- (rows whose first column is not a 4-digit year are dropped). Columns are renamed
-- positionally from the embedded header text.
-- Values of '.' in numeric columns mean null and are stripped via nullif before try_to_number.

with

source as (

    select * from {{ source('ripple_raw', 'FED_EIA861_SALES_ULT_CUST') }}

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
        {{ dbt_utils.generate_surrogate_key(['UNNAMED_0', 'UNNAMED_1', 'UNNAMED_6', 'UNNAMED_3', 'UNNAMED_4']) }}
            || '-'
            || row_number() over (
                   partition by UNNAMED_0, UNNAMED_1, UNNAMED_6, UNNAMED_3, UNNAMED_4
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
        trim(UNNAMED_3)                                              as part,
        trim(UNNAMED_4)                                              as service_type,
        trim(UNNAMED_5)                                              as data_type,
        trim(UNNAMED_6)                                              as state,
        trim(UNNAMED_7)                                              as ownership,
        trim(UNNAMED_8)                                              as ba_code,
        try_to_number(nullif(trim(REVENUES), '.'))                   as residential_revenues_thousand_dollars,
        try_to_number(nullif(trim(SALES), '.'))                      as residential_sales_mwh,
        try_to_number(nullif(trim(CUSTOMERS), '.'))                  as residential_customers,
        try_to_number(nullif(trim(REVENUES_1), '.'))                 as commercial_revenues_thousand_dollars,
        try_to_number(nullif(trim(SALES_1), '.'))                    as commercial_sales_mwh,
        try_to_number(nullif(trim(CUSTOMERS_1), '.'))                as commercial_customers,
        try_to_number(nullif(trim(REVENUES_2), '.'))                 as industrial_revenues_thousand_dollars,
        try_to_number(nullif(trim(SALES_2), '.'))                    as industrial_sales_mwh,
        try_to_number(nullif(trim(CUSTOMERS_2), '.'))                as industrial_customers,
        try_to_number(nullif(trim(REVENUES_3), '.'))                 as transportation_revenues_thousand_dollars,
        try_to_number(nullif(trim(SALES_3), '.'))                    as transportation_sales_mwh,
        try_to_number(nullif(trim(CUSTOMERS_3), '.'))                as transportation_customers,
        try_to_number(nullif(trim(REVENUES_4), '.'))                 as total_revenues_thousand_dollars,
        try_to_number(nullif(trim(SALES_4), '.'))                    as total_sales_mwh,
        try_to_number(nullif(trim(CUSTOMERS_4), '.'))                as total_customers,

        -- metadata
        try_to_timestamp(_INGESTED_AT)                               as _loaded_at,
        _SOURCE_RUN_ID                                               as _source_run_id,
        _SRC_FILE                                                    as _src_file

    from keyed

)

select * from renamed
