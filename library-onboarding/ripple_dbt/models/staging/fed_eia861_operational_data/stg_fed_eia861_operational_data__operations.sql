{{ config(materialized='view') }}

-- EIA-861 annual electric utility survey, 2024 vintage (all rows are reporting year 2024).
-- GRAIN: surrogate over (data_year, utility_number, state); grain not verifiable pre-clean.
-- The Excel loader landed the real header as the first data row; it is filtered out below
-- (rows whose first column is not a 4-digit year are dropped). Columns are renamed
-- positionally from the embedded header text.
-- Values of '.' in numeric columns mean null and are stripped via nullif before try_to_number.

with

source as (

    select * from {{ source('ripple_raw', 'FED_EIA861_OPERATIONAL_DATA') }}

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
        {{ dbt_utils.generate_surrogate_key(['UNNAMED_0', 'UNNAMED_1', 'UNNAMED_3']) }}
            || '-'
            || row_number() over (
                   partition by UNNAMED_0, UNNAMED_1, UNNAMED_3
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
        trim(UNNAMED_3)                                              as state,
        trim(UNNAMED_4)                                              as ownership_type,
        trim(UNNAMED_5)                                              as nerc_region,
        try_to_number(nullif(trim(MEGAWATTS), '.'))                  as summer_peak_demand_mw,
        try_to_number(nullif(trim(UNNAMED_7), '.'))                  as winter_peak_demand_mw,
        try_to_number(nullif(trim(UNNAMED_8), '.'))                  as net_generation_mwh,
        try_to_number(nullif(trim(UNNAMED_9), '.'))                  as wholesale_power_purchases_mwh,
        try_to_number(nullif(trim(POWER_EXCHANGED), '.'))            as exchange_energy_received_mwh,
        try_to_number(nullif(trim(UNNAMED_11), '.'))                 as exchange_energy_delivered_mwh,
        try_to_number(nullif(trim(UNNAMED_12), '.'))                 as net_power_exchanged_mwh,
        try_to_number(nullif(trim(WHEELED_POWER), '.'))              as wheeled_power_received_mwh,
        try_to_number(nullif(trim(UNNAMED_14), '.'))                 as wheeled_power_delivered_mwh,
        try_to_number(nullif(trim(UNNAMED_15), '.'))                 as net_wheeled_power_mwh,
        try_to_number(nullif(trim(UNNAMED_16), '.'))                 as transmission_by_other_losses_mwh,
        try_to_number(nullif(trim(UNNAMED_17), '.'))                 as total_sources_mwh,
        try_to_number(nullif(trim(MEGAWATTHOURS), '.'))              as sales_to_ultimate_customers_mwh,
        try_to_number(nullif(trim(UNNAMED_19), '.'))                 as sales_for_resale_mwh,
        try_to_number(nullif(trim(UNNAMED_20), '.'))                 as furnished_without_charge_mwh,
        try_to_number(nullif(trim(UNNAMED_21), '.'))                 as consumed_by_respondent_without_charge_mwh,
        try_to_number(nullif(trim(UNNAMED_22), '.'))                 as total_energy_losses_mwh,
        try_to_number(nullif(trim(UNNAMED_23), '.'))                 as total_disposition_mwh,
        try_to_number(nullif(trim(THOUSANDS_DOLLARS), '.'))          as revenue_from_retail_sales_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_25), '.'))                 as revenue_from_delivery_customers_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_26), '.'))                 as revenue_from_sales_for_resale_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_27), '.'))                 as revenue_from_credits_or_adjustments_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_28), '.'))                 as revenue_from_transmission_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_29), '.'))                 as revenue_from_other_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_30), '.'))                 as total_revenue_thousand_dollars,
        trim(UNNAMED_31)                                             as data_type,

        -- metadata
        try_to_timestamp(_INGESTED_AT)                               as _loaded_at,
        _SOURCE_RUN_ID                                               as _source_run_id,
        _SRC_FILE                                                    as _src_file

    from keyed

)

select * from renamed
