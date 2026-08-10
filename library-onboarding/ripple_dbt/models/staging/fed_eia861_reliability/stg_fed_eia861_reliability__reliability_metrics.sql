{{ config(materialized='view') }}

-- EIA-861 annual electric utility survey, 2024 vintage (all rows are reporting year 2024).
-- GRAIN: surrogate over (data_year, utility_number, state); grain not verifiable pre-clean.
-- The Excel loader landed the real header as the first data row; it is filtered out below
-- (rows whose first column is not a 4-digit year are dropped). Columns are renamed
-- positionally from the embedded header text.
-- Values of '.' in numeric columns mean null and are stripped via nullif before try_to_number.

with

source as (

    select * from {{ source('ripple_raw', 'FED_EIA861_RELIABILITY') }}

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
        trim(UNNAMED_4)                                              as ownership,
        try_to_number(nullif(trim(ALL_EVENTS_WITH_MAJOR_EVENT_DAYS), '.')) as ieee_saidi_with_med_minutes,
        try_to_number(nullif(trim(UNNAMED_6), '.'))                  as ieee_saifi_with_med,
        try_to_number(nullif(trim(UNNAMED_7), '.'))                  as ieee_caidi_with_med_minutes,
        try_to_number(nullif(trim(WITHOUT_MAJOR_EVENT_DAYS), '.'))   as ieee_saidi_without_med_minutes,
        try_to_number(nullif(trim(UNNAMED_9), '.'))                  as ieee_saifi_without_med,
        try_to_number(nullif(trim(UNNAMED_10), '.'))                 as ieee_caidi_without_med_minutes,
        try_to_number(nullif(trim(LOSS_OF_SUPPLY_REMOVED_WITH_MAJOR_EVENT_DAYS), '.')) as ieee_saidi_loss_of_supply_removed_minutes,
        try_to_number(nullif(trim(UNNAMED_12), '.'))                 as ieee_saifi_loss_of_supply_removed,
        try_to_number(nullif(trim(UNNAMED_13), '.'))                 as ieee_caidi_loss_of_supply_removed_minutes,
        try_to_number(nullif(trim(COL), '.'))                        as ieee_number_of_customers,
        try_to_number(nullif(trim(UNNAMED_15), '.'))                 as ieee_highest_distribution_voltage_kv,
        trim(UNNAMED_16)                                             as ieee_outages_recorded_automatically,
        try_to_number(nullif(trim(ALL_EVENTS_WITH_MAJOR_EVENT_DAYS_1), '.')) as other_saidi_with_med_minutes,
        try_to_number(nullif(trim(UNNAMED_18), '.'))                 as other_saifi_with_med,
        try_to_number(nullif(trim(UNNAMED_19), '.'))                 as other_caidi_with_med_minutes,
        try_to_number(nullif(trim(WITHOUT_MAJOR_EVENT_DAYS_1), '.')) as other_saidi_without_med_minutes,
        try_to_number(nullif(trim(UNNAMED_21), '.'))                 as other_saifi_without_med,
        try_to_number(nullif(trim(UNNAMED_22), '.'))                 as other_caidi_without_med_minutes,
        try_to_number(nullif(trim(C_1), '.'))                        as other_number_of_customers,
        trim(UNNAMED_24)                                             as inactive_accounts_included,
        trim(UNNAMED_25)                                             as momentary_interruptions,
        try_to_number(nullif(trim(UNNAMED_26), '.'))                 as other_highest_distribution_voltage_kv,
        trim(UNNAMED_27)                                             as other_outages_recorded_automatically,

        -- metadata
        try_to_timestamp(_INGESTED_AT)                               as _loaded_at,
        _SOURCE_RUN_ID                                               as _source_run_id,
        _SRC_FILE                                                    as _src_file

    from keyed

)

select * from renamed
