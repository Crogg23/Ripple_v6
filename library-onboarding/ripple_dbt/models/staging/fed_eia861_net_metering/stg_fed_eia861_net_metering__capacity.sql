{{ config(materialized='view') }}

-- EIA-861 annual electric utility survey, 2024 vintage (all rows are reporting year 2024).
-- GRAIN: surrogate over (data_year, utility_number, state, technology_type); grain not verifiable pre-clean.
-- The Excel loader landed the real header as the first data row; it is filtered out below
-- (rows whose first column is not a 4-digit year are dropped). Columns are renamed
-- positionally from the embedded header text.
-- Values of '.' in numeric columns mean null and are stripped via nullif before try_to_number.

with

source as (

    select * from {{ source('ripple_raw', 'FED_EIA861_NET_METERING') }}

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
        {{ dbt_utils.generate_surrogate_key(['UNNAMED_0', 'UNNAMED_2', 'UNNAMED_1', 'CAPACITY_MW']) }}
            || '-'
            || row_number() over (
                   partition by UNNAMED_0, UNNAMED_2, UNNAMED_1, CAPACITY_MW
                   order by hash(*)
               ) as record_id
    from filtered

),

renamed as (

    select

        -- identifiers
        record_id,
        try_to_number(nullif(trim(UNNAMED_0), '.'))                  as data_year,
        trim(UNNAMED_1)                                              as state,
        try_to_number(nullif(trim(UNNAMED_2), '.'))                  as utility_number,
        trim(UNNAMED_3)                                              as utility_name,
        trim(UNNAMED_4)                                              as ba_code,
        trim(CAPACITY_MW)                                            as technology_type,
        try_to_number(nullif(trim(UNNAMED_6), '.'))                  as residential_capacity_mw,
        try_to_number(nullif(trim(UNNAMED_7), '.'))                  as commercial_capacity_mw,
        try_to_number(nullif(trim(UNNAMED_8), '.'))                  as industrial_capacity_mw,
        try_to_number(nullif(trim(UNNAMED_9), '.'))                  as transportation_capacity_mw,
        try_to_number(nullif(trim(UNNAMED_10), '.'))                 as total_capacity_mw,
        try_to_number(nullif(trim(INSTALLATIONS), '.'))              as residential_installations,
        try_to_number(nullif(trim(UNNAMED_12), '.'))                 as commercial_installations,
        try_to_number(nullif(trim(UNNAMED_13), '.'))                 as industrial_installations,
        try_to_number(nullif(trim(UNNAMED_14), '.'))                 as transportation_installations,
        try_to_number(nullif(trim(UNNAMED_15), '.'))                 as total_installations,
        try_to_number(nullif(trim(ENERGY_SOLD_BACK_MWH), '.'))       as residential_energy_sold_back_mwh,
        try_to_number(nullif(trim(UNNAMED_17), '.'))                 as commercial_energy_sold_back_mwh,
        try_to_number(nullif(trim(UNNAMED_18), '.'))                 as industrial_energy_sold_back_mwh,
        try_to_number(nullif(trim(UNNAMED_19), '.'))                 as transportation_energy_sold_back_mwh,
        try_to_number(nullif(trim(UNNAMED_20), '.'))                 as total_energy_sold_back_mwh,
        try_to_number(nullif(trim(VIRTUAL_CAPACITY_1_MW_AND_OVER_MW), '.')) as residential_virtual_capacity_1_mw_and_over_mw,
        try_to_number(nullif(trim(UNNAMED_22), '.'))                 as commercial_virtual_capacity_1_mw_and_over_mw,
        try_to_number(nullif(trim(UNNAMED_23), '.'))                 as industrial_virtual_capacity_1_mw_and_over_mw,
        try_to_number(nullif(trim(UNNAMED_24), '.'))                 as transportation_virtual_capacity_1_mw_and_over_mw,
        try_to_number(nullif(trim(UNNAMED_25), '.'))                 as total_virtual_capacity_1_mw_and_over_mw,
        try_to_number(nullif(trim(VIRTUAL_CUSTOMERS_1_MW_AND_OVER), '.')) as residential_virtual_customers_1_mw_and_over,
        try_to_number(nullif(trim(UNNAMED_27), '.'))                 as commercial_virtual_customers_1_mw_and_over,
        try_to_number(nullif(trim(UNNAMED_28), '.'))                 as industrial_virtual_customers_1_mw_and_over,
        try_to_number(nullif(trim(UNNAMED_29), '.'))                 as transportation_virtual_customers_1_mw_and_over,
        try_to_number(nullif(trim(UNNAMED_30), '.'))                 as total_virtual_customers_1_mw_and_over,
        try_to_number(nullif(trim(VIRTUAL_CAPACITY_UNDER_1_MW_MW), '.')) as residential_virtual_capacity_under_1_mw_mw,
        try_to_number(nullif(trim(UNNAMED_32), '.'))                 as commercial_virtual_capacity_under_1_mw_mw,
        try_to_number(nullif(trim(UNNAMED_33), '.'))                 as industrial_virtual_capacity_under_1_mw_mw,
        try_to_number(nullif(trim(UNNAMED_34), '.'))                 as transportation_virtual_capacity_under_1_mw_mw,
        try_to_number(nullif(trim(UNNAMED_35), '.'))                 as total_virtual_capacity_under_1_mw_mw,
        try_to_number(nullif(trim(VIRTUAL_CUSTOMERS_UNDER_1_MW), '.')) as residential_virtual_customers_under_1_mw,
        try_to_number(nullif(trim(UNNAMED_37), '.'))                 as commercial_virtual_customers_under_1_mw,
        try_to_number(nullif(trim(UNNAMED_38), '.'))                 as industrial_virtual_customers_under_1_mw,
        try_to_number(nullif(trim(UNNAMED_39), '.'))                 as transportation_virtual_customers_under_1_mw,
        try_to_number(nullif(trim(UNNAMED_40), '.'))                 as total_virtual_customers_under_1_mw,
        try_to_number(nullif(trim(PV_PAIRED_BATTERY_CAPACITY_MW), '.')) as residential_pv_paired_battery_capacity_mw,
        try_to_number(nullif(trim(UNNAMED_42), '.'))                 as commercial_pv_paired_battery_capacity_mw,
        try_to_number(nullif(trim(UNNAMED_43), '.'))                 as industrial_pv_paired_battery_capacity_mw,
        try_to_number(nullif(trim(UNNAMED_44), '.'))                 as transportation_pv_paired_battery_capacity_mw,
        try_to_number(nullif(trim(UNNAMED_45), '.'))                 as total_pv_paired_battery_capacity_mw,
        try_to_number(nullif(trim(PV_PAIRED_INSTALLATIONS), '.'))    as residential_pv_paired_installations,
        try_to_number(nullif(trim(UNNAMED_47), '.'))                 as commercial_pv_paired_installations,
        try_to_number(nullif(trim(UNNAMED_48), '.'))                 as industrial_pv_paired_installations,
        try_to_number(nullif(trim(UNNAMED_49), '.'))                 as transportation_pv_paired_installations,
        try_to_number(nullif(trim(UNNAMED_50), '.'))                 as total_pv_paired_installations,
        try_to_number(nullif(trim(PV_PAIRED_ENERGY_CAPACITY_MWH), '.')) as residential_pv_paired_energy_capacity_mwh,
        try_to_number(nullif(trim(UNNAMED_52), '.'))                 as commercial_pv_paired_energy_capacity_mwh,
        try_to_number(nullif(trim(UNNAMED_53), '.'))                 as industrial_pv_paired_energy_capacity_mwh,
        try_to_number(nullif(trim(UNNAMED_54), '.'))                 as transportation_pv_paired_energy_capacity_mwh,
        try_to_number(nullif(trim(UNNAMED_55), '.'))                 as total_pv_paired_energy_capacity_mwh,
        try_to_number(nullif(trim(NOT_PV_PAIRED_BATTERY_CAPACITY_MW), '.')) as residential_not_pv_paired_battery_capacity_mw,
        try_to_number(nullif(trim(UNNAMED_57), '.'))                 as commercial_not_pv_paired_battery_capacity_mw,
        try_to_number(nullif(trim(UNNAMED_58), '.'))                 as industrial_not_pv_paired_battery_capacity_mw,
        try_to_number(nullif(trim(UNNAMED_59), '.'))                 as transportation_not_pv_paired_battery_capacity_mw,
        try_to_number(nullif(trim(UNNAMED_60), '.'))                 as total_not_pv_paired_battery_capacity_mw,
        try_to_number(nullif(trim(NOT_PV_PAIRED_INSTALLATIONS), '.')) as residential_not_pv_paired_installations,
        try_to_number(nullif(trim(UNNAMED_62), '.'))                 as commercial_not_pv_paired_installations,
        try_to_number(nullif(trim(UNNAMED_63), '.'))                 as industrial_not_pv_paired_installations,
        try_to_number(nullif(trim(UNNAMED_64), '.'))                 as transportation_not_pv_paired_installations,
        try_to_number(nullif(trim(UNNAMED_65), '.'))                 as total_not_pv_paired_installations,
        try_to_number(nullif(trim(NOT_PV_PAIRED_ENERGY_CAPACITY_MWH), '.')) as residential_not_pv_paired_energy_capacity_mwh,
        try_to_number(nullif(trim(UNNAMED_67), '.'))                 as commercial_not_pv_paired_energy_capacity_mwh,
        try_to_number(nullif(trim(UNNAMED_68), '.'))                 as industrial_not_pv_paired_energy_capacity_mwh,
        try_to_number(nullif(trim(UNNAMED_69), '.'))                 as transportation_not_pv_paired_energy_capacity_mwh,
        try_to_number(nullif(trim(UNNAMED_70), '.'))                 as total_not_pv_paired_energy_capacity_mwh,
        try_to_number(nullif(trim(CAPACITY_MW_1), '.'))              as residential_capacity_mw_grp2,
        try_to_number(nullif(trim(UNNAMED_72), '.'))                 as commercial_capacity_mw_grp2,
        try_to_number(nullif(trim(UNNAMED_73), '.'))                 as industrial_capacity_mw_grp2,
        try_to_number(nullif(trim(UNNAMED_74), '.'))                 as transportation_capacity_mw_grp2,
        try_to_number(nullif(trim(UNNAMED_75), '.'))                 as total_capacity_mw_grp2,
        try_to_number(nullif(trim(INSTALLATIONS_1), '.'))            as residential_installations_grp2,
        try_to_number(nullif(trim(UNNAMED_77), '.'))                 as commercial_installations_grp2,
        try_to_number(nullif(trim(UNNAMED_78), '.'))                 as industrial_installations_grp2,
        try_to_number(nullif(trim(UNNAMED_79), '.'))                 as transportation_installations_grp2,
        try_to_number(nullif(trim(UNNAMED_80), '.'))                 as total_installations_grp2,
        try_to_number(nullif(trim(ENERGY_SOLD_BACK_MWH_1), '.'))     as residential_energy_sold_back_mwh_grp2,
        try_to_number(nullif(trim(UNNAMED_82), '.'))                 as commercial_energy_sold_back_mwh_grp2,
        try_to_number(nullif(trim(UNNAMED_83), '.'))                 as industrial_energy_sold_back_mwh_grp2,
        try_to_number(nullif(trim(UNNAMED_84), '.'))                 as transportation_energy_sold_back_mwh_grp2,
        try_to_number(nullif(trim(UNNAMED_85), '.'))                 as total_energy_sold_back_mwh_grp2,
        try_to_number(nullif(trim(CAPACITY_MW_2), '.'))              as residential_capacity_mw_grp3,
        try_to_number(nullif(trim(UNNAMED_87), '.'))                 as commercial_capacity_mw_grp3,
        try_to_number(nullif(trim(UNNAMED_88), '.'))                 as industrial_capacity_mw_grp3,
        try_to_number(nullif(trim(UNNAMED_89), '.'))                 as transportation_capacity_mw_grp3,
        try_to_number(nullif(trim(UNNAMED_90), '.'))                 as total_capacity_mw_grp3,
        try_to_number(nullif(trim(INSTALLATIONS_2), '.'))            as residential_installations_grp3,
        try_to_number(nullif(trim(UNNAMED_92), '.'))                 as commercial_installations_grp3,
        try_to_number(nullif(trim(UNNAMED_93), '.'))                 as industrial_installations_grp3,
        try_to_number(nullif(trim(UNNAMED_94), '.'))                 as transportation_installations_grp3,
        try_to_number(nullif(trim(UNNAMED_95), '.'))                 as total_installations_grp3,
        try_to_number(nullif(trim(ENERGY_SOLD_BACK_MWH_2), '.'))     as residential_energy_sold_back_mwh_grp3,
        try_to_number(nullif(trim(UNNAMED_97), '.'))                 as commercial_energy_sold_back_mwh_grp3,
        try_to_number(nullif(trim(UNNAMED_98), '.'))                 as industrial_energy_sold_back_mwh_grp3,
        try_to_number(nullif(trim(UNNAMED_99), '.'))                 as transportation_energy_sold_back_mwh_grp3,
        try_to_number(nullif(trim(UNNAMED_100), '.'))                as total_energy_sold_back_mwh_grp3,
        try_to_number(nullif(trim(CAPACITY_MW_3), '.'))              as residential_capacity_mw_grp4,
        try_to_number(nullif(trim(UNNAMED_102), '.'))                as commercial_capacity_mw_grp4,
        try_to_number(nullif(trim(UNNAMED_103), '.'))                as industrial_capacity_mw_grp4,
        try_to_number(nullif(trim(UNNAMED_104), '.'))                as transportation_capacity_mw_grp4,
        try_to_number(nullif(trim(UNNAMED_105), '.'))                as total_capacity_mw_grp4,
        try_to_number(nullif(trim(INSTALLATIONS_3), '.'))            as residential_installations_grp4,
        try_to_number(nullif(trim(UNNAMED_107), '.'))                as commercial_installations_grp4,
        try_to_number(nullif(trim(UNNAMED_108), '.'))                as industrial_installations_grp4,
        try_to_number(nullif(trim(UNNAMED_109), '.'))                as transportation_installations_grp4,
        try_to_number(nullif(trim(UNNAMED_110), '.'))                as total_installations_grp4,
        try_to_number(nullif(trim(ENERGY_SOLD_BACK_MWH_3), '.'))     as residential_energy_sold_back_mwh_grp4,
        try_to_number(nullif(trim(UNNAMED_112), '.'))                as commercial_energy_sold_back_mwh_grp4,
        try_to_number(nullif(trim(UNNAMED_113), '.'))                as industrial_energy_sold_back_mwh_grp4,
        try_to_number(nullif(trim(UNNAMED_114), '.'))                as transportation_energy_sold_back_mwh_grp4,
        try_to_number(nullif(trim(UNNAMED_115), '.'))                as total_energy_sold_back_mwh_grp4,

        -- metadata
        try_to_timestamp(_INGESTED_AT)                               as _loaded_at,
        _SOURCE_RUN_ID                                               as _source_run_id,
        _SRC_FILE                                                    as _src_file

    from keyed

)

select * from renamed
