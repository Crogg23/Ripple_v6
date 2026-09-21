{{ config(materialized='view') }}

-- EIA-861 annual electric utility survey, 2024 vintage (all rows are reporting year 2024).
-- GRAIN: one row per utility per state per interconnection type (UTILITY_NUMBER+STATE+TYPE is near-unique: 495 distinct of 507 rows).
-- Values of '.' in numeric columns mean null and are stripped via nullif before try_to_number.

with

source as (

    select * from {{ source('ripple_raw', 'FED_EIA861_NON_NET_METERING_DISTRIBUTED') }}

),

keyed as (

    -- Surrogate-key idiom (see stg_fed_fjc_idb_civil): the natural composite is near-unique,
    -- so a row_number() over the full-row hash is appended as a deterministic tiebreaker.
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['UTILITY_NUMBER', 'STATE', 'TYPE']) }}
            || '-'
            || row_number() over (
                   partition by UTILITY_NUMBER, STATE, TYPE
                   order by hash(*)
               ) as record_id
    from source

),

renamed as (

    select

        -- identifiers
        record_id,
        {{ stg_int("nullif(trim(YEAR), '.')") }}                       as data_year,
        trim(STATE)                                                  as state,
        {{ stg_int("nullif(trim(UTILITY_NUMBER), '.')") }}             as utility_number,
        trim(UTILITY_NAME)                                           as utility_name,
        trim(BA_CODE)                                                as ba_code,
        {{ stg_int("nullif(trim(NUMBER_OF_GENERATORS), '.')") }}       as number_of_generators,
        {{ stg_float("nullif(trim(TOTAL_CAPACITY), '.')") }}             as total_capacity_mw,
        {{ stg_float("nullif(trim(CAPACITY_BACK_UP_ONLY), '.')") }}      as capacity_back_up_only_mw,
        {{ stg_float("nullif(trim(CAPACITY_UTILITY_OWNED), '.')") }}     as capacity_utility_owned_mw,
        trim(TYPE)                                                   as technology_type,
        {{ stg_float("nullif(trim(RESIDENTIAL), '.')") }}                as residential_capacity_mw_tech_01,
        {{ stg_float("nullif(trim(COMMERCIAL), '.')") }}                 as commercial_capacity_mw_tech_01,
        {{ stg_float("nullif(trim(INDUSTRIAL), '.')") }}                 as industrial_capacity_mw_tech_01,
        {{ stg_int("nullif(trim(TRANSPORTATION), '.')") }}             as transportation_capacity_mw_tech_01,
        {{ stg_float("nullif(trim(DIRECT_CONNECTED), '.')") }}           as direct_connected_capacity_mw_tech_01,
        {{ stg_float("nullif(trim(TOTAL), '.')") }}                      as total_capacity_mw_tech_01,
        {{ stg_float("nullif(trim(RESIDENTIAL_1), '.')") }}              as residential_capacity_mw_tech_02,
        {{ stg_float("nullif(trim(COMMERCIAL_1), '.')") }}               as commercial_capacity_mw_tech_02,
        {{ stg_float("nullif(trim(INDUSTRIAL_1), '.')") }}               as industrial_capacity_mw_tech_02,
        {{ stg_int("nullif(trim(TRANSPORTATION_1), '.')") }}           as transportation_capacity_mw_tech_02,
        {{ stg_float("nullif(trim(DIRECT_CONNECTED_1), '.')") }}         as direct_connected_capacity_mw_tech_02,
        {{ stg_float("nullif(trim(TOTAL_1), '.')") }}                    as total_capacity_mw_tech_02,
        {{ stg_float("nullif(trim(RESIDENTIAL_2), '.')") }}              as residential_capacity_mw_tech_03,
        {{ stg_float("nullif(trim(COMMERCIAL_2), '.')") }}               as commercial_capacity_mw_tech_03,
        {{ stg_float("nullif(trim(INDUSTRIAL_2), '.')") }}               as industrial_capacity_mw_tech_03,
        {{ stg_int("nullif(trim(TRANSPORTATION_2), '.')") }}           as transportation_capacity_mw_tech_03,
        {{ stg_float("nullif(trim(DIRECT_CONNECTED_2), '.')") }}         as direct_connected_capacity_mw_tech_03,
        {{ stg_float("nullif(trim(TOTAL_2), '.')") }}                    as total_capacity_mw_tech_03,
        {{ stg_float("nullif(trim(RESIDENTIAL_3), '.')") }}              as residential_capacity_mw_tech_04,
        {{ stg_float("nullif(trim(COMMERCIAL_3), '.')") }}               as commercial_capacity_mw_tech_04,
        {{ stg_float("nullif(trim(INDUSTRIAL_3), '.')") }}               as industrial_capacity_mw_tech_04,
        {{ stg_int("nullif(trim(TRANSPORTATION_3), '.')") }}           as transportation_capacity_mw_tech_04,
        {{ stg_float("nullif(trim(DIRECT_CONNECTED_3), '.')") }}         as direct_connected_capacity_mw_tech_04,
        {{ stg_float("nullif(trim(TOTAL_3), '.')") }}                    as total_capacity_mw_tech_04,
        {{ stg_float("nullif(trim(RESIDENTIAL_4), '.')") }}              as residential_capacity_mw_tech_05,
        {{ stg_float("nullif(trim(COMMERCIAL_4), '.')") }}               as commercial_capacity_mw_tech_05,
        {{ stg_float("nullif(trim(INDUSTRIAL_4), '.')") }}               as industrial_capacity_mw_tech_05,
        {{ stg_int("nullif(trim(TRANSPORTATION_4), '.')") }}           as transportation_capacity_mw_tech_05,
        {{ stg_float("nullif(trim(DIRECT_CONNECTED_4), '.')") }}         as direct_connected_capacity_mw_tech_05,
        {{ stg_float("nullif(trim(TOTAL_4), '.')") }}                    as total_capacity_mw_tech_05,
        {{ stg_float("nullif(trim(RESIDENTIAL_5), '.')") }}              as residential_capacity_mw_tech_06,
        {{ stg_float("nullif(trim(COMMERCIAL_5), '.')") }}               as commercial_capacity_mw_tech_06,
        {{ stg_float("nullif(trim(INDUSTRIAL_5), '.')") }}               as industrial_capacity_mw_tech_06,
        {{ stg_int("nullif(trim(TRANSPORTATION_5), '.')") }}           as transportation_capacity_mw_tech_06,
        {{ stg_float("nullif(trim(DIRECT_CONNECTED_5), '.')") }}         as direct_connected_capacity_mw_tech_06,
        {{ stg_float("nullif(trim(TOTAL_5), '.')") }}                    as total_capacity_mw_tech_06,
        {{ stg_float("nullif(trim(RESIDENTIAL_6), '.')") }}              as residential_capacity_mw_tech_07,
        {{ stg_float("nullif(trim(COMMERCIAL_6), '.')") }}               as commercial_capacity_mw_tech_07,
        {{ stg_float("nullif(trim(INDUSTRIAL_6), '.')") }}               as industrial_capacity_mw_tech_07,
        {{ stg_int("nullif(trim(TRANSPORTATION_6), '.')") }}           as transportation_capacity_mw_tech_07,
        {{ stg_float("nullif(trim(DIRECT_CONNECTED_6), '.')") }}         as direct_connected_capacity_mw_tech_07,
        {{ stg_float("nullif(trim(TOTAL_6), '.')") }}                    as total_capacity_mw_tech_07,
        {{ stg_float("nullif(trim(RESIDENTIAL_7), '.')") }}              as residential_capacity_mw_tech_08,
        {{ stg_float("nullif(trim(COMMERCIAL_7), '.')") }}               as commercial_capacity_mw_tech_08,
        {{ stg_float("nullif(trim(INDUSTRIAL_7), '.')") }}               as industrial_capacity_mw_tech_08,
        {{ stg_int("nullif(trim(TRANSPORTATION_7), '.')") }}           as transportation_capacity_mw_tech_08,
        {{ stg_float("nullif(trim(DIRECT_CONNECTED_7), '.')") }}         as direct_connected_capacity_mw_tech_08,
        {{ stg_float("nullif(trim(TOTAL_7), '.')") }}                    as total_capacity_mw_tech_08,
        {{ stg_int("nullif(trim(RESIDENTIAL_8), '.')") }}              as residential_capacity_mw_tech_09,
        {{ stg_float("nullif(trim(COMMERCIAL_8), '.')") }}               as commercial_capacity_mw_tech_09,
        {{ stg_float("nullif(trim(INDUSTRIAL_8), '.')") }}               as industrial_capacity_mw_tech_09,
        {{ stg_int("nullif(trim(TRANSPORTATION_8), '.')") }}           as transportation_capacity_mw_tech_09,
        {{ stg_float("nullif(trim(DIRECT_CONNECTED_8), '.')") }}         as direct_connected_capacity_mw_tech_09,
        {{ stg_float("nullif(trim(TOTAL_8), '.')") }}                    as total_capacity_mw_tech_09,
        {{ stg_float("nullif(trim(RESIDENTIAL_9), '.')") }}              as residential_capacity_mw_tech_10,
        {{ stg_float("nullif(trim(COMMERCIAL_9), '.')") }}               as commercial_capacity_mw_tech_10,
        {{ stg_float("nullif(trim(INDUSTRIAL_9), '.')") }}               as industrial_capacity_mw_tech_10,
        {{ stg_int("nullif(trim(TRANSPORTATION_9), '.')") }}           as transportation_capacity_mw_tech_10,
        {{ stg_float("nullif(trim(DIRECT_CONNECTED_9), '.')") }}         as direct_connected_capacity_mw_tech_10,
        {{ stg_float("nullif(trim(TOTAL_9), '.')") }}                    as total_capacity_mw_tech_10,
        {{ stg_float("nullif(trim(RESIDENTIAL_10), '.')") }}             as residential_capacity_mw_all_tech,
        {{ stg_float("nullif(trim(COMMERCIAL_10), '.')") }}              as commercial_capacity_mw_all_tech,
        {{ stg_float("nullif(trim(INDUSTRIAL_10), '.')") }}              as industrial_capacity_mw_all_tech,
        {{ stg_int("nullif(trim(TRANSPORTATION_10), '.')") }}          as transportation_capacity_mw_all_tech,
        {{ stg_float("nullif(trim(DIRECT_CONNECTED_10), '.')") }}        as direct_connected_capacity_mw_all_tech,
        {{ stg_float("nullif(trim(TOTAL_10), '.')") }}                   as total_capacity_mw_all_tech,

        -- metadata
        {{ stg_ts('_INGESTED_AT') }}                               as _loaded_at,
        _SOURCE_RUN_ID                                               as _source_run_id,
        _SRC_FILE                                                    as _src_file

    from keyed

)

select * from renamed
