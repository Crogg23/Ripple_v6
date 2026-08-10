{{ config(materialized='view') }}

-- EIA-861 annual electric utility survey, 2024 vintage (all rows are reporting year 2024).
-- GRAIN: surrogate over (data_year, utility_number, state); grain not verifiable pre-clean.
-- The Excel loader landed the real header as the first data row; it is filtered out below
-- (rows whose first column is not a 4-digit year are dropped). Columns are renamed
-- positionally from the embedded header text.
-- Values of '.' in numeric columns mean null and are stripped via nullif before try_to_number.

with

source as (

    select * from {{ source('ripple_raw', 'FED_EIA861_ENERGY_EFFICIENCY') }}

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
        trim(UNNAMED_4)                                              as ba_code,
        try_to_number(nullif(trim(ENERGY_SAVINGS_MWH), '.'))         as residential_incremental_energy_savings_mwh,
        try_to_number(nullif(trim(UNNAMED_6), '.'))                  as commercial_incremental_energy_savings_mwh,
        try_to_number(nullif(trim(UNNAMED_7), '.'))                  as industrial_incremental_energy_savings_mwh,
        try_to_number(nullif(trim(UNNAMED_8), '.'))                  as transportation_incremental_energy_savings_mwh,
        try_to_number(nullif(trim(UNNAMED_9), '.'))                  as total_incremental_energy_savings_mwh,
        try_to_number(nullif(trim(PEAK_DEMAND_SAVINGS_MW), '.'))     as residential_incremental_peak_demand_savings_mw,
        try_to_number(nullif(trim(UNNAMED_11), '.'))                 as commercial_incremental_peak_demand_savings_mw,
        try_to_number(nullif(trim(UNNAMED_12), '.'))                 as industrial_incremental_peak_demand_savings_mw,
        try_to_number(nullif(trim(UNNAMED_13), '.'))                 as transportation_incremental_peak_demand_savings_mw,
        try_to_number(nullif(trim(UNNAMED_14), '.'))                 as total_incremental_peak_demand_savings_mw,
        try_to_number(nullif(trim(ENERGY_SAVINGS_MWH_1), '.'))       as residential_life_cycle_energy_savings_mwh,
        try_to_number(nullif(trim(UNNAMED_16), '.'))                 as commercial_life_cycle_energy_savings_mwh,
        try_to_number(nullif(trim(UNNAMED_17), '.'))                 as industrial_life_cycle_energy_savings_mwh,
        try_to_number(nullif(trim(UNNAMED_18), '.'))                 as transportation_life_cycle_energy_savings_mwh,
        try_to_number(nullif(trim(UNNAMED_19), '.'))                 as total_life_cycle_energy_savings_mwh,
        try_to_number(nullif(trim(PEAK_DEMAND_SAVINGS_MW_1), '.'))   as residential_life_cycle_peak_demand_savings_mw,
        try_to_number(nullif(trim(UNNAMED_21), '.'))                 as commercial_life_cycle_peak_demand_savings_mw,
        try_to_number(nullif(trim(UNNAMED_22), '.'))                 as industrial_life_cycle_peak_demand_savings_mw,
        try_to_number(nullif(trim(UNNAMED_23), '.'))                 as transportation_life_cycle_peak_demand_savings_mw,
        try_to_number(nullif(trim(UNNAMED_24), '.'))                 as total_life_cycle_peak_demand_savings_mw,
        try_to_number(nullif(trim(CUSTOMER_INCENTIVES_THOUSAND_DOLLARS), '.')) as residential_incremental_customer_incentives_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_26), '.'))                 as commercial_incremental_customer_incentives_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_27), '.'))                 as industrial_incremental_customer_incentives_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_28), '.'))                 as transportation_incremental_customer_incentives_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_29), '.'))                 as total_incremental_customer_incentives_thousand_dollars,
        try_to_number(nullif(trim(ALL_OTHER_COSTS_THOUSAND_DOLLARS), '.')) as residential_incremental_all_other_costs_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_31), '.'))                 as commercial_incremental_all_other_costs_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_32), '.'))                 as industrial_incremental_all_other_costs_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_33), '.'))                 as transportation_incremental_all_other_costs_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_34), '.'))                 as total_incremental_all_other_costs_thousand_dollars,
        try_to_number(nullif(trim(CUSTOMER_INCENTIVES_THOUSAND_DOLLARS_1), '.')) as residential_life_cycle_customer_incentives_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_36), '.'))                 as commercial_life_cycle_customer_incentives_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_37), '.'))                 as industrial_life_cycle_customer_incentives_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_38), '.'))                 as transportation_life_cycle_customer_incentives_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_39), '.'))                 as total_life_cycle_customer_incentives_thousand_dollars,
        try_to_number(nullif(trim(ALL_OTHER_COSTS_THOUSAND_DOLLARS_1), '.')) as residential_life_cycle_all_other_costs_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_41), '.'))                 as commercial_life_cycle_all_other_costs_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_42), '.'))                 as industrial_life_cycle_all_other_costs_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_43), '.'))                 as transportation_life_cycle_all_other_costs_thousand_dollars,
        try_to_number(nullif(trim(UNNAMED_44), '.'))                 as total_life_cycle_all_other_costs_thousand_dollars,
        try_to_number(nullif(trim(YEARS), '.'))                      as residential_weighted_average_life_years,
        try_to_number(nullif(trim(UNNAMED_46), '.'))                 as commercial_weighted_average_life_years,
        try_to_number(nullif(trim(UNNAMED_47), '.'))                 as industrial_weighted_average_life_years,
        try_to_number(nullif(trim(UNNAMED_48), '.'))                 as transportation_weighted_average_life_years,
        trim(UNNAMED_49)                                             as website,

        -- metadata
        try_to_timestamp(_INGESTED_AT)                               as _loaded_at,
        _SOURCE_RUN_ID                                               as _source_run_id,
        _SRC_FILE                                                    as _src_file

    from keyed

)

select * from renamed
