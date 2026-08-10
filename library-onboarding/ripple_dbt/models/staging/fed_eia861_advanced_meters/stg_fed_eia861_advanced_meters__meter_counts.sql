{{ config(materialized='view') }}

-- EIA-861 annual electric utility survey, 2024 vintage (all rows are reporting year 2024).
-- GRAIN: one row per utility per state (UTILITY_NUMBER+STATE is near-unique: 2,683 distinct of 2,725 rows).
-- NOTE: Meter-group identities for the last two column groups (daily digital access) are inferred from the EIA-861 2024 workbook layout.
-- Values of '.' in numeric columns mean null and are stripped via nullif before try_to_number.

with

source as (

    select * from {{ source('ripple_raw', 'FED_EIA861_ADVANCED_METERS') }}

),

keyed as (

    -- Surrogate-key idiom (see stg_fed_fjc_idb_civil): the natural composite is near-unique,
    -- so a row_number() over the full-row hash is appended as a deterministic tiebreaker.
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['UTILITY_NUMBER', 'STATE']) }}
            || '-'
            || row_number() over (
                   partition by UTILITY_NUMBER, STATE
                   order by hash(*)
               ) as record_id
    from source

),

renamed as (

    select

        -- identifiers
        record_id,
        try_to_number(nullif(trim(DATA_YEAR), '.'))                  as data_year,
        try_to_number(nullif(trim(UTILITY_NUMBER), '.'))             as utility_number,
        trim(UTILITY_NAME)                                           as utility_name,
        trim(OWNERSHIP)                                              as ownership,
        trim(SHORT_FORM)                                             as short_form,
        trim(STATE)                                                  as state,
        trim(BA_CODE)                                                as ba_code,
        try_to_number(nullif(trim(RESIDENTIAL), '.'))                as residential_amr_meters,
        try_to_number(nullif(trim(COMMERCIAL), '.'))                 as commercial_amr_meters,
        try_to_number(nullif(trim(INDUSTRIAL), '.'))                 as industrial_amr_meters,
        try_to_number(nullif(trim(TRANSPORTATION), '.'))             as transportation_amr_meters,
        try_to_number(nullif(trim(TOTAL), '.'))                      as total_amr_meters,
        try_to_number(nullif(trim(RESIDENTIAL_1), '.'))              as residential_ami_meters,
        try_to_number(nullif(trim(COMMERCIAL_1), '.'))               as commercial_ami_meters,
        try_to_number(nullif(trim(INDUSTRIAL_1), '.'))               as industrial_ami_meters,
        try_to_number(nullif(trim(TRANSPORTATION_1), '.'))           as transportation_ami_meters,
        try_to_number(nullif(trim(TOTAL_1), '.'))                    as total_ami_meters,
        try_to_number(nullif(trim(RESIDENTIAL_2), '.'))              as residential_ami_home_area_network_meters,
        try_to_number(nullif(trim(COMMERCIAL_2), '.'))               as commercial_ami_home_area_network_meters,
        try_to_number(nullif(trim(INDUSTRIAL_2), '.'))               as industrial_ami_home_area_network_meters,
        try_to_number(nullif(trim(TRANSPORTATION_2), '.'))           as transportation_ami_home_area_network_meters,
        try_to_number(nullif(trim(TOTAL_2), '.'))                    as total_ami_home_area_network_meters,
        try_to_number(nullif(trim(RESIDENTIAL_3), '.'))              as residential_non_amr_ami_meters,
        try_to_number(nullif(trim(COMMERCIAL_3), '.'))               as commercial_non_amr_ami_meters,
        try_to_number(nullif(trim(INDUSTRIAL_3), '.'))               as industrial_non_amr_ami_meters,
        try_to_number(nullif(trim(TRANSPORTATION_3), '.'))           as transportation_non_amr_ami_meters,
        try_to_number(nullif(trim(TOTAL_3), '.'))                    as total_non_amr_ami_meters,
        try_to_number(nullif(trim(RESIDENTIAL_4), '.'))              as residential_total_meters,
        try_to_number(nullif(trim(COMMERCIAL_4), '.'))               as commercial_total_meters,
        try_to_number(nullif(trim(INDUSTRIAL_4), '.'))               as industrial_total_meters,
        try_to_number(nullif(trim(TRANSPORTATION_4), '.'))           as transportation_total_meters,
        try_to_number(nullif(trim(TOTAL_4), '.'))                    as total_total_meters,
        try_to_number(nullif(trim(RESIDENTIAL_5), '.'))              as residential_energy_served_ami_mwh,
        try_to_number(nullif(trim(COMMERCIAL_5), '.'))               as commercial_energy_served_ami_mwh,
        try_to_number(nullif(trim(INDUSTRIAL_5), '.'))               as industrial_energy_served_ami_mwh,
        try_to_number(nullif(trim(TRANSPORTATION_5), '.'))           as transportation_energy_served_ami_mwh,
        try_to_number(nullif(trim(TOTAL_5), '.'))                    as total_energy_served_ami_mwh,
        try_to_number(nullif(trim(RESIDENTIAL_6), '.'))              as residential_ami_daily_digital_access_meters,
        try_to_number(nullif(trim(COMMERCIAL_6), '.'))               as commercial_ami_daily_digital_access_meters,
        try_to_number(nullif(trim(INDUSTRIAL_6), '.'))               as industrial_ami_daily_digital_access_meters,
        try_to_number(nullif(trim(TRANSPORTATION_6), '.'))           as transportation_ami_daily_digital_access_meters,
        try_to_number(nullif(trim(TOTAL_6), '.'))                    as total_ami_daily_digital_access_meters,
        try_to_number(nullif(trim(RESIDENTIAL_7), '.'))              as residential_energy_served_daily_digital_access_mwh,
        try_to_number(nullif(trim(COMMERCIAL_7), '.'))               as commercial_energy_served_daily_digital_access_mwh,
        try_to_number(nullif(trim(INDUSTRIAL_7), '.'))               as industrial_energy_served_daily_digital_access_mwh,
        try_to_number(nullif(trim(TRANSPORTATION_7), '.'))           as transportation_energy_served_daily_digital_access_mwh,
        try_to_number(nullif(trim(TOTAL_7), '.'))                    as total_energy_served_daily_digital_access_mwh,

        -- metadata
        try_to_timestamp(_INGESTED_AT)                               as _loaded_at,
        _SOURCE_RUN_ID                                               as _source_run_id,
        _SRC_FILE                                                    as _src_file

    from keyed

)

select * from renamed
