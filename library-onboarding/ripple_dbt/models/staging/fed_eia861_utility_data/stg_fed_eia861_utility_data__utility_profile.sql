{{ config(materialized='view') }}

-- EIA-861 annual electric utility survey, 2024 vintage (all rows are reporting year 2024).
-- GRAIN: one row per utility per state (UTILITY_NUMBER+STATE is near-unique: 1,699 distinct of 1,701 rows).
-- Values of '.' in numeric columns mean null and are stripped via nullif before try_to_number.

with

source as (

    select * from {{ source('ripple_raw', 'FED_EIA861_UTILITY_DATA') }}

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
        trim(STATE)                                                  as state,
        trim(OWNERSHIP_TYPE)                                         as ownership_type,
        trim(NERC_REGION)                                            as nerc_region,
        trim(TRE)                                                    as nerc_tre,
        trim(FRCC)                                                   as nerc_frcc,
        trim(MRO)                                                    as nerc_mro,
        trim(NPCC)                                                   as nerc_npcc,
        trim(RFC)                                                    as nerc_rfc,
        trim(SERC)                                                   as nerc_serc,
        trim(SPP)                                                    as nerc_spp,
        trim(WECC)                                                   as nerc_wecc,
        trim(CAISO)                                                  as rto_caiso,
        trim(ERCOT)                                                  as rto_ercot,
        trim(PJM)                                                    as rto_pjm,
        trim(NYISO)                                                  as rto_nyiso,
        trim(SPP_1)                                                  as rto_spp,
        trim(MISO)                                                   as rto_miso,
        trim(ISONE)                                                  as rto_isone,
        trim(OTHER)                                                  as rto_other,
        trim(GENERATION)                                             as activity_generation,
        trim(TRANSMISSION)                                           as activity_transmission,
        trim(BUYING_TRANSMISSION)                                    as activity_buying_transmission,
        trim(DISTRIBUTION)                                           as activity_distribution,
        trim(BUYING_DISTRIBUTION)                                    as activity_buying_distribution,
        trim(WHOLESALE_MARKETING)                                    as activity_wholesale_marketing,
        trim(RETAIL_MARKETING)                                       as activity_retail_marketing,
        trim(BUNDLED)                                                as activity_bundled,
        trim(ALT_FUEL_VEHICLE)                                       as alt_fuel_vehicle,
        trim(ALT_FUEL_VEHICLE_2)                                     as alt_fuel_vehicle_2,

        -- metadata
        try_to_timestamp(_INGESTED_AT)                               as _loaded_at,
        _SOURCE_RUN_ID                                               as _source_run_id,
        _SRC_FILE                                                    as _src_file

    from keyed

)

select * from renamed
